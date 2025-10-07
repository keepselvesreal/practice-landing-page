# 생성 시간: Tue Sep 17 16:29:00 KST 2025
# 핵심 내용: 책 레벨 처리 프로세서
# 상세 내용:
#   - BookProcessor (라인 18-45): 책 레벨 데이터 처리 클래스
#   - identify_relevant_chapters (라인 27-45): book_toc.md에서 연관 장 식별
# 상태: active

"""
Query Answering Service V2 - 책 레벨 프로세서

book_toc.md를 분석하여 사용자 질의와 연관된 장들을 식별하는 프로세서
"""

from pathlib import Path
from typing import List
from ..routing.processing_strategy import ProcessingStrategy
from utils.query_config_manager import QueryConfigManager
from utils.logger_v2 import Logger
from services.toc_query_matching_service import TocQueryMatcher
from services.ai_service_v4 import AIService


class BookProcessor:
    """책 레벨 데이터 처리 프로세서"""
    
    def __init__(self, config_manager: QueryConfigManager, logger: Logger, ai_service: AIService):
        self.config = config_manager
        self.logger = logger
        self.toc_matcher = TocQueryMatcher(ai_service, logger)
        
    async def identify_relevant_chapters(self, query: str, strategy: ProcessingStrategy) -> List[str]:
        """book_toc.md에서 연관 장 식별"""
        
        # 설정 파일의 file_patterns 사용
        book_path = Path(self.config.config.base_data_path) / strategy.book_name
        toc_filename = self.config.config.file_patterns["book_toc"]
        toc_file = book_path / toc_filename
        
        if not toc_file.exists():
            self.logger.warning(f"목차 파일을 찾을 수 없음: {toc_file}")
            return []
        
        try:
            with open(toc_file, 'r', encoding='utf-8') as f:
                toc_content = f.read()
            
            # AI 기반 목차 매칭으로 연관 장 찾기
            matched_chapters = await self.toc_matcher.match_query_to_toc(query, toc_content)
            
            self.logger.info(f"AI 기반 연관 장 식별 완료: {len(matched_chapters)}개")
            return matched_chapters
            
        except Exception as e:
            self.logger.error(f"목차 분석 실패: {e}")
            return []