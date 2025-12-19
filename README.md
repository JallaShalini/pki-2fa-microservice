# pki-2fa-Microservice                                   

A secure, containerized microservice implementing Public Key Infrastructure (PKI) and Time-based One-Time Password (TOTP) two-factor authentication.

## Features

- **RSA 4096-bit Encryption**: Secure seed transmission using RSA/OAEP with SHA-256
- **TOTP 2FA**: Time-based One-Time Password authentication with ±30 second tolerance
- **RESTful API**: Three endpoints for seed management and 2FA operations
- **Docker Containerization**: Multi-stage build with persistent data storage
- **Automated Cron Jobs**: Minute-by-minute 2FA code generation and logging
- **Production-Ready**: UTC timezone, proper error handling, and security best practices

## Quick Start

Clone and run
git clone https://github.com/JallaShalini/pki-2fa-microservice.git
cd pki-2fa-microservice
docker-compose up --build -d

Test API (http://localhost:8080)
curl http://localhost:8080/health
curl http://localhost:8080/generate-2fa


## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/decrypt-seed` | POST | Decrypt and store encrypted seed |
| `/generate-2fa` | GET | Generate 6-digit TOTP code |
| `/verify-2fa` | POST | Verify TOTP code (±30s tolerance) |
| `/health` | GET | Health check |

## Project Structure

pki-2fa-microservice/
├── app/
│ ├── api/
│ │ ├── init.py
│ │ ├── models.py # Pydantic request/response models
│ │ └── routes.py # API endpoint implementations
│ ├── crypto/
│ │ ├── init.py
│ │ ├── keys.py # RSA key loading utilities
│ │ └── rsa_ops.py # RSA encryption/decryption operations
│ ├── storage/
│ │ ├── init.py
│ │ └── seed_store.py # Persistent seed storage
│ ├── totp/
│ │ ├── init.py
│ │ └── totp_service.py # TOTP generation and verification
│ ├── init.py
│ ├── config.py # Application configuration
│ ├── logging_config.py # Logging setup
│ └── main.py # FastAPI application
├── cron/
│ └── 2fa-cron # Cron job configuration
├── scripts/
│ ├── generate_commit_proof.py
│ ├── log_2fa_cron.py # Cron execution script
│ └── request_seed.py # Seed request from instructor API
├── tests/
│ ├── init.py
│ ├── test_api.py # API endpoint tests
│ ├── test_cron.py # Cron job tests
│ ├── test_crypto.py # Cryptography tests
│ └── test_totp.py # TOTP generation tests
├── .gitattributes
├── .gitignore
├── conftest.py # Pytest configuration
├── Dockerfile # Multi-stage Docker build
├── docker-compose.yml # Docker orchestration
├── instructor_public.pem # Instructor's public key
├── README.md
├── requirements.txt # Python dependencies
├── student_private.pem # Student private key (for assignment)
└── student_public.pem # Student public key


## Testing
Run all tests
python -m pytest tests/ -v

View cron output (wait 70+ seconds)
docker exec pki-2fa-microservice cat /cron/last_code.txt


## Technology Stack

- **Python 3.10** | **FastAPI** | **Docker**
- **Cryptography**: RSA-4096, OAEP-SHA256, PSS
- **TOTP**: pyotp with SHA-1, 30s periods

## Author

**Jalla Shalini**  
[GitHub Repository](https://github.com/JallaShalini/pki-2fa-microservice)
