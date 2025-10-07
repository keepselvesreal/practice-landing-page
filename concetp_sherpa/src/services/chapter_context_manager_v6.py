# 생성 시간: 2024-09-20 00:05:00 KST  
# 핵심 내용: 심플 파일 기반 Chapter 컨텍스트 캐싱 매니저 (메타데이터만 저장)
# 상세 내용:
#   - SimpleFileCache (라인 20-60): 메타데이터만 저장하는 파일 캐시
#   - ChapterContextManager (라인 65-150): 세션 재생성 기반 컨텍스트 매니저 
#   - _is_cache_valid (라인 155-170): 캐시 유효성 검증
#   - _setup_chapter_context (라인 175-195): 컨텍스트 설정
# 상태: active
# 참조: chapter_context_manager_v5.py (직렬화 문제 해결)

import hashlib
import asyncio
import json
import time
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from pathlib import Path

class SimpleFileCache:
    """메타데이터만 저장하는 간단한 파일 캐시"""
    
    def __init__(self, cache_dir: str = None):
        if cache_dir is None:
            cache_dir = Path(__file__).parent.parent.parent / "cache" / "chapter_contexts"
        
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_ttl = 3600  # 1시간 TTL
    
    def _get_metadata_file_path(self, chapter_hash: str) -> Path:
        """메타데이터 파일 경로"""
        return self.cache_dir / f"metadata_{chapter_hash}.json"
    
    def save_metadata(self, chapter_hash: str, metadata: dict):
        """메타데이터만 파일에 저장"""
        try:
            metadata_file = self._get_metadata_file_path(chapter_hash)
            
            # datetime 객체를 timestamp로 변환
            serializable_metadata = {}
            for key, value in metadata.items():
                if isinstance(value, datetime):
                    serializable_metadata[key] = value.timestamp()
                else:
                    serializable_metadata[key] = value
            
            cache_data = {
                "chapter_hash": chapter_hash,
                "metadata": serializable_metadata,
                "saved_at": time.time()
            }
            
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"⚠️ 메타데이터 저장 실패 (해시: {chapter_hash}): {e}")
    
    def load_metadata(self, chapter_hash: str) -> Optional[dict]:
        """파일에서 메타데이터 로드"""
        try:
            metadata_file = self._get_metadata_file_path(chapter_hash)
            
            if not metadata_file.exists():
                return None
            
            with open(metadata_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
            
            # TTL 확인
            saved_at = cache_data.get("saved_at", 0)
            if time.time() - saved_at > self.cache_ttl:
                # 만료된 파일 삭제
                metadata_file.unlink(missing_ok=True)
                return None
            
            # timestamp를 datetime으로 변환
            metadata = cache_data["metadata"]
            for key, value in metadata.items():
                if key in ['created_at', 'last_used'] and isinstance(value, (int, float)):
                    metadata[key] = datetime.fromtimestamp(value)
            
            return metadata
            
        except Exception as e:
            print(f"⚠️ 메타데이터 로드 실패 (해시: {chapter_hash}): {e}")
            return None
    
    def update_metadata(self, chapter_hash: str, metadata_updates: dict):
        """메타데이터 업데이트"""
        existing_metadata = self.load_metadata(chapter_hash)
        if existing_metadata:
            existing_metadata.update(metadata_updates)
            self.save_metadata(chapter_hash, existing_metadata)
    
    def cleanup_expired_metadata(self):
        """만료된 메타데이터 파일 정리"""
        if not self.cache_dir.exists():
            return
            
        metadata_files = list(self.cache_dir.glob("metadata_*.json"))
        expired_count = 0
        
        for metadata_file in metadata_files:
            try:
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    cache_data = json.load(f)
                
                saved_at = cache_data.get("saved_at", 0)
                if time.time() - saved_at > self.cache_ttl:
                    metadata_file.unlink(missing_ok=True)
                    expired_count += 1
                    
            except Exception as e:
                print(f"⚠️ 만료 파일 정리 중 오류: {metadata_file} - {e}")
        
        if expired_count > 0:
            print(f"🧹 만료된 메타데이터 파일 정리: {expired_count}개")
    
    def get_cache_stats(self) -> dict:
        """캐시 통계"""
        if not self.cache_dir.exists():
            return {"metadata_files": 0}
            
        metadata_files = len(list(self.cache_dir.glob("metadata_*.json")))
        return {"metadata_files": metadata_files}

class ChapterContextManager:
    """세션 재생성 기반 장 조합별 컨텍스트 매니저"""
    
    def __init__(self, ai_service, logger, config_manager):
        self.ai_service = ai_service
        self.logger = logger
        self.config = config_manager
        
        # 메타데이터만 저장하는 파일 캐시
        self.file_cache = SimpleFileCache()
        
        # 메모리 내 세션 캐시 (현재 프로세스에서만 유효)
        self.session_cache: Dict[str, Any] = {}  # {chapter_hash: session_info}

    def generate_chapter_hash(self, chapters: List[str]) -> str:
        """장 조합으로 고유 해시 생성"""
        chapters_sorted = sorted(chapters)
        return hashlib.md5(':'.join(chapters_sorted).encode()).hexdigest()[:12]

    async def get_or_setup_context_cache(self, chapters: List[str], strategy):
        """장 조합별 컨텍스트 캐시 확보 + 설정"""
        chapter_hash = self.generate_chapter_hash(chapters)
        
        # 1. 메모리 캐시 확인 (현재 프로세스에서 이미 생성된 세션)
        if chapter_hash in self.session_cache:
            session_info = self.session_cache[chapter_hash]
            if await self._is_context_cache_valid(session_info):
                self.logger.info(f"♻️ 메모리 캐시 재사용 (해시: {chapter_hash}) | 장: {chapters}")
                
                # 메타데이터 업데이트
                self.file_cache.update_metadata(chapter_hash, {
                    "last_used": datetime.now(),
                    "usage_count": self.file_cache.load_metadata(chapter_hash).get("usage_count", 0) + 1
                })
                
                return session_info
        
        # 2. 파일 메타데이터 확인 (이전 프로세스에서 생성된 캐시 정보)
        metadata = self.file_cache.load_metadata(chapter_hash)
        if metadata:
            # 이전에 같은 장 조합이 처리되었음을 확인
            self.logger.info(f"📂 이전 세션 기록 발견 (해시: {chapter_hash}) | 장: {chapters}")
            created_time = metadata['created_at'].strftime('%H:%M:%S')
            self.logger.info(f"   📊 이전 캐시 정보: 생성시간={created_time}, 사용횟수={metadata['usage_count']}")
            
            # 새 세션 생성하지만, 같은 컨텍스트로 빠르게 설정 가능
            self.logger.info(f"🔄 동일 장 조합으로 새 세션 생성 (컨텍스트 재설정)")
        
        # 3. 새 세션 생성 + 컨텍스트 설정
        session_info = await self.ai_service.create_session()
        await self._setup_chapter_context(session_info, strategy)
        
        # 4. 메모리 캐시에 저장
        self.session_cache[chapter_hash] = session_info
        
        # 5. 메타데이터 저장/업데이트
        if metadata:
            # 기존 메타데이터 업데이트
            metadata_updates = {
                "last_used": datetime.now(),
                "usage_count": metadata["usage_count"] + 1
            }
            self.file_cache.update_metadata(chapter_hash, metadata_updates)
            log_message = f"🔄 장 조합 재처리 (해시: {chapter_hash}) | 장: {chapters}"
        else:
            # 새 메타데이터 생성
            new_metadata = {
                "created_at": datetime.now(),
                "last_used": datetime.now(), 
                "chapters": chapters,
                "usage_count": 1
            }
            self.file_cache.save_metadata(chapter_hash, new_metadata)
            log_message = f"🆕 새 장 조합 처리 (해시: {chapter_hash}) | 장: {chapters}"
        
        self.logger.info(log_message)
        cache_stats = self.file_cache.get_cache_stats()
        self.logger.info(f"   💾 캐시 통계: 메모리 {len(self.session_cache)}개, 메타데이터 {cache_stats['metadata_files']}개")
        
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
        
        self.logger.info(f"🤖 컨텍스트로 AI 질의 실행 중...")
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
        """만료된 캐시 정리"""
        self.file_cache.cleanup_expired_metadata()
        
    def get_cache_stats(self) -> dict:
        """캐시 통계 정보"""
        file_stats = self.file_cache.get_cache_stats()
        return {
            "memory_sessions": len(self.session_cache),
            "metadata_files": file_stats["metadata_files"]
        }