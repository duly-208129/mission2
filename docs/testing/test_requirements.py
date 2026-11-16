"""Mission edge cases; temporary storage never modifies the player's state."""
import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from main import default_quizzes
from quiz_game import QuizGame


class Requirements(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.game = QuizGame.__new__(QuizGame)
        self.game.defaults = default_quizzes()
        self.game.path = Path(self.temp.name) / 'state.json'
        self.game.quizzes = []
        self.game.best_score = 0
        self.game.history = []
        self.output = io.StringIO()
        self.capture = contextlib.redirect_stdout(self.output)
        self.capture.__enter__()
        self.addCleanup(self.capture.__exit__, None, None, None)

    def test_missing_and_corrupt_storage(self):
        self.game.load_state()
        self.assertEqual(len(self.game.quizzes), 6)
        for content in ('{broken', '[]', '{"quizzes":[null],"best_score":0}',
                        '{"quizzes":[],"best_score":true}',
                        '{"quizzes":[],"best_score":101}'):
            self.game.path.write_text(content, encoding='utf-8')
            self.game.load_state()
            self.assertEqual(len(self.game.quizzes), 6)
            self.assertEqual(self.game.best_score, 0)

    def test_invalid_question_types(self):
        row = default_quizzes()[0].to_dict()
        for key, value in (('question', None), ('choices', 'abcd'), ('answer', True)):
            data = {'quizzes': [dict(row, **{key: value})], 'best_score': 0}
            self.game.path.write_text(json.dumps(data), encoding='utf-8')
            self.game.load_state()
            self.assertEqual(len(self.game.quizzes), 6)

    def test_input_validation(self):
        with patch('builtins.input', side_effect=['', 'abc', '9', ' 1 ']):
            self.assertEqual(self.game.number('menu', 1, 7), 1)
        self.assertEqual(self.output.getvalue().count('사이의 숫자'), 3)

    def test_play_reprompts_and_hint_score_persists(self):
        self.game.quizzes = [default_quizzes()[0]]
        with patch('builtins.input', side_effect=['0', '0', '1', '', 'abc', '0', 'H', 'H', ' 2 ']):
            self.game.play()
        self.assertIn('빈 답', self.output.getvalue())
        self.assertEqual(self.game.best_score, 70)
        self.game.load_state()
        self.assertEqual(self.game.history[-1]['score'], 70)

    def test_safe_interrupt_and_eof(self):
        self.game.load_state()
        for error in (KeyboardInterrupt, EOFError):
            with patch('builtins.input', side_effect=error):
                self.game.run()
            self.assertIn('종료 요청', self.output.getvalue())
            self.assertTrue(self.game.path.exists())

    def test_empty_and_unplayed(self):
        self.game.play()
        self.game.show()
        self.game.show_score()
        self.assertIn('등록된 문제가 없습니다', self.output.getvalue())
        self.assertIn('아직 완료한 게임이 없습니다', self.output.getvalue())

    def test_write_failure(self):
        with patch.object(Path, 'write_text', side_effect=PermissionError('denied')):
            self.assertFalse(self.game.save_state())
        self.assertIn('저장 실패', self.output.getvalue())


if __name__ == '__main__':
    unittest.main(verbosity=2)
