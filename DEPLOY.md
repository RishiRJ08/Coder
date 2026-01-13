# Deployment and Secrets

This file describes the repository secrets and a simple Render deployment flow used by the CI workflow.

Repository secrets (GitHub Settings → Secrets → Actions):

- `GITHUB_TOKEN` (automatically provided) — used to authenticate to GHCR for pushing images. No action needed in most repos.
- `CR_PAT` (optional) — Personal Access Token with `write:packages` if you need a dedicated token for GHCR.
- `RENDER_API_KEY` — Render API key (service-level) used to trigger deploys via the Render API.
- `RENDER_SERVICE_ID` — Render Service ID (the target service to deploy).

Render deploy trigger (used by CI):

The CI workflow builds and pushes a Docker image to GHCR. If `RENDER_API_KEY` and `RENDER_SERVICE_ID` are present, the workflow will POST to the Render API to create a new deploy for the given service. Ensure your Render service is configured to pull images from GHCR or is set up to use your Docker image.

To obtain `RENDER_API_KEY`:

1. Log into Render → Dashboard → Account Settings → API Keys → create an API key.
2. Save the API key in the repository secrets as `RENDER_API_KEY`.

To obtain `RENDER_SERVICE_ID`:

1. In Render Dashboard open your service and copy the service ID from the URL or from the service settings.
2. Save it as `RENDER_SERVICE_ID` in repository secrets.

Security

- Do not add private keys or API keys to the repo. Use GitHub Secrets.
- Limit token permissions where possible.
