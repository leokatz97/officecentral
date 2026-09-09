// Mark a submission handled / not handled.
import { readJsonBody, sendJson, methodNotAllowed } from '../../lib/http.js';
import { isAuthed } from '../../lib/auth.js';
import { storeConfigured, getSubmission, saveSubmission, validId } from '../../lib/store.js';

export default async function handler(req, res) {
  if (req.method !== 'POST') return methodNotAllowed(res, 'POST');
  if (!isAuthed(req)) return sendJson(res, 401, { ok: false, error: 'Please sign in.' });
  if (!storeConfigured()) return sendJson(res, 503, { ok: false, error: 'Storage is not set up.' });
  const body = (await readJsonBody(req)) || {};
  if (!validId(body.id)) return sendJson(res, 400, { ok: false, error: 'Bad id.' });
  try {
    const record = await getSubmission(body.id);
    if (!record) return sendJson(res, 404, { ok: false, error: 'Not found.' });
    record.handled = Boolean(body.handled);
    record.handledAt = record.handled ? new Date().toISOString() : null;
    await saveSubmission(record);
    sendJson(res, 200, { ok: true, submission: record });
  } catch (err) {
    console.error('Update failed', err);
    sendJson(res, 500, { ok: false, error: 'Could not save the change.' });
  }
}
