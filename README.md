# 한국 역사 퀴즈 게임

Python 입문 미션을 위한 콘솔 프로그램입니다. 한국사 6문제로 시작하며 문제 등록·목록·플레이·최고 점수·게임 기록을 지원합니다.

## 주제 선정 이유

학교와 일상에서 접하는 한국사를 짧은 객관식 문제로 복습하기 위해 선택했습니다. 조선·고려 건국과 훈민정음 같은 기초 지식부터 임진왜란·가야·독립협회까지 난이도를 나눴고, 정답 해설을 통해 배경을 함께 배울 수 있습니다.

## 실행 방법

Python **3.10 이상**, Git이 필요합니다. 외부 라이브러리는 사용하지 않습니다.

```powershell
git clone https://github.com/duly-208129/mission2.git
cd mission2
py --version
py main.py
```

현재 컴퓨터의 기존 작업 폴더에서는 다음과 같이 실행합니다.

```powershell
cd "C:\Users\k'\mission2\k_history_quiz"
py main.py
```

`py` 대신 `python`을 사용할 수 있습니다. 메뉴에서 번호를 입력하고 Enter를 누릅니다. 종료는 7번입니다.

```text
=== K-History Quiz Adventure ===
1. 퀴즈 풀기  2. 문제 추가  3. 문제 목록  4. 문제 삭제
5. 최고 점수  6. 게임 기록  7. 종료
```

## 기능 목록

- 기본 역사 6문제: 초급 3개, 중급 3개. 선택지는 각 4개, 정답은 1~4입니다.
- 분야·난이도·문제 수 선택, 중복 없는 무작위 출제
- 정답·오답 안내, 해설, 문제당 1회 힌트
- 문제 추가·목록·삭제, 최고 점수, 날짜와 점수가 포함된 게임 기록
- 숫자 입력의 공백 제거, 빈 값·문자·범위 초과 입력의 안내 및 재입력
- Ctrl+C와 EOF 발생 시 안내하고 저장 후 종료
- 파일 누락 시 기본 데이터 생성, 손상된 파일의 안내와 기본 데이터 복구, 저장 실패 안내

힌트 없이 정답이면 10점, 힌트 사용 후 정답이면 7점, 오답이면 0점입니다. 최종 점수는 `round(획득 점수 / (문제 수 × 10) × 100)`입니다. 예를 들어 5문제에서 일반 정답 3개, 힌트 정답 1개, 오답 1개이면 74점입니다. 빈 정답은 다시 입력해야 합니다.

## 파일 구조

```text
mission2/
├── main.py              # 기본 6문제와 시작점
├── quiz.py              # Quiz 데이터·검증·채점
├── quiz_game.py         # QuizGame 메뉴·진행·저장
├── state.json           # 현재 퀴즈·최고 점수·게임 기록
├── .gitignore
├── README.md
└── docs/
    ├── mission-checklist.md
    ├── testing/         # 실행 로그, 검사 코드, 실제 출력 창 캡처
    └── git-evidence/    # Git 실습 로그와 확인 자료
```

## 데이터 파일

`state.json`의 기본 위치는 **프로젝트 루트**입니다. 실행한 터미널의 현재 폴더와 관계없이 `quiz_game.py`가 있는 폴더를 사용합니다. UTF-8 JSON으로 읽고 쓰며, 저장 시 임시 파일 `state.json.tmp`를 만든 뒤 교체합니다.

```json
{
  "quizzes": [
    {
      "question": "조선을 건국한 인물은?",
      "choices": ["왕건", "이성계", "세종", "정조"],
      "answer": 2,
      "hint": "조선의 초대 왕입니다.",
      "explanation": "이성계는 1392년에 조선을 건국했습니다.",
      "category": "역사",
      "level": "초급"
    }
  ],
  "best_score": 0,
  "history": []
}
```

위 예시는 구조 설명을 위해 문제 1개만 표시했습니다. 기본 문제는 6개이며 기존 사용자가 저장한 문제와 플레이 기록은 보존합니다. `best_score`는 0~100 정수입니다. `history`에는 `played_at`, `category`, `level`, `questions`, `correct`, `score`를 저장합니다. 선택 기능인 `history` 키가 없는 최소 저장 파일도 읽을 수 있습니다.

파일이 손상되면 기본 문제로 시작합니다. 시작 시 원본 파일은 유지되지만 이후 정상 저장이나 종료 시 복구 데이터로 교체되므로 원본을 조사하려면 먼저 백업하세요. 저장 오류는 안내하고 프로그램을 유지합니다. JSON 전체를 읽고 쓰므로 대량 데이터나 동시 실행에는 적합하지 않습니다.

## 코드와 학습 포인트

`Quiz`는 dataclass로 문제의 속성과 채점·검증·JSON 변환을 묶습니다. 자동 생성되는 `__init__`이 속성을 초기화하고 `__post_init__`에서 값을 검증합니다. `self`는 현재 객체를 가리킵니다. `QuizGame`은 퀴즈 목록, 최고 점수, 기록을 보유하고 입력·플레이·추가·목록·저장 메서드를 분리합니다.

정답과 점수는 `int`, 문제와 입력은 `str`, 힌트 사용 여부는 `bool`, 문제·기록은 `list`, JSON 항목은 `dict`로 표현합니다. `if/elif/else`는 메뉴 분기, `for`는 문제와 선택지 순회, `while`은 메뉴 반복과 재입력에 사용합니다. 함수는 매개변수로 값을 받아 반환값을 돌려줍니다. 파일 오류는 `try/except`로 처리합니다.

클래스는 데이터와 동작의 책임을 찾기 쉽게 합니다. 다만 현재 게임 클래스가 입출력과 저장을 함께 담당하므로, 규모가 커지면 이를 분리할 수 있습니다. 기본 문제의 목록 복사는 얕은 복사이므로 내부 문제 객체를 직접 변경하는 확장에는 주의가 필요합니다.

## 검증과 제출 자료

```powershell
py docs/testing/run_local_tests.py
py docs/testing/test_requirements.py
```

테스트는 임시 폴더에서 실행하며 사용자 `state.json`을 변경하지 않습니다. 메뉴, 100점 채점, 재실행 후 최고 점수·등록 문제 유지, 목록, 삭제를 검사했습니다. 추가로 빈 입력·손상 데이터·힌트 감점·Ctrl+C·EOF·쓰기 실패 등 7개 테스트가 통과했습니다.

- [기능 검증 요약](docs/testing/09-summary.txt)
- [예외 처리 테스트](docs/testing/requirements-results.txt)
- [환경 확인 화면](docs/testing/environment.png)
- [추가 화면](docs/testing/07-add.png), [목록 화면](docs/testing/10-list.png)
- [플레이 화면](docs/testing/05-quiz.png), [점수·재실행 화면](docs/testing/06-restart.png)
- [Git 그래프 화면](docs/testing/git-graph.png)
- [요구사항 대조표](docs/mission-checklist.md)
- [clone → 변경·commit·push → 기존 폴더 pull 실습](docs/git-evidence/mission-workflow.txt)

화면 자료는 실제 명령 출력 로그를 표시한 전용 창을 캡처한 것입니다. 로그 파일에서 전체 출력을 확인할 수 있습니다.

## Git 기록

제출 브랜치는 `main`입니다. 기존 `master`와 별개였던 과거 `main` 이력을 삭제하거나 재작성하지 않고 병합했습니다. 현재 루트 구조를 채택하여 예전 중첩 폴더 및 빌드 산출물은 현재 트리에서 제외했습니다. 과거 커밋에서는 확인할 수 있습니다.

`fix/mission-requirements`에서 입력·데이터 검증 및 회귀 테스트를 작업한 후 `main`에 `--no-ff`로 병합했습니다. 과거 기능 개발 과정에 없던 커밋을 소급해서 만들지 않았으며, 기존 기록과 실제 보완 작업으로 10개 이상의 커밋을 확보했습니다.

`init`은 저장소 초기화, `add`는 변경 선택, `commit`은 로컬 기록 저장, `push`는 원격 반영, `clone`은 저장소 복제, `pull`은 원격 변경 수신·통합, `checkout`은 브랜치 전환에 사용합니다. 병합은 `merge`로 수행합니다. 복제 실습 및 새 로컬 저장소의 `init` 결과는 실습 로그에 남겼습니다.

저장소 URL: https://github.com/duly-208129/mission2
