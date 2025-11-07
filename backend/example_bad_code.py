"""ruff와 mypy 테스트용 나쁜 코드"""

import os
import sys
import json  # 사용 안 함


def calculate_total(price, quantity):  # 타입 힌트 없음
    # 너무 긴 줄 -------------------------------------------------------------------------
    result = price * quantity  # 띄어쓰기 없음
    return result


def get_user_name(user_id):
    """타입 체킹 테스트"""
    if user_id > 0:
        return "Juan"
    return None  # 때로는 str, 때로는 None


def unused_function():
    x = 1
    y = 2
    return x  # y는 사용 안 함


# 실행 시
if __name__ == "__main__":
    total = calculate_total(100, 5)
    print(total)
