# Registering the GitHub App (exact values)

Use the manifest below when creating the app from a manifest, or copy the values into the "Create a GitHub App" UI.

Manifest (use these exact fields and replace hostnames with your production URL):

```yaml
name: Coder GitHub App
url: https://YOUR_DOMAIN_OR_HOST
hook_attributes:
  url: https://YOUR_DOMAIN_OR_HOST/webhook
  active: true
redirect_url: https://YOUR_DOMAIN_OR_HOST/setup
public: false
default_permissions:
  contents: read
  issues: write
  pull_requests: write
default_events:
  - push
  - pull_request
```

Exact values / notes:
- `name`: Coder GitHub App
- `url`: the public URL where your app's web UI runs (example: `https://app.example.com`).
- `hook_attributes.url`: webhook endpoint `https://<your-host>/webhook` (must be reachable from GitHub).
- `redirect_url`: `https://<your-host>/setup` (where GitHub redirects after install/configuration).
- `public`: set to `false` for private/internal apps.
- `default_permissions` and `default_events`: recommended minimal permissions for this scaffold.

After creating the app in GitHub Developer Settings (or using the manifest flow):

1. In the GitHub App settings, generate and download the private key. Store it somewhere secure (do not commit).
2. Set the webhook secret in the App settings; copy it to your server environment as `WEBHOOK_SECRET`.
3. Note the App ID (use `GITHUB_APP_ID` env var) and the Installation ID when you install the app to a repository.

Required environment variables (for `app.py`):
- `GITHUB_APP_ID` — the numeric App ID from the GitHub App page.
- `GITHUB_PRIVATE_KEY_PATH` — path to the PEM private key (default `secrets/app-private-key.pem`).
- `WEBHOOK_SECRET` — the webhook secret you set in the App settings.
- `PORT` — optional, default 5000.

Recommended repository secrets for CI/CD:
- `CR_PAT` (optional) — a Personal Access Token with `write:packages` and `read:packages` if `GITHUB_TOKEN` cannot push to GHCR for your account.

Security notes:
- Never commit private keys or secrets to the repository. Use the `secrets/` directory locally (ignored via `.gitignore`) or use your platform's secrets store.
- In production, host the app behind HTTPS and keep webhook endpoints protected.
