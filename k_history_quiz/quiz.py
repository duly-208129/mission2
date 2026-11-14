from dataclasses import dataclass


@dataclass
class Quiz:
    question: str
    choices: list[str]
    answer: int
    hint: str
    explanation: str
    category: str
    level: str

    def __post_init__(self):
        if not self.question.strip() or len(self.choices) != 4:
            raise ValueError('문제와 4개 선택지가 필요합니다.')
        if any(not str(choice).strip() for choice in self.choices):
            raise ValueError('선택지는 비어 있을 수 없습니다.')
        if self.answer not in (1, 2, 3, 4):
            raise ValueError('정답은 1~4여야 합니다.')

    def to_dict(self):
        return vars(self).copy()

    @classmethod
    def from_dict(cls, data):
        return cls(**{key: data[key] for key in cls.__dataclass_fields__})

    def score(self, user_answer, used_hint):
        if user_answer is None:
            return 0
        if user_answer == self.answer:
            return 7 if used_hint else 10
        return 0
