# Delivery Information Form (sales reps)

Small standalone web app for Steve's sales team. Lives outside `theme/` on
purpose: it is not part of the Shopify storefront. Hosted on Vercel.

## What it does

- `/schoolhouse`, `/office-central`, `/brant`: the rep form, one per company.
  Same questions; the logo colour and the email recipients change.
- On submit the form is (1) saved and (2) emailed to that company's delivery
  inbox. The rep sees a confirmation with everything they entered.
- `/admin`: password-protected list of every submission. Search, filter by
  company or rep, open a row for full details, tick "handled", download CSV.

## Change the questions, reps, or recipients

Everything lives in `lib/brands.js`. Edit and redeploy.

## Vercel setup (one time)

1. **Storage:** project → Storage → Create Database → Blob → connect to the
   project. This injects `BLOB_READ_WRITE_TOKEN`.
2. **Email:** project → Settings → Environment Variables:
   - `SMTP_USER`: the Gmail / Google Workspace address that sends the email.
   - `SMTP_PASS`: a Gmail App Password for that account
     (Google Account → Security → 2-Step Verification → App passwords).
   - Optional: `SMTP_HOST`, `SMTP_PORT` (defaults: `smtp.gmail.com`, `465`),
     `MAIL_FROM`.
3. **Admin password:** `ADMIN_PASSWORD` (6+ characters).
4. Redeploy after adding variables.

Until storage and email are both connected, the admin view shows what is
still missing. If neither is connected, the form tells the rep it could not
be delivered instead of silently dropping the entry.

## Files

```
api/            Vercel serverless functions (submit, brands, admin/*)
lib/            brands + fields, storage (Vercel Blob), email (nodemailer), auth
public/         static pages: index (picker), form, admin, app.css
vercel.json     clean URLs, brand rewrites, security headers
```

## Local run

There is no framework. Any static server plus the `api/` handlers works;
`vercel dev` is the simplest.
