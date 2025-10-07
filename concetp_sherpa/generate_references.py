# 생성 시간: 2025-09-24 10:42:10 KST
# 핵심 내용: 워크스페이스 준비 결과 데이터를 테스트 폴더 구조로 변환하는 스크립트 (임포트 문제 해결)
# 상세 내용:
#   - main (라인 18-85): 메인 실행 함수 (의존성 임포트 개선)
#   - process_book_data (라인 87-129): 개별 책 데이터 처리 함수
#   - create_chapter_folders (라인 131-155): 장별 폴더 생성 및 파일 저장
#   - save_chapter_files (라인 157-184): chapter_toc.json, content.md 파일 저장
#   - add_line_numbers_to_content (라인 186-221): content.md에 라인 번호 추가
# 상태: active
# 참조: create_test_data_structure.py (임포트 문제 수정)

import os
import json
import sys
import re
import asyncio
from pathlib import Path

# 정규화 함수 직접 정의 (의존성 제거)
def normalize_title(title: str) -> str:
    """제목 정규화 함수 - 특수문자 제거 및 언더스코어 변환"""
    title_clean = re.sub(r'[^\w\s.-]', '', title)
    title_clean = re.sub(r'[-\s]+', '_', title_clean).strip('_')
    return title_clean

async def main():
    """
    workspace_preparation_v3.py로 처리된 책 데이터를
    /references 폴더에 정규화된 구조로 저장
    """

    # 처리할 책들 - data 폴더의 모든 PDF 파일 자동 탐색
    project_root = Path(__file__).parent.parent
    data_folder = str(project_root / "data")
    output_base_folder = str(project_root / "references")

    # data 폴더의 모든 PDF 파일 자동 수집
    target_books = [f.name for f in Path(data_folder).glob("*.pdf")]

    if not target_books:
        print(f"⚠️ {data_folder}에서 PDF 파일을 찾을 수 없습니다.")
        return

    # 출력 폴더 생성
    os.makedirs(output_base_folder, exist_ok=True)

    print("🔄 테스트 데이터 구조 생성 시작...")
    print(f"📂 입력 폴더: {data_folder}")
    print(f"📂 출력 폴더: {output_base_folder}")
    print(f"📚 발견된 PDF: {len(target_books)}개")

    # sys.path에 필요한 경로들 추가
    concetp_src = os.path.join(str(project_root), "concetp_sherpa", "src")
    stages_path = os.path.join(concetp_src, "stages")

    for path in [concetp_src, stages_path]:
        if path not in sys.path:
            sys.path.insert(0, path)

    print(f"📦 sys.path에 추가된 경로: {concetp_src}, {stages_path}")

    # WorkspacePreparationStage 임포트
    try:
        from workspace_preparation_v3 import WorkspacePreparationStage
        print("✅ WorkspacePreparationStage 임포트 성공")
        print(f"✅ 클래스: {WorkspacePreparationStage}")
    except ImportError as e:
        print(f"❌ workspace_preparation_v3 임포트 실패: {e}")
        print(f"❌ 경로 확인: {stages_path}")
        print(f"❌ 현재 sys.path: {sys.path[:5]}")
        return
    except Exception as e:
        print(f"❌ 기타 임포트 오류: {e}")
        import traceback
        traceback.print_exc()
        return

    # 설정 매니저와 로거 팩토리 (간단한 더미 구현)
    class DummyConfigManager:
        def __init__(self):
            self.pipeline_config = {
                'workspace_preparation': {
                    'chapter_selection': {
                        'mode': 'all',
                        'selected_chapters': []
                    }
                }
            }

    class DummyLoggerFactory:
        pass

    config_manager = DummyConfigManager()
    logger_factory = DummyLoggerFactory()

    # 각 책 처리
    for book_filename in target_books:
        book_path = os.path.join(data_folder, book_filename)

        if not os.path.exists(book_path):
            print(f"⚠️ 파일을 찾을 수 없음: {book_path}")
            continue

        print(f"\n📖 처리 중: {book_filename}")

        try:
            result = await process_book_data(book_path, output_base_folder,
                                           config_manager, logger_factory,
                                           WorkspacePreparationStage)
            if result['success']:
                print(f"✅ 완료: {result['normalized_title']} ({result['chapters_count']}개 장)")
            else:
                print(f"❌ 실패: {result['error']}")

        except Exception as e:
            print(f"❌ 오류: {str(e)}")
            import traceback
            traceback.print_exc()

    print("\n🎉 테스트 데이터 구조 생성 완료!")

async def process_book_data(book_path: str, output_base_folder: str,
                          config_manager, logger_factory, WorkspacePreparationStage):
    """
    개별 책 데이터를 처리하여 테스트 폴더 구조 생성

    Args:
        book_path: PDF 파일 경로
        output_base_folder: 출력 기본 폴더
        config_manager: 설정 매니저
        logger_factory: 로거 팩토리
        WorkspacePreparationStage: 워크스페이스 준비 클래스

    Returns:
        Dict: 처리 결과 정보
    """

    # WorkspacePreparationStage 인스턴스 생성
    processor = WorkspacePreparationStage(config_manager, logger_factory)

    # PDF 처리 실행
    stage_input = {
        'data': {'pdf_path': book_path},
        'error': None
    }

    result = await processor.process(stage_input)

    if result['error'] or not result['data']:
        return {
            'success': False,
            'error': result['error'] or '처리 실패'
        }

    # 결과 데이터 추출
    book_info = result['data']['book_information']
    chapters_data = result['data']['chapters_data']

    normalized_book_title = book_info['normalized_title']

    # 책별 폴더 생성
    book_folder = os.path.join(output_base_folder, normalized_book_title)
    os.makedirs(book_folder, exist_ok=True)

    # 각 장별 폴더 및 파일 생성
    chapters_created = await create_chapter_folders(book_folder, chapters_data)

    return {
        'success': True,
        'normalized_title': normalized_book_title,
        'chapters_count': chapters_created,
        'error': None
    }

async def create_chapter_folders(book_folder: str, chapters_data: list):
    """
    각 장별 폴더 생성 및 파일 저장

    Args:
        book_folder: 책 폴더 경로
        chapters_data: 장 데이터 리스트

    Returns:
        int: 생성된 장 개수
    """

    chapters_created = 0

    for chapter_data in chapters_data:
        # 장 제목 정규화
        chapter_title = chapter_data['chapter_title']
        normalized_chapter_title = normalize_title(chapter_title)

        # 장 폴더 생성
        chapter_folder = os.path.join(book_folder, normalized_chapter_title)
        os.makedirs(chapter_folder, exist_ok=True)

        # 파일 저장
        await save_chapter_files(chapter_folder, chapter_data)

        chapters_created += 1
        print(f"  📁 생성: {normalized_chapter_title}")

    return chapters_created

async def save_chapter_files(chapter_folder: str, chapter_data: dict):
    """
    chapter_toc.json과 content.md 파일 저장 (라인 번호 추가)

    Args:
        chapter_folder: 장 폴더 경로
        chapter_data: 장 데이터
    """

    # chapter_toc.json 저장
    toc_file_path = os.path.join(chapter_folder, "chapter_toc.json")
    with open(toc_file_path, 'w', encoding='utf-8') as f:
        json.dump(chapter_data['chapter_toc'], f, ensure_ascii=False, indent=2)

    # content.md 저장 (라인 번호 추가)
    content_file_path = os.path.join(chapter_folder, "content.md")
    content_with_line_numbers = add_line_numbers_to_content(chapter_data['content_text'])
    with open(content_file_path, 'w', encoding='utf-8') as f:
        f.write(content_with_line_numbers)

def add_line_numbers_to_content(content_text: str) -> str:
    """
    content.md 텍스트에 IDE 스타일 라인 번호 추가

    Args:
        content_text: 원본 텍스트 내용

    Returns:
        str: 라인 번호가 추가된 텍스트
    """

    if not content_text:
        return content_text

    # 텍스트를 라인별로 분할
    lines = content_text.splitlines()

    # 라인 번호 추가
    numbered_lines = []
    for line_num, line in enumerate(lines, start=1):
        # Line X: 형식으로 라인 번호 표시
        numbered_line = f"Line {line_num}: {line}"
        numbered_lines.append(numbered_line)

    # 라인들을 다시 결합
    return "\n".join(numbered_lines)

if __name__ == "__main__":
    asyncio.run(main())