# 생성 시간: Wed Sep 17 15:54:04 KST 2025
# 핵심 내용: Query Service V2 전용 설정 관리자
# 상세 내용:
#   - QueryConfig (라인 19-30): 질의 처리 설정 데이터 클래스
#   - QueryConfigManager (라인 33-87): 설정 파일 기반 시스템 관리자
#   - _load_config (라인 45-73): 설정 파일 로드 및 검증
#   - get_file_path (라인 75-78): 파일 패턴 기반 경로 생성
#   - update_mode (라인 80-84): 런타임 모드 변경
# 상태: active

"""
Query Answering Service V2 - 설정 관리

config.yaml 파일을 기반으로 시스템의 동작 방식을 제어하고,
런타임에 설정을 변경할 수 있는 기능을 제공
"""

import yaml
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Dict, Any
from services.query_answering.routing.processing_strategy import PrimaryMode, SectionMode
from exceptions.query_exceptions import ConfigurationError


@dataclass
class QueryConfig:
    """질의 처리 설정"""
    base_data_path: str
    default_book: str
    primary_mode: PrimaryMode
    section_mode: SectionMode
    max_concurrent: int
    cache_enabled: bool
    cache_ttl: int
    file_patterns: Dict[str, str]
    matching_config: Dict[str, Any]


class QueryConfigManager:
    """설정 파일 기반 시스템 관리자"""
    
    def __init__(self, config_path: str = "config/query_service_config.yaml"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
        
    def _load_config(self) -> QueryConfig:
        """설정 파일 로드 및 검증"""
        try:
            if not self.config_path.exists():
                raise ConfigurationError(f"설정 파일을 찾을 수 없습니다: {self.config_path}")
                
            with open(self.config_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                
            qs_config = data['query_service']
            
            return QueryConfig(
                base_data_path=qs_config['base_paths']['data_root'],
                default_book=qs_config['base_paths']['default_book'],
                primary_mode=PrimaryMode(qs_config['response_modes']['primary_mode']),
                section_mode=SectionMode(qs_config['response_modes']['section_mode']),
                max_concurrent=qs_config['performance']['max_concurrent_requests'],
                cache_enabled=qs_config['performance']['cache_enabled'],
                cache_ttl=qs_config['performance']['cache_ttl_seconds'],
                file_patterns=qs_config['file_patterns'],
                matching_config=qs_config['matching']
            )
            
        except Exception as e:
            raise ConfigurationError(f"설정 파일 로드 실패: {e}")
    
    def get_file_path(self, pattern_key: str, **kwargs) -> str:
        """파일 패턴 기반 경로 생성"""
        pattern = self.config.file_patterns[pattern_key]
        return pattern.format(**kwargs)
    
    def update_mode(self, primary_mode: PrimaryMode, section_mode: Optional[SectionMode] = None):
        """런타임 모드 변경"""
        self.config.primary_mode = primary_mode
        if section_mode and primary_mode == PrimaryMode.SECTION_BASED:
            self.config.section_mode = section_mode
            
    def reload_config(self):
        """설정 파일 재로드"""
        self.config = self._load_config()
    
    def get(self, key: str, default=None, config_type: str = None):
        """설정 값 조회 (AI 서비스 호환용)"""
        # AI 설정 요청인 경우 AI 설정 파일에서 읽기
        if config_type == "ai":
            return self._get_ai_config(key, default)
        
        # AI 서비스에서 사용하는 일반적인 설정 키들에 대한 기본값 제공
        default_settings = {
            "ai_provider": "gemini",
            "model": "gemini-1.5-pro",
            "temperature": 0.1,
            "max_tokens": 4000
        }
        return default_settings.get(key, default)
    
    def _get_ai_config(self, key: str, default=None):
        """AI 설정 파일에서 설정 값 조회"""
        try:
            ai_config_path = Path("config/ai_config.yaml")
            if not ai_config_path.exists():
                return default
                
            with open(ai_config_path, 'r', encoding='utf-8') as f:
                ai_config = yaml.safe_load(f)
            
            # 키 경로 탐색 (예: "stage_specific_ai.query_with_selection" 또는 "default_ai")
            keys = key.split('.')
            current = ai_config
            
            for k in keys:
                if isinstance(current, dict) and k in current:
                    current = current[k]
                else:
                    return default
                    
            return current if current is not None else default
            
        except Exception as e:
            # 로거가 없을 수 있으므로 조용히 실패
            return default