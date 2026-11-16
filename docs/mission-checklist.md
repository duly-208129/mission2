# 미션 요구사항 대조 (2026-11-16)

| 요구사항 | 구현·증빙 |
|---|---|
| 콘솔 메뉴, 종료, 오입력 재입력 | quiz_game.py: run, number, text |
| 주제 선정과 5개 이상 직접 작성 | README 주제 선정 이유, main.py 한국사 6문제 |
| Quiz·QuizGame 2개 클래스와 메서드 분리 | quiz.py, quiz_game.py |
| 문제 추가·목록·플레이·최고 점수 | 실제 CLI 검증 04~10 로그와 PNG |
| 재실행 후 등록 문제와 최고 점수 유지 | 06-restart.txt, 10-list.txt |
| 루트 state.json, UTF-8, 파일 오류 처리 | load_state, save_state, test_requirements.py |
| 빈 값·문자·범위 초과·공백 처리 | test_input_validation, test_play_reprompts_and_hint_score_persists |
| Ctrl+C 및 EOF 안전 종료 | test_safe_interrupt_and_eof |
| 파일 누락·손상 복구, 쓰기 실패 | test_missing_and_corrupt_storage, test_write_failure |
| 기본·빈 퀴즈 및 아직 플레이하지 않은 점수 | test_empty_and_unplayed |
| GitHub 코드 공개 및 10개 이상 커밋 | main 이력, git-graph.txt/png |
| 브랜치 생성·checkout·merge | fix/mission-requirements → main, merge 커밋 |
| clone 후 복제본 변경·commit·push, 원본 pull | git-evidence/mission-workflow.txt |
| init/add/commit/push/pull/checkout/clone | 기존 이력 및 mission-workflow.txt |
| README 필수 6항목 | 개요·주제 선정·실행·기능·파일 구조·데이터 파일 |
| 환경 및 실행·Git 로그 화면 | testing/environment.png, 05/06/07/10 PNG, git-graph.png |
| 보너스 | 랜덤·문제 수 선택·힌트 감점·삭제·게임 기록 구현 |

기존 구현은 여러 기능이 한 번에 커밋되어 있었습니다. 과거 각 기능 완성 직후 개별 커밋했다는 기록을 소급해서 만들지는 않았습니다. 보완 작업은 코드 수정, 테스트, 문서, 실습으로 나누어 실제 커밋하고 병합했습니다. 학습자가 직접 구현 내용을 설명할 수 있는지는 별도 확인이 필요합니다.

## 첨부 과제 재검토 결과 (2026-11-17)

첨부 과제의 필수 기능, 개발 환경, 제약 사항, 제출물과 대조했습니다. 기본 한국사 6문제, 두 클래스, 메뉴·추가·목록·플레이·최고 점수·저장 및 보너스 5종은 구현되어 있습니다. 기존 HEAD에는 21개 커밋과 병합 기록이 있습니다.

| 발견 사항 | 보완·확인 결과 |
|---|---|
| README의 로컬 실행 경로가 코드가 없는 중첩 폴더를 가리킴 | 실제 코드가 있는 `C:\Users\k'\mission2`로 수정 |
| Python 최소 버전 표시, 환경 화면 접근, 테스트 케이스 설명 부족 | Python 3.10 이상 명시, 환경 화면·로그 링크와 테스트 표 추가 |
| 변수·함수·클래스·JSON·파일 입출력·Git 학습 설명 부족 | 실제 코드 예시를 연결하여 설명 보완 |
| 파일 존재 확인 단계의 읽기 권한 오류가 예외 처리 바깥에 있음 | 존재 확인도 복구 처리 범위 안으로 이동 |
| 읽기 오류·잘못된 UTF-8·게임 도중 중단·오답 후 최고 점수 보존 검증 부족 | 회귀 테스트 추가, 총 10개 통과 |
| 실제 콘솔 흐름 재확인 | 메뉴·100점·재실행·추가·목록·삭제 모두 통과, 원본 state.json SHA-256 동일 |

실행 결과는 `testing/requirements-results.txt`, `testing/09-summary.txt` 및 개별 로그를 확인하세요. 기존 PNG는 이전 실행의 화면 자료이며, 최신 재검증 결과는 텍스트 로그입니다.

이 보완은 로컬 작업입니다. GitHub 최종 제출에는 보완 파일의 커밋과 push가 필요합니다. 기존 개발 당시 기능별 커밋 순서나 학습자의 직접 설명 여부는 이번 수정으로 대신할 수 없습니다.
