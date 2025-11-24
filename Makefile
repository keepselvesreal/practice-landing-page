.PHONY: help deploy-backend deploy-frontend deploy-staging test-staging smoke-test-staging deploy-staging-verified smoke-test-production deploy-production-backend deploy-production-frontend deploy-production test-e2e-docker clean

# 기본 타겟
help:
	@echo "K-Beauty Landing Page - Makefile"
	@echo ""
	@echo "=== E2E Tests ==="
	@echo "  make test-e2e-docker            - Run E2E tests with docker-compose (auto cleanup)"
	@echo ""
	@echo "=== Staging Commands ==="
	@echo "  make deploy-backend             - Deploy backend only (staging)"
	@echo "  make deploy-frontend            - Deploy frontend only (staging)"
	@echo "  make deploy-staging             - Deploy backend + frontend (staging)"
	@echo "  make deploy-staging-verified    - Deploy + E2E tests (staging)"
	@echo "  make test-staging               - Run E2E tests against staging"
	@echo "  make smoke-test-staging         - Run smoke tests against staging"
	@echo ""
	@echo "=== Production Commands ==="
	@echo "  make deploy-production-backend  - Deploy backend only (production)"
	@echo "  make deploy-production-frontend - Deploy frontend only (production)"
	@echo "  make deploy-production          - Deploy backend + frontend + smoke test (production)"
	@echo "  make smoke-test-production      - Run smoke tests against production"
	@echo ""
	@echo "=== Utilities ==="
	@echo "  make clean                      - Clean up build artifacts"
	@echo ""
	@echo "Environment variables:"
	@echo "  ENV_FILE             - Environment file to use (required for deploy-backend/frontend)"

# 기본 배포 (staging으로 매핑)
deploy-backend: deploy-staging-backend

deploy-frontend: deploy-staging-frontend

# Staging 백엔드 배포
deploy-staging-backend:
	@echo "🚀 Deploying backend to Cloud Run (Staging)..."
	@ENV_FILE=.env.staging ./scripts/deploy-backend.sh

# Staging 프론트엔드 배포
deploy-staging-frontend:
	@echo "🚀 Deploying frontend to Firebase Hosting (Staging)..."
	@ENV_FILE=.env.staging ./scripts/deploy-frontend.sh

# 스모크 테스트 (Staging)
smoke-test-staging:
	@echo "🧪 Running smoke tests on staging..."
	@./scripts/smoke-test.sh

# Staging E2E 테스트
test-staging:
	@echo "🧪 Running E2E tests against staging..."
	@./scripts/test-staging.sh
	
# Staging 전체 배포 (백엔드 → 프론트엔드)
deploy-staging: deploy-staging-backend deploy-staging-frontend
	@echo "✅ Staging deployment complete!"

# Staging 배포 + E2E 검증 (안전한 배포)
deploy-staging-verified: deploy-staging test-staging
	@echo "🎉 Staging deployment verified with E2E tests!"

# Production 백엔드 배포
deploy-production-backend:
	@echo "🚀 Deploying backend to Cloud Run (Production)..."
	@ENV_FILE=.env.production ./scripts/deploy-backend.sh

# Production 프론트엔드 배포
deploy-production-frontend:
	@echo "🚀 Deploying frontend to Firebase Hosting (Production)..."
	@ENV_FILE=.env.production ./scripts/deploy-frontend.sh

# 스모크 테스트 (Production)
smoke-test-production:
	@echo "🧪 Running smoke tests on production..."
	@ENV_FILE=.env.production ./scripts/smoke-test.sh

# Production 전체 배포 (백엔드 → 프론트엔드 → 스모크 테스트)
deploy-production: deploy-production-backend deploy-production-frontend smoke-test-production
	@echo "✅ Production deployment complete!"

# E2E 테스트 (도커 환경)
test-e2e-docker:
	@echo "🔨 Building latest images..."
	docker compose -f docker-compose.test.yml build
	@echo "🐳 Starting services with docker compose..."
	docker compose -f docker-compose.test.yml up -d
	@echo "⏳ Waiting for services to be ready..."
	@sleep 15
	@echo "🧪 Running E2E tests..."
	cd backend && TEST_ENV=docker BASE_URL=http://localhost:8080 \
		uv run pytest tests/e2e/ -v -s
	@echo "🧹 Cleaning up..."
	docker compose -f docker-compose.test.yml down -v --rmi all
	@echo "✅ Docker E2E tests complete!"

# 정리
clean:
	@echo "🧹 Cleaning up..."
	@rm -rf backend/.pytest_cache
	@rm -rf backend/.venv
	@rm -rf backend/__pycache__
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Cleanup complete!"
