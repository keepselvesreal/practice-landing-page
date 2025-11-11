"""개발 DB 초기 데이터 생성"""
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.models.db import ProductDB

# .env 파일 로드
env_path = Path(__file__).parent.parent.parent / ".env"
if env_path.exists():
    load_dotenv(env_path)

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# Engine 생성
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def seed_products():
    """상품 초기 데이터 생성"""
    db = SessionLocal()
    try:
        # 기존 상품이 있는지 확인
        existing_product = db.query(ProductDB).filter(ProductDB.id == 1).first()
        if existing_product:
            print("✅ 상품 데이터가 이미 존재합니다.")
            print(f"   - {existing_product.name}: {existing_product.price/100:.2f} PHP (재고: {existing_product.stock})")
            return

        # 초기 상품 생성
        product = ProductDB(
            name="조선미녀 맑은쌀 선크림 50ml",
            price=57500,  # 575 페소 (센타보)
            stock=100,  # 초기 재고 100개
        )
        db.add(product)
        db.commit()

        print("✅ 초기 상품 데이터가 생성되었습니다.")
        print(f"   - ID: {product.id}")
        print(f"   - 상품명: {product.name}")
        print(f"   - 가격: {product.price/100:.2f} PHP")
        print(f"   - 재고: {product.stock}개")
    except Exception as e:
        db.rollback()
        print(f"❌ 오류 발생: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("🌱 Seed 데이터 생성 시작...")
    seed_products()
    print("🎉 완료!")
