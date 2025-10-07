# 생성 시간: Wed Sep 17 15:54:04 KST 2025
# 핵심 내용: Query Answering Service V2 전용 예외 클래스들
# 상세 내용:
#   - QueryServiceError (라인 17): 기본 예외 클래스
#   - ConfigurationError (라인 21): 설정 관련 예외
#   - NoMatchFoundError (라인 25): 매칭 결과 없음 예외
#   - FileProcessingError (라인 29): 파일 처리 예외
#   - InvalidInputError (라인 33): 잘못된 입력 예외
# 상태: active

"""
Query Answering Service V2 - 전용 예외 클래스들

시스템의 다양한 에러 상황을 구체적으로 분류하여 처리할 수 있도록
세분화된 예외 클래스를 제공
"""


class QueryServiceError(Exception):
    """Query Service 기본 예외 클래스"""
    pass


class ConfigurationError(QueryServiceError):
    """설정 파일 로드 및 검증 관련 예외"""
    pass


class NoMatchFoundError(QueryServiceError):
    """질의와 매칭되는 결과를 찾을 수 없는 경우"""
    pass


class FileProcessingError(QueryServiceError):
    """파일 로드, 파싱 등 파일 처리 관련 예외"""
    pass


class InvalidInputError(QueryServiceError):
    """잘못된 입력 데이터 관련 예외"""
    pass


class ProcessingStrategyError(QueryServiceError):
    """처리 전략 생성 및 실행 관련 예외"""
    pass


class ResponseGenerationError(QueryServiceError):
    """응답 생성 관련 예외"""
    pass