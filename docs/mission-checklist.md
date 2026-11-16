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
