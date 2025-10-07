# 생성 시간: 2024-09-19 23:58:00 KST  
# 핵심 내용: 파일 기반 지속성 Chapter 컨텍스트 캐싱 매니저 (프로세스 간 캐시 지속성)
# 상세 내용:
#   - FileBasedChapterContextManager (라인 20-80): 파일 기반 캐시 지속성 매니저
#   - SessionInfoSerializer (라인 85-140): SessionInfo 직렬화/역직렬화
#   - ChapterContextManager (라인 145-220): 파일 캐시 통합 장 컨텍스트 매니저 
#   - _save_cache_to_file (라인 225-245): 캐시 파일 저장
#   - _load_cache_from_file (라인 250-280): 캐시 파일 로드
# 상태: active
# 참조: chapter_context_manager_v4.py (파일 지속성 추가)

import hashlib
import asyncio
import json
import pickle
import time
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from pathlib import Path

from services.ai_service_v4 import SessionInfo

class SessionInfoSerializer:
    """SessionInfo 직렬화/역직렬화 유틸리티"""
    
    @staticmethod
    def serialize_session_info(session_info: SessionInfo) -> Dict[str, Any]:
        """SessionInfo를 딕셔너리로 직렬화"""
        try:
            # session_data는 제공자별로 다른 형태이므로 pickle을 사용하여 바이너리 직렬화
            serialized_session_data = pickle.dumps(session_info.session_data).hex()
            
            return {
                "provider_type": session_info.provider_type,
                "session_data_hex": serialized_session_data,
                "created_at": session_info.created_at,
                "message_count": session_info.message_count,
                "serialized_at": time.time()
            }
        except Exception as e:
            raise ValueError(f"SessionInfo 직렬화 실패: {e}")
    
    @staticmethod
    def deserialize_session_info(data: Dict[str, Any]) -> SessionInfo:
        """딕셔너리에서 SessionInfo 복원"""
        try:
            # 바이너리 데이터를 복원
            session_data = pickle.loads(bytes.fromhex(data["session_data_hex"]))
            
            # SessionInfo 객체 재생성
            session_info = SessionInfo(
                provider_type=data["provider_type"],
                session_data=session_data
            )
            session_info.created_at = data["created_at"] 
            session_info.message_count = data["message_count"]
            
            return session_info
        except Exception as e:
            raise ValueError(f"SessionInfo 역직렬화 실패: {e}")

class FileBasedChapterContextManager:
    """파일 기반 캐시 지속성 매니저"""
    
    def __init__(self, cache_dir: str = None):
        if cache_dir is None:
            # 기본 캐시 디렉토리 설정
            cache_dir = Path(__file__).parent.parent.parent / "cache" / "chapter_contexts"
        
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # 메모리 캐시 (빠른 액세스용)
        self.memory_cache: Dict[str, SessionInfo] = {}
        self.metadata_cache: Dict[str, dict] = {}
        
        # 초기화 시 파일에서 캐시 로드
        self._load_all_caches()
        
        self.cache_ttl = 3600  # 1시간 TTL
    
    def _get_cache_file_path(self, chapter_hash: str) -> Path:
        """캐시 파일 경로 생성"""
        return self.cache_dir / f"cache_{chapter_hash}.json"
    
    def _save_cache_to_file(self, chapter_hash: str, session_info: SessionInfo, metadata: dict):
        """캐시를 파일에 저장"""
        try:
            cache_file = self._get_cache_file_path(chapter_hash)
            
            # SessionInfo 직렬화
            serialized_session = SessionInfoSerializer.serialize_session_info(session_info)
            
            cache_data = {
                "chapter_hash": chapter_hash,
                "session_info": serialized_session,
                "metadata": metadata,
                "saved_at": time.time()
            }
            
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"⚠️ 캐시 파일 저장 실패 (해시: {chapter_hash}): {e}")
    
    def _load_cache_from_file(self, chapter_hash: str) -> tuple[Optional[SessionInfo], Optional[dict]]:
        """파일에서 캐시 로드"""
        try:
            cache_file = self._get_cache_file_path(chapter_hash)
            
            if not cache_file.exists():
                return None, None
            
            with open(cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
            
            # TTL 확인
            saved_at = cache_data.get("saved_at", 0)
            if time.time() - saved_at > self.cache_ttl:
                # 만료된 캐시 파일 삭제
                cache_file.unlink(missing_ok=True)
                return None, None
            
            # SessionInfo 역직렬화
            session_info = SessionInfoSerializer.deserialize_session_info(cache_data["session_info"])
            metadata = cache_data["metadata"]
            
            return session_info, metadata
            
        except Exception as e:
            print(f"⚠️ 캐시 파일 로드 실패 (해시: {chapter_hash}): {e}")
            return None, None
    
    def _load_all_caches(self):
        """모든 캐시 파일을 메모리로 로드"""
        if not self.cache_dir.exists():
            return
            
        cache_files = list(self.cache_dir.glob("cache_*.json"))
        loaded_count = 0
        
        for cache_file in cache_files:
            try:
                chapter_hash = cache_file.stem.replace("cache_", "")
                session_info, metadata = self._load_cache_from_file(chapter_hash)
                
                if session_info and metadata:
                    self.memory_cache[chapter_hash] = session_info
                    self.metadata_cache[chapter_hash] = metadata
                    loaded_count += 1
                    
            except Exception as e:
                print(f"⚠️ 캐시 파일 로드 중 오류: {cache_file} - {e}")
        
        if loaded_count > 0:
            print(f"📂 파일에서 {loaded_count}개 캐시 복원 완료")
    
    def get_cache(self, chapter_hash: str) -> tuple[Optional[SessionInfo], Optional[dict]]:
        """캐시 조회 (메모리 → 파일 순)"""
        # 1. 메모리 캐시 확인
        if chapter_hash in self.memory_cache:
            return self.memory_cache[chapter_hash], self.metadata_cache.get(chapter_hash)
        
        # 2. 파일 캐시 확인
        session_info, metadata = self._load_cache_from_file(chapter_hash)
        if session_info and metadata:
            # 메모리 캐시에 저장
            self.memory_cache[chapter_hash] = session_info
            self.metadata_cache[chapter_hash] = metadata
            
        return session_info, metadata
    
    def set_cache(self, chapter_hash: str, session_info: SessionInfo, metadata: dict):
        """캐시 저장 (메모리 + 파일)"""
        # 메모리 캐시 저장
        self.memory_cache[chapter_hash] = session_info
        self.metadata_cache[chapter_hash] = metadata
        
        # 파일 캐시 저장
        self._save_cache_to_file(chapter_hash, session_info, metadata)
    
    def update_metadata(self, chapter_hash: str, metadata_updates: dict):
        """메타데이터 업데이트"""
        if chapter_hash in self.metadata_cache:
            self.metadata_cache[chapter_hash].update(metadata_updates)
            
            # 파일에도 반영
            session_info = self.memory_cache.get(chapter_hash)
            if session_info:
                self._save_cache_to_file(chapter_hash, session_info, self.metadata_cache[chapter_hash])
    
    def cleanup_expired_caches(self):
        """만료된 캐시 정리"""
        now = time.time()
        expired_hashes = []
        
        # 메모리 캐시에서 만료된 항목 찾기
        for chapter_hash, metadata in self.metadata_cache.items():
            created_at = metadata.get("created_at", datetime.now()).timestamp() if isinstance(metadata.get("created_at"), datetime) else metadata.get("created_at", now)
            if now - created_at > self.cache_ttl:
                expired_hashes.append(chapter_hash)
        
        # 만료된 캐시 제거
        for chapter_hash in expired_hashes:
            # 메모리에서 제거
            self.memory_cache.pop(chapter_hash, None)
            self.metadata_cache.pop(chapter_hash, None)
            
            # 파일에서 제거
            cache_file = self._get_cache_file_path(chapter_hash)
            cache_file.unlink(missing_ok=True)
        
        if expired_hashes:
            print(f"🧹 만료된 캐시 정리: {len(expired_hashes)}개")
    
    def get_cache_stats(self) -> dict:
        """캐시 통계 정보"""
        return {
            "memory_cache_size": len(self.memory_cache),
            "cache_usage": {hash_key: metadata.get("usage_count", 0) for hash_key, metadata in self.metadata_cache.items()},
            "cache_files": len(list(self.cache_dir.glob("cache_*.json")))
        }

class ChapterContextManager:
    """파일 기반 캐시를 활용한 장 조합별 컨텍스트 매니저"""
    
    def __init__(self, ai_service, logger, config_manager):
        self.ai_service = ai_service
        self.logger = logger
        self.config = config_manager
        
        # 파일 기반 캐시 매니저 사용
        self.file_cache = FileBasedChapterContextManager()

    def generate_chapter_hash(self, chapters: List[str]) -> str:
        """장 조합으로 고유 해시 생성"""
        chapters_sorted = sorted(chapters)
        return hashlib.md5(':'.join(chapters_sorted).encode()).hexdigest()[:12]

    async def get_or_setup_context_cache(self, chapters: List[str], strategy):
        """장 조합별 컨텍스트 캐시 확보 + 설정 (파일 캐시 활용)"""
        chapter_hash = self.generate_chapter_hash(chapters)
        
        # 캐시 조회 (메모리 → 파일)
        session_info, metadata = self.file_cache.get_cache(chapter_hash)
        
        if session_info and metadata and await self._is_context_cache_valid(session_info):
            # 캐시 재사용
            self.logger.info(f"♻️ 장 컨텍스트 캐시 재사용 (해시: {chapter_hash}) | 장: {chapters}")
            created_time = metadata['created_at']
            if isinstance(created_time, datetime):
                time_str = created_time.strftime('%H:%M:%S')
            else:
                time_str = datetime.fromtimestamp(created_time).strftime('%H:%M:%S')
            self.logger.info(f"   📊 캐시 정보: 생성시간={time_str}, 사용횟수={metadata['usage_count']}")
            
            # 사용 통계 업데이트
            metadata_updates = {
                "last_used": datetime.now(),
                "usage_count": metadata["usage_count"] + 1
            }
            self.file_cache.update_metadata(chapter_hash, metadata_updates)
            
            return session_info

        # 새 컨텍스트 캐시 생성 
        session_info = await self.ai_service.create_session()
        
        # 컨텍스트 설정
        await self._setup_chapter_context(session_info, strategy)
        
        # 캐시에 저장 (메모리 + 파일)
        metadata = {
            "created_at": datetime.now(),
            "last_used": datetime.now(), 
            "chapters": chapters,
            "usage_count": 1
        }
        self.file_cache.set_cache(chapter_hash, session_info, metadata)
        
        self.logger.info(f"🆕 새 컨텍스트 캐시 생성 (해시: {chapter_hash}) | 장: {chapters}")
        cache_stats = self.file_cache.get_cache_stats()
        self.logger.info(f"   💾 캐시 통계: 메모리 {cache_stats['memory_cache_size']}개, 파일 {cache_stats['cache_files']}개")
        return session_info

    async def _setup_chapter_context(self, session_info, strategy):
        """컨텍스트 캐시에 장 내용 설정"""
        # 장 content 로드
        contents = []
        book_path = Path(self.config.config.base_data_path) / strategy.book_name
        
        for chapter_id in strategy.target_chapters:
            chapter_content_file = book_path / chapter_id / "content.md"
            if chapter_content_file.exists():
                with open(chapter_content_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    contents.append(f"# {chapter_id}\n{content}")

        combined_content = "\n\n".join(contents)
        
        context_setup_prompt = f"""다음은 참조할 장들의 내용입니다. 이후 질의에서는 이 내용을 바탕으로 답변해주세요.

{combined_content}

**중요한 응답 규칙:**
1. 이 내용을 기억하고 있다가, 다음 질의들에 대해 위 내용을 바탕으로 답변해주세요.
2. 컨텐츠에 없는 내용은 추측하지 마세요.
3. **답변 생성 시 반드시 참조한 섹션명과 줄 번호 정보를 답변 끝에 표시해주세요.**
   형식: [참조: 섹션명 (줄 XX-XX)]"""

        await self.ai_service.query_with_persistent_session(context_setup_prompt, session_info)

    async def query_with_cached_context(self, query: str, session_info) -> str:
        """캐시된 컨텍스트로 질의"""
        simple_query = f"질의: {query}"
        
        self.logger.info(f"🤖 캐시된 컨텍스트로 AI 질의 실행 중...")
        self.logger.info(f"   📝 질의 길이: {len(simple_query)}자")
        
        response = await self.ai_service.query_with_persistent_session(simple_query, session_info)
        
        self.logger.info(f"✅ AI 응답 수신 완료 (길이: {len(response)}자)")
        return response

    async def _is_context_cache_valid(self, session_info) -> bool:
        """컨텍스트 캐시 유효성 검증"""
        try:
            return session_info is not None and hasattr(session_info, 'session_data')
        except:
            return False

    def cleanup_expired_caches(self):
        """만료된 컨텍스트 캐시 정리"""
        self.file_cache.cleanup_expired_caches()
        
    def get_cache_stats(self) -> dict:
        """캐시 통계 정보 반환"""
        return self.file_cache.get_cache_stats()