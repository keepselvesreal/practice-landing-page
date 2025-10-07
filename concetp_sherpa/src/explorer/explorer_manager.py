# 생성 시간: Thu Sep 18 11:56:30 KST 2025
# 핵심 내용: Knowledge Sherpa Explorer 메인 관리자 클래스 (Level 2 - 다중 선택 + JSON 지속성)
# 상세 내용:
#   - ExplorerManager (라인 25-140): Level 2 다중 선택 및 지속성 관리자
#   - __init__ (라인 30-40): 데이터 경로, 설정 파일, 선택 상태 초기화
#   - get_selection_state (라인 42-47): 현재 선택 상태 반환
#   - select_book (라인 49-55): 책 선택 (다중 지원)
#   - select_chapter (라인 57-65): 장 선택 (책별 다중 지원)
#   - reset_selection (라인 67-72): 모든 선택 상태 초기화
#   - save_state (라인 74-80): JSON 파일로 상태 저장
#   - load_state (라인 82-90): JSON 파일에서 상태 복원
#   - create_processing_strategy (라인 92-140): Level 1 호환 ProcessingStrategy 생성
# 상태: active
# 참조: explorer_manager.py (Level 1 원본)

"""
Knowledge Sherpa Explorer Manager V2

Level 2 기능: 다중 선택 + JSON 지속성 저장 + 자동 복원
Level 1 기능과 호환성 유지
"""

from pathlib import Path
from typing import List, Set, Optional

from .filesystem.scanner import FileSystemScanner
from .selection.selection_state import SelectionState
from .persistence.persistence_manager import PersistenceManager
from ..services.query_answering.routing.processing_strategy import (
    ProcessingStrategy, 
    PrimaryMode, 
    SectionMode
)


class ExplorerManager:
    """
    Knowledge Sherpa 탐색 시스템 메인 관리자 (Level 2)
    
    Level 2 기능:
    - 다중 선택 (책/장/섹션)
    - JSON 기반 지속성 저장
    - 자동 상태 복원
    """
    
    def __init__(self, data_path: str, config_file: Optional[str] = None):
        """
        탐색 시스템 초기화 (Level 2)
        
        Args:
            data_path: 데이터 폴더 경로
            config_file: JSON 설정 파일 경로 (선택적)
        """
        self.data_path = Path(data_path)
        self.scanner = FileSystemScanner()
        
        # Level 2: 다중 선택 상태 관리
        self.selection_state = SelectionState()
        
        # Level 2: JSON 지속성 관리
        default_config = self.data_path.parent / "config" / "explorer_config.json"
        self.persistence_manager = PersistenceManager(config_file or str(default_config))
        
        # Level 1 호환성: 기존 selected_books 속성 유지 (Set으로 변환)
        self.selected_books: Set[str] = set(self.selection_state.selected_books)
    
    def get_selection_state(self) -> SelectionState:
        """
        현재 선택 상태 반환 (Level 2 전용)
        
        Returns:
            SelectionState 객체
        """
        return self.selection_state
    
    def select_book(self, book_name: str) -> None:
        """
        책 선택 (다중 선택 지원)
        
        Args:
            book_name: 선택할 책 이름
        """
        self.selection_state.add_book(book_name)
        # Level 1 호환성: selected_books 동기화
        self.selected_books = set(self.selection_state.selected_books)
    
    def select_chapter(self, chapter_name: str) -> None:
        """
        장 선택 (다중 선택 지원)
        
        Args:
            chapter_name: 선택할 장 이름
        """
        self.selection_state.add_chapter(chapter_name)
        # Level 1 호환성: selected_books 동기화
        self.selected_books = set(self.selection_state.selected_books)
    
    def select_section(self, section_name: str) -> None:
        """
        섹션 선택 (다중 선택 지원)
        
        Args:
            section_name: 선택할 섹션 이름
        """
        self.selection_state.add_section(section_name)
    
    def reset_selection(self) -> None:
        """
        모든 선택 상태 초기화
        """
        self.selection_state.reset()
        self.selected_books = set(self.selection_state.selected_books)
    
    def save_state(self) -> bool:
        """
        현재 선택 상태를 JSON 파일로 저장
        
        Returns:
            저장 성공 여부
        """
        return self.persistence_manager.save_state(self.selection_state)
    
    def load_state(self) -> bool:
        """
        JSON 파일에서 선택 상태 복원
        
        Returns:
            복원 성공 여부
        """
        loaded_state = self.persistence_manager.load_state()
        if loaded_state:
            self.selection_state = loaded_state
            self.selected_books = set(self.selection_state.selected_books)
            return True
        return False
    
    # Level 1 호환성: 기존 메서드들 유지
    def get_books(self) -> List[str]:
        """실제 데이터 폴더에서 책 목록 스캔"""
        try:
            return self.scanner.scan_books(self.data_path)
        except Exception as e:
            print(f"🔴 책 스캔 오류: {e}")
            return []
    
    def get_chapters(self, book_name: str) -> List[str]:
        """특정 책의 장 목록 스캔"""
        try:
            book_path = self.data_path / book_name
            return self.scanner.scan_chapters(book_path)
        except Exception as e:
            print(f"🔴 장 스캔 오류: {e}")
            return []
    
    def get_sections(self, book_name: str, chapter_name: str) -> List[str]:
        """특정 장의 섹션 목록 스캔"""
        try:
            chapter_path = self.data_path / book_name / chapter_name
            return self.scanner.scan_sections(chapter_path)
        except Exception as e:
            print(f"🔴 섹션 스캔 오류: {e}")
            return []
    
    def create_processing_strategy(self) -> ProcessingStrategy:
        """
        선택된 정보를 ProcessingStrategy로 변환 (Level 1 호환)
        
        Returns:
            ProcessingStrategy 객체
        """
        if not self.selection_state.selected_books:
            # 🔴 선택된 책이 없을 때 기본값 처리
            selected_book = "Data_Oriented_Programming"
        else:
            selected_book = self.selection_state.selected_books[0]
            
        # Level 2: 장/섹션 선택이 있으면 더 구체적인 전략 생성
        target_chapters = None
        target_sections = None
        
        if self.selection_state.selected_chapters:
            target_chapters = self.selection_state.selected_chapters.copy()
        
        if self.selection_state.selected_sections:
            # 섹션 선택이 있으면 section-based 모드
            sections_list = []
            for section in self.selection_state.selected_sections:
                sections_list.append({"chapter": "unknown", "section_file": section})
            target_sections = sections_list
            
        return ProcessingStrategy(
            needs_chapter_identification=target_chapters is None,
            needs_section_identification=target_sections is None,
            book_name=selected_book,
            target_chapters=target_chapters,
            target_sections=target_sections,
            processing_mode=PrimaryMode.SECTION_BASED if target_sections else PrimaryMode.CHAPTER_BASED,
            section_mode=SectionMode.COMBINED
        )