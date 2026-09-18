# 🚀 나만의 프롬프트 관리 프로그램 (Prompt Manager)

> 파이썬(Python 3.10+) 기본 문법만을 활용하여 제작된 콘솔 기반 프롬프트 관리 및 생산성 도구입니다.  
> 흩어져 있는 업무/창작용 프롬프트들을 체계적으로 분류, 검색, 즐겨찾기하고 영속화할 수 있습니다.

---

## 📌 주요 특징 및 기능 목록

### 1. 기본 필수 기능
- **프롬프트 추가 (`add_prompt`)**: 제목, 내용, 카테고리를 입력받아 신규 프롬프트 등록 (공백 입력 방어)
- **프롬프트 목록 조회 (`show_list`)**: 전체 프롬프트를 번호, 카테고리, 제목, ⭐ 즐겨찾기 여부와 함께 출력
- **카테고리별 조회 (`filter_by_category`)**: 특정 카테고리를 선택하여 해당 분야의 프롬프트만 필터링
- **키워드 검색 (`search_prompt`)**: 제목 또는 본문에 키워드가 포함된 프롬프트 검색
- **프롬프트 상세 보기 (`show_detail`)**: 전체 본문 열람 및 상세 조회 시 조회수(views) 자동 누적
- **즐겨찾기 관리 (`toggle_favorite`)**: 프롬프트 번호 입력을 통한 즐겨찾기 On/Off 토글
- **즐겨찾기 목록 (`show_favorites`)**: 즐겨찾기(⭐)로 지정된 프롬프트만 모아서 확인

### 2. 보너스 구현 기능
- **프롬프트 수정 / 삭제 (`manage_crud`)**: 등록된 프롬프트의 내용 수정 및 삭제 (CRUD 완성)
- **인기 프롬프트 정렬 (`show_top_prompts`)**: 조회수(views) 기준 내림차순 정렬 및 Top 랭킹 확인
- **JSON 영속화 (`save_and_load_json`)**: `prompts.json` 파일로 데이터 저장 및 불러오기
- **Markdown 내보내기 (`export_to_markdown`)**: 카테고리별로 정돈된 `exported_prompts.md` 마크다운 문서 생성

---

## 🗂 지원 카테고리
1. **텍스트 생성**: 블로그 글 작성, 카피라이팅, 기사 요약 등 텍스트 중심 프롬프트
2. **이미지 생성**: Midjourney, DALL-E, Stable Diffusion 등 고품질 이미지 생성 키워드
3. **영상 생성**: 유튜브 쇼츠, 릴스, 틱톡 등 숏폼 바이럴 영상 기획 및 연출 대본
4. **페르소나**: 시니어 IT 개발자, 전문 마케터, 비즈니스 컨설턴트 등 특정 전문가 역할 부여
5. **자동화**: 회의록 요약, 액션 아이템 추출, 업무 보고서 자동 생성
6. **기타**: 사용자 정의 신규 카테고리 직접 등록 지원

---

## 💻 실행 방법 (Getting Started)

### 요구 사양
- Python 3.10 이상
- 외부 라이브러리(`pip install`) 설치 불필요 (순수 내장 라이브러리 사용)

### 실행 명령어
```bash
# 1. 저장소 클론 (필요 시)
git clone https://github.com/hissuuummin/A1-1.git

# 2. 프로그램 실행
python main.py
```

---

## 📁 프로젝트 파일 구조
```text
├── .gitignore          # Git 제외 파일 설정
├── README.md           # 프로젝트 문서 및 사용 가이드
├── requirement.txt     # 과제 요구사항 명세서
├── PLAN.md             # 단계별 개발 계획 및 Git 전략서
├── TEST_REPORT.md      # 기능 검증 및 테스트 결과 보고서 (13/13 통과)
├── prompts_data.py     # 초기 탑재 프롬프트 5종 및 카테고리 데이터 모듈
└── main.py             # 콘솔 메뉴 및 핵심/보너스 기능 구현체
```

---

## 🛠 버전 관리 (Git / GitHub)
- 기능 단위 커밋(최소 10개 이상) 관리
- `feature/prompt-list` 브랜치 분기 후 `main` 브랜치로 병합(`checkout`, `merge`) 이력 수록
- 필수 Git 명령어(`init`, `add`, `commit`, `push`, `pull`, `checkout`, `clone`, `merge`) 실습 완료
