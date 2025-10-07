# 생성 시간: Tue Sep 17 16:50:00 KST 2025
# 핵심 내용: Query Answering Service V2 응답 생성기
# 상세 내용:
#   - ResponseGenerator (라인 20-108): 응답 생성 핵심 클래스
#   - generate_response (라인 30-58): 통합 응답 생성 (장/섹션 결합 모드)
#   - generate_individual_responses (라인 60-82): 개별 응답 생성 (섹션 개별 모드)
#   - _load_content_files (라인 84-108): 컨텐츠 파일 로드 유틸리티
# 상태: active

"""
Query Answering Service V2 - 응답 생성기

처리 전략에 따라 적절한 컨텐츠를 로드하고 AI를 활용해 응답을 생성하는 시스템
"""

from pathlib import Path
from typing import List, Dict
from ..routing.processing_strategy import ProcessingStrategy, PrimaryMode, SectionMode
from utils.query_config_manager import QueryConfigManager
from utils.logger_v2 import Logger
from services.ai_service_v4 import AIService


class ResponseGenerator:
    """응답 생성 핵심 클래스"""
    
    def __init__(self, config_manager: QueryConfigManager, logger: Logger, ai_service: AIService):
        self.config = config_manager
        self.logger = logger
        self.ai_service = ai_service
        
    async def generate_response(self, query: str, strategy: ProcessingStrategy) -> str:
        """통합 응답 생성 (장 기반 또는 섹션 결합 모드)"""
        
        # 컨텐츠 로드
        contents = await self._load_content_files(strategy)
        
        if not contents:
            self.logger.warning("응답 생성용 컨텐츠를 찾을 수 없음")
            return "죄송합니다. 해당 질의에 대한 정보를 찾을 수 없습니다."
        
        # AI 기반 응답 생성
        combined_content = "\n\n".join(contents)
        
        prompt = f"""
다음 컨텐츠를 바탕으로 사용자의 질의에 답변해주세요.

질의: {query}

컨텐츠:
{combined_content}

답변은 정확하고 구체적으로 작성해주시고, 컨텐츠에 없는 내용은 추측하지 마세요.
"""
        
        try:
            response = await self.ai_service.query_single_request(prompt)
            self.logger.info(f"응답 생성 완료: {len(response)}자")
            return response
            
        except Exception as e:
            self.logger.error(f"AI 응답 생성 실패: {e}")
            return "죄송합니다. 응답 생성 중 오류가 발생했습니다."
    
    async def generate_individual_responses(self, query: str, strategy: ProcessingStrategy) -> List[str]:
        """개별 응답 생성 (섹션 개별 모드)"""
        
        if strategy.section_mode != SectionMode.INDIVIDUAL:
            self.logger.warning("개별 응답 생성은 INDIVIDUAL 모드에서만 지원됩니다")
            return []
        
        responses = []
        book_path = Path(self.config.config.base_data_path) / strategy.book_name
        
        for section_info in strategy.target_sections:
            chapter_id = section_info["chapter"]
            section_file = section_info["section_file"]
            
            # 섹션 파일 로드
            section_path = book_path / chapter_id / self.config.get_file_path("section_info", section_file=section_file)
            
            if section_path.exists():
                try:
                    with open(section_path, 'r', encoding='utf-8') as f:
                        section_content = f.read()
                    
                    # 개별 섹션에 대한 응답 생성
                    prompt = f"""
다음 섹션 내용을 바탕으로 사용자의 질의에 답변해주세요.

질의: {query}

섹션 내용:
{section_content}

답변은 이 섹션의 내용에 한정해서 작성해주세요.
"""
                    
                    response = await self.ai_service.query_single_request(prompt)
                    responses.append(response)
                    
                except Exception as e:
                    self.logger.error(f"섹션 응답 생성 실패 {section_path}: {e}")
                    responses.append(f"섹션 {section_file} 처리 중 오류가 발생했습니다.")
            else:
                self.logger.warning(f"섹션 파일을 찾을 수 없음: {section_path}")
                responses.append(f"섹션 {section_file}을 찾을 수 없습니다.")
        
        self.logger.info(f"개별 응답 생성 완료: {len(responses)}개 응답")
        return responses
    
    async def _load_content_files(self, strategy: ProcessingStrategy) -> List[str]:
        """컨텐츠 파일 로드 유틸리티"""
        
        contents = []
        book_path = Path(self.config.config.base_data_path) / strategy.book_name
        
        if strategy.processing_mode == PrimaryMode.CHAPTER_BASED:
            # 장 기반: 장 컨텐츠 파일들 로드
            for chapter_id in strategy.target_chapters:
                chapter_content_file = book_path / chapter_id / self.config.get_file_path("chapter_content", chapter_name=chapter_id)
                
                if chapter_content_file.exists():
                    try:
                        with open(chapter_content_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                            contents.append(content)
                    except Exception as e:
                        self.logger.warning(f"장 컨텐츠 로드 실패 {chapter_content_file}: {e}")
                else:
                    self.logger.warning(f"장 컨텐츠 파일을 찾을 수 없음: {chapter_content_file}")
        
        elif strategy.processing_mode == PrimaryMode.SECTION_BASED:
            # 섹션 기반: 섹션 정보 파일들 로드
            if strategy.target_sections:
                for section_info in strategy.target_sections:
                    chapter_id = section_info["chapter"]
                    section_file = section_info["section_file"]
                    
                    section_path = book_path / chapter_id / self.config.get_file_path("section_info", section_file=section_file)
                    
                    if section_path.exists():
                        try:
                            with open(section_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                contents.append(content)
                        except Exception as e:
                            self.logger.warning(f"섹션 컨텐츠 로드 실패 {section_path}: {e}")
                    else:
                        self.logger.warning(f"섹션 파일을 찾을 수 없음: {section_path}")
        
        self.logger.info(f"컨텐츠 로드 완료: {len(contents)}개 파일")
        return contents