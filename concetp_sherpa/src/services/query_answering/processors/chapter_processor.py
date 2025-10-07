# 생성 시간: Tue Sep 17 16:30:00 KST 2025
# 핵심 내용: 장 레벨 처리 프로세서
# 상세 내용:
#   - ChapterProcessor (라인 18-65): 장 레벨 데이터 처리 클래스
#   - process_chapter_based (라인 27-45): 장 기반 모드 처리
#   - process_section_based (라인 47-65): 섹션 기반 모드 처리 (섹션 식별)
# 상태: active

"""
Query Answering Service V2 - 장 레벨 프로세서

장 기반 모드와 섹션 기반 모드로 장 데이터를 처리하는 프로세서
"""

from pathlib import Path
from typing import List, Dict
from ..routing.processing_strategy import ProcessingStrategy
from utils.query_config_manager import QueryConfigManager
from utils.logger_v2 import Logger
from services.toc_query_matching_service import TocQueryMatcher
from services.ai_service_v4 import AIService


class ChapterProcessor:
    """장 레벨 데이터 처리 프로세서"""
    
    def __init__(self, config_manager: QueryConfigManager, logger: Logger, ai_service: AIService):
        self.config = config_manager
        self.logger = logger
        self.toc_matcher = TocQueryMatcher(ai_service)
        
    async def process_chapter_based(self, query: str, strategy: ProcessingStrategy) -> List[str]:
        """장 기반 모드 처리: 장 목차 파일들 로드"""
        
        contents = []
        book_path = Path(self.config.config.base_data_path) / strategy.book_name
        
        for chapter_id in strategy.target_chapters:
            # 설정 파일의 chapter_toc 패턴 사용
            chapter_toc_filename = self.config.get_file_path("chapter_toc", chapter_name=chapter_id)
            chapter_toc_file = book_path / chapter_id / chapter_toc_filename
            
            if chapter_toc_file.exists():
                try:
                    with open(chapter_toc_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        contents.append(content)
                        
                except Exception as e:
                    self.logger.warning(f"장 목차 로드 실패 {chapter_toc_file}: {e}")
            else:
                self.logger.warning(f"장 목차 파일을 찾을 수 없음: {chapter_toc_file}")
        
        self.logger.info(f"장 기반 처리 완료: {len(contents)}개 장 내용 로드")
        return contents
        
    async def process_section_based(self, query: str, strategy: ProcessingStrategy) -> Dict[str, List[str]]:
        """섹션 기반 모드 처리: 각 장에서 연관 섹션 식별"""
        
        chapter_sections = {}
        book_path = Path(self.config.config.base_data_path) / strategy.book_name
        
        for chapter_id in strategy.target_chapters:
            # 설정 파일의 chapter_toc 패턴 사용
            chapter_toc_filename = self.config.get_file_path("chapter_toc", chapter_name=chapter_id)
            chapter_toc_file = book_path / chapter_id / chapter_toc_filename
            
            if chapter_toc_file.exists():
                try:
                    with open(chapter_toc_file, 'r', encoding='utf-8') as f:
                        chapter_toc_content = f.read()
                    
                    # AI 기반 목차 매칭으로 연관 섹션 찾기
                    matched_sections = await self.toc_matcher.match_query_to_toc(query, chapter_toc_content)
                    
                    chapter_sections[chapter_id] = matched_sections
                    
                except Exception as e:
                    self.logger.warning(f"장 목차 분석 실패 {chapter_toc_file}: {e}")
                    
        self.logger.info(f"섹션 기반 처리 완료: {len(chapter_sections)}개 장에서 섹션 식별")
        return chapter_sections