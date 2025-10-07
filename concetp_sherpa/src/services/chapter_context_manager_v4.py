# 생성 시간: 2024-09-19 15:45:00 KST  
# 핵심 내용: 전역 싱글톤 기반 Chapter 컨텍스트 캐싱 매니저 (캐시 지속성 개선)
# 상세 내용:
#   - GlobalChapterContextManager (라인 15-35): 전역 싱글톤 캐시 매니저
#   - ChapterContextManager (라인 40-70): 장 조합별 컨텍스트 캐싱 (올바른 메서드 사용)
#   - generate_chapter_hash (라인 75-80): 장 조합 해시 생성  
#   - get_or_setup_context_cache (라인 85-115): 컨텍스트 설정 (싱글톤 캐시 활용)
#   - query_with_cached_context (라인 120-135): 캐시된 컨텍스트로 질의 (올바른 메서드명)
# 상태: active
# 참조: chapter_context_manager_v3.py (캐시 지속성 개선)

import hashlib
import asyncio
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from pathlib import Path

class GlobalChapterContextManager:
    """전역 싱글톤 컨텍스트 캐시 매니저"""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GlobalChapterContextManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.context_cache: Dict[str, str] = {}  # {chapter_hash: session_info}
            self.context_metadata: Dict[str, dict] = {}  # 컨텍스트 메타데이터
            self.cache_ttl = 3600  # 1시간 TTL
            GlobalChapterContextManager._initialized = True
    
    def get_instance(self):
        """싱글톤 인스턴스 반환"""
        return self
    
    def clear_cache(self):
        """캐시 초기화 (테스트용)"""
        self.context_cache.clear()
        self.context_metadata.clear()

class ChapterContextManager:
    """장 조합 기반 컨텍스트 캐싱 매니저 (싱글톤 캐시 활용)"""
    
    def __init__(self, ai_service, logger, config_manager):
        self.ai_service = ai_service
        self.logger = logger
        self.config = config_manager
        # 전역 캐시 매니저 사용
        self.global_cache = GlobalChapterContextManager()
        
    @property
    def context_cache(self):
        """전역 캐시에 대한 프록시"""
        return self.global_cache.context_cache
    
    @property
    def context_metadata(self):
        """전역 메타데이터에 대한 프록시"""
        return self.global_cache.context_metadata

    def generate_chapter_hash(self, chapters: List[str]) -> str:
        """장 조합으로 고유 해시 생성"""
        chapters_sorted = sorted(chapters)
        return hashlib.md5(':'.join(chapters_sorted).encode()).hexdigest()[:12]

    async def get_or_setup_context_cache(self, chapters: List[str], strategy):
        """장 조합별 컨텍스트 캐시 확보 + 설정 (전역 캐시 활용)"""
        chapter_hash = self.generate_chapter_hash(chapters)
        
        # 기존 컨텍스트 캐시 확인 (전역 캐시에서)
        if chapter_hash in self.context_cache:
            session_info = self.context_cache[chapter_hash]
            if await self._is_context_cache_valid(session_info):
                # 캐시 재사용 상세 로깅
                metadata = self.context_metadata[chapter_hash]
                self.logger.info(f"♻️ 장 컨텍스트 캐시 재사용 (해시: {chapter_hash}) | 장: {chapters}")
                self.logger.info(f"   📊 캐시 정보: 생성시간={metadata['created_at'].strftime('%H:%M:%S')}, 사용횟수={metadata['usage_count']}")
                
                # 사용 통계 업데이트
                self.context_metadata[chapter_hash]["last_used"] = datetime.now()
                self.context_metadata[chapter_hash]["usage_count"] += 1
                
                return session_info

        # 새 컨텍스트 캐시 생성 
        session_info = await self.ai_service.create_session()
        
        # ✅ 핵심: 컨텍스트 설정 (한 번만!)
        await self._setup_chapter_context(session_info, strategy)
        
        # 전역 캐시에 저장
        self.context_cache[chapter_hash] = session_info
        self.context_metadata[chapter_hash] = {
            "created_at": datetime.now(),
            "last_used": datetime.now(), 
            "chapters": chapters,
            "usage_count": 1
        }
        
        self.logger.info(f"🆕 새 컨텍스트 캐시 생성 (해시: {chapter_hash}) | 장: {chapters}")
        self.logger.info(f"   💾 전역 캐시 통계: 총 {len(self.context_cache)}개 캐시 보유")
        return session_info

    async def _setup_chapter_context(self, session_info, strategy):
        """컨텍스트 캐시에 장 내용 설정 (한 번만 실행)"""
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
        
        # ✅ 개선된 컨텍스트 설정 프롬프트
        context_setup_prompt = f"""다음은 참조할 장들의 내용입니다. 이후 질의에서는 이 내용을 바탕으로 답변해주세요.

{combined_content}

**중요한 응답 규칙:**
1. 이 내용을 기억하고 있다가, 다음 질의들에 대해 위 내용을 바탕으로 답변해주세요.
2. 컨텐츠에 없는 내용은 추측하지 마세요.
3. **답변 생성 시 반드시 참조한 섹션명과 줄 번호 정보를 답변 끝에 표시해주세요.**
   형식: [참조: 섹션명 (줄 XX-XX)]"""

        # ✅ 올바른 메서드명 사용
        await self.ai_service.query_with_persistent_session(context_setup_prompt, session_info)

    async def query_with_cached_context(self, query: str, session_info) -> str:
        """캐시된 컨텍스트로 질의 (질의만 전송!)"""
        # ✅ 핵심: 질의만 전송 (컨텍스트는 이미 캐시에 있음)
        simple_query = f"질의: {query}"
        
        self.logger.info(f"🤖 캐시된 컨텍스트로 AI 질의 실행 중...")
        self.logger.info(f"   📝 질의 길이: {len(simple_query)}자")
        
        # ✅ 올바른 메서드명 사용
        response = await self.ai_service.query_with_persistent_session(simple_query, session_info)
        
        self.logger.info(f"✅ AI 응답 수신 완료 (길이: {len(response)}자)")
        return response

    async def _is_context_cache_valid(self, session_info) -> bool:
        """컨텍스트 캐시 유효성 검증"""
        try:
            # SessionInfo 객체의 유효성 확인
            return session_info is not None and hasattr(session_info, 'session_data')
        except:
            return False

    async def cleanup_expired_caches(self):
        """만료된 컨텍스트 캐시 정리"""
        now = datetime.now()
        expired_hashes = []
        
        for hash_key, metadata in self.context_metadata.items():
            if now - metadata["created_at"] > timedelta(seconds=self.global_cache.cache_ttl):
                expired_hashes.append(hash_key)

        for hash_key in expired_hashes:
            if hash_key in self.context_cache:
                del self.context_cache[hash_key]
            if hash_key in self.context_metadata:
                del self.context_metadata[hash_key]

        if expired_hashes:
            self.logger.info(f"🧹 만료된 컨텍스트 캐시 정리: {len(expired_hashes)}개")
            
    def get_cache_stats(self) -> dict:
        """캐시 통계 정보 반환"""
        return {
            "total_caches": len(self.context_cache),
            "cache_usage": {hash_key: metadata["usage_count"] for hash_key, metadata in self.context_metadata.items()},
            "cache_age": {hash_key: (datetime.now() - metadata["created_at"]).seconds for hash_key, metadata in self.context_metadata.items()}
        }