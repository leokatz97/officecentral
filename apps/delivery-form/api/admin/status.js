// Which pieces are set up. Safe to expose: booleans only, but still behind sign-in
// except for the adminPassword flag the sign-in screen needs.
import { sendJson, methodNotAllowed } from '../../lib/http.js';
import { adminConfigured, isAuthed } from '../../lib/auth.js';
import { storeConfigured } from '../../lib/store.js';
import { mailConfigured } from '../../lib/mail.js';
import { BRANDS } from '../../lib/brands.js';

export default function handler(req, res) {
  if (req.method !== 'GET') return methodNotAllowed(res, 'GET');
  const authed = isAuthed(req);
  const payload = { adminPassword: adminConfigured(), authed };
  if (authed) {
    payload.store = storeConfigured();
    payload.mail = mailConfigured();
    payload.recipients = Object.fromEntries(
      Object.values(BRANDS).map((b) => [b.slug, { name: b.name, to: b.mailTo, cc: b.mailCc }]),
    );
  }
  sendJson(res, 200, payload);
}
