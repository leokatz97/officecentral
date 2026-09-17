// Sends the completed form by email through Gmail SMTP (or any SMTP host).
// Env vars: SMTP_USER, SMTP_PASS (a Gmail App Password), optional SMTP_HOST,
// SMTP_PORT, MAIL_FROM.
import nodemailer from 'nodemailer';
import { FIELDS, displayValue } from './brands.js';

export function mailConfigured() {
  return Boolean(process.env.SMTP_USER && process.env.SMTP_PASS);
}

// A Gmail App Password is exactly 16 lowercase letters. Reporting the shape of
// whatever is configured (never the value) turns "invalid login" into a
// specific, fixable answer: wrong kind of password, or spaces left in.
export function passwordShape() {
  const raw = process.env.SMTP_PASS || '';
  if (!raw) return { set: false };
  const stripped = raw.replace(/\s/g, '');
  return {
    set: true,
    chars: raw.length,
    hasSpaces: /\s/.test(raw),
    looksRight: /^[a-zA-Z]{16}$/.test(stripped),
  };
}

function transport() {
  const port = Number(process.env.SMTP_PORT || 465);
  return nodemailer.createTransport({
    host: process.env.SMTP_HOST || 'smtp.gmail.com',
    port,
    secure: port === 465,
    // Google displays App Passwords in four spaced groups; the spaces are
    // presentational and must not be sent.
    auth: { user: process.env.SMTP_USER, pass: (process.env.SMTP_PASS || '').replace(/\s/g, '') },
  });
}

function escapeHtml(s) {
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

export function buildEmail(brand, record) {
  const v = record.values;
  const subject = `Delivery Info: ${v.customer} | Quote #${v.quote} | ${v.rep.split(' (')[0]}`;

  const rows = FIELDS.map((f) => [f.label, displayValue(f, v[f.key]) || '—']);
  rows.push(['Submitted', new Date(record.submittedAt).toLocaleString('en-CA', { timeZone: 'America/Toronto' }) + ' (Toronto)']);
  rows.push(['Form', brand.name]);

  const text = [`${brand.name} — Delivery Information`, '', ...rows.map(([k, val]) => `${k}: ${val}`)].join('\n');

  const html = `<!doctype html><html><body style="font-family:Arial,Helvetica,sans-serif;color:#222;font-size:15px">
<h2 style="margin:0 0 4px;color:${brand.accent}">${escapeHtml(brand.name)}</h2>
<p style="margin:0 0 16px;color:#555">Delivery Information submitted by ${escapeHtml(v.rep)}</p>
<table cellpadding="0" cellspacing="0" style="border-collapse:collapse;min-width:420px">
${rows
  .map(
    ([k, val]) => `<tr>
  <td style="padding:8px 12px;border:1px solid #ddd;background:#f6f6f6;font-weight:bold;vertical-align:top;white-space:nowrap">${escapeHtml(k)}</td>
  <td style="padding:8px 12px;border:1px solid #ddd;vertical-align:top">${escapeHtml(val).replace(/\n/g, '<br>')}</td>
</tr>`,
  )
  .join('\n')}
</table>
</body></html>`;

  return { subject, text, html };
}

// A plain address in From looks like a stranger to spam filters; a display
// name makes the notification recognisable in the delivery team's inbox.
function fromAddress() {
  if (process.env.MAIL_FROM) return process.env.MAIL_FROM;
  return { name: 'Office Central Delivery Forms', address: process.env.SMTP_USER };
}

// Sent from the admin view to prove the email path works end to end.
export async function sendTestEmail(brand) {
  const when = new Date().toLocaleString('en-CA', { timeZone: 'America/Toronto' });
  const info = await transport().sendMail({
    from: fromAddress(),
    to: brand.mailTo.join(', '),
    cc: brand.mailCc.length ? brand.mailCc.join(', ') : undefined,
    subject: `Test: ${brand.name} delivery form`,
    text: `This is a test from the ${brand.name} delivery information form, sent ${when} (Toronto).\n\nIf you can read this, delivery form emails reach this inbox. Nothing to action.\n\nIf this landed in junk or spam, mark it "not junk" so real submissions come through.`,
  });
  return info.messageId;
}

export async function sendSubmissionEmail(brand, record) {
  const { subject, text, html } = buildEmail(brand, record);
  const info = await transport().sendMail({
    from: fromAddress(),
    to: brand.mailTo.join(', '),
    cc: brand.mailCc.length ? brand.mailCc.join(', ') : undefined,
    replyTo: record.values.contactEmail || undefined,
    subject,
    text,
    html,
  });
  return info.messageId;
}
