# 생성 시간: Thu Sep 18 11:42:15 KST 2025
# 핵심 내용: Knowledge Sherpa Explorer 메인 관리자 클래스 (MVP 버전)
# 상세 내용:
#   - ExplorerManager (라인 22-80): 메인 탐색 시스템 관리자
#   - __init__ (라인 27-32): 데이터 경로 초기화 및 선택 상태 설정
#   - get_books (라인 34-42): 실제 폴더에서 책 목록 스캔
#   - get_chapters (라인 44-52): 특정 책의 장 목록 스캔  
#   - get_sections (라인 54-67): 특정 장의 섹션 목록 스캔
#   - select_book (라인 69-74): 책 선택 상태 저장
#   - create_processing_strategy (라인 76-80): ProcessingStrategy 객체 생성
# 상태: active

"""
Knowledge Sherpa Explorer Manager

메인 진입점: 책/장/섹션 탐색 및 선택 관리
TDD MVP 버전: 최소 기능으로 테스트 통과에 집중
"""

from pathlib import Path
from typing import List, Set

from .filesystem.scanner import FileSystemScanner
from ..services.query_answering.routing.processing_strategy import (
    ProcessingStrategy, 
    PrimaryMode, 
    SectionMode
)


class ExplorerManager:
    """
    Knowledge Sherpa 탐색 시스템 메인 관리자
    
    책 → 장 → 섹션 계층적 탐색 및 선택 관리
    """
    
    def __init__(self, data_path: str):
        """
        탐색 시스템 초기화
        
        Args:
            data_path: 데이터 폴더 경로 (/refactoring/tests/data)
        """
        self.data_path = Path(data_path)
        self.scanner = FileSystemScanner()
        self.selected_books: Set[str] = set()
        
    def get_books(self) -> List[str]:
        """
        실제 데이터 폴더에서 책 목록 스캔
        
        Returns:
            책 폴더명 리스트 (예: ['Data_Oriented_Programming'])
        """
        try:
            return self.scanner.scan_books(self.data_path)
        except Exception as e:
            # 🔴 에러 발생 - 로깅 시스템 연동 필요
            print(f"🔴 책 스캔 오류: {e}")
            return []
    
    def get_chapters(self, book_name: str) -> List[str]:
        """
        특정 책의 장 목록 스캔
        
        Args:
            book_name: 책 이름 (예: 'Data_Oriented_Programming')
            
        Returns:
            장 폴더명 리스트
        """
        try:
            book_path = self.data_path / book_name
            return self.scanner.scan_chapters(book_path)
        except Exception as e:
            print(f"🔴 장 스캔 오류: {e}")
            return []
    
    def get_sections(self, book_name: str, chapter_name: str) -> List[str]:
        """
        특정 장의 섹션 목록 스캔
        
        Args:
            book_name: 책 이름
            chapter_name: 장 이름
            
        Returns:
            섹션 파일명 리스트
        """
        try:
            chapter_path = self.data_path / book_name / chapter_name
            return self.scanner.scan_sections(chapter_path)
        except Exception as e:
            print(f"🔴 섹션 스캔 오류: {e}")
            return []
    
    def select_book(self, book_name: str) -> None:
        """
        책 선택 상태 저장
        
        Args:
            book_name: 선택할 책 이름
        """
        self.selected_books.add(book_name)
        print(f"🟢 책 선택됨: {book_name}")
    
    def create_processing_strategy(self) -> ProcessingStrategy:
        """
        선택된 정보를 ProcessingStrategy로 변환
        
        Returns:
            ProcessingStrategy 객체 (기존 인터페이스 사용)
        """
        if not self.selected_books:
            # 🔴 선택된 책이 없을 때 기본값 처리
            selected_book = "Data_Oriented_Programming"
        else:
            selected_book = list(self.selected_books)[0]
            
        return ProcessingStrategy(
            needs_chapter_identification=False,
            needs_section_identification=False,
            book_name=selected_book,
            target_chapters=None,
            target_sections=None,
            processing_mode=PrimaryMode.CHAPTER_BASED,
            section_mode=SectionMode.COMBINED
        )