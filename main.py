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


def show_list(prompts: list[dict]) -> None:
    """2. 전체 프롬프트 목록을 출력하는 함수."""
    print("\n=== 프롬프트 목록 ===")
    if not prompts:
        print("등록된 프롬프트가 없습니다.")
        return

    for idx, p in enumerate(prompts, start=1):
        star = " ⭐" if p.get("favorite") else ""
        print(f"{idx}. [{p['category']}] {p['title']}{star}")

    print(f"\n총 {len(prompts)}개의 프롬프트")


def filter_by_category(prompts: list[dict]) -> None:
    """3. 카테고리를 선택받아 해당 카테고리 프롬프트만 출력하는 함수."""
    print("\n=== 카테고리별 조회 ===")
    available_categories = list(dict.fromkeys(CATEGORIES + [p["category"] for p in prompts]))

    for idx, cat in enumerate(available_categories, start=1):
        print(f"{idx}) {cat}")

    choice = input("선택: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(available_categories)):
        print(">> 올바른 카테고리 번호를 입력해주세요.")
        return

    selected_category = available_categories[int(choice) - 1]
    filtered = [p for p in prompts if p["category"] == selected_category]

    print(f"\n[{selected_category}] 카테고리 프롬프트:")
    if not filtered:
        print("해당 카테고리에 프롬프트가 없습니다.")
        return

    for idx, p in enumerate(filtered, start=1):
        star = " ⭐" if p.get("favorite") else ""
        print(f"{idx}. {p['title']}{star}")

    print(f"\n총 {len(filtered)}개의 프롬프트")


def search_prompt(prompts: list[dict]) -> None:
    """4. 키워드를 입력받아 제목 또는 내용에 포함된 프롬프트를 검색하는 함수."""
    print("\n=== 프롬프트 검색 ===")
    keyword = get_non_empty_input("검색어: ").lower()

    results = [
        p for p in prompts
        if keyword in p["title"].lower() or keyword in p["content"].lower()
    ]

    print("\n검색 결과:")
    if not results:
        print("일치하는 프롬프트가 없습니다.")
        return

    for idx, p in enumerate(results, start=1):
        star = " ⭐" if p.get("favorite") else ""
        print(f"{idx}. [{p['category']}] {p['title']}{star}")

    print(f"\n{len(results)}개의 프롬프트를 찾았습니다.")


def main() -> None:
    """프로그램 진입점 및 메인 실행 루프."""
    prompts = copy.deepcopy(INITIAL_PROMPTS)

    while True:
        show_menu()
        choice = input("선택: ").strip()

        if choice == "1":
            add_prompt(prompts)
        elif choice == "2":
            show_list(prompts)
        elif choice == "3":
            filter_by_category(prompts)
        elif choice == "4":
            search_prompt(prompts)
        elif choice == "0":
            print("\n프로그램을 종료합니다. 이용해주셔서 감사합니다!")
            break
        else:
            print("\n>> 준비 중이거나 잘못된 번호입니다.")


if __name__ == "__main__":
    main()
