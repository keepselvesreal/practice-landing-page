.PHONY: help deploy-backend deploy-frontend deploy-all test-staging clean

# 기본 타겟
help:
	@echo "K-Beauty Landing Page - Deployment Makefile"
	@echo ""
	@echo "Available targets:"
	@echo "  make deploy-backend   - Deploy backend to Cloud Run"
	@echo "  make deploy-frontend  - Deploy frontend to Firebase Hosting"
	@echo "  make deploy-all       - Deploy both backend and frontend"
	@echo "  make test-staging     - Run E2E tests against staging"
	@echo "  make full-deploy      - Deploy all and run tests"
	@echo "  make clean            - Clean up build artifacts"
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

# 정리
clean:
	@echo "🧹 Cleaning up..."
	@rm -rf backend/.pytest_cache
	@rm -rf backend/.venv
	@rm -rf backend/__pycache__
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Cleanup complete!"
