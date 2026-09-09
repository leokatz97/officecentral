// Small helpers so the API handlers work the same under Vercel's Node
// runtime and the local dev server (plain Node http objects).

export async function readJsonBody(req, limit = 64 * 1024) {
  if (req.body !== undefined && req.body !== null) {
    if (typeof req.body === 'string') return safeParse(req.body);
    if (Buffer.isBuffer(req.body)) return safeParse(req.body.toString('utf8'));
    return req.body;
  }
  return new Promise((resolve) => {
    let data = '';
    req.on('data', (chunk) => {
      data += chunk;
      if (data.length > limit) {
        resolve(null);
        req.destroy();
      }
    });
    req.on('end', () => resolve(safeParse(data)));
    req.on('error', () => resolve(null));
  });
}

function safeParse(text) {
  try {
    const parsed = JSON.parse(text || '{}');
    return parsed && typeof parsed === 'object' ? parsed : null;
  } catch {
    return null;
  }
}

export function sendJson(res, status, payload, extraHeaders = {}) {
  res.statusCode = status;
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.setHeader('Cache-Control', 'no-store');
  for (const [k, v] of Object.entries(extraHeaders)) res.setHeader(k, v);
  res.end(JSON.stringify(payload));
}

export function methodNotAllowed(res, allow) {
  res.setHeader('Allow', allow);
  sendJson(res, 405, { ok: false, error: `Use ${allow}.` });
}

export function parseCookies(req) {
  const header = req.headers.cookie || '';
  const out = {};
  for (const part of header.split(';')) {
    const idx = part.indexOf('=');
    if (idx === -1) continue;
    const name = part.slice(0, idx).trim();
    if (name) out[name] = decodeURIComponent(part.slice(idx + 1).trim());
  }
  return out;
}
