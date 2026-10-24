# Production session routing

The browser calls `/api/*` on its Vercel origin, with credentials included.
Next.js forwards requests to `NEXT_PUBLIC_API_URL` (the Render origin).
Set `NEXT_PUBLIC_API_URL=https://powermananager.onrender.com` before rebuilding
and deploying Vercel. Do not point it at the Vercel frontend itself.

The proxy preserves separate Set-Cookie headers. Host-only cookies are stored
under the Vercel host because that is the host the browser contacted. Their
HttpOnly, Secure, SameSite=None, Path=/ and expiration attributes are unchanged.
Only PowerManage cookies are forwarded to Render. CSRF validation stays enabled.
This avoids depending on browser third-party cookie permissions.

Render: keep SESSION_COOKIE_SECURE=true, SESSION_COOKIE_SAMESITE=none,
SESSION_TTL_HOURS=168 and exact trusted CORS_ORIGINS. Do not add cookie Domain.
Users need to sign in once again after switching from direct Render requests.

Verify Chrome, a private window and another browser using the same production
URL: login must set cookies for the frontend host; the subsequent `/api/auth/me`
request must include them and return 200. Repeat after 30 seconds and a reload.
Check both administrator and normal-user accounts, then verify logout clears
the cookies and `/api/auth/me` returns 401. Each distinct preview hostname has
its own cookie jar and requires its own login.
