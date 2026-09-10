import { sendJson, methodNotAllowed } from '../../lib/http.js';
import { clearCookie } from '../../lib/auth.js';

export default function handler(req, res) {
  if (req.method !== 'POST') return methodNotAllowed(res, 'POST');
  sendJson(res, 200, { ok: true }, { 'Set-Cookie': clearCookie() });
}
