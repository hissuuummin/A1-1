"""
나만의 프롬프트 관리 프로그램 (main.py)
"""

import copy
import sys
from prompts_data import CATEGORIES, INITIAL_PROMPTS

# Windows 터미널에서 ⭐ 이모지 및 유니코드 출력을 위해 UTF-8 인코딩 설정
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stdin.reconfigure(encoding="utf-8")
    except Exception:
        pass


def get_non_empty_input(prompt_text: str) -> str:
    """공백이 아닌 문자열을 입력받을 때까지 반복 요청하는 헬퍼 함수."""
    while True:
        value = input(prompt_text).strip()
        if value:
            return value
        print(">> 입력값이 비어있습니다. 다시 입력해주세요.")


def select_category() -> str:
    """카테고리 목록을 보여주고 선택받거나 직접 입력받는 함수."""
    print("\n카테고리 선택:")
    for idx, cat in enumerate(CATEGORIES, start=1):
        print(f"{idx}) {cat}")
    print(f"{len(CATEGORIES) + 1}) 직접 입력")

    while True:
        choice = input("선택: ").strip()
        if choice.isdigit():
            choice_num = int(choice)
            if 1 <= choice_num <= len(CATEGORIES):
                return CATEGORIES[choice_num - 1]
            if choice_num == len(CATEGORIES) + 1:
                custom_cat = get_non_empty_input("새 카테고리명 입력: ")
                if custom_cat not in CATEGORIES:
                    CATEGORIES.append(custom_cat)
                return custom_cat
        print(">> 올바른 번호를 선택해주세요.")


def show_menu() -> None:
    """메인 메뉴 출력 함수."""
    print("\n" + "=" * 32)
    print("      나만의 프롬프트 관리")
    print("=" * 32)
    print(" 1. 프롬프트 추가")
    print(" 2. 프롬프트 목록")
    print(" 3. 카테고리별 조회")
    print(" 4. 프롬프트 검색")
    print(" 5. 프롬프트 상세 보기")
    print(" 6. 즐겨찾기 관리")
    print(" 7. 즐겨찾기 목록")
    print("-" * 32)
    print(" 0. 종료")
    print("=" * 32)


def add_prompt(prompts: list[dict]) -> None:
    """1. 신규 프롬프트를 등록하는 함수."""
    print("\n=== 프롬프트 추가 ===")
    title = get_non_empty_input("제목: ")
    content = get_non_empty_input("내용: ")
    category = select_category()

    next_id = max((p.get("id", 0) for p in prompts), default=0) + 1

    new_item = {
        "id": next_id,
        "title": title,
        "content": content,
        "category": category,
        "favorite": False,
        "views": 0,
    }
    prompts.append(new_item)
    print("\n프롬프트가 추가되었습니다!")



def main() -> None:
    """프로그램 진입점 및 메인 실행 루프."""
    prompts = copy.deepcopy(INITIAL_PROMPTS)

    while True:
        show_menu()
        choice = input("선택: ").strip()

        if choice == "1":
            add_prompt(prompts)
        elif choice == "0":
            print("\n프로그램을 종료합니다. 이용해주셔서 감사합니다!")
            break
        else:
            print("\n>> 준비 중이거나 잘못된 번호입니다.")


if __name__ == "__main__":
    main()
