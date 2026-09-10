// Submission storage on Vercel Blob (private). One JSON file per submission.
// Connecting a Blob store to the Vercel project injects a read-write token.
// Vercel names it BLOB_READ_WRITE_TOKEN by default, or <prefix>_READ_WRITE_TOKEN
// when the store was connected with a custom prefix, so accept either.
import { put, list, get } from '@vercel/blob';

const PREFIX = 'submissions/';
const ID_RE = /^[A-Za-z0-9-]{10,80}$/;
const MAX_LISTED = 2000;

function blobToken() {
  if (process.env.BLOB_READ_WRITE_TOKEN) return process.env.BLOB_READ_WRITE_TOKEN;
  const key = Object.keys(process.env).find(
    (k) => k.endsWith('_READ_WRITE_TOKEN') && String(process.env[k]).startsWith('vercel_blob_rw_'),
  );
  return key ? process.env[key] : '';
}

export function storeConfigured() {
  return Boolean(blobToken());
}

export function newId() {
  const stamp = new Date().toISOString().replace(/[:.]/g, '-').replace('Z', '');
  const rand = Math.random().toString(36).slice(2, 8);
  return `${stamp}-${rand}`;
}

export function validId(id) {
  return typeof id === 'string' && ID_RE.test(id);
}

export async function saveSubmission(record) {
  if (!validId(record.id)) throw new Error('Bad submission id');
  await put(`${PREFIX}${record.id}.json`, JSON.stringify(record), {
    access: 'private',
    contentType: 'application/json',
    addRandomSuffix: false,
    allowOverwrite: true,
    token: blobToken(),
  });
}

export async function getSubmission(id) {
  if (!validId(id)) return null;
  const result = await get(`${PREFIX}${id}.json`, { access: 'private', useCache: false, token: blobToken() });
  if (!result || !result.stream) return null;
  return JSON.parse(await new Response(result.stream).text());
}

export async function listSubmissions() {
  const blobs = [];
  let cursor;
  do {
    const page = await list({ prefix: PREFIX, cursor, limit: 1000, token: blobToken() });
    blobs.push(...page.blobs);
    cursor = page.hasMore ? page.cursor : undefined;
  } while (cursor && blobs.length < MAX_LISTED);

  // Newest first; ids start with an ISO timestamp so pathname order is time order.
  blobs.sort((a, b) => (a.pathname < b.pathname ? 1 : -1));

  const records = await mapLimit(blobs, 12, async (blob) => {
    try {
      const result = await get(blob.url, { access: 'private', useCache: false, token: blobToken() });
      if (!result || !result.stream) return null;
      return JSON.parse(await new Response(result.stream).text());
    } catch (err) {
      console.error('Could not read submission', blob.pathname, err);
      return null;
    }
  });
  return records.filter(Boolean);
}

async function mapLimit(items, limit, fn) {
  const out = new Array(items.length);
  let next = 0;
  async function worker() {
    while (next < items.length) {
      const i = next++;
      out[i] = await fn(items[i]);
    }
  }
  await Promise.all(Array.from({ length: Math.min(limit, items.length) }, worker));
  return out;
}
