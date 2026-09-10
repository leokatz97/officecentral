import { sendJson, methodNotAllowed } from '../../lib/http.js';
import { isAuthed } from '../../lib/auth.js';
import { storeConfigured, listSubmissions } from '../../lib/store.js';

export default async function handler(req, res) {
  if (req.method !== 'GET') return methodNotAllowed(res, 'GET');
  if (!isAuthed(req)) return sendJson(res, 401, { ok: false, error: 'Please sign in.' });
  if (!storeConfigured()) return sendJson(res, 200, { ok: true, submissions: [], storeConfigured: false });
  try {
    const submissions = await listSubmissions();
    sendJson(res, 200, { ok: true, submissions, storeConfigured: true });
  } catch (err) {
    console.error('List failed', err);
    sendJson(res, 500, { ok: false, error: 'Could not load submissions.' });
  }
}
