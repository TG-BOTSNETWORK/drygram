# Authentication

DryGram supports the latest secure authentication protocols.

## QR Code Login
```python
qr_link = await client.request_qr_code()
# Render qr_link as QR Code
```

## 2FA & Password Verification
```python
await client.submit_password("your_secret_password")
```
