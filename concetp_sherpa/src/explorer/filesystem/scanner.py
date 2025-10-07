# 생성 시간: Thu Sep 18 11:44:20 KST 2025  
# 핵심 내용: 실제 파일시스템 폴더/파일 스캔 기능 (Mock 사용 금지)
# 상세 내용:
#   - FileSystemScanner (라인 20-75): 실제 폴더 구조 스캔 클래스
#   - scan_books (라인 25-35): 데이터 폴더에서 책 폴더들 스캔
#   - scan_chapters (라인 37-47): 특정 책의 장 폴더들 스캔
#   - scan_sections (라인 49-65): 특정 장의 섹션 파일들 스캔 
#   - _is_valid_directory (라인 67-75): 유효한 폴더인지 검증
# 상태: active

"""
Knowledge Sherpa FileSystem Scanner

실제 폴더 구조를 스캔하여 책/장/섹션 목록을 제공
Mock 데이터 사용 금지 - 실제 파일시스템만 사용
"""

from pathlib import Path
from typing import List
import logging

# 로깅 설정
logger = logging.getLogger(__name__)


class FileSystemScanner:
    """
    실제 파일시스템 스캔 클래스
    
    /refactoring/tests/data/ 구조를 스캔하여 실제 폴더/파일 목록 제공
    """
    
    def scan_books(self, data_path: Path) -> List[str]:
        """
        데이터 폴더에서 책 목록 스캔
        
        Args:
            data_path: 데이터 폴더 경로
            
        Returns:
            책 폴더명 리스트 (예: ['Data_Oriented_Programming'])
        """
        try:
            if not data_path.exists():
                logger.warning(f"데이터 경로가 존재하지 않음: {data_path}")
                return []
                
            books = [d.name for d in data_path.iterdir() 
                    if d.is_dir() and self._is_valid_directory(d)]
            logger.info(f"🟢 스캔된 책 수: {len(books)} - {books}")
            return sorted(books)
            
        except (PermissionError, OSError) as e:
            logger.error(f"🔴 책 스캔 중 오류: {e}")
            return []
    
    def scan_chapters(self, book_path: Path) -> List[str]:
        """
        특정 책의 장 목록 스캔
        
        Args:
            book_path: 책 폴더 경로
            
        Returns:
            장 폴더명 리스트
        """
        try:
            if not book_path.exists():
                logger.warning(f"책 경로가 존재하지 않음: {book_path}")
                return []
                
            chapters = [d.name for d in book_path.iterdir() 
                       if d.is_dir() and self._is_valid_directory(d)]
            logger.info(f"🟢 스캔된 장 수: {len(chapters)} - {chapters}")
            return sorted(chapters)
            
        except (PermissionError, OSError) as e:
            logger.error(f"🔴 장 스캔 중 오류: {e}")
            return []
    
    def scan_sections(self, chapter_path: Path) -> List[str]:
        """
        특정 장의 섹션 목록 스캔
        
        Args:
            chapter_path: 장 폴더 경로
            
        Returns:
            섹션 파일명 리스트 (unified_info_docs 폴더 내 .md 파일들)
        """
        try:
            # unified_info_docs 폴더 확인
            unified_docs_path = chapter_path / "unified_info_docs"
            if not unified_docs_path.exists():
                logger.warning(f"unified_info_docs 폴더가 없음: {unified_docs_path}")
                return []
                
            # .md 파일들만 필터링
            sections = [f.name for f in unified_docs_path.iterdir() 
                       if f.is_file() and f.suffix == '.md']
            logger.info(f"🟢 스캔된 섹션 수: {len(sections)} - {sections[:3]}...")
            return sorted(sections)
            
        except (PermissionError, OSError) as e:
            logger.error(f"🔴 섹션 스캔 중 오류: {e}")
            return []
    
    def _is_valid_directory(self, path: Path) -> bool:
        """
        유효한 디렉토리인지 확인
        
        Args:
            path: 확인할 경로
            
        Returns:
            유효한 디렉토리 여부
        """
        # 숨김 폴더나 시스템 폴더 제외
        return not path.name.startswith('.') and not path.name.startswith('__')