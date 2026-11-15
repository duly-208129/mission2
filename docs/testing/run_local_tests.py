"""Run real CLI processes in an isolated source copy and retain their output."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
original = hashlib.sha256((ROOT / 'state.json').read_bytes()).hexdigest()
env = dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONUTF8='1')

with tempfile.TemporaryDirectory(prefix='k_history_quiz_') as directory:
    work = Path(directory)
    for name in ('main.py', 'quiz.py', 'quiz_game.py'):
        shutil.copy2(ROOT / name, work / name)

    def run(filename, title, args, inputs=None):
        result = subprocess.run(args, cwd=work, env=env, input=inputs,
                                text=True, encoding='utf-8', capture_output=True, timeout=30)
        transcript = (f'{title}\n실행 시각: {datetime.now().astimezone().isoformat()}\n'
                      f'작업 폴더: {work}\nPS> ' + subprocess.list2cmdline(args) + '\n')
        if inputs is not None:
            transcript += '표준 입력(줄 순서): ' + repr(inputs) + '\n'
        transcript += result.stdout + result.stderr + f'\n종료 코드: {result.returncode}\n'
        (OUT / filename).write_text(transcript, encoding='utf-8')
        print(transcript)
        assert result.returncode == 0, filename
        return result.stdout

    run('01-python.txt', '로컬 Python 버전', [sys.executable, '--version'])
    run('02-git.txt', '로컬 Git 버전', ['git', '--version'])
    run('03-compile.txt', 'Python 문법 검사', [sys.executable, '-m', 'py_compile', 'main.py', 'quiz.py', 'quiz_game.py'])
    output = run('04-menu.txt', '테스트 1: 메뉴 표시 및 종료', [sys.executable, 'main.py'], '7\n')
    assert '종료합니다.' in output
    # A fixed seed selects the same question; the actual CLI still runs unchanged.
    output = run('05-quiz.txt', '테스트 2: 역사/초급 1문제 정답 및 채점',
                 [sys.executable, '-c', "import random, runpy; random.seed(0); runpy.run_path('main.py', run_name='__main__')"],
                 '1\n2\n1\n1\n3\n7\n')
    assert '최종 100점' in output
    output = run('06-restart.txt', '테스트 3: 새 프로세스에서 최고 점수 및 기록 조회',
                 [sys.executable, 'main.py'], '5\n6\n7\n')
    assert '최고 점수: 100' in output and "'score': 100" in output
    run('07-add.txt', '테스트 4: 문제 추가', [sys.executable, 'main.py'],
        '2\n로컬 테스트 전용 문제\n선택지1\n선택지2\n선택지3\n선택지4\n1\n테스트 힌트\n테스트 해설\n역사\n1\n7\n')
    state = json.loads((work / 'state.json').read_text(encoding='utf-8'))
    assert len(state['quizzes']) == 13 and state['quizzes'][-1]['question'] == '로컬 테스트 전용 문제'
    run('08-delete.txt', '테스트 5: 추가한 13번 문제 삭제', [sys.executable, 'main.py'], '4\n13\ny\n7\n')
    state = json.loads((work / 'state.json').read_text(encoding='utf-8'))
    assert len(state['quizzes']) == 12
    assert all(q['question'] != '로컬 테스트 전용 문제' for q in state['quizzes'])
    assert state['best_score'] == 100 and state['history'][-1]['score'] == 100
    assert hashlib.sha256((ROOT / 'state.json').read_bytes()).hexdigest() == original
    summary = ('PASS: 메뉴 표시 및 종료\nPASS: 정답 채점 100점\n'
               'PASS: 재실행 후 최고 점수 및 기록 유지\nPASS: 추가 후 JSON 13문제\n'
               'PASS: 삭제 후 JSON 12문제\nPASS: 원본 state.json SHA-256 동일\n'
               f'SHA-256: {original}\n')
    (OUT / '09-summary.txt').write_text(summary, encoding='utf-8')
    print(summary)
