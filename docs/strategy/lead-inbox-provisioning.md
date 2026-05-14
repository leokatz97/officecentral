# LEAD-INBOX-1 Provisioning Checklist
_2026-05-14 · Step 21 of the launch tracker · Manual provisioning work for Steve to walk through in email provider + DNS UI._

---

## Current state (discovered via DNS investigation)

- **Email provider:** Microsoft 365 — specifically **Microsoft 365 from GoDaddy** (tenant: `netorgft17732759.onmicrosoft.com`)
  - MX record: `brantbusinessinteriors-com.mail.protection.outlook.com.` (priority 0)
  - Admin portal: **email.godaddy.com** (NOT admin.microsoft.com — GoDaddy hosts this tenant through their own reseller panel)

- **DNS host:** GoDaddy
  - NS records: `ns59.domaincontrol.com.` / `ns60.domaincontrol.com.`
  - DNS changes made here: **GoDaddy Domain Portfolio → Manage DNS**

- **Existing SPF:** ⚠️ **Present but wrong**
  - Found: `"v=spf1 include:secureserver.net -all"`
  - Problem: `secureserver.net` is GoDaddy's legacy email SPF include, NOT Microsoft 365. Outbound mail from M365 is not covered by this record. DKIM passing (see below) is masking this gap — if DKIM ever breaks, outbound mail will fail DMARC and get rejected.
  - Action: **Update** — add `include:spf.protection.outlook.com`

- **Existing DKIM:** ✅ **Active on selector1**
  - `selector1._domainkey.brantbusinessinteriors.com` has a full RSA public key
  - `selector2._domainkey.brantbusinessinteriors.com` is the standby CNAME (normal M365 rotation pattern)
  - Action: **None needed** — DKIM is already configured and working

- **Existing DMARC:** ⚠️ **Present but missing reporting address**
  - Found: `"v=DMARC1; p=reject;"`
  - `p=reject` is the maximum enforcement level — this is unusually strict for an unmonitored domain. It's working (legitimate M365 mail passes via DKIM alignment), but if anything breaks, mail silently disappears with zero visibility.
  - No `rua=` (aggregate reporting) or `ruf=` (forensic reporting) tag — you are receiving zero DMARC reports.
  - Action: **Update** — add `rua=` so you can see what's passing and what's failing

- **Mailboxes (quotes@, design@, info@):** Cannot verify without admin access. Steve to check in GoDaddy M365 admin.

---

## Hands-on provisioning steps for Steve

### Step 1: Create the three mailboxes (GoDaddy M365 admin UI)

1. Go to **email.godaddy.com** → sign in with your GoDaddy account
2. Navigate to the **Microsoft 365 admin panel** (Manage → Admin → Users)
3. For each of the three addresses below, create a new user mailbox **OR** confirm it already exists:

   | Inbox | Purpose |
   |---|---|
   | `quotes@brantbusinessinteriors.com` | All quote requests (from the Quote modal, PDP CTAs) |
   | `design@brantbusinessinteriors.com` | Design consultation requests (Design Services page) |
   | `info@brantbusinessinteriors.com` | General contact / OECM / Industries inquiries |

4. Set forwarding for each to `steve@brantbusinessinteriors.com` so they all land in one place. In GoDaddy M365 admin: Users → [select user] → Mail → Email Forwarding → Add forwarding address.
5. Note the alias/mailbox names — you'll need them when wiring the Shopify contact form routing in LEAD-3.

> **GoDaddy M365 note:** You manage this through GoDaddy's interface, not admin.microsoft.com. If you hit admin.microsoft.com it may redirect you — use email.godaddy.com as the entry point.

---

### Step 2: Fix the SPF record (GoDaddy DNS)

The SPF record currently authorizes GoDaddy legacy email servers but **not Microsoft 365**. This needs to include M365's SPF range.

1. Go to **GoDaddy** → My Products → Domains → `brantbusinessinteriors.com` → **Manage DNS**
2. Find the existing **TXT record** at the root (`@`) that contains `v=spf1 include:secureserver.net -all`
3. **Edit** that record (do not add a second SPF — only one is allowed):

   | Field | Value |
   |---|---|
   | Type | TXT |
   | Host | @ |
   | TXT Value | `v=spf1 include:secureserver.net include:spf.protection.outlook.com -all` |
   | TTL | 1 Hour |

   The only change is adding ` include:spf.protection.outlook.com` before the `-all`. The existing `secureserver.net` include can stay (it covers any GoDaddy-origin mail).

4. Save. Changes propagate in ~15–30 minutes.

---

### Step 3: DKIM — no action needed

DKIM is already configured and active:
- `selector1._domainkey.brantbusinessinteriors.com` has a live RSA public key
- This was generated during the original M365 setup (GoDaddy handles this automatically for their M365 tenants)
- No action required

> **If you ever need to rotate DKIM keys:** GoDaddy M365 admin → Email Security → DKIM → Rotate. GoDaddy will generate a new key for the standby selector and swap after propagation.

---

### Step 4: Add a DMARC reporting address (GoDaddy DNS)

The existing `p=reject` is fine — it means only properly authenticated mail gets through. The problem is you have no visibility into what's failing or passing.

1. Go to **GoDaddy → Manage DNS** for `brantbusinessinteriors.com`
2. Find the existing **TXT record** at `_dmarc` host that contains `v=DMARC1; p=reject;`
3. **Edit** that record:

   | Field | Value |
   |---|---|
   | Type | TXT |
   | Host | `_dmarc` |
   | TXT Value | `v=DMARC1; p=reject; rua=mailto:dmarc-reports@brantbusinessinteriors.com` |
   | TTL | 1 Hour |

   This routes DMARC aggregate reports (daily XML summaries of all mail that used your domain) to `dmarc-reports@brantbusinessinteriors.com`. Create that mailbox in Step 1, or forward it to `steve@brantbusinessinteriors.com`.

   > **Why keep `p=reject`?** With working DKIM (selector1 is live), legitimate M365 mail passes DMARC. `p=reject` protects against spoofing — someone pretending to send from `@brantbusinessinteriors.com` gets blocked. Downgrading to `p=none` would be a step backward.

4. Save.

---

### Step 5: Send test emails — verify receipt

After creating the mailboxes and waiting ~15–30 min for DNS propagation:

1. From a **personal** email address (Gmail / Hotmail — external domain), send a test message to each:
   - `quotes@brantbusinessinteriors.com`
   - `design@brantbusinessinteriors.com`
   - `info@brantbusinessinteriors.com`

2. Confirm each arrives at `steve@brantbusinessinteriors.com` (or whoever you set as the forward target)

3. Reply from `steve@brantbusinessinteriors.com` to each test. Confirm the reply lands in your personal inbox (not spam folder).

4. Take a screenshot of each received + replied test — these are the evidence for marking LEAD-INBOX-1 ✅ in the build tracker.

---

## Verification session prompt (LEAD-INBOX-1 Phase 3)

After completing all manual steps above, paste this into a fresh Claude Code session:

```
You are running LEAD-INBOX-1 Phase 3 — DNS verification after manual provisioning.

Run these checks and report pass/fail for each:

1. SPF — confirm M365 include is present:
   dig TXT brantbusinessinteriors.com +short | grep spf
   PASS if output contains: include:spf.protection.outlook.com
   FAIL if only secureserver.net is present

2. DKIM selector1 — confirm still live:
   dig TXT selector1._domainkey.brantbusinessinteriors.com +short
   PASS if output contains a DKIM public key (v=DKIM1; k=rsa; p=...)
   FAIL if empty or NXDOMAIN

3. DMARC — confirm rua= is present:
   dig TXT _dmarc.brantbusinessinteriors.com +short
   PASS if output contains rua=mailto:
   FAIL if only "v=DMARC1; p=reject;" with no rua

4. MX — confirm M365 is still the mail handler (no accidental change):
   dig MX brantbusinessinteriors.com +short
   PASS if output contains mail.protection.outlook.com
   FAIL if changed

Report: PASS/FAIL per check, plus the raw dig output for each.
If all 4 pass, print: "LEAD-INBOX-1 Phase 3 COMPLETE — mark ✅ in build tracker."
```

---

## DNS records summary (current state + target state)

| Record | Type | Host | Current | Target | Action |
|---|---|---|---|---|---|
| MX | MX | @ | `brantbusinessinteriors-com.mail.protection.outlook.com.` | (unchanged) | None |
| SPF | TXT | @ | `v=spf1 include:secureserver.net -all` | `v=spf1 include:secureserver.net include:spf.protection.outlook.com -all` | **Update** |
| DKIM selector1 | TXT | `selector1._domainkey` | Live RSA key (2048-bit) | (unchanged) | None |
| DKIM selector2 | CNAME | `selector2._domainkey` | Standby CNAME | (unchanged) | None |
| DMARC | TXT | `_dmarc` | `v=DMARC1; p=reject;` | `v=DMARC1; p=reject; rua=mailto:dmarc-reports@brantbusinessinteriors.com` | **Update** |

---

## Steve's hands-on time estimate

| Step | Task | Active time |
|---|---|---|
| Step 1 | Create 3 mailboxes + set forwarding in GoDaddy M365 admin | ~15 min |
| Step 2 | Update SPF record in GoDaddy DNS | ~5 min |
| Step 3 | DKIM — no action | 0 min |
| Step 4 | Update DMARC record in GoDaddy DNS | ~5 min |
| Step 5 | Send + confirm 3 test emails | ~10 min |
| — | Wait for DNS propagation | ~15–30 min (passive) |
| Phase 3 | Verification session | ~5 min |

**Total active time: ~40 min. Total elapsed: ~1 hour.**
