# Deployment Guide

This guide details best practices for deploying DryGram applications in production.

## Systemd Service configuration

Deploy your bot using a standard systemd service unit:

`/etc/systemd/system/drygram-bot.service`:
```ini
[Unit]
Description=DryGram Asynchronous Bot Daemon
After=network.target

[Service]
Type=simple
User=botuser
WorkingDirectory=/opt/my_bot
ExecStart=/opt/my_bot/venv/bin/python main.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

## Docker Container configuration

Create a lightweight container image for your DryGram app:

`Dockerfile`:
```dockerfile
FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

## Security Best Practices

- **Vault Encryption**: Encrypt session files using `EncryptedSession` or supply password keys to `export_session()` to protect authorization details.
- **Environment Variables**: Never commit `api_id` or `api_hash` to git. Load them from env vars:
  ```python
  import os
  api_id = int(os.environ["TELEGRAM_API_ID"])
  api_hash = os.environ["TELEGRAM_API_HASH"]
  ```
