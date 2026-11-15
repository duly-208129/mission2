import json
import random
from datetime import datetime
from pathlib import Path
from quiz import Quiz


class QuizGame:
    def __init__(self, defaults):
        self.defaults = defaults
        self.path = Path(__file__).resolve().parent / 'state.json'
        self.quizzes = []
        self.best_score = 0
        self.history = []
        self.load_state()

    def load_state(self):
        if not self.path.exists():
            self.quizzes = self.defaults.copy()
            self.save_state()
            return
        try:
            data = json.loads(self.path.read_text(encoding='utf-8'))
            self.quizzes = [Quiz.from_dict(q) for q in data['quizzes']]
            self.best_score = int(data['best_score'])
            self.history = data['history']
            if not isinstance(self.history, list) or not 0 <= self.best_score <= 100:
                raise ValueError('저장 데이터 값 오류')
        except (OSError, ValueError, TypeError, KeyError) as exc:
            print(f'저장 데이터 오류: {exc}')
            print('원본 파일은 유지하고 기본 문제로 시작합니다. 백업 후 파일을 점검하세요.')
            self.quizzes = self.defaults.copy()
            self.best_score = 0
            self.history = []

    def save_state(self):
        data = {'quizzes':[q.to_dict() for q in self.quizzes],
                'best_score':self.best_score,'history':self.history}
        temp = self.path.with_suffix('.json.tmp')
        try:
            temp.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
            temp.replace(self.path)
            return True
        except OSError as exc:
            print(f'저장 실패: {exc}')
            return False

    @staticmethod
    def number(prompt, low, high):
        while True:
            value = input(prompt).strip()
            try:
                number = int(value)
                if low <= number <= high:
                    return number
            except ValueError:
                pass
            print(f'{low}~{high} 사이의 숫자를 입력하세요.')

    @staticmethod
    def text(prompt):
        while True:
            value = input(prompt).strip()
            if value:
                return value
            print('빈 값은 입력할 수 없습니다.')

    def play(self):
        if not self.quizzes:
            print('등록된 문제가 없습니다.')
            return
        categories = ['전체'] + sorted({q.category for q in self.quizzes})
        print('\n분야 선택:', ', '.join(f'{i}.{c}' for i,c in enumerate(categories)))
        category = categories[self.number('분야 번호: ',0,len(categories)-1)]
        levels = ['전체','초급','중급','고급']
        print('난이도 선택:', ', '.join(f'{i}.{x}' for i,x in enumerate(levels)))
        level = levels[self.number('난이도 번호: ',0,3)]
        pool = [q for q in self.quizzes if (category=='전체' or q.category==category)
                and (level=='전체' or q.level==level)]
        if not pool:
            print('조건에 맞는 문제가 없습니다.')
            return
        count = self.number(f'출제 문제 수(1~{len(pool)}): ',1,len(pool))
        questions = random.sample(pool,count)
        total = 0
        correct = 0
        for i,q in enumerate(questions,1):
            print(f'\n[{i}/{count}] [{q.category}/{q.level}] {q.question}')
            for j,choice in enumerate(q.choices,1):
                print(f'{j}. {choice}')
            hint = False
            while True:
                entry = input('정답 1~4 / H 힌트 / Enter 건너뛰기: ').strip()
                if entry.lower()=='h':
                    if hint:
                        print('힌트는 한 번만 사용할 수 있습니다.')
                    else:
                        print('힌트:',q.hint)
                        hint=True
                    continue
                if entry=='':
                    answer=None
                    break
                if entry in ('1','2','3','4'):
                    answer=int(entry)
                    break
                print('1~4, H 또는 Enter를 입력하세요.')
            gained=q.score(answer,hint)
            total+=gained
            if answer==q.answer:
                correct+=1
                print('정답입니다!')
            else:
                print(f'정답은 {q.answer}번입니다.')
            print('해설:',q.explanation)
            print(f'이번 문제 {gained}점')
        score=round(total/(count*10)*100)
        print(f'\n결과: {count}문제 / 정답 {correct}개 / 획득 {total}점 / 최종 {score}점')
        self.best_score=max(self.best_score,score)
        self.history.append({'played_at':datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                             'category':category,'level':level,'questions':count,
                             'correct':correct,'score':score})
        self.save_state()

    def add(self):
        question=self.text('문제: ')
        choices=[self.text(f'{i}번 선택지: ') for i in range(1,5)]
        answer=self.number('정답 번호(1~4): ',1,4)
        hint=self.text('힌트: ')
        explanation=self.text('해설: ')
        category=self.text('분야(예: 역사/문화): ')
        level=['초급','중급','고급'][self.number('난이도(1 초급, 2 중급, 3 고급): ',1,3)-1]
        self.quizzes.append(Quiz(question,choices,answer,hint,explanation,category,level))
        self.save_state()
        print('문제가 추가되었습니다.')

    def show(self):
        if not self.quizzes:
            print('등록된 문제가 없습니다.')
        for i,q in enumerate(self.quizzes,1):
            print(f'{i}. [{q.category}/{q.level}] {q.question}')

    def delete(self):
        if not self.quizzes:
            print('삭제할 문제가 없습니다.')
            return
        self.show()
        number=self.number('삭제 번호(0 취소): ',0,len(self.quizzes))
        if number and input('정말 삭제할까요? (y/N): ').strip().lower()=='y':
            self.quizzes.pop(number-1)
            self.save_state()
            print('삭제되었습니다.')

    def run(self):
        try:
            while True:
                print('\n=== K-History Quiz Adventure ===')
                print('1. 퀴즈 풀기  2. 문제 추가  3. 문제 목록  4. 문제 삭제')
                print('5. 최고 점수  6. 게임 기록  7. 종료')
                choice=self.number('선택: ',1,7)
                if choice==1:self.play()
                elif choice==2:self.add()
                elif choice==3:self.show()
                elif choice==4:self.delete()
                elif choice==5:print('최고 점수:',self.best_score)
                elif choice==6:
                    if not self.history:print('기록이 없습니다.')
                    for record in self.history:print(record)
                else:
                    self.save_state()
                    print('종료합니다.')
                    return
        except (KeyboardInterrupt,EOFError):
            print('\n종료 요청을 받았습니다.')
            self.save_state()
