# 생성 시간: Tue Sep 17 16:38:00 KST 2025
# 핵심 내용: AI 기반 목차 질의 매칭 시스템
# 상세 내용:
#   - TocQueryMatcher (라인 18-70): AI 기반 목차 매칭 서비스 클래스
#   - match_query_to_toc (라인 27-50): 질의와 목차 매칭 메인 메서드
#   - _generate_prompt (라인 52-70): AI 매칭용 프롬프트 생성
#   - _parse_ai_response (라인 72-90): AI 응답 파싱 및 헤더 추출
# 상태: active

"""
Query Answering Service V2 - AI 기반 목차 질의 매칭 시스템

사용자의 질의와 목차 내용을 AI로 분석하여, 질의와 관련성이 높은 목차 항목의 헤더 제목을 반환하는 서비스
"""

from typing import List, Optional
from services.ai_service_v4 import AIService


class TocQueryMatcher:
    """간단한 AI 기반 목차 매칭 서비스"""
    
    def __init__(self, ai_service: AIService, logger=None):
        """AI 서비스 의존성 주입"""
        self.ai_service = ai_service
        self.logger = logger
        
    async def match_query_to_toc(
        self, 
        user_query: str, 
        toc_content: str,
        max_retries: int = 3
    ) -> List[str]:
        """
        질의와 목차 매칭 메인 메서드 - 파싱 실패 시 재요청
        
        Args:
            user_query: 사용자 질의
            toc_content: 목차 내용
            max_retries: 최대 재시도 횟수 (기본: 3)
            
        Returns:
            List[str]: 매칭된 헤더 제목들 (최대 3개, 관련성 없으면 빈 리스트)
        """
        if not user_query.strip() or not toc_content.strip():
            return []
        
        for attempt in range(max_retries):
            try:
                # AI 프롬프트 생성
                prompt = self._generate_prompt(user_query, toc_content, attempt + 1)
                
                # AI 서비스 호출
                ai_response = await self.ai_service.query_single_request(prompt)
                
                # AI 응답 파싱
                matched_headers = self._parse_ai_response(ai_response)
                
                # 파싱 성공 시 결과 반환
                if matched_headers:
                    if self.logger:
                        self.logger.info(f"✅ AI 매칭 성공 (시도 {attempt + 1}/{max_retries})")
                    return matched_headers
                else:
                    # 파싱 실패 시 재시도
                    if self.logger:
                        self.logger.warning(f"🔄 파싱 실패 - 재시도 {attempt + 1}/{max_retries}")
                    if attempt == max_retries - 1:
                        if self.logger:
                            self.logger.error(f"❌ {max_retries}회 시도 후 파싱 실패")
                        return []
                
            except Exception as e:
                if self.logger:
                    self.logger.error(f"❌ AI 매칭 오류 (시도 {attempt + 1}/{max_retries}): {e}")
                if attempt == max_retries - 1:
                    return []
        
        return []
        
    def _generate_prompt(self, query: str, toc_content: str, attempt: int = 1) -> str:
        """범용 AI 매칭 프롬프트 - 장/섹션 모두 지원"""
        
        retry_instruction = ""
        if attempt > 1:
            retry_instruction = f"""
**⚠️ 재시도 {attempt}회차: 이전 응답이 올바른 형식이 아니었습니다.**
**반드시 아래 정확한 형식으로만 응답하세요:**
"""
        
        prompt = f"""사용자 질의: "{query}"

다음 목차에서 질의와 **밀접하게 관련된 제목만** 선택하세요.
{retry_instruction}
**중요한 규칙:**
1. **제목만 선택**: 추출된 하위 정보(핵심 정보, 상세 정보, 상세 핵심 정보, 주요 화제, 부차 화제) 섹션 위에 표시된 제목만 선택
2. **하위 정보 제외**: 핵심 정보, 상세 정보, 상세 핵심 정보, 주요 화제, 부차 화제 등의 하위 설명 내용은 선택하지 마세요
3. **헤더 기호 절대 제외**: #, ## 등의 마크다운 헤더 기호는 절대 포함하지 마세요
4. **최대 3개**: 관련성이 높은 순서로 최대 3개까지만 선택
5. **엄격한 관련성**: 질의와 직접적으로 관련된 제목만 선택
6. **판단 이유 필수**: 각 제목을 선택한 구체적인 이유를 명시

**선택 대상 제목 예시:**
- 1_Complexity_of_object_oriented_programming
- 15_lev1_1_Complexity_of_object_oriented_programming_info.md
- 18_lev3_1.1.2_UML_101_info.md

목차:
{toc_content}

**정확한 응답 형식 (관련된 제목이 있을 경우만):**
1. [제목1] - 이유: [이 제목을 선택한 구체적인 판단 근거]
2. [제목2] - 이유: [이 제목을 선택한 구체적인 판단 근거]
3. [제목3] - 이유: [이 제목을 선택한 구체적인 판단 근거]

관련된 제목이 없으면: "관련 항목 없음"
"""
        return prompt
        
    def _parse_ai_response(self, response: str) -> List[str]:
        """AI 응답 파싱 및 헤더 추출 - 판단 이유 로깅 포함"""
        
        if not response or "관련 항목 없음" in response:
            if self.logger:
                self.logger.info("🚫 AI가 관련된 장을 찾지 못했습니다")
            return []
        
        matched_headers = []
        lines = response.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # 번호와 제목, 이유 파싱 (예: "1. 장제목 - 이유: 판단근거")
            import re
            # 패턴: "숫자. [장제목] - 이유: [판단근거]"
            header_reason_match = re.match(r'^\d+\.\s*(.+?)\s*-\s*이유:\s*(.+)$', line)
            if header_reason_match:
                chapter_title = header_reason_match.group(1).strip()
                reasoning = header_reason_match.group(2).strip()
                
                # ## 기호 제거 (AI가 실수로 포함한 경우 대비)
                if chapter_title.startswith("## "):
                    chapter_title = chapter_title[3:].strip()
                
                # 로깅으로 판단 이유 출력
                if self.logger:
                    self.logger.info(f"🎯 AI가 식별한 연관된 장: {chapter_title}")
                    self.logger.info(f"💭 판단 이유: {reasoning}")
                
                matched_headers.append(chapter_title)
            else:
                # 이유가 없는 경우 기존 방식으로 파싱
                header_match = re.match(r'^\d+\.\s*(.+)$', line)
                if header_match:
                    chapter_title = header_match.group(1).strip()
                    # " - 이유:" 부분이 있으면 제거
                    if " - 이유:" in chapter_title:
                        chapter_title = chapter_title.split(" - 이유:")[0].strip()
                    
                    # ## 기호 제거 (AI가 실수로 포함한 경우 대비)
                    if chapter_title.startswith("## "):
                        chapter_title = chapter_title[3:].strip()
                    
                    if self.logger:
                        self.logger.info(f"🎯 AI가 식별한 연관된 장: {chapter_title}")
                        self.logger.warning(f"💭 판단 이유: 제공되지 않음")
                    
                    matched_headers.append(chapter_title)
                
            # 최대 3개 제한
            if len(matched_headers) >= 3:
                break
        
        return matched_headers