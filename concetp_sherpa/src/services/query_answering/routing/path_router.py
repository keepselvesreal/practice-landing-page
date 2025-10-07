# 생성 시간: Wed Sep 17 16:25:00 KST 2025
# 핵심 내용: 경로 기반 자동 라우팅 엔진
# 상세 내용:
#   - PathRouter (라인 18-78): 경로 기반 자동 라우팅 엔진 클래스
#   - route_query (라인 27-40): 입력 레벨에 따른 처리 전략 생성
#   - _route_book_level (라인 42-53): 책 레벨 라우팅 로직
#   - _route_chapter_level (라인 55-67): 장 레벨 라우팅 로직  
#   - _route_section_level (라인 69-78): 섹션 레벨 라우팅 로직 (Early Exit)
# 상태: active

"""
Query Answering Service V2 - 경로 기반 자동 라우팅 엔진

QueryInput을 분석하여 적절한 ProcessingStrategy를 생성하는 라우터.
입력 레벨과 설정에 따라 최적화된 처리 전략을 자동으로 결정.
"""

from typing import Optional
from .query_input import QueryInput, InputLevel
from .processing_strategy import ProcessingStrategy, PrimaryMode, SectionMode
from utils.query_config_manager import QueryConfigManager


class PathRouter:
    """경로 기반 자동 라우팅 엔진"""
    
    def __init__(self, config_manager: QueryConfigManager):
        self.config = config_manager
        
    async def route_query(self, query_input: QueryInput) -> ProcessingStrategy:
        """입력 레벨에 따른 처리 전략 생성"""
        
        input_level = query_input.input_level
        parsed = query_input.parsed_paths
        
        if input_level == InputLevel.BOOK_LEVEL:
            return await self._route_book_level(query_input.user_query, parsed["book_name"])
        elif input_level == InputLevel.CHAPTER_LEVEL:
            return await self._route_chapter_level(query_input.user_query, parsed)
        elif input_level == InputLevel.SECTION_LEVEL:
            return await self._route_section_level(query_input.user_query, parsed)
        else:
            raise ValueError(f"지원하지 않는 입력 레벨: {input_level}")
    
    async def _route_book_level(self, query: str, book_name: str) -> ProcessingStrategy:
        """책 레벨: 연관 장 식별 필요"""
        return ProcessingStrategy(
            needs_chapter_identification=True,
            needs_section_identification=self.config.config.primary_mode == PrimaryMode.SECTION_BASED,
            book_name=book_name,
            target_chapters=None,
            target_sections=None,
            processing_mode=self.config.config.primary_mode,
            section_mode=self.config.config.section_mode
        )
    
    async def _route_chapter_level(self, query: str, parsed: dict) -> ProcessingStrategy:
        """장 레벨: 장은 특정되었고, 모드에 따라 섹션 식별 여부 결정"""
        return ProcessingStrategy(
            needs_chapter_identification=False,
            needs_section_identification=self.config.config.primary_mode == PrimaryMode.SECTION_BASED,
            book_name=parsed["book_name"],
            target_chapters=parsed["chapters"],
            target_sections=None,
            processing_mode=self.config.config.primary_mode,
            section_mode=self.config.config.section_mode
        )
    
    async def _route_section_level(self, query: str, parsed: dict) -> ProcessingStrategy:
        """섹션 레벨: 모든 것이 특정되었음, 식별 과정 불필요 (Early Exit 최적화)"""
        return ProcessingStrategy(
            needs_chapter_identification=False,
            needs_section_identification=False,
            book_name=parsed["book_name"],
            target_chapters=parsed["chapters"],
            target_sections=parsed["sections"],
            processing_mode=PrimaryMode.SECTION_BASED,  # 섹션이 특정되면 강제로 섹션 기반
            section_mode=self.config.config.section_mode
        )