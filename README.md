# DevOps Deployment Monitor

A lightweight Python web application built with **Flask**. It exposes a simple deployment-status page and JSON endpoints that can be used by a load balancer, monitoring tool, or CI/CD pipeline to verify that an application deployment is responding.

> **Project status:** The Flask application is implemented. Docker packaging and CI/CD automation are the next steps; this repository currently does not include a `Dockerfile`, Jenkinsfile, or GitHub Actions workflow. The page text mentioning Docker/Jenkins is descriptive placeholder text, not proof that a pipeline is configured.

## Features

- Home page showing application name, version, environment, and host name.
- `GET /health` — health-check response with a UTC timestamp.
- `GET /version` — application version and environment.
- `GET /deployment` — deployment status, host name, and UTC timestamp.
- Configuration through environment variables.
- Structured application logging to standard output.

## Tech stack

- Python
- Flask 3.1.2
- Environment-based configuration

## Repository structure

```text
python-devops-project/
├── app/
│   ├── __init__.py       # Flask application factory
│   ├── config.py         # Environment-based configuration
│   └── routes.py         # Web page and API endpoints
├── .dockerignore
├── .env.example          # Example configuration (no secrets)
├── .gitignore
├── app.py                # Application entry point
├── requirements.txt
└── README.md
```

## Prerequisites

- Python 3.10 or later
- `pip`
- Git

## Run locally

### 1. Clone the repository

```bash
git clone https://github.com/<YOUR_GITHUB_USERNAME>/<YOUR_REPOSITORY>.git
cd <YOUR_REPOSITORY>
```

### 2. Create and activate a virtual environment

**Linux / macOS**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows PowerShell**
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example file and edit values if needed.

**Linux / macOS**
```bash
cp .env.example .env
```

**Windows PowerShell**
```powershell
Copy-Item .env.example .env
```

The application reads environment variables from the process environment. The `.env` file is an example for your own reference; the application does not automatically load it. Export variables in your shell or configure them in your deployment environment.

| Variable | Default | Purpose |
|---|---|---|
| `APP_NAME` | `DevOps Deployment Monitor` | Display name |
| `APP_VERSION` | `1.0.0` | Application version |
| `ENVIRONMENT` | `Development` | Environment label |
| `FLASK_DEBUG` | `false` | Enables Flask debug mode when true |
| `HOST` | `0.0.0.0` | Bind address |
| `PORT` | `5000` | HTTP port |
| `LOG_LEVEL` | `INFO` | Python logging level |

### 5. Start the application

```bash
python app.py
```

Open `http://localhost:5000` in your browser.

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/` | Human-readable application status page |
| `GET` | `/health` | Health check; returns HTTP 200 when the app responds |
| `GET` | `/version` | Application version and environment |
| `GET` | `/deployment` | Deployment status and server hostname |

Example health-check request:

```bash
curl http://localhost:5000/health
```

Example response (timestamp will vary):

```json
{
  "status": "healthy",
  "application": "DevOps Deployment Monitor",
  "version": "1.0.0",
  "timestamp": "2026-01-01T00:00:00+00:00"
}
```

## CI/CD implementation plan

The intended delivery flow for this project is:

1. Developer pushes code to GitHub.
2. CI pipeline checks out the repository and installs Python dependencies.
3. Automated tests and quality checks run.
4. A Docker image is built and tagged with the Git commit SHA.
5. The image is pushed to a container registry.
6. CD deploys the image to the target server.
7. The pipeline calls `/health` and fails if the health check does not pass.

**Not implemented yet:** automated tests, Docker image build, registry publishing, deployment automation, and post-deployment health verification. These should be added incrementally rather than claiming they already exist.

## Security and repository hygiene

- Do not commit `.env`, credentials, SSH private keys, cloud access keys, or registry passwords.
- Keep secrets in GitHub Actions Secrets or your CI/CD platform's credential store.
- Do not enable Flask debug mode in a deployed environment.
- Use a production WSGI server (for example, Gunicorn) instead of Flask's development server for production deployment.
- Review `.gitignore` before the first push to ensure virtual environments, caches, logs, and local secrets are excluded.

## License

No license has been added yet. Add a `LICENSE` file before permitting reuse or redistribution.
