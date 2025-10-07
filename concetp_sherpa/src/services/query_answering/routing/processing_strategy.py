# 생성 시간: Wed Sep 17 15:54:04 KST 2025
# 핵심 내용: 처리 전략 및 응답 모드 정의
# 상세 내용:
#   - PrimaryMode (라인 18-21): 주요 응답 모드 열거형
#   - SectionMode (라인 24-27): 섹션 처리 모드 열거형
#   - ProcessingStrategy (라인 30-40): 처리 전략 데이터 클래스
# 상태: active

"""
Query Answering Service V2 - 처리 전략 정의

입력 레벨과 설정에 따라 어떤 방식으로 데이터를 처리하고 응답을 생성할지를
결정하는 전략 객체를 정의
"""

from dataclasses import dataclass
from typing import Optional, List, Dict
from enum import Enum


class PrimaryMode(Enum):
    """주요 응답 모드"""
    CHAPTER_BASED = "chapter_based"    # 장 기반 응답
    SECTION_BASED = "section_based"    # 섹션 기반 응답


class SectionMode(Enum):
    """섹션 처리 모드 (section_based 시에만 적용)"""
    COMBINED = "combined"      # 결합 섹션 기반
    INDIVIDUAL = "individual"  # 개별 섹션 기반


@dataclass
class ProcessingStrategy:
    """처리 전략 정의"""
    needs_chapter_identification: bool  # 장 식별 필요 여부
    needs_section_identification: bool  # 섹션 식별 필요 여부
    book_name: str                     # 대상 책 이름
    target_chapters: Optional[List[str]]              # 대상 장들
    target_sections: Optional[List[Dict[str, str]]]   # 대상 섹션들 [{"chapter": "...", "section_file": "..."}]
    processing_mode: PrimaryMode        # 처리 모드
    section_mode: SectionMode          # 섹션 모드
    
    def is_early_exit_possible(self) -> bool:
        """Early Exit 최적화 가능 여부"""
        return not self.needs_chapter_identification and not self.needs_section_identification
    
    def requires_toc_matching(self) -> bool:
        """목차 매칭 필요 여부"""
        return self.needs_chapter_identification or self.needs_section_identification