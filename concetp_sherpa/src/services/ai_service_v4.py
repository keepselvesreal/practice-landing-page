# 생성 시간: Sat Sep  6 11:15:45 KST 2025
# 핵심 내용: 통합 AI 서비스 - 새로운 인터페이스 (query_single_request, query_with_persistent_session)
# 상세 내용:
#   - SessionInfo (라인 25-40): 세션 정보 클래스 (간소화)
#   - AIProvider (라인 42-70): 새로운 메서드 인터페이스 추상 클래스
#   - ClaudeSDKProvider (라인 72-150): Claude SDK 구현
#   - GeminiProvider (라인 152-230): Gemini Chat 구현  
#   - OpenAIProvider (라인 232-310): OpenAI Assistant 구현
#   - AIService (라인 312-380): 통합 AI 서비스 클래스
# 상태: active
# 참조: ai_service_v3.py (인터페이스 교체)

import os
import logging
import uuid
import time
import json
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass, field
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

@dataclass
class SessionInfo:
    """AI 제공자별 세션 정보를 담는 단순 래퍼 클래스"""
    
    def __init__(self, provider_type: str, session_data: Any):
        self.provider_type = provider_type  # "claude", "gemini", "openai"
        self.session_data = session_data    # 각 provider의 네이티브 세션 데이터
        self.created_at = time.time()
        self.message_count = 0
    
    def update_usage(self):
        """세션 사용 시간 업데이트"""
        self.message_count += 1

class AIProvider(ABC):
    """AI 제공자 추상 클래스 - 새로운 인터페이스"""
    
    def __init__(self, config: Dict[str, Any], logger: logging.Logger):
        self.config = config
        self.logger = logger
        self.sessions: Dict[str, SessionInfo] = {}  # 세션 정보 저장
    
    @abstractmethod
    async def query_single_request(self, prompt: str, additional_data: Optional[Dict[str, Any]] = None) -> str:
        """
        일회성 AI 쿼리 - 세션을 사용하지 않는 단발성 요청
        
        Args:
            prompt: 질의 프롬프트
            additional_data: 추가 입력 데이터 (파일 경로, 구조화된 데이터 등)
        """
        pass

    @abstractmethod
    async def query_with_persistent_session(self, prompt: str, session_info: SessionInfo, 
                                          additional_data: Optional[Dict[str, Any]] = None) -> str:
        """
        세션 유지 AI 쿼리 - SessionInfo 객체를 직접 사용
        
        Args:
            prompt: 질의 프롬프트
            session_info: SessionInfo 객체 (제공자별 네이티브 세션 데이터 포함)
            additional_data: 추가 입력 데이터
        """
        pass
    
    @abstractmethod
    async def create_session(self) -> SessionInfo:
        """새로운 대화 세션 생성 - 각 provider가 구체 구현"""
        pass

    @abstractmethod
    def get_name(self) -> str:
        """AI 제공자 이름 반환"""
        pass

    def get_session_info(self, session_id: str) -> Optional[SessionInfo]:
        """세션 정보 조회"""
        return self.sessions.get(session_id)

class ClaudeSDKProvider(AIProvider):
    """Claude SDK를 이용한 AI 제공자 구현"""
    
    def __init__(self, config: Dict[str, Any], logger: logging.Logger):
        super().__init__(config, logger)
        
    async def query_single_request(self, prompt: str, additional_data: Optional[Dict[str, Any]] = None) -> str:
        """Claude 단발성 쿼리"""
        try:
            from claude_code_sdk import query as claude_query
            
            # additional_data 처리
            enhanced_prompt = prompt
            if additional_data:
                for key, value in additional_data.items():
                    if key == "toc_data":
                        enhanced_prompt += f"\n\n구조 정보:\n{json.dumps(value, ensure_ascii=False, indent=2)}"
                    elif key == "file_paths":
                        enhanced_prompt += f"\n\n관련 파일들:\n{', '.join(value)}"
            
            # Claude SDK 쿼리 실행 (v3와 동일한 방식)
            responses = []
            
            async for message in claude_query(prompt=enhanced_prompt):
                self.logger.info(f"메시지 타입: {type(message).__name__}")
                if hasattr(message, 'content'):
                    content = message.content
                    if isinstance(content, list):
                        for block in content:
                            if hasattr(block, 'text'):
                                responses.append(block.text)
                                self.logger.info(f"응답 받음: {block.text[:100]}...")
                    elif hasattr(content, 'text'):
                        responses.append(content.text)
                        self.logger.info(f"응답 받음: {content.text[:100]}...")
            
            response_text = '\n'.join(responses) if responses else ''
            self.logger.info(f"Claude SDK 응답 길이: {len(response_text)} 문자")
            return response_text
            
        except Exception as e:
            self.logger.error(f"Claude 단발성 쿼리 실패: {e}")
            raise

    async def create_session(self) -> SessionInfo:
        """Claude 세션 생성 - session_id 문자열을 SessionInfo로 래핑"""
        try:
            session_id = await self._create_claude_session()  # 내부 로직
            self.logger.info(f"Claude 세션 생성: {session_id[:12]}...")
            return SessionInfo("claude", session_id)
        except Exception as e:
            self.logger.error(f"Claude 세션 생성 실패: {e}")
            raise

    async def _create_claude_session(self) -> str:
        """Claude 세션 ID 생성 (내부 구현)"""
        try:
            from claude_code_sdk import create_session
            session_id = await create_session()
            return session_id
        except Exception as e:
            self.logger.error(f"Claude 네이티브 세션 생성 실패: {e}")
            # 임시 세션 ID 생성
            return f"claude_session_{uuid.uuid4().hex[:16]}"

    async def query_with_persistent_session(self, prompt: str, session_info: SessionInfo, 
                                          additional_data: Optional[Dict[str, Any]] = None) -> str:
        """Claude SDK를 사용한 지속적인 세션 대화 (실제 세션 ID 획득 방식)"""
        try:
            from claude_code_sdk import ClaudeSDKClient, query as claude_query, ClaudeCodeOptions
            
            # additional_data 처리 (기존 로직 유지)
            enhanced_prompt = prompt
            if additional_data:
                for key, value in additional_data.items():
                    if key == "toc_data":
                        enhanced_prompt += f"\n\n구조 정보:\n{json.dumps(value, ensure_ascii=False, indent=2)}"
                    elif key == "file_paths":
                        enhanced_prompt += f"\n\n관련 파일들:\n{', '.join(value)}"
            
            responses = []
            
            # 첫 번째 쿼리: ClaudeSDKClient로 세션 시작하고 실제 세션 ID 획득
            if session_info.message_count == 0:
                self.logger.info(f"🆕 새로운 ClaudeSDKClient 세션 시작...")
                async with ClaudeSDKClient() as client:
                    await client.query(enhanced_prompt)
                    async for msg in client.receive_response():
                        # 실제 세션 ID 추출 시도
                        if hasattr(msg, 'session_id'):
                            actual_session_id = msg.session_id
                            session_info.session_data = actual_session_id  # 실제 세션 ID로 업데이트
                            self.logger.info(f"✅ 실제 세션 ID 획득: {actual_session_id}")
                        
                        # 응답 내용 수집
                        if hasattr(msg, 'content'):
                            content = msg.content
                            if isinstance(content, list):
                                for block in content:
                                    if hasattr(block, 'text'):
                                        responses.append(block.text)
                                        self.logger.info(f"응답 받음: {block.text[:100]}...")
                            elif hasattr(content, 'text'):
                                responses.append(content.text)
                                self.logger.info(f"응답 받음: {content.text[:100]}...")
                        elif hasattr(msg, 'result'):
                            responses.append(str(msg.result))
                            self.logger.info(f"결과 받음: {str(msg.result)[:100]}...")
            else:
                # 후속 쿼리: 실제 세션 ID로 resume
                actual_session_id = session_info.session_data
                self.logger.info(f"🔗 기존 세션으로 대화 이어가기: {actual_session_id}")
                
                async for message in claude_query(
                    prompt=enhanced_prompt,
                    options=ClaudeCodeOptions(resume=actual_session_id)
                ):
                    self.logger.info(f"메시지 타입: {type(message).__name__}")
                    if hasattr(message, 'content'):
                        content = message.content
                        if isinstance(content, list):
                            for block in content:
                                if hasattr(block, 'text'):
                                    responses.append(block.text)
                                    self.logger.info(f"응답 받음: {block.text[:100]}...")
                        elif hasattr(content, 'text'):
                            responses.append(content.text)
                            self.logger.info(f"응답 받음: {content.text[:100]}...")
                    elif hasattr(message, 'result'):
                        responses.append(str(message.result))
                        self.logger.info(f"결과 받음: {str(message.result)[:100]}...")
            
            response_text = '\n'.join(responses) if responses else ''
            self.logger.info(f"✅ Claude SDK 세션 응답 길이: {len(response_text)} 문자")
            
            # 세션 사용량 업데이트
            session_info.update_usage()
            
            return response_text
            
        except Exception as e:
            self.logger.error(f"❌ Claude SDK 세션 쿼리 실패: {e}")
            raise
    
    def get_name(self) -> str:
        return "Claude SDK"

class GeminiProvider(AIProvider):
    """Gemini를 이용한 AI 제공자 구현"""
    
    def __init__(self, config: Dict[str, Any], logger: logging.Logger):
        super().__init__(config, logger)
        self.api_key = config.get('api_key') or os.getenv('GEMINI_API_KEY')
        self.model_name = config.get('model', 'gemini-2.0-flash-lite')
        
    async def query_single_request(self, prompt: str, additional_data: Optional[Dict[str, Any]] = None) -> str:
        """Gemini 단발성 쿼리"""
        try:
            import google.generativeai as genai
            
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel(self.model_name)
            
            # additional_data 처리
            enhanced_prompt = prompt
            if additional_data:
                for key, value in additional_data.items():
                    if key == "toc_data":
                        enhanced_prompt += f"\n\n목차 구조:\n{json.dumps(value, ensure_ascii=False, indent=2)}"
                    elif key == "context_info":
                        enhanced_prompt += f"\n\n맥락 정보:\n{value}"
            
            response = model.generate_content(enhanced_prompt)
            response_text = response.text if response.text else "응답이 비어있습니다"
            
            # AI 상호작용 로깅 (enhanced_prompt와 response 저장)
            if hasattr(self, 'logger') and self.logger:
                stage_name = "gemini_query"
                if additional_data and 'stage_name' in additional_data:
                    stage_name = additional_data['stage_name']
                
                self.logger.log_ai_interaction(
                    stage_name=stage_name,
                    model_name=self.model_name,
                    enhanced_prompt=enhanced_prompt,
                    response=response_text
                )
            
            return response_text
            
        except Exception as e:
            self.logger.error(f"Gemini 단발성 쿼리 실패: {e}")
            raise

    async def create_session(self) -> SessionInfo:
        """Gemini 채팅 세션 생성 - chat 객체를 SessionInfo로 래핑"""
        try:
            chat_object = self._create_gemini_chat()
            self.logger.info(f"Gemini 세션 생성: {id(chat_object)}")
            return SessionInfo("gemini", chat_object)
        except Exception as e:
            self.logger.error(f"Gemini 세션 생성 실패: {e}")
            raise

    def _create_gemini_chat(self):
        """Gemini 채팅 객체 생성 (내부 구현)"""
        try:
            import google.generativeai as genai
            
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel(self.model_name)
            chat = model.start_chat(history=[])
            
            return chat
        except Exception as e:
            self.logger.error(f"Gemini 채팅 객체 생성 실패: {e}")
            raise

    async def query_with_persistent_session(self, prompt: str, session_info: SessionInfo, 
                                          additional_data: Optional[Dict[str, Any]] = None) -> str:
        try:
            # additional_data 처리 (기존 로직)
            enhanced_prompt = prompt
            if additional_data:
                for key, value in additional_data.items():
                    if key == "toc_data":
                        enhanced_prompt += f"\n\n목차 구조:\n{json.dumps(value, ensure_ascii=False, indent=2)}"
                    elif key == "context_info":
                        enhanced_prompt += f"\n\n맥락 정보:\n{value}"
            
            # SessionInfo에서 Gemini chat 객체 추출
            chat_session = session_info.session_data
            
            # Gemini 직접 호출
            response = chat_session.send_message(enhanced_prompt)
            result = response.text if response.text else "응답이 비어있습니다"
            
            # 세션 사용량 업데이트
            session_info.update_usage()
            
            return result
            
        except Exception as e:
            self.logger.error(f"Gemini 세션 쿼리 실패: {e}")
            raise
    
    def get_name(self) -> str:
        return "Gemini"

class AnthropicProvider(AIProvider):
    """Anthropic API를 직접 사용한 AI 제공자 구현"""
    
    def __init__(self, config: Dict[str, Any], logger: logging.Logger):
        super().__init__(config, logger)
        self.api_key = config.get('api_key') or os.getenv('ANTHROPIC_API_KEY')
        self.model_name = config.get('model', 'claude-3-5-sonnet-20241022')
        
    async def query_single_request(self, prompt: str, additional_data: Optional[Dict[str, Any]] = None) -> str:
        """Anthropic API 단발성 쿼리"""
        try:
            from anthropic import AsyncAnthropic
            
            if not self.api_key:
                raise ValueError("ANTHROPIC_API_KEY가 설정되지 않았습니다")
            
            # additional_data 처리
            enhanced_prompt = prompt
            if additional_data:
                for key, value in additional_data.items():
                    if key == "toc_data":
                        enhanced_prompt += f"\n\n구조 정보:\n{json.dumps(value, ensure_ascii=False, indent=2)}"
                    elif key == "file_paths":
                        enhanced_prompt += f"\n\n관련 파일들:\n{', '.join(value)}"
            
            # Anthropic 클라이언트 생성
            client = AsyncAnthropic(api_key=self.api_key)
            
            # API 호출
            response = await client.messages.create(
                model=self.model_name,
                max_tokens=self.config.get('max_tokens', 8192),
                temperature=self.config.get('temperature', 0.1),
                messages=[{
                    "role": "user", 
                    "content": enhanced_prompt
                }]
            )
            
            # 응답 텍스트 추출
            response_text = ""
            if hasattr(response, 'content') and response.content:
                for block in response.content:
                    if hasattr(block, 'text'):
                        response_text += block.text
            
            self.logger.info(f"Anthropic API 응답 길이: {len(response_text)} 문자")
            return response_text
            
        except Exception as e:
            self.logger.error(f"Anthropic 단발성 쿼리 실패: {e}")
            raise

    async def create_session(self) -> SessionInfo:
        """Anthropic 세션 생성 - 대화 기록을 담는 SessionInfo 생성"""
        try:
            session_id = str(uuid.uuid4())
            # Anthropic는 대화 기록을 messages 배열로 관리
            session_data = {
                "messages": [],  # 대화 기록 저장
                "model": self.model_name,
                "api_key": self.api_key
            }
            self.logger.info(f"Anthropic 세션 생성: {session_id[:12]}...")
            
            session_info = SessionInfo("anthropic", session_data)
            self.sessions[session_id] = session_info
            return session_info
            
        except Exception as e:
            self.logger.error(f"Anthropic 세션 생성 실패: {e}")
            raise

    async def query_with_persistent_session(self, prompt: str, session_info: SessionInfo, 
                                          additional_data: Optional[Dict[str, Any]] = None) -> str:
        """Anthropic API를 사용한 지속적인 세션 대화"""
        try:
            from anthropic import AsyncAnthropic
            
            if not self.api_key:
                raise ValueError("ANTHROPIC_API_KEY가 설정되지 않았습니다")
            
            # additional_data 처리
            enhanced_prompt = prompt
            if additional_data:
                for key, value in additional_data.items():
                    if key == "toc_data":
                        enhanced_prompt += f"\n\n구조 정보:\n{json.dumps(value, ensure_ascii=False, indent=2)}"
                    elif key == "file_paths":
                        enhanced_prompt += f"\n\n관련 파일들:\n{', '.join(value)}"
            
            # 세션 데이터에서 대화 기록 가져오기
            session_data = session_info.session_data
            messages = session_data.get("messages", [])
            
            # 새로운 사용자 메시지 추가
            messages.append({
                "role": "user",
                "content": enhanced_prompt
            })
            
            # Anthropic 클라이언트 생성
            client = AsyncAnthropic(api_key=self.api_key)
            
            self.logger.info(f"🔗 Anthropic 세션 대화 (메시지 수: {len(messages)})")
            
            # API 호출 (전체 대화 기록 포함)
            response = await client.messages.create(
                model=self.model_name,
                max_tokens=self.config.get('max_tokens', 8192),
                temperature=self.config.get('temperature', 0.1),
                messages=messages
            )
            
            # 응답 텍스트 추출
            response_text = ""
            if hasattr(response, 'content') and response.content:
                for block in response.content:
                    if hasattr(block, 'text'):
                        response_text += block.text
            
            # 어시스턴트 응답을 대화 기록에 추가
            messages.append({
                "role": "assistant",
                "content": response_text
            })
            
            # 세션 데이터 업데이트
            session_data["messages"] = messages
            session_info.update_usage()
            
            self.logger.info(f"✅ Anthropic API 세션 응답 길이: {len(response_text)} 문자")
            return response_text
            
        except Exception as e:
            self.logger.error(f"❌ Anthropic API 세션 쿼리 실패: {e}")
            raise
    
    def get_name(self) -> str:
        return "Anthropic API"

class OpenAIProvider(AIProvider):
    """OpenAI를 이용한 AI 제공자 구현"""
    
    def __init__(self, config: Dict[str, Any], logger: logging.Logger):
        super().__init__(config, logger)
        self.api_key = config.get('api_key') or os.getenv('OPENAI_API_KEY')
        self.model_name = config.get('model', 'gpt-4')
        self.assistant_id = config.get('assistant_id')
        
    async def query_single_request(self, prompt: str, additional_data: Optional[Dict[str, Any]] = None) -> str:
        """OpenAI 단발성 쿼리"""
        try:
            import openai
            
            client = openai.AsyncOpenAI(api_key=self.api_key)
            
            # additional_data 처리
            enhanced_prompt = prompt
            if additional_data:
                for key, value in additional_data.items():
                    if key == "system_message":
                        enhanced_prompt = f"시스템: {value}\n\n사용자: {enhanced_prompt}"
                    elif key == "context_data":
                        enhanced_prompt += f"\n\n참고 데이터:\n{json.dumps(value, ensure_ascii=False, indent=2)}"
            
            response = await client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": enhanced_prompt}]
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            self.logger.error(f"OpenAI 단발성 쿼리 실패: {e}")
            raise

    async def create_session(self) -> SessionInfo:
        """OpenAI 스레드 세션 생성 - thread_id를 SessionInfo로 래핑"""
        try:
            thread_id = await self._create_openai_thread()
            self.logger.info(f"OpenAI 세션 생성: {thread_id}")
            return SessionInfo("openai", thread_id)
        except Exception as e:
            self.logger.error(f"OpenAI 세션 생성 실패: {e}")
            raise

    async def _create_openai_thread(self) -> str:
        """OpenAI 스레드 생성 (내부 구현)"""
        try:
            import openai
            
            client = openai.AsyncOpenAI(api_key=self.api_key)
            thread = await client.beta.threads.create()
            
            return thread.id
        except Exception as e:
            self.logger.error(f"OpenAI 스레드 생성 실패: {e}")
            # 임시 스레드 ID 생성
            return f"openai_thread_{uuid.uuid4().hex[:16]}"

    async def query_with_persistent_session(self, prompt: str, session_info: SessionInfo, 
                                          additional_data: Optional[Dict[str, Any]] = None) -> str:
        try:
            import openai
            
            client = openai.AsyncOpenAI(api_key=self.api_key)
            
            # additional_data 처리 (기존 로직)
            enhanced_prompt = prompt
            if additional_data:
                for key, value in additional_data.items():
                    if key == "system_message":
                        enhanced_prompt = f"시스템: {value}\n\n사용자: {enhanced_prompt}"
                    elif key == "context_data":
                        enhanced_prompt += f"\n\n참고 데이터:\n{json.dumps(value, ensure_ascii=False, indent=2)}"
            
            # SessionInfo에서 OpenAI thread_id 추출
            thread_id = session_info.session_data
            
            # OpenAI 직접 호출 (기존 내부 로직)
            message = await client.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=enhanced_prompt
            )
            
            if self.assistant_id:
                run = await client.beta.threads.runs.create(
                    thread_id=thread_id,
                    assistant_id=self.assistant_id
                )
                
                # 실행 완료 대기 (간소화)
                import asyncio
                for _ in range(30):  # 최대 30초 대기
                    run_status = await client.beta.threads.runs.retrieve(
                        thread_id=thread_id,
                        run_id=run.id
                    )
                    if run_status.status == 'completed':
                        break
                    await asyncio.sleep(1)
                
                # 응답 받기
                messages = await client.beta.threads.messages.list(thread_id=thread_id)
                response_text = messages.data[0].content[0].text.value if messages.data else "응답 없음"
            else:
                # Assistant 없이 직접 채팅 방식
                messages_list = await client.beta.threads.messages.list(thread_id=thread_id)
                response = await client.chat.completions.create(
                    model=self.model_name,
                    messages=[{"role": "user", "content": enhanced_prompt}]
                )
                response_text = response.choices[0].message.content
            
            # 세션 사용량 업데이트
            session_info.update_usage()
            
            return response_text
            
        except Exception as e:
            self.logger.error(f"OpenAI 세션 쿼리 실패: {e}")
            raise
    
    def get_name(self) -> str:
        return "OpenAI"

class AIService:
    """통합 AI 서비스 - 새로운 인터페이스"""
    
    def __init__(self, config_manager, logger, stage_name: str):
        """
        Args:
            config_manager: 설정 관리자
            logger: 로거 인스턴스
            stage_name: 설정 단계명 (예: "information_integration.detect_section_content")
        """
        self.config_manager = config_manager
        self.logger = logger
        self.stage_name = stage_name
        
        # 설정에 따른 제공자 초기화
        self.provider = self._create_provider()
    
    def _create_provider(self) -> AIProvider:
        """설정에 따른 AI 제공자 생성"""
        try:
            self.logger.info(f"🔍 AI 제공자 생성 시작 - stage_name: {self.stage_name}")
            # 설정에서 제공자 정보 가져오기
            try:
                ai_config = self.config_manager.get(f"stage_specific_ai.{self.stage_name}", {}, "ai")
                self.logger.info(f"📋 읽어온 AI 설정: {ai_config}")
            except Exception as config_error:
                self.logger.error(f"❌ 설정 읽기 실패: {config_error}")
                raise
            
            if not ai_config:
                # default_ai 설정으로 fallback
                self.logger.info("🔄 stage_specific_ai 설정이 없어서 default_ai로 fallback")
                ai_config = self.config_manager.get("default_ai", {
                    "provider": "gemini", 
                    "model": "gemini-2.0-flash-lite"
                }, "ai")
                self.logger.info(f"🎯 fallback으로 읽어온 default_ai 설정: {ai_config}")
            
            provider_name = ai_config.get("provider", "gemini").lower()
            self.logger.info(f"🎯 제공자 이름: {provider_name}")
            
            if provider_name == "claude" or provider_name == "claude_code":
                self.logger.info(f"Claude SDK 제공자 생성 시도 - config: {ai_config}")
                return ClaudeSDKProvider(ai_config, self.logger)
            elif provider_name == "anthropic":
                self.logger.info(f"Anthropic API 제공자 생성 시도 - config: {ai_config}")
                return AnthropicProvider(ai_config, self.logger)
            elif provider_name == "gemini":
                return GeminiProvider(ai_config, self.logger)  
            elif provider_name == "openai":
                return OpenAIProvider(ai_config, self.logger)
            else:
                self.logger.warning(f"알 수 없는 제공자: {provider_name}, Gemini로 대체")
                return GeminiProvider(ai_config, self.logger)
                
        except Exception as e:
            self.logger.error(f"AI 제공자 생성 실패: {e}")
            # 폴백: 기본 Gemini 제공자
            return GeminiProvider({"provider": "gemini", "model": "gemini-2.0-flash-lite"}, self.logger)
    
    async def query_single_request(self, prompt: str, additional_data: Optional[Dict[str, Any]] = None) -> str:
        """
        AI 쿼리 실행 (단발성)
        
        Args:
            prompt: 질의 프롬프트
            additional_data: 추가 입력 데이터 (파일 경로, TOC 데이터, 설정값 등)
        """
        try:
            self.logger.info(f"[{self.stage_name}] AI 단발성 쿼리 시작 - {self.provider.get_name()}")
            return await self.provider.query_single_request(prompt, additional_data)
        except Exception as e:
            error_msg = f"AI 단발성 쿼리 실패: {e}"
            self.logger.error(error_msg)
            raise Exception(error_msg)

    async def query_with_persistent_session(self, prompt: str, session_info: SessionInfo, 
                                          additional_data: Optional[Dict[str, Any]] = None) -> str:
        """
        세션을 유지하면서 AI 쿼리 실행
        
        Args:
            prompt: 질의 프롬프트
            session_info: SessionInfo 객체 (create_session()에서 반환된 객체)
            additional_data: 추가 입력 데이터
        """
        try:
            self.logger.info(f"[{self.stage_name}] 세션 쿼리 시작 - {self.provider.get_name()} ({session_info.provider_type})")
            return await self.provider.query_with_persistent_session(prompt, session_info, additional_data)
        except Exception as e:
            error_msg = f"세션 쿼리 실패: {e}"
            self.logger.error(error_msg)
            raise Exception(error_msg)

    async def create_session(self) -> SessionInfo:
        """새로운 AI 세션 생성 - provider가 SessionInfo 반환"""
        try:
            self.logger.info(f"[{self.stage_name}] 세션 생성 시작 - {self.provider.get_name()}")
            return await self.provider.create_session()  # SessionInfo 객체 반환
        except Exception as e:
            error_msg = f"세션 생성 실패: {e}"
            self.logger.error(error_msg)
            raise Exception(error_msg)
    
    def get_name(self) -> str:
        """AI 제공자 이름 반환"""
        return self.provider.get_name()
    
    def get_config_summary(self) -> Dict[str, Any]:
        """현재 설정 요약 반환"""
        return {
            "provider": self.provider.get_name(),
            "stage": self.stage_name
        }