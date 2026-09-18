"""
나만의 프롬프트 관리 프로그램 (main.py)

- Python 3.10+ 표준 라이브러리만을 사용하여 구현
- 프롬프트 추가, 목록 조회, 카테고리별 필터링, 검색, 상세 보기, 즐겨찾기 관리 기능 제공
- 보너스 과제 포함: 수정/삭제(CRUD), 조회수(views) 카운트 & Top 목록, JSON 영속화, Markdown 내보내기
"""

import copy
import json
import os
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
    print(" [보너스 기능]")
    print(" 8. 프롬프트 수정 / 삭제")
    print(" 9. 인기 프롬프트 (조회수 Top)")
    print(" 10. JSON 저장 및 불러오기")
    print(" 11. 카테고리별 Markdown 내보내기")
    print("-" * 32)
    print(" 0. 종료")
    print("=" * 32)


def add_prompt(prompts: list[dict]) -> None:
    """1. 신규 프롬프트를 등록하는 함수."""
    print("\n=== 프롬프트 추가 ===")
    title = get_non_empty_input("제목: ")
    content = get_non_empty_input("내용: ")
    category = select_category()

    # 고유 ID 생성 (기존 최대 ID + 1)
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
    # 현재 등록된 프롬프트들에 존재하는 카테고리 + 기본 카테고리 목록
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


def show_detail(prompts: list[dict]) -> None:
    """5. 프롬프트 상세 내용을 출력하고 조회수를 증가시키는 함수."""
    print("\n=== 프롬프트 상세 보기 ===")
    if not prompts:
        print("등록된 프롬프트가 없습니다.")
        return

    choice = input("번호 입력: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(prompts)):
        print(">> 올바른 프롬프트 번호를 입력해주세요.")
        return

    p = prompts[int(choice) - 1]
    p["views"] = p.get("views", 0) + 1  # 보너스: 조회수 카운트

    star = "⭐" if p.get("favorite") else "해제됨"
    print("\n" + "─" * 40)
    print(f"제목: {p['title']}")
    print(f"카테고리: {p['category']}")
    print(f"즐겨찾기: {star}")
    print(f"조회수: {p['views']}회")
    print("─" * 40)
    print("내용:")
    print(p["content"])
    print("─" * 40)


def toggle_favorite(prompts: list[dict]) -> None:
    """6. 프롬프트 번호를 입력받아 즐겨찾기를 추가/해제하는 함수."""
    print("\n=== 즐겨찾기 관리 ===")
    if not prompts:
        print("등록된 프롬프트가 없습니다.")
        return

    choice = input("프롬프트 번호 입력: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(prompts)):
        print(">> 올바른 프롬프트 번호를 입력해주세요.")
        return

    p = prompts[int(choice) - 1]
    p["favorite"] = not p.get("favorite", False)

    status_str = "추가" if p["favorite"] else "해제"
    print(f"'{p['title']}' 프롬프트를 즐겨찾기에 {status_str}했습니다!")


def show_favorites(prompts: list[dict]) -> None:
    """7. 즐겨찾기된 프롬프트만 모아서 출력하는 함수."""
    print("\n=== 즐겨찾기 목록 ===")
    favorites = [p for p in prompts if p.get("favorite")]

    if not favorites:
        print("즐겨찾기로 등록된 프롬프트가 없습니다.")
        return

    for idx, p in enumerate(favorites, start=1):
        print(f"{idx}. [{p['category']}] {p['title']} ⭐")

    print(f"\n총 {len(favorites)}개의 즐겨찾기")


# -------------------------------------------------------------
# 보너스 과제 기능 모듈
# -------------------------------------------------------------

def manage_crud(prompts: list[dict]) -> None:
    """8. [보너스 2] 프롬프트 수정(Update) 및 삭제(Delete) 기능."""
    print("\n=== 프롬프트 수정 / 삭제 ===")
    if not prompts:
        print("등록된 프롬프트가 없습니다.")
        return

    print("1) 프롬프트 수정")
    print("2) 프롬프트 삭제")
    sub_choice = input("선택: ").strip()

    if sub_choice == "1":
        choice = input("수정할 프롬프트 번호 입력: ").strip()
        if not choice.isdigit() or not (1 <= int(choice) <= len(prompts)):
            print(">> 올바른 프롬프트 번호를 입력해주세요.")
            return
        target = prompts[int(choice) - 1]
        print(f"\n현재 제목: {target['title']}")
        new_title = input("새 제목 (변경 없으면 엔터): ").strip()
        if new_title:
            target["title"] = new_title

        print(f"\n현재 내용: {target['content'][:30]}...")
        new_content = input("새 내용 (변경 없으면 엔터): ").strip()
        if new_content:
            target["content"] = new_content

        change_cat = input(f"카테고리({target['category']})를 변경하시겠습니까? (y/N): ").strip().lower()
        if change_cat == "y":
            target["category"] = select_category()

        print("프롬프트가 성공적으로 수정되었습니다!")

    elif sub_choice == "2":
        choice = input("삭제할 프롬프트 번호 입력: ").strip()
        if not choice.isdigit() or not (1 <= int(choice) <= len(prompts)):
            print(">> 올바른 프롬프트 번호를 입력해주세요.")
            return
        target = prompts[int(choice) - 1]
        confirm = input(f"정말로 '{target['title']}' 프롬프트를 삭제하시겠습니까? (y/N): ").strip().lower()
        if confirm == "y":
            deleted = prompts.pop(int(choice) - 1)
            print(f"'{deleted['title']}' 프롬프트가 삭제되었습니다.")
    else:
        print(">> 올바른 번호를 선택해주세요.")


def show_top_prompts(prompts: list[dict]) -> None:
    """9. [보너스 2] 조회수 기준 Top 정렬 기능."""
    print("\n=== 인기 프롬프트 (조회수 Top 순) ===")
    if not prompts:
        print("등록된 프롬프트가 없습니다.")
        return

    sorted_prompts = sorted(prompts, key=lambda x: x.get("views", 0), reverse=True)
    for idx, p in enumerate(sorted_prompts, start=1):
        star = " ⭐" if p.get("favorite") else ""
        print(f"{idx}. [{p['category']}] {p['title']}{star} (조회수: {p.get('views', 0)}회)")


def save_and_load_json(prompts: list[dict]) -> None:
    """10. [보너스 1] JSON 파일로 저장 및 불러오기."""
    filepath = "prompts.json"
    print("\n=== JSON 영속화 관리 ===")
    print("1) 현재 프롬프트들을 prompts.json 파일로 저장")
    print("2) prompts.json 파일에서 프롬프트 불러오기")
    choice = input("선택: ").strip()

    if choice == "1":
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(prompts, f, ensure_ascii=False, indent=4)
            print(f"성공적으로 {len(prompts)}개의 프롬프트를 '{filepath}'에 저장했습니다.")
        except Exception as e:
            print(f">> 저장 중 오류 발생: {e}")

    elif choice == "2":
        if not os.path.exists(filepath):
            print(f">> '{filepath}' 파일이 존재하지 않습니다.")
            return
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                loaded_data = json.load(f)
            prompts.clear()
            prompts.extend(loaded_data)
            print(f"성공적으로 '{filepath}'에서 {len(prompts)}개의 프롬프트를 불러왔습니다.")
        except Exception as e:
            print(f">> 불러오기 중 오류 발생: {e}")
    else:
        print(">> 올바른 번호를 입력해주세요.")


def export_to_markdown(prompts: list[dict]) -> None:
    """11. [보너스 1] 전체 프롬프트를 카테고리별 Markdown 파일로 내보내기."""
    filepath = "exported_prompts.md"
    print("\n=== 카테고리별 Markdown 내보내기 ===")
    if not prompts:
        print("내보낼 프롬프트가 없습니다.")
        return

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("# 프롬프트 모음집 (Prompt Collection)\n\n")
            f.write(f"> 총 {len(prompts)}개의 프롬프트가 수록되어 있습니다.\n\n")

            # 카테고리별 그룹화
            categorized: dict[str, list[dict]] = {}
            for p in prompts:
                categorized.setdefault(p["category"], []).append(p)

            for cat, items in categorized.items():
                f.write(f"## 📁 {cat}\n\n")
                for p in items:
                    star = " ⭐ (즐겨찾기)" if p.get("favorite") else ""
                    f.write(f"### {p['title']}{star}\n")
                    f.write(f"- **조회수**: {p.get('views', 0)}회\n\n")
                    f.write("```text\n")
                    f.write(p["content"] + "\n")
                    f.write("```\n\n")
                    f.write("---\n\n")

        print(f"성공적으로 '{filepath}' 파일로 마크다운 문서를 내보냈습니다!")
    except Exception as e:
        print(f">> 마크다운 내보내기 실패: {e}")


def main() -> None:
    """프로그램 진입점 및 메인 실행 루프."""
    # 기본 프롬프트 복사본으로 메모리 데이터 초기화
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
        elif choice == "5":
            show_detail(prompts)
        elif choice == "6":
            toggle_favorite(prompts)
        elif choice == "7":
            show_favorites(prompts)
        elif choice == "8":
            manage_crud(prompts)
        elif choice == "9":
            show_top_prompts(prompts)
        elif choice == "10":
            save_and_load_json(prompts)
        elif choice == "11":
            export_to_markdown(prompts)
        elif choice == "0":
            print("\n프로그램을 종료합니다. 이용해주셔서 감사합니다!")
            break
        else:
            print("\n>> 잘못된 번호입니다. 메뉴의 번호를 확인하고 다시 입력해주세요.")


if __name__ == "__main__":
    main()
