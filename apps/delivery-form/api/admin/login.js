import { readJsonBody, sendJson, methodNotAllowed } from '../../lib/http.js';
import { adminConfigured, passwordMatches, issueCookie } from '../../lib/auth.js';

export default async function handler(req, res) {
  if (req.method !== 'POST') return methodNotAllowed(res, 'POST');
  if (!adminConfigured()) {
    return sendJson(res, 503, { ok: false, error: 'Admin password is not set up yet.', setup: true });
  }
  const body = (await readJsonBody(req)) || {};
  if (!passwordMatches(body.password)) {
    return sendJson(res, 401, { ok: false, error: 'Wrong password.' });
  }
  sendJson(res, 200, { ok: true }, { 'Set-Cookie': issueCookie() });
}
