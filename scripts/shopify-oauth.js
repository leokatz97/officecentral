const http = require('http');
const https = require('https');
const crypto = require('crypto');
const { exec } = require('child_process');
const fs = require('fs');

const CLIENT_ID = process.env.SHOPIFY_CLIENT_ID;
const CLIENT_SECRET = process.env.SHOPIFY_CLIENT_SECRET;
const STORE = 'office-central-online.myshopify.com';
const SCOPES = 'read_products,write_products';
const REDIRECT_URI = 'http://localhost:3000/callback';

const state = crypto.randomBytes(16).toString('hex');
const authUrl = `https://${STORE}/admin/oauth/authorize?client_id=${CLIENT_ID}&scope=${SCOPES}&redirect_uri=${encodeURIComponent(REDIRECT_URI)}&state=${state}`;

const server = http.createServer((req, res) => {
  const url = new URL(req.url, 'http://localhost:3000');
  if (url.pathname !== '/callback') {
    res.end('Not found');
    return;
  }

  const returnedState = url.searchParams.get('state');
  const code = url.searchParams.get('code');

  if (returnedState !== state) {
    res.end('State mismatch — possible CSRF. Try again.');
    server.close();
    return;
  }

  const postData = `client_id=${CLIENT_ID}&client_secret=${CLIENT_SECRET}&code=${code}`;
  const options = {
    hostname: STORE,
    path: '/admin/oauth/access_token',
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Content-Length': Buffer.byteLength(postData),
    },
  };

  const tokenReq = https.request(options, (tokenRes) => {
    let data = '';
    tokenRes.on('data', (chunk) => { data += chunk; });
    tokenRes.on('end', () => {
      const parsed = JSON.parse(data);
      if (parsed.access_token) {
        fs.writeFileSync('.env', `SHOPIFY_TOKEN=${parsed.access_token}\nSHOPIFY_STORE=${STORE}\n`);
        console.log('\n✅ Success! Token saved to .env');
        console.log(`Token: ${parsed.access_token}`);
        res.end('<h1>Connected! You can close this tab.</h1>');
      } else {
        console.error('Error:', data);
        res.end('<h1>Error — check terminal for details.</h1>');
      }
      server.close();
    });
  });

  tokenReq.write(postData);
  tokenReq.end();
});

server.listen(3000, () => {
  console.log('Opening Shopify in your browser...');
  exec(`open "${authUrl}"`);
  console.log('\nIf browser did not open, visit:\n' + authUrl);
});
