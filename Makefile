.PHONY: help deploy-backend deploy-frontend deploy-all test-staging smoke-test-staging smoke-test-production deploy-production-backend deploy-production-frontend deploy-production clean

# 기본 타겟
help:
	@echo "K-Beauty Landing Page - Deployment Makefile"
	@echo ""
	@echo "=== Staging Deployment ==="
	@echo "  make deploy-backend          - Deploy backend to Cloud Run (staging)"
	@echo "  make deploy-frontend         - Deploy frontend to Firebase Hosting (staging)"
	@echo "  make deploy-all              - Deploy both backend and frontend (staging)"
	@echo "  make test-staging            - Run E2E tests against staging"
	@echo "  make smoke-test-staging      - Run smoke tests against staging"
	@echo "  make full-deploy             - Deploy all and run E2E tests (staging)"
	@echo ""
	@echo "=== Production Deployment ==="
	@echo "  make deploy-production-backend   - Deploy backend to production"
	@echo "  make deploy-production-frontend  - Deploy frontend to production"
	@echo "  make deploy-production           - Deploy all to production + smoke test"
	@echo "  make smoke-test-production       - Run smoke tests against production"
	@echo ""
	@echo "=== Other ==="
	@echo "  make clean               - Clean up build artifacts"
	@echo ""
	@echo "Environment variables:"
	@echo "  ENV_FILE             - Environment file to use (default: .env.staging)"

# 백엔드 배포
deploy-backend:
	@echo "🚀 Deploying backend to Cloud Run..."
	@./scripts/deploy-backend.sh

# 프론트엔드 배포
deploy-frontend:
	@echo "🚀 Deploying frontend to Firebase Hosting..."
	@./scripts/deploy-frontend.sh

# 전체 배포 (백엔드 → 프론트엔드)
deploy-all: deploy-backend deploy-frontend
	@echo "✅ All deployments complete!"

# 스테이징 테스트
test-staging:
	@echo "🧪 Running E2E tests..."
	@./scripts/test-staging.sh

# 전체 배포 + 테스트
full-deploy: deploy-all test-staging
	@echo "🎉 Full deployment and testing complete!"

# 스모크 테스트 (Staging)
smoke-test-staging:
	@echo "🧪 Running smoke tests on staging..."
	@./scripts/smoke-test.sh

# 스모크 테스트 (Production)
smoke-test-production:
	@echo "🧪 Running smoke tests on production..."
	@ENV_FILE=.env.production ./scripts/smoke-test.sh

# Production 백엔드 배포
deploy-production-backend:
	@echo "🚀 Deploying backend to Cloud Run (Production)..."
	@ENV_FILE=.env.production ./scripts/deploy-backend.sh

# Production 프론트엔드 배포
deploy-production-frontend:
	@echo "🚀 Deploying frontend to Firebase Hosting (Production)..."
	@ENV_FILE=.env.production ./scripts/deploy-frontend.sh

# Production 전체 배포 (백엔드 → 프론트엔드 → 스모크 테스트)
deploy-production: deploy-production-backend deploy-production-frontend smoke-test-production
	@echo "✅ Production deployment complete!"

# 정리
clean:
	@echo "🧹 Cleaning up..."
	@rm -rf backend/.pytest_cache
	@rm -rf backend/.venv
	@rm -rf backend/__pycache__
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Cleanup complete!"
