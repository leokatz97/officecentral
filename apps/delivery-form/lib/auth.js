// Admin sign-in: one shared password (ADMIN_PASSWORD env var) exchanged for
// a signed, expiring cookie. No accounts, no database.
import { createHash, createHmac, timingSafeEqual } from 'node:crypto';
import { parseCookies } from './http.js';

export const COOKIE_NAME = 'df_admin';
const SESSION_DAYS = 30;

export function adminConfigured() {
  return typeof process.env.ADMIN_PASSWORD === 'string' && process.env.ADMIN_PASSWORD.length >= 6;
}

function secret() {
  // Derive the signing key from the password so rotating the password
  // also signs everyone out.
  return createHash('sha256').update(`df-admin:${process.env.ADMIN_PASSWORD}`).digest();
}

function sign(exp) {
  return createHmac('sha256', secret()).update(String(exp)).digest('base64url');
}

export function passwordMatches(candidate) {
  if (!adminConfigured() || typeof candidate !== 'string') return false;
  const a = createHash('sha256').update(candidate).digest();
  const b = createHash('sha256').update(process.env.ADMIN_PASSWORD).digest();
  return timingSafeEqual(a, b);
}

export function issueCookie() {
  const exp = Date.now() + SESSION_DAYS * 24 * 60 * 60 * 1000;
  const value = `${exp}.${sign(exp)}`;
  return `${COOKIE_NAME}=${value}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=${SESSION_DAYS * 24 * 60 * 60}`;
}

export function clearCookie() {
  return `${COOKIE_NAME}=; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=0`;
}

export function isAuthed(req) {
  if (!adminConfigured()) return false;
  const raw = parseCookies(req)[COOKIE_NAME];
  if (!raw) return false;
  const [expStr, sig] = raw.split('.');
  const exp = Number(expStr);
  if (!Number.isFinite(exp) || exp < Date.now() || !sig) return false;
  const expected = Buffer.from(sign(exp));
  const given = Buffer.from(sig);
  return expected.length === given.length && timingSafeEqual(expected, given);
}
