# 생성 시간: Thu Sep 18 16:15:00 KST 2025
# 핵심 내용: Knowledge Sherpa Explorer 대화형 UI 통합 컴포넌트
# 상세 내용:
#   - InteractiveExplorer (라인 25-180): 기존 시스템과 새 UI 연결
#   - run (라인 30-120): 메인 탐색 루프 (새 키보드 핸들러 사용)
#   - _handle_navigation (라인 125-150): 폴더/파일 탐색 처리
#   - _handle_selection (라인 155-170): 선택 상태 관리
#   - _save_configuration (라인 175-180): 설정 저장 처리
# 상태: active
# 참조: knowledge_sherpa_explorer.py (스탠드얼론 버전)

"""
Knowledge Sherpa Explorer - 대화형 UI 통합 컴포넌트

기존 ExplorerManager + 새로운 키보드 핸들러 통합
완전히 작동하는 터미널 UI 제공
"""

import os
import sys
from typing import List, Optional, Dict, Any
from pathlib import Path

from .enhanced_keyboard_handler import EnhancedKeyboardHandler, KeyAction
from .ui_renderer import UIRenderer
from ..explorer_manager import ExplorerManager
from ..filesystem.scanner import FileSystemScanner


class InteractiveExplorer:
    """
    대화형 Knowledge Sherpa 탐색기
    
    기존 ExplorerManager와 새로운 UI/키보드 시스템 통합
    """
    
    def __init__(self, data_path: str, config_file: Optional[str] = None):
        """
        대화형 탐색기 초기화
        
        Args:
            data_path: 데이터 폴더 경로
            config_file: 설정 파일 경로
        """
        self.manager = ExplorerManager(data_path, config_file)
        self.keyboard_handler = EnhancedKeyboardHandler()
        self.ui_renderer = UIRenderer()
        self.scanner = FileSystemScanner()
        
        # 현재 상태
        self.current_path = Path(data_path)
        self.current_index = 0
        self.selected_items_order = []  # 선택 순서 유지
        self.item_types = {}  # 각 항목의 타입 저장
        self.item_paths = {}  # 각 항목이 선택된 경로 저장
        self.path_history = ["data"]
        self.save_info_shown = False
        
        # 이전 선택 상태 초기화 (매번 새로 시작)
        self.manager.reset_selection()
    
    def run(self) -> None:
        """메인 탐색 루프 실행"""
        # 바로 시작 (Enter키 입력 없이)
        
        while True:
            # 현재 경로의 항목들 스캔
            items = self._scan_current_path()
            
            # UI 렌더링
            self._render_interface(items)
            
            # 키 입력 처리
            key_input = self.keyboard_handler.get_key()
            action = self.keyboard_handler.handle_key(key_input)
            
            # 액션 처리
            if action.action_type == "quit":
                self._handle_quit()
                break
            elif action.action_type == "move":
                self._handle_movement(action, items)
            elif action.action_type == "select":
                self._handle_selection(items)
            elif action.action_type == "navigate":
                self._handle_navigation(items)
            elif action.action_type == "back":
                self._handle_back()
            elif action.action_type == "save":
                self._handle_save()
            elif action.action_type == "ignore":
                self.save_info_shown = False
                continue
    
    def _scan_current_path(self) -> List[tuple]:
        """현재 경로의 폴더와 파일 스캔"""
        items = []
        try:
            for item in os.listdir(self.current_path):
                item_path = self.current_path / item
                if item_path.is_dir():
                    items.append(('folder', item))
                else:
                    items.append(('file', item))
        except PermissionError:
            self.ui_renderer.console.print("❌ 접근 권한이 없습니다.")
            return []
        
        # 폴더 먼저, 파일 나중에 정렬
        items.sort(key=lambda x: (x[0] == 'file', x[1]))
        return items
    
    def _render_interface(self, items: List[tuple]) -> None:
        """인터페이스 렌더링"""
        # 화면 클리어
        os.system('clear')
        
        self.ui_renderer.console.print("🔍 Knowledge Sherpa Explorer")
        self.ui_renderer.console.print(f"📍 위치: {self.current_path}")
        self.ui_renderer.console.print("⌨️  조작: ↑↓(이동) Space(선택) Enter(진입/미리보기) ESC(뒤로) S(저장) Q(종료)")
        
        if len(self.path_history) > 1:
            self.ui_renderer.console.print(f"🗂️  경로: {' > '.join(self.path_history)}")
        
        self.ui_renderer.console.print("=" * 85)
        
        if not items:
            self.ui_renderer.console.print("❌ 항목이 없습니다.")
            return
        
        # 선택된 항목들 집합
        selected_set = set(self.selected_items_order)
        
        # 항목들 표시
        for i, (item_type, item_name) in enumerate(items):
            selected = "✓" if item_name in selected_set else " "
            icon = "📁" if item_type == 'folder' else "📄"
            
            if i == self.current_index:
                self.ui_renderer.console.print(f"→ [{selected}] {i+1:2d}. {icon} {item_name} ←")
            else:
                self.ui_renderer.console.print(f"  [{selected}] {i+1:2d}. {icon} {item_name}")
        
        # 하단 정보
        self.ui_renderer.console.print("-" * 85)
        self.ui_renderer.console.print(f"📊 현재: {self.current_index + 1}/{len(items)} | 선택됨: {len(self.selected_items_order)}개")
        
        if self.selected_items_order:
            # 선택 순서를 아이콘과 함께 표시
            selection_display = []
            for item_name in self.selected_items_order:
                if item_name in self.item_types:
                    icon = "📁" if self.item_types[item_name] == 'folder' else "📄"
                    selection_display.append(f"{icon}{item_name}")
                else:
                    selection_display.append(item_name)
            
            self.ui_renderer.console.print(f"🎯 선택 순서: {' → '.join(selection_display)}")
    
    def _handle_movement(self, action: KeyAction, items: List[tuple]) -> None:
        """위아래 이동 처리"""
        if not items:
            return
            
        if action.direction == "up":
            self.current_index = (self.current_index - 1) % len(items)
        elif action.direction == "down":
            self.current_index = (self.current_index + 1) % len(items)
        
        self.save_info_shown = False
    
    def _handle_selection(self, items: List[tuple]) -> None:
        """선택/해제 토글 처리"""
        if not items:
            return
            
        item_type, item_name = items[self.current_index]
        
        if item_name in self.selected_items_order:
            # 선택 해제
            self.selected_items_order.remove(item_name)
            if item_name in self.item_types:
                del self.item_types[item_name]
            if item_name in self.item_paths:
                del self.item_paths[item_name]
        else:
            # 선택 추가 (순서 유지)
            self.selected_items_order.append(item_name)
            self.item_types[item_name] = item_type
            # 선택된 시점의 경로 저장
            self.item_paths[item_name] = str(self.current_path)
        
        self.save_info_shown = False
    
    def _handle_navigation(self, items: List[tuple]) -> None:
        """Enter: 폴더 진입 또는 파일 미리보기"""
        if not items:
            return
            
        item_type, item_name = items[self.current_index]
        item_path = self.current_path / item_name
        
        if item_type == 'folder':
            # 폴더 진입
            self.current_path = item_path
            self.current_index = 0
            self.path_history.append(item_name)
        else:
            # 파일 미리보기
            self._preview_file(item_path)
        
        self.save_info_shown = False
    
    def _handle_back(self) -> None:
        """ESC: 뒤로 가기"""
        if len(self.path_history) > 1:
            self.path_history.pop()
            self.current_path = self.current_path.parent
            self.current_index = 0
            self.save_info_shown = False
    
    def _handle_save(self) -> None:
        """S키: 선택 정보 표시 후 저장 확인"""
        if not self.selected_items_order:
            self.ui_renderer.console.print("\n📭 선택된 항목이 없어서 저장할 내용이 없습니다.")
            try:
                if sys.stdin.isatty():
                    input("\n👆 Enter키를 눌러 계속...")
            except:
                pass
            return
        
        # 선택 정보 표시
        self._show_selection_info()
        self.ui_renderer.console.print("\n💾 정말 저장하시겠습니까?")
        self.ui_renderer.console.print("   [S] 저장    [다른키] 취소")
        
        # 다음 키 입력 대기
        next_key = self.keyboard_handler.get_key()
        next_action = self.keyboard_handler.handle_key(next_key)
        
        if next_action.action_type == "save":
            # S키를 다시 눌렀으면 저장
            if self._save_configuration():
                self.ui_renderer.console.print("\n🎉 저장이 완료되었습니다!")
                self.ui_renderer.console.print("📄 config/explorer_config.json 파일을 확인하세요.")
                try:
                    if sys.stdin.isatty():
                        input("\n👆 Enter키를 눌러 계속...")
                except:
                    pass
            else:
                self.ui_renderer.console.print("\n❌ 저장에 실패했습니다.")
                try:
                    if sys.stdin.isatty():
                        input("\n👆 Enter키를 눌러 계속...")
                except:
                    pass
        else:
            # 다른 키를 눌렀으면 취소 (Enter 없이 바로 돌아감)
            self.ui_renderer.console.print("\n❌ 저장이 취소되었습니다.")
            # 취소 시에는 Enter키 없이 바로 메인 화면으로
    
    def _handle_quit(self) -> None:
        """종료 처리"""
        self.ui_renderer.console.print("\n👋 Knowledge Sherpa Explorer를 종료합니다.")
        if self.selected_items_order:
            self.ui_renderer.console.print("\n📋 최종 선택된 항목들:")
            for i, item in enumerate(self.selected_items_order, 1):
                icon = "📁" if self.item_types.get(item) == 'folder' else "📄"
                self.ui_renderer.console.print(f"  {i}. {icon} {item}")
    
    def _preview_file(self, file_path: Path) -> None:
        """파일 미리보기"""
        self.ui_renderer.console.print("\n" + "="*70)
        self.ui_renderer.console.print(f"📄 파일 미리보기: {file_path.name}")
        self.ui_renderer.console.print("="*70)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # 처음 25줄 표시
            for i, line in enumerate(lines[:25], 1):
                self.ui_renderer.console.print(f"{i:3d}: {line.rstrip()}")
            
            if len(lines) > 25:
                self.ui_renderer.console.print(f"\n... 그 외 {len(lines) - 25}줄 더 있음")
            
            self.ui_renderer.console.print(f"\n📊 파일 정보: {len(lines)}줄, {file_path.stat().st_size:,}바이트")
                
        except Exception as e:
            self.ui_renderer.console.print(f"❌ 파일을 읽을 수 없습니다: {e}")
        
        try:
            if sys.stdin.isatty():
                input("\n👆 Enter키를 눌러 계속...")
        except:
            pass
    
    def _show_selection_info(self) -> bool:
        """선택 정보 표시"""
        if not self.selected_items_order:
            return False
        
        self.ui_renderer.console.print("\n" + "="*70)
        self.ui_renderer.console.print("📋 선택된 항목들 (선택 순서)")
        self.ui_renderer.console.print("="*70)
        
        for i, item_name in enumerate(self.selected_items_order, 1):
            if item_name in self.item_types:
                icon = "📁" if self.item_types[item_name] == 'folder' else "📄"
                self.ui_renderer.console.print(f"{i:2d}. {icon} {item_name}")
            else:
                self.ui_renderer.console.print(f"{i:2d}. ❓ {item_name}")
        
        self.ui_renderer.console.print(f"\n📊 총 {len(self.selected_items_order)}개 항목 선택됨")
        return True
    
    def _save_configuration(self) -> bool:
        """설정 저장 - 각 항목이 선택된 경로 기준으로 분류"""
        try:
            # ExplorerManager의 선택 상태 초기화 후 업데이트
            self.manager.reset_selection()
            
            data_path = Path("/home/nadle/projects/Knowledge_Sherpa/v2/refactoring/tests/data")
            
            # 선택된 항목들을 각각의 선택 경로에 따라 처리
            for item_name in self.selected_items_order:
                item_type = self.item_types.get(item_name, 'file')
                item_selected_path = Path(self.item_paths.get(item_name, str(self.current_path)))
                
                # 선택된 경로의 깊이로 계층 판단
                try:
                    relative_path = item_selected_path.relative_to(data_path)
                    path_parts = relative_path.parts if relative_path != Path('.') else []
                    depth = len(path_parts)
                except ValueError:
                    # data 경로 밖에 있는 경우 기본값
                    depth = 0
                
                if depth == 0:
                    # data 폴더 (1단계) - 모든 것이 책
                    if item_type == 'folder':
                        self.manager.select_book(item_name)
                    else:
                        # 파일도 책으로 처리 (확장자 제거)
                        book_name = item_name.rsplit('.', 1)[0] if '.' in item_name else item_name
                        self.manager.select_book(book_name)
                        
                elif depth == 1:
                    # 책 폴더 내부 (2단계) - 모든 것이 장
                    if item_type == 'folder':
                        self.manager.select_chapter(item_name)
                    else:
                        # 파일도 장으로 처리 (확장자 제거)
                        chapter_name = item_name.rsplit('.', 1)[0] if '.' in item_name else item_name
                        self.manager.select_chapter(chapter_name)
                        
                elif depth >= 2:
                    # 장 폴더 내부 또는 더 깊은 곳 (3단계+) - 모든 것이 섹션
                    if item_type == 'folder':
                        self.manager.select_section(item_name)
                    else:
                        # 파일을 섹션으로 처리 (확장자 제거)
                        section_name = item_name.rsplit('.', 1)[0] if '.' in item_name else item_name
                        self.manager.select_section(section_name)
            
            # 실제 설정 저장
            success = self.manager.save_state()
            
            return success
            
        except Exception as e:
            self.ui_renderer.console.print(f"❌ 저장 실패: {e}")
            return False