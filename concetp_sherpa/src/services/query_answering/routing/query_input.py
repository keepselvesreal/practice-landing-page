# 생성 시간: Wed Sep 17 15:54:04 KST 2025
# 핵심 내용: 경로 기반 질의 입력 자동 감지 시스템
# 상세 내용:
#   - InputLevel (라인 19-24): 입력 레벨 열거형 (책/장/섹션)
#   - QueryInput (라인 27-92): 경로 기반 질의 입력 클래스
#   - _detect_input_level (라인 37-56): 경로 패턴으로 레벨 자동 감지
#   - _parse_paths (라인 58-92): 레벨별 경로 파싱 로직
# 상태: active

"""
Query Answering Service V2 - 경로 기반 질의 입력 처리

사용자가 제공한 경로들을 분석하여 자동으로 입력 레벨(책/장/섹션)을 감지하고,
적절한 처리 전략을 수립할 수 있도록 입력 데이터를 구조화
"""

from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Any
from exceptions.query_exceptions import InvalidInputError


class InputLevel(Enum):
    """입력 레벨 자동 감지"""
    BOOK_LEVEL = "book_level"      # 책 폴더명만 제공
    CHAPTER_LEVEL = "chapter_level" # 장 폴더명 제공
    SECTION_LEVEL = "section_level" # 섹션 파일명 제공


@dataclass
class QueryInput:
    """경로 기반 질의 입력"""
    user_query: str
    input_paths: List[str]  # 제공된 경로들 (책/장/섹션 구분 없이)
    
    def __post_init__(self):
        """입력 후 자동 레벨 감지 및 파싱"""
        self.input_level = self._detect_input_level()
        self.parsed_paths = self._parse_paths()
    
    def _detect_input_level(self) -> InputLevel:
        """경로 패턴으로 입력 레벨 자동 감지"""
        if not self.input_paths:
            raise InvalidInputError("입력 경로가 없습니다")
            
        # 첫 번째 경로로 레벨 판단
        first_path = self.input_paths[0].strip()
        path_parts = first_path.split('/')
        
        if len(path_parts) == 1:
            # "Data_Oriented_Programming" -> 책 레벨
            return InputLevel.BOOK_LEVEL
        elif len(path_parts) == 2:
            # "Data_Oriented_Programming/1_Complexity_of_..." -> 장 레벨  
            return InputLevel.CHAPTER_LEVEL
        elif len(path_parts) >= 3:
            # "Data_Oriented_Programming/1_Complexity_of_.../15_lev1_1_..." -> 섹션 레벨
            return InputLevel.SECTION_LEVEL
        else:
            raise InvalidInputError(f"알 수 없는 경로 패턴: {first_path}")
    
    def _parse_paths(self) -> Dict[str, Any]:
        """경로 파싱 결과"""
        if self.input_level == InputLevel.BOOK_LEVEL:
            return {
                "book_name": self.input_paths[0],
                "chapters": None,
                "sections": None
            }
        elif self.input_level == InputLevel.CHAPTER_LEVEL:
            book_name = self.input_paths[0].split('/')[0]
            chapters = [path.split('/')[1] for path in self.input_paths]
            return {
                "book_name": book_name,
                "chapters": chapters,
                "sections": None
            }
        elif self.input_level == InputLevel.SECTION_LEVEL:
            book_name = self.input_paths[0].split('/')[0]
            sections_info = []
            for path in self.input_paths:
                parts = path.split('/')
                sections_info.append({
                    "chapter": parts[1],
                    "section_file": parts[2] if len(parts) > 2 else parts[-1]
                })
            return {
                "book_name": book_name,
                "chapters": list(set(s["chapter"] for s in sections_info)),
                "sections": sections_info
            }
        
    def get_book_name(self) -> str:
        """책 이름 반환"""
        return self.parsed_paths["book_name"]
    
    def get_chapters(self) -> List[str]:
        """장 목록 반환"""
        chapters = self.parsed_paths.get("chapters")
        return chapters if chapters is not None else []
    
    def get_sections(self) -> List[Dict[str, str]]:
        """섹션 정보 목록 반환"""
        sections = self.parsed_paths.get("sections")
        return sections if sections is not None else []