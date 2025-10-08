# Cosmetics Landing Page

MVP for cosmetics product with affiliate program, built with Hexagonal Architecture and TDD.

## Business Goals
- 10 MVP sales
- 5 influencer partnerships

## Tech Stack
- **Backend**: FastAPI + SQLAlchemy
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **Payment**: PayPal
- **Address Validation**: Google Places API
- **Email**: Gmail SMTP

## Architecture
Hexagonal Architecture (Ports and Adapters):
- **Domain Layer**: Business logic (Order, Affiliate entities)
- **Application Layer**: Use cases and ports
- **Adapter Layer**: External integrations (Web, DB, PayPal, etc.)
- **Config Layer**: Dependency injection

## Setup
```bash
# Install dependencies
uv pip install -e ".[dev]"

# Copy environment file
cp .env.example .env

# Run tests
pytest

# Run server
uvicorn src.cosmetics_landing.config.main:app --reload
```

## Project Structure
See `docs/landing_page/imple_guide_v2.md` for detailed architecture documentation.
