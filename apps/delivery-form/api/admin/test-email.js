// Sends a test email to one company's delivery inbox so the office can prove
// the email path works without submitting a real form.
import { readJsonBody, sendJson, methodNotAllowed } from '../../lib/http.js';
import { isAuthed } from '../../lib/auth.js';
import { getBrand } from '../../lib/brands.js';
import { mailConfigured, sendTestEmail } from '../../lib/mail.js';

export default async function handler(req, res) {
  if (req.method !== 'POST') return methodNotAllowed(res, 'POST');
  if (!isAuthed(req)) return sendJson(res, 401, { ok: false, error: 'Please sign in.' });
  if (!mailConfigured()) return sendJson(res, 503, { ok: false, error: 'Email is not set up yet.' });
  const body = (await readJsonBody(req)) || {};
  const brand = getBrand(body.brand);
  if (!brand) return sendJson(res, 400, { ok: false, error: 'Unknown form.' });
  try {
    await sendTestEmail(brand);
    sendJson(res, 200, { ok: true, to: brand.mailTo, cc: brand.mailCc });
  } catch (err) {
    console.error('Test email failed', err);
    sendJson(res, 502, { ok: false, error: String(err && err.message ? err.message : err).slice(0, 300) });
  }
}
