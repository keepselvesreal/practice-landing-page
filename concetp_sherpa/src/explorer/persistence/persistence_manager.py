# 생성 시간: Thu Sep 18 11:53:20 KST 2025
# 핵심 내용: JSON 기반 선택 상태 지속성 저장/복원 관리자
# 상세 내용:
#   - PersistenceManager (라인 22-85): JSON 파일 기반 상태 관리 클래스
#   - __init__ (라인 27-32): 설정 파일 경로 초기화
#   - save_state (라인 34-45): SelectionState를 JSON 파일로 저장
#   - load_state (라인 47-60): JSON 파일에서 SelectionState 복원
#   - _ensure_directory (라인 62-70): 설정 파일 디렉토리 자동 생성
#   - _create_default_config (라인 72-85): 기본 설정 파일 생성
# 상태: active

"""
Knowledge Sherpa Explorer - 지속성 관리자

SelectionState의 JSON 기반 저장/복원 기능
실제 파일 시스템 사용 - Mock 데이터 금지
"""

import json
import logging
from pathlib import Path
from typing import Optional

from ..selection.selection_state import SelectionState

logger = logging.getLogger(__name__)


class PersistenceManager:
    """
    JSON 기반 선택 상태 지속성 관리자
    
    SelectionState를 JSON 파일로 저장/복원하는 기능 제공
    """
    
    def __init__(self, config_file_path: str):
        """
        지속성 관리자 초기화
        
        Args:
            config_file_path: JSON 설정 파일 경로
        """
        self.config_path = Path(config_file_path)
        self._ensure_directory()
    
    def save_state(self, selection_state: SelectionState) -> bool:
        """
        SelectionState를 JSON 파일로 저장
        
        Args:
            selection_state: 저장할 선택 상태
            
        Returns:
            저장 성공 여부
        """
        try:
            config_data = {
                "data_path": str(self.config_path.parent.parent / "data"),  # 기본 데이터 경로
                "selection_state": selection_state.to_dict(),
                "preferences": {
                    "auto_load_last_selection": True,
                    "show_breadcrumb": True
                }
            }
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"🟢 선택 상태 저장 완료: {self.config_path}")
            return True
            
        except (OSError, json.JSONEncodeError) as e:
            logger.error(f"🔴 선택 상태 저장 실패: {e}")
            return False
    
    def load_state(self) -> Optional[SelectionState]:
        """
        JSON 파일에서 SelectionState 복원
        
        Returns:
            복원된 선택 상태 (실패시 None)
        """
        try:
            if not self.config_path.exists():
                logger.info(f"설정 파일이 없음 - 기본 상태 반환: {self.config_path}")
                return SelectionState()  # 빈 상태 반환
            
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            selection_data = config_data.get("selection_state", {})
            selection_state = SelectionState.from_dict(selection_data)
            
            logger.info(f"🟢 선택 상태 복원 완료: {len(selection_state.selected_books)}개 책")
            return selection_state
            
        except (OSError, json.JSONDecodeError, KeyError) as e:
            logger.error(f"🔴 선택 상태 복원 실패: {e}")
            return SelectionState()  # 오류시 빈 상태 반환
    
    def _ensure_directory(self) -> None:
        """
        설정 파일 디렉토리 존재 확인 및 생성
        """
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            logger.error(f"🔴 설정 디렉토리 생성 실패: {e}")
    
    def _create_default_config(self) -> bool:
        """
        기본 설정 파일 생성
        
        Returns:
            생성 성공 여부
        """
        try:
            default_config = {
                "data_path": str(self.config_path.parent.parent / "tests" / "data"),
                "selection_state": SelectionState().to_dict(),
                "preferences": {
                    "auto_load_last_selection": True,
                    "show_breadcrumb": True,
                    "enable_quick_presets": True
                }
            }
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=2, ensure_ascii=False)
            
            logger.info(f"🟢 기본 설정 파일 생성: {self.config_path}")
            return True
            
        except (OSError, json.JSONEncodeError) as e:
            logger.error(f"🔴 기본 설정 파일 생성 실패: {e}")
            return False