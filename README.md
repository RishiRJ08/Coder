# Coder — GitHub App scaffold

This repository contains a minimal scaffold to turn this project into a GitHub App.

Quick steps

1. Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

2. Generate a private key (PEM) and keep it secret:

```bash
mkdir -p secrets
openssl genrsa -out secrets/app-private-key.pem 2048
```

3. Set required environment variables and run the example server:

```bash
export GITHUB_APP_ID=<your-app-id>
export GITHUB_PRIVATE_KEY_PATH=secrets/app-private-key.pem
export WEBHOOK_SECRET=<your-webhook-secret>
python3 app.py
```

4. Create the GitHub App from the manifest: open GitHub → Settings → Developer settings → GitHub Apps → "Create a GitHub App from a manifest" and use `.github/manifest.yml` (or paste values) and set the app's URLs to your server.

Notes

- The endpoint `/jwt` returns a short-lived app JWT (for testing). Use it to request installation access tokens.
- The endpoint `/webhook` receives GitHub webhooks and validates the signature using `WEBHOOK_SECRET`.
- Do NOT commit real private keys. Add them to `secrets/` and keep the files out of git.

Publishing the static game with GitHub Pages

- The game is available as a static site at `docs/index.html`. GitHub Pages will publish the `docs/` folder on push to `main`.
- There's an Actions workflow `.github/workflows/pages.yml` that publishes `docs/` to GitHub Pages automatically.
- After pushing, go to your repository Settings → Pages to confirm the site URL. The site will be available at `https://<your-username>.github.io/<repo>/`.
