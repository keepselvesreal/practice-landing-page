# 생성 시간: Tue Sep 17 16:31:00 KST 2025
# 핵심 내용: 섹션 레벨 처리 프로세서
# 상세 내용:
#   - SectionProcessor (라인 18-50): 섹션 레벨 데이터 처리 클래스
#   - process_sections (라인 27-50): 개별 섹션 내용 로드
# 상태: active

"""
Query Answering Service V2 - 섹션 레벨 프로세서

개별 섹션 파일들을 처리하는 프로세서 (Early Exit 최적화 대상)
"""

from pathlib import Path
from typing import List, Dict
from ..routing.processing_strategy import ProcessingStrategy
from utils.query_config_manager import QueryConfigManager
from utils.logger_v2 import Logger


class SectionProcessor:
    """섹션 레벨 데이터 처리 프로세서"""
    
    def __init__(self, config_manager: QueryConfigManager, logger: Logger):
        self.config = config_manager
        self.logger = logger
        
    async def process_sections(self, query: str, strategy: ProcessingStrategy) -> Dict[str, List[str]]:
        """개별 섹션 내용을 장별로 그룹화하여 로드"""
        
        contents_by_chapter = {}
        book_path = Path(self.config.config.base_data_path) / strategy.book_name
        
        for section_info in strategy.target_sections:
            chapter_id = section_info["chapter"]
            section_file = section_info["section_file"]
            
            # 장별 리스트 초기화
            if chapter_id not in contents_by_chapter:
                contents_by_chapter[chapter_id] = []
            
            # 섹션 파일 경로 (.md 확장자 처리)
            if section_file.endswith('.md'):
                section_path = book_path / chapter_id / "unified_info_docs" / section_file
            else:
                section_path = book_path / chapter_id / "unified_info_docs" / f"{section_file}.md"
            
            if section_path.exists():
                try:
                    with open(section_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        contents_by_chapter[chapter_id].append(content)
                        
                except Exception as e:
                    self.logger.warning(f"섹션 내용 로드 실패 {section_path}: {e}")
            else:
                self.logger.warning(f"섹션 파일을 찾을 수 없음: {section_path}")
        
        total_sections = sum(len(sections) for sections in contents_by_chapter.values())
        self.logger.info(f"섹션 처리 완료: {total_sections}개 섹션 내용을 {len(contents_by_chapter)}개 장별로 로드")
        return contents_by_chapter