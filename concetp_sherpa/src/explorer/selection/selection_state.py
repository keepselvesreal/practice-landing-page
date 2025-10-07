# 생성 시간: Thu Sep 18 11:51:15 KST 2025
# 핵심 내용: 다중 선택 상태 관리를 위한 데이터 모델
# 상세 내용:
#   - SelectionState (라인 20-55): 책/장/섹션 다중 선택 상태 저장 클래스
#   - selected_books (라인 25): Set으로 관리되는 선택된 책들
#   - selected_chapters (라인 26): 책별 장 선택 상태 Dict[str, Set[str]]
#   - selected_sections (라인 27): 장별 섹션 선택 상태 Dict[str, Set[str]]
#   - to_dict (라인 35-45): JSON 직렬화를 위한 딕셔너리 변환
#   - from_dict (라인 47-55): JSON 역직렬화를 위한 클래스 메서드
# 상태: active

"""
Knowledge Sherpa Explorer - 선택 상태 관리

다중 선택 상태를 추적하고 JSON 직렬화/역직렬화 지원
책 → 장 → 섹션 계층적 선택 구조
"""

from dataclasses import dataclass, field
from typing import Dict, Set, List, Any, Optional
from datetime import datetime
import pytz


def get_korea_time() -> datetime:
    """한국 시간으로 현재 시간 반환"""
    korea_tz = pytz.timezone('Asia/Seoul')
    return datetime.now(korea_tz)


@dataclass
class SelectionState:
    """
    다중 선택 상태 관리 클래스
    
    책/장/섹션의 계층적 다중 선택을 추적하고 JSON 직렬화 지원
    """
    selected_books: List[str] = field(default_factory=list)
    selected_chapters: List[str] = field(default_factory=list)
    selected_sections: List[str] = field(default_factory=list)
    last_updated: datetime = field(default_factory=get_korea_time)
    
    def add_book(self, book_name: str) -> None:
        """책 선택 추가"""
        if book_name not in self.selected_books:
            self.selected_books.append(book_name)
        self.last_updated = get_korea_time()
    
    def add_chapter(self, chapter_name: str) -> None:
        """장 선택 추가"""
        if chapter_name not in self.selected_chapters:
            self.selected_chapters.append(chapter_name)
        self.last_updated = get_korea_time()
    
    def add_section(self, section_name: str) -> None:
        """섹션 선택 추가"""
        if section_name not in self.selected_sections:
            self.selected_sections.append(section_name)
        self.last_updated = get_korea_time()
    
    def remove_book(self, book_name: str) -> None:
        """책 선택 제거"""
        if book_name in self.selected_books:
            self.selected_books.remove(book_name)
        self.last_updated = get_korea_time()
    
    def remove_chapter(self, chapter_name: str) -> None:
        """장 선택 제거"""
        if chapter_name in self.selected_chapters:
            self.selected_chapters.remove(chapter_name)
        self.last_updated = get_korea_time()
    
    def remove_section(self, section_name: str) -> None:
        """섹션 선택 제거"""
        if section_name in self.selected_sections:
            self.selected_sections.remove(section_name)
        self.last_updated = get_korea_time()
    
    def reset(self) -> None:
        """모든 선택 상태 초기화"""
        self.selected_books.clear()
        self.selected_chapters.clear()
        self.selected_sections.clear()
        self.last_updated = get_korea_time()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        JSON 직렬화를 위한 딕셔너리 변환
        
        Returns:
            직렬화 가능한 딕셔너리
        """
        return {
            "selected_books": self.selected_books,
            "selected_chapters": self.selected_chapters,
            "selected_sections": self.selected_sections,
            "last_updated": self.last_updated.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SelectionState':
        """
        JSON 역직렬화를 위한 클래스 메서드
        
        Args:
            data: 딕셔너리 데이터
            
        Returns:
            SelectionState 인스턴스
        """
        return cls(
            selected_books=data.get("selected_books", []),
            selected_chapters=data.get("selected_chapters", []),
            selected_sections=data.get("selected_sections", []),
            last_updated=cls._parse_datetime(data.get("last_updated"))
        )
    
    @classmethod
    def _parse_datetime(cls, date_str: Optional[str]) -> datetime:
        """
        날짜 문자열을 datetime으로 파싱 (null 값 처리 포함)
        
        Args:
            date_str: ISO 형식 날짜 문자열 또는 None
            
        Returns:
            datetime 객체 (없으면 현재 한국 시간)
        """
        if date_str is None:
            return get_korea_time()
        
        try:
            return datetime.fromisoformat(date_str)
        except (ValueError, TypeError):
            # 파싱 실패시 현재 한국 시간 반환
            return get_korea_time()