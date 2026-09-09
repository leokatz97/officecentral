// Sends the completed form by email through Gmail SMTP (or any SMTP host).
// Env vars: SMTP_USER, SMTP_PASS (a Gmail App Password), optional SMTP_HOST,
// SMTP_PORT, MAIL_FROM.
import nodemailer from 'nodemailer';
import { FIELDS } from './brands.js';

export function mailConfigured() {
  return Boolean(process.env.SMTP_USER && process.env.SMTP_PASS);
}

function transport() {
  const port = Number(process.env.SMTP_PORT || 465);
  return nodemailer.createTransport({
    host: process.env.SMTP_HOST || 'smtp.gmail.com',
    port,
    secure: port === 465,
    auth: { user: process.env.SMTP_USER, pass: process.env.SMTP_PASS },
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

  const rows = FIELDS.map((f) => [f.label, v[f.key] || '—']);
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

export async function sendSubmissionEmail(brand, record) {
  const { subject, text, html } = buildEmail(brand, record);
  const info = await transport().sendMail({
    from: process.env.MAIL_FROM || process.env.SMTP_USER,
    to: brand.mailTo.join(', '),
    cc: brand.mailCc.length ? brand.mailCc.join(', ') : undefined,
    replyTo: record.values.contactEmail || undefined,
    subject,
    text,
    html,
  });
  return info.messageId;
}
