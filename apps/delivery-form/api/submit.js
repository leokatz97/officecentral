// Receives a completed form: saves it, emails it, and tells the rep what happened.
import { getBrand, validateSubmission } from '../lib/brands.js';
import { readJsonBody, sendJson, methodNotAllowed } from '../lib/http.js';
import { storeConfigured, saveSubmission, newId } from '../lib/store.js';
import { mailConfigured, sendSubmissionEmail } from '../lib/mail.js';

export default async function handler(req, res) {
  if (req.method !== 'POST') return methodNotAllowed(res, 'POST');

  const body = await readJsonBody(req);
  if (!body) return sendJson(res, 400, { ok: false, error: 'Could not read the form.' });

  // Honeypot: real people never fill this hidden box.
  if (body.website) return sendJson(res, 200, { ok: true, id: newId(), stored: false, emailed: false });

  const brand = getBrand(body.brand);
  if (!brand) return sendJson(res, 400, { ok: false, error: 'Unknown form.' });

  const { values, errors } = validateSubmission(body, brand);
  if (Object.keys(errors).length) return sendJson(res, 422, { ok: false, errors });

  const record = {
    id: newId(),
    brand: brand.slug,
    submittedAt: new Date().toISOString(),
    values,
    handled: false,
    handledAt: null,
    email: { status: mailConfigured() ? 'pending' : 'not-configured', to: brand.mailTo, cc: brand.mailCc, error: null, sentAt: null },
  };

  let stored = false;
  if (storeConfigured()) {
    try {
      await saveSubmission(record);
      stored = true;
    } catch (err) {
      console.error('Blob save failed', err);
    }
  }

  let emailed = false;
  if (mailConfigured()) {
    try {
      await sendSubmissionEmail(brand, record);
      record.email.status = 'sent';
      record.email.sentAt = new Date().toISOString();
      emailed = true;
    } catch (err) {
      console.error('Email failed', err);
      record.email.status = 'failed';
      record.email.error = String(err && err.message ? err.message : err).slice(0, 300);
    }
    if (stored) {
      try {
        await saveSubmission(record);
      } catch (err) {
        console.error('Blob update failed', err);
      }
    }
  }

  if (!stored && !emailed) {
    return sendJson(res, 500, {
      ok: false,
      error: 'The form could not be delivered. Please call the office with the details.',
    });
  }

  sendJson(res, 200, { ok: true, id: record.id, stored, emailed });
}
