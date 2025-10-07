#!/usr/bin/env python3
# 생성 시간: Thu Sep 18 16:00:00 KST 2025
# 핵심 내용: 향상된 키보드 핸들러 - 안정적인 터미널 입력 처리
# 상세 내용:
#   - EnhancedKeyboardHandler (라인 25-110): 안정적인 키보드 입력 처리
#   - get_key (라인 30-85): 논블로킹 ESC 처리 및 화살표 키 안정성
#   - KeyAction (라인 15-20): 키 액션 데이터 클래스
# 상태: active
# 참조: knowledge_sherpa_explorer.py (안정적인 키보드 처리)

"""
Knowledge Sherpa Explorer - 향상된 키보드 핸들러

기존 터미널 호환성 문제를 해결한 안정적인 키보드 입력 처리
"""

import os
import sys
import termios
import tty
import fcntl
from dataclasses import dataclass
from typing import Optional
import logging

logger = logging.getLogger(__name__)


@dataclass
class KeyAction:
    """키보드 액션 데이터 클래스"""
    action_type: str  # "move", "select", "navigate", "quit", "back", "save", "ignore"
    direction: Optional[str] = None  # "up", "down" (move 액션시)
    value: Optional[str] = None  # 추가 값


class EnhancedKeyboardHandler:
    """
    향상된 키보드 입력 처리 클래스
    
    안정적인 터미널 호환성과 논블로킹 ESC 처리 제공
    """
    
    def __init__(self):
        """키보드 핸들러 초기화"""
        self.save_pressed_once = False
    
    def get_key(self) -> str:
        """
        안정적인 키보드 입력 받기
        
        Returns:
            입력된 키 문자열
        """
        try:
            # 비대화형 환경 확인
            if not sys.stdin.isatty():
                return 'q'
            
            # raw mode 설정
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            tty.setraw(sys.stdin.fileno())
            old_flags = fcntl.fcntl(fd, fcntl.F_GETFL)
            
            key = sys.stdin.read(1)
            
            # ESC 키 처리 (화살표 키와 순수 ESC 구분)
            if ord(key) == 27:  # ESC
                try:
                    # 논블로킹 모드로 추가 문자 확인
                    fcntl.fcntl(fd, fcntl.F_SETFL, old_flags | os.O_NONBLOCK)
                    
                    try:
                        next_char = sys.stdin.read(1)
                        if next_char == '[':
                            direction = sys.stdin.read(1)
                            if direction == 'A':
                                return 'up'
                            elif direction == 'B':
                                return 'down'
                            elif direction == 'C':
                                return 'ignore'  # 오른쪽 화살표 무시
                            elif direction == 'D':
                                return 'ignore'  # 왼쪽 화살표 무시
                            else:
                                return 'escape'
                        else:
                            return 'escape'
                    except (BlockingIOError, IOError):
                        # 추가 데이터가 없으면 순수한 ESC
                        return 'escape'
                    finally:
                        fcntl.fcntl(fd, fcntl.F_SETFL, old_flags)
                except:
                    return 'escape'
            
            # 기본 키 처리
            if key == 'q':
                return 'quit'
            elif key == ' ':
                return 'space'
            elif key == '\r' or key == '\n':
                return 'enter'
            elif key.lower() == 's':
                return 'save'
            
            return 'ignore'
            
        except Exception as e:
            logger.debug(f"키 입력 오류: {e}")
            return 'quit'
        finally:
            if 'old_settings' in locals():
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    
    def handle_key(self, key_input: str) -> KeyAction:
        """
        키 입력을 액션으로 변환
        
        Args:
            key_input: 키 입력 문자열
            
        Returns:
            KeyAction 객체
        """
        if key_input == 'up':
            return KeyAction("move", direction="up")
        elif key_input == 'down':
            return KeyAction("move", direction="down")
        elif key_input == 'space':
            return KeyAction("select")
        elif key_input == 'enter':
            return KeyAction("navigate")
        elif key_input == 'escape':
            return KeyAction("back")
        elif key_input == 'save':
            return KeyAction("save")
        elif key_input == 'quit':
            return KeyAction("quit")
        else:
            return KeyAction("ignore", value=key_input)
    
    def reset_save_state(self):
        """저장 상태 리셋"""
        self.save_pressed_once = False