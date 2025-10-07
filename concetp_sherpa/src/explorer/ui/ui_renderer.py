# 생성 시간: Thu Sep 18 12:00:15 KST 2025
# 핵심 내용: Rich 라이브러리 기반 터미널 UI 렌더링 컴포넌트
# 상세 내용:
#   - UIRenderer (라인 25-120): Rich 기반 UI 렌더링 클래스
#   - render_book_menu (라인 30-55): 책 목록 메뉴 렌더링 (선택 표시 포함)
#   - render_chapter_menu (라인 57-75): 장 목록 메뉴 렌더링
#   - render_breadcrumb (라인 77-90): 탐색 경로 브레드크럼 렌더링
#   - render_status_bar (라인 92-105): 하단 상태바 렌더링
#   - _create_menu_item (라인 107-120): 메뉴 아이템 생성 헬퍼 메서드
# 상태: active

"""
Knowledge Sherpa Explorer - UI 렌더링 컴포넌트

Rich 라이브러리를 사용한 터미널 UI 렌더링
메뉴, 브레드크럼, 상태바 등 UI 요소 생성
"""

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.align import Align
from typing import List, Set, Optional, Union
import logging

logger = logging.getLogger(__name__)


class UIRenderer:
    """
    Rich 라이브러리 기반 터미널 UI 렌더러
    
    터미널에서 보기 좋은 메뉴, 브레드크럼, 상태바 등을 렌더링
    """
    
    def __init__(self):
        """UI 렌더러 초기화"""
        self.console = Console()
    
    def render_book_menu(
        self, 
        books: List[str], 
        selected_books: Optional[Set[str]] = None,
        selected_index: int = 0
    ) -> Panel:
        """
        책 목록 메뉴 렌더링 (선택 상태 포함)
        
        Args:
            books: 책 목록
            selected_books: 선택된 책들 (Set)
            selected_index: 현재 커서 위치
            
        Returns:
            Rich Panel 객체
        """
        if not books:
            return Panel("📚 책을 찾을 수 없습니다.", title="책 목록", border_style="red")
        
        selected_books = selected_books or set()
        table = Table(show_header=False, show_edge=False, padding=(0, 1))
        table.add_column("selection", width=3)
        table.add_column("item", style="bold")
        table.add_column("status", width=10)
        
        for i, book in enumerate(books):
            # 커서 표시
            cursor = "→" if i == selected_index else " "
            
            # 선택 상태 표시
            status = "✓ 선택됨" if book in selected_books else ""
            
            # 책 이름 스타일
            book_style = "green" if book in selected_books else "white"
            if i == selected_index:
                book_style = f"bold {book_style}"
            
            table.add_row(
                cursor,
                Text(f"📚 {book}", style=book_style),
                Text(status, style="green" if status else "dim")
            )
        
        return Panel(
            table,
            title="📚 책 목록",
            subtitle="[Enter] 진입 | [Space] 선택 | [Q] 종료",
            border_style="blue",
            height=len(books) + 5  # 고정 높이 설정
        )
    
    def render_chapter_menu(
        self,
        book_name: str,
        chapters: List[str],
        selected_chapters: Optional[Set[str]] = None,
        selected_index: int = 0
    ) -> Panel:
        """
        장 목록 메뉴 렌더링
        
        Args:
            book_name: 책 이름
            chapters: 장 목록
            selected_chapters: 선택된 장들
            selected_index: 현재 커서 위치
            
        Returns:
            Rich Panel 객체
        """
        if not chapters:
            return Panel("📁 장을 찾을 수 없습니다.", title=f"📚 {book_name}", border_style="red")
        
        selected_chapters = selected_chapters or set()
        table = Table(show_header=False, show_edge=False, padding=(0, 1))
        table.add_column("selection", width=3)
        table.add_column("item", style="bold")
        table.add_column("status", width=10)
        
        for i, chapter in enumerate(chapters):
            cursor = "→" if i == selected_index else " "
            status = "✓ 선택됨" if chapter in selected_chapters else ""
            chapter_style = "green" if chapter in selected_chapters else "white"
            if i == selected_index:
                chapter_style = f"bold {chapter_style}"
            
            table.add_row(
                cursor,
                Text(f"📁 {chapter}", style=chapter_style),
                Text(status, style="green" if status else "dim")
            )
        
        return Panel(
            table,
            title=f"📚 {book_name} > 📁 장 목록",
            subtitle="[Enter] 진입 | [Space] 선택 | [Esc] 뒤로 | [Q] 종료",
            border_style="blue"
        )
    
    def render_breadcrumb(self, path: List[str]) -> Text:
        """
        탐색 경로 브레드크럼 렌더링
        
        Args:
            path: 경로 리스트 (예: ["Data_Oriented_Programming", "chapter_1"])
            
        Returns:
            Rich Text 객체
        """
        if not path:
            return Text("🏠 홈", style="dim")
        
        breadcrumb = Text()
        for i, item in enumerate(path):
            if i == 0:
                breadcrumb.append("📚 ", style="blue")
            else:
                breadcrumb.append(" > 📁 ", style="dim")
            breadcrumb.append(item, style="bold")
        
        return breadcrumb
    
    def render_status_bar(self, selected_count: int, total_count: int) -> Panel:
        """
        하단 상태바 렌더링
        
        Args:
            selected_count: 선택된 항목 수
            total_count: 전체 항목 수
            
        Returns:
            Rich Panel 객체
        """
        status_text = f"선택됨: {selected_count}/{total_count}"
        if selected_count > 0:
            status_text += " | [S] 저장 | [R] 리셋"
        
        return Panel(
            Align.center(Text(status_text, style="bold")),
            border_style="green" if selected_count > 0 else "dim",
            height=3  # 상태바 고정 높이
        )
    
    def _create_menu_item(
        self, 
        icon: str, 
        text: str, 
        is_selected: bool = False, 
        is_highlighted: bool = False
    ) -> Text:
        """
        메뉴 아이템 생성 헬퍼 메서드
        
        Args:
            icon: 아이콘 (📚, 📁 등)
            text: 텍스트
            is_selected: 선택 여부
            is_highlighted: 하이라이트 여부
            
        Returns:
            Rich Text 객체
        """
        item = Text()
        item.append(icon + " ")
        
        style = "white"
        if is_selected:
            style = "green"
        if is_highlighted:
            style = f"bold {style}"
        
        item.append(text, style=style)
        
        if is_selected:
            item.append(" ✓", style="green")
        
        return item