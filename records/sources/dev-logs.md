# cc-session: 98fbdd69-53d7-462a-b781-bf480e8ba241

## 커밋 ID: 71ca1e87fd3b7d802b8f5c851814d3b6942366e4

### Playwright E2E 테스트 접근 방식 변경
- **상황**: Outside-In TDD로 E2E 테스트를 먼저 작성하려고 Playwright 사용 시도
- **문제**: `page.request.get(f"{base_url}/api/orders/{order_number}")` 호출 시 `connect ECONNREFUSED 127.0.0.1:8000` 에러 발생
- **원인**: Playwright의 `page.request`는 실제 HTTP 요청을 보내므로 localhost:8000에서 실행 중인 서버가 필요한데, 테스트 환경에서는 서버가 실행되지 않음
- **해결**: FastAPI의 TestClient로 변경. TestClient는 ASGI 앱을 직접 호출하므로 실제 서버 실행 없이 테스트 가능
- **교훈**: E2E 테스트라도 API 레벨 테스트에서는 TestClient가 더 실용적. Playwright는 실제 브라우저 UI 테스트가 필요할 때 사용

### httpx 패키지 누락
- **상황**: TestClient로 변경 후 테스트 실행
- **문제**: `RuntimeError: The starlette.testclient module requires the httpx package to be installed`
- **원인**: FastAPI의 TestClient는 내부적으로 starlette.testclient를 사용하고, 이는 httpx에 의존. pyproject.toml에 httpx가 dependencies에 없었음
- **해결**: `uv pip install httpx`로 설치 (httpx + httpcore 패키지 설치됨)
- **교훈**: FastAPI TestClient 사용 시 httpx가 필수 의존성임을 인지

### Mock 데이터 KeyError 처리
- **상황**: 404 실패 케이스 테스트 작성 후 실행
- **문제**: `KeyError: 'ORD-99999999'` 발생하며 500 Internal Server Error 반환. 원하는 404 응답이 아님
- **원인**: `MOCK_ORDERS[order_number]`로 딕셔너리에서 키 존재 여부 체크 없이 바로 접근
- **해결**:
  ```python
  if order_number not in MOCK_ORDERS:
      raise HTTPException(status_code=404, detail=f"Order {order_number} not found")
  ```
- **교훈**: API에서 존재하지 않는 리소스 조회 시 명시적인 404 처리 필요. 예외를 그대로 던지면 500 에러가 됨
