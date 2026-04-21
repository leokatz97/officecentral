#!/usr/bin/env python3
"""Pull recent paid orders and verify tax + payment method correctness."""
import json
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent.parent
env = {}
for line in (ROOT / ".env").read_text().splitlines():
    if "=" in line and not line.strip().startswith("#"):
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip()

TOKEN = env["SHOPIFY_TOKEN"]
STORE = env["SHOPIFY_STORE"]

def api(path):
    req = Request(
        f"https://{STORE}/admin/api/2024-10/{path}",
        headers={"X-Shopify-Access-Token": TOKEN, "Content-Type": "application/json"},
    )
    with urlopen(req) as resp:
        return json.loads(resp.read())

# Pull last ~100 orders, any status
orders = api("orders.json?status=any&limit=100&fields=id,name,created_at,financial_status,total_price,total_tax,tax_lines,shipping_address,gateway,payment_gateway_names,currency")["orders"]

print(f"Pulled {len(orders)} recent orders\n")
print("=" * 70)
print("TAX CHECK — paid orders shipping to Canadian addresses")
print("=" * 70)

province_expected = {
    "ON": ("HST", 0.13),
    "NB": ("HST", 0.15),
    "NS": ("HST", 0.15),
    "NL": ("HST", 0.15),
    "PE": ("HST", 0.15),
    "BC": ("GST+PST", 0.12),
    "AB": ("GST", 0.05),
    "SK": ("GST+PST", 0.11),
    "MB": ("GST+PST", 0.12),
    "QC": ("GST+QST", 0.14975),
    "YT": ("GST", 0.05),
    "NT": ("GST", 0.05),
    "NU": ("GST", 0.05),
}

tax_rows = []
for o in orders:
    if o.get("financial_status") != "paid":
        continue
    addr = o.get("shipping_address") or {}
    if (addr.get("country_code") or "").upper() != "CA":
        continue
    prov = (addr.get("province_code") or "").upper()
    subtotal = float(o["total_price"]) - float(o["total_tax"])
    if subtotal <= 0:
        continue
    effective_rate = float(o["total_tax"]) / subtotal
    expected_name, expected_rate = province_expected.get(prov, ("?", None))
    tax_line_names = [tl.get("title", "?") for tl in (o.get("tax_lines") or [])]
    ok = expected_rate is not None and abs(effective_rate - expected_rate) < 0.01
    tax_rows.append((o["name"], prov, f"${subtotal:,.2f}", f"${float(o['total_tax']):,.2f}",
                     f"{effective_rate*100:.2f}%", f"{expected_name} ({expected_rate*100 if expected_rate else '?'}%)",
                     ",".join(tax_line_names) or "(none)", "OK" if ok else "MISMATCH"))

if not tax_rows:
    print("  No paid Canadian orders found in the last 100.")
else:
    print(f"{'Order':<10}{'Prov':<6}{'Subtotal':<14}{'Tax':<12}{'Rate':<10}{'Expected':<22}{'Tax lines':<30}Status")
    print("-" * 130)
    for r in tax_rows[:40]:
        print(f"{r[0]:<10}{r[1]:<6}{r[2]:<14}{r[3]:<12}{r[4]:<10}{r[5]:<22}{r[6]:<30}{r[7]}")
    ok_count = sum(1 for r in tax_rows if r[7] == "OK")
    print(f"\n  {ok_count}/{len(tax_rows)} paid Canadian orders tax-calculated correctly within 1%.")

print()
print("=" * 70)
print("PAYMENT METHOD CHECK — gateways used on paid orders")
print("=" * 70)

gateway_counter = Counter()
gateway_revenue = defaultdict(float)
for o in orders:
    if o.get("financial_status") != "paid":
        continue
    gws = o.get("payment_gateway_names") or ([o["gateway"]] if o.get("gateway") else [])
    for gw in gws:
        gateway_counter[gw or "(none)"] += 1
        gateway_revenue[gw or "(none)"] += float(o["total_price"])

total_paid = sum(gateway_counter.values())
if total_paid == 0:
    print("  No paid orders found.")
else:
    print(f"{'Gateway':<35}{'Orders':<10}{'Revenue'}")
    print("-" * 60)
    for gw, n in gateway_counter.most_common():
        print(f"{gw:<35}{n:<10}${gateway_revenue[gw]:,.2f}")
    print(f"\n  {total_paid} paid orders across {len(gateway_counter)} live gateway(s).")

print()
print("=" * 70)
print("FINANCIAL STATUS BREAKDOWN — last 100 orders")
print("=" * 70)
status_counter = Counter(o.get("financial_status") or "(unknown)" for o in orders)
for s, n in status_counter.most_common():
    print(f"  {s:<20}{n}")
