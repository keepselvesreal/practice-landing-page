---
version: 1
created_date: 25-11-07 15:38
note:
---

## 메모

### 입력 검증 (필수)

**customer_name:**
- 2자 이상, 50자 이하

**customer_email:**
- email-validator 라이브러리 사용
- RFC 5322 표준 검증

```python
from email_validator import validate_email, EmailNotValidError

try:
    validate_email(customer_email)
except EmailNotValidError:
    raise ValidationError("이메일 형식이 올바르지 않습니다")
```

**customer_phone:**
- 필리핀 형식: 09XX-XXX-XXXX (11자리) 또는 +63 9XX XXX XXXX
- 정규식: `^(09\d{9}|\+639\d{9})$`
- 09로 시작: 총 11자리, +639로 시작: 총 12자리

**quantity:**
- 1 이상
- 재고 이하

**shipping_address:**
- 10자 이상

---

### 검증 실패 시
```json
{
  "error": "입력값이 유효하지 않습니다",
  "code": "VALIDATION_ERROR",
  "details": {
    "customer_email": "이메일 형식이 올바르지 않습니다",
    "quantity": "수량은 1 이상이어야 합니다"
  }
}
```
