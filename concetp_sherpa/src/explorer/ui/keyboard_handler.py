# 생성 시간: Thu Sep 18 12:02:30 KST 2025
# 핵심 내용: 키보드 입력 처리 및 액션 매핑 시스템
# 상세 내용:
#   - KeyboardAction (라인 25-35): 키보드 액션 데이터 클래스
#   - KeyboardHandler (라인 38-95): 키보드 입력 처리 클래스
#   - handle_key (라인 45-70): 키 입력을 액션으로 변환
#   - get_key (라인 72-85): 실제 키보드 입력 받기 (Mock 가능)
#   - _create_action (라인 87-95): 액션 객체 생성 헬퍼
# 상태: active

"""
Knowledge Sherpa Explorer - 키보드 이벤트 핸들러

키보드 입력을 받아서 액션 객체로 변환
Enter/Space 이중 액션 시스템 구현
"""

import sys
import tty
import termios
from dataclasses import dataclass
from typing import Optional, Dict, Callable
import logging

logger = logging.getLogger(__name__)


@dataclass
class KeyboardAction:
    """
    키보드 액션 데이터 클래스
    
    키 입력을 구조화된 액션으로 변환
    """
    action_type: str  # "move", "select", "navigate", "quit", "back"
    direction: Optional[str] = None  # "up", "down" (move 액션시)
    value: Optional[str] = None  # 추가 값


class KeyboardHandler:
    """
    키보드 입력 처리 및 액션 매핑 클래스
    
    Enter/Space 이중 액션 시스템과 키보드 네비게이션 지원
    """
    
    def __init__(self):
        """키보드 핸들러 초기화"""
        self.key_mappings: Dict[str, Callable[[], KeyboardAction]] = {
            # 네비게이션 키 (위아래만)
            'up': lambda: self._create_action("move", direction="up"),
            'down': lambda: self._create_action("move", direction="down"),
            
            # 이중 액션 시스템
            'enter': lambda: self._create_action("navigate"),  # 진입/탐색
            'space': lambda: self._create_action("select"),    # 선택/해제
            
            # 제어 키
            'q': lambda: self._create_action("quit"),
            'escape': lambda: self._create_action("back"),
            's': lambda: self._create_action("save"),
            'r': lambda: self._create_action("reset"),
            
            # 프리셋 키 (F1-F4 시뮬레이션)
            'f1': lambda: self._create_action("preset", value="1"),
            'f2': lambda: self._create_action("preset", value="2"),
            'f3': lambda: self._create_action("preset", value="3"),
            'f4': lambda: self._create_action("preset", value="4"),
        }
    
    def handle_key(self, key_input: str) -> KeyboardAction:
        """
        키 입력을 액션으로 변환
        
        Args:
            key_input: 키 입력 문자열
            
        Returns:
            KeyboardAction 객체
        """
        key_lower = key_input.lower().strip()
        
        if key_lower in self.key_mappings:
            action = self.key_mappings[key_lower]()
            logger.debug(f"키 '{key_input}' → 액션 '{action.action_type}'")
            return action
        else:
            # 알 수 없는 키는 무시 (아무 작업도 하지 않음)
            return self._create_action("ignore", value=key_input)
    
    def get_key(self) -> str:
        """
        실제 키보드 입력 받기
        
        Mock 테스트에서 패치 가능한 메서드
        
        Returns:
            입력된 키 문자열
        """
        # Claude Code 환경 감지 (간단한 fallback)
        if not sys.stdin.isatty():
            return 'q'  # 비대화형 환경에서는 종료
        
        try:
            # Unix/Linux 터미널에서 단일 키 입력 받기
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            tty.setraw(sys.stdin.fileno())
            
            key = sys.stdin.read(1)
            
            # 특수 키 처리 (화살표 키 등)
            if ord(key) == 27:  # ESC 시퀀스 시작
                try:
                    # 0.1초 대기하여 추가 문자가 있는지 확인
                    import select
                    if select.select([sys.stdin], [], [], 0.1)[0]:
                        # 화살표 키 등의 시퀀스
                        key += sys.stdin.read(2)
                        if key == '\x1b[A':
                            return 'up'
                        elif key == '\x1b[B':
                            return 'down'
                        elif key == '\x1b[C':
                            return 'ignore'  # right 키는 무시
                        elif key == '\x1b[D':
                            return 'ignore'  # left 키는 무시
                        else:
                            return 'escape'
                    else:
                        # 순수한 ESC 키
                        return 'escape'
                except Exception:
                    # 화살표 키 처리 중 오류 발생시 ESC로 처리
                    return 'escape'
            
            # 일반 키 매핑
            key_map = {
                '\r': 'enter',    # Enter
                '\n': 'enter',    # Enter (alternative)
                ' ': 'space',     # Space
                '\x7f': 'backspace',  # Backspace
                '\t': 'tab',      # Tab
            }
            
            return key_map.get(key, key)
            
        except Exception as e:
            # Claude Code 환경에서는 터미널 입력이 제한적이므로 조용히 처리
            logger.debug(f"키 입력 제한: {type(e).__name__}: {e}")
            # 연속된 오류를 방지하기 위해 짧은 대기
            import time
            time.sleep(0.1)
            return 'ignore'  # 오류시 무시 (종료하지 않음)
        finally:
            if 'old_settings' in locals():
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    
    def _create_action(
        self, 
        action_type: str, 
        direction: Optional[str] = None, 
        value: Optional[str] = None
    ) -> KeyboardAction:
        """
        액션 객체 생성 헬퍼 메서드
        
        Args:
            action_type: 액션 타입
            direction: 방향 (선택적)
            value: 값 (선택적)
            
        Returns:
            KeyboardAction 객체
        """
        return KeyboardAction(
            action_type=action_type,
            direction=direction,
            value=value
        )