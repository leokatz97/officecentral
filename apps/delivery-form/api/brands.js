import { publicBrands, FIELDS, OTHER } from '../lib/brands.js';
import { sendJson, methodNotAllowed } from '../lib/http.js';

export default function handler(req, res) {
  if (req.method !== 'GET') return methodNotAllowed(res, 'GET');
  sendJson(res, 200, { brands: publicBrands(), fields: FIELDS, other: OTHER });
}
