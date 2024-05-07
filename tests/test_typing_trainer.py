import unittest
from unittest.mock import Mock, patch, mock_open
from speed import HeatmapGenerator, UserStats, TypingTrainer
from tkinter import Tk, Event

class TestHeatmapGenerator(unittest.TestCase):
    def test_update_error_data(self):
        hg = HeatmapGenerator()
        correct_word = "hello"
        user_input = "hallo"
        hg.update_error_data(correct_word, user_input)
        self.assertEqual(hg.error_data, {'e': 1})

    def test_generate_heatmap(self):
        hg = HeatmapGenerator()
        hg.error_data = {'e': 2, 'l': 1, 'o': 3}
        result = hg.generate_heatmap()
        expected = "Top 3 Keyboard Errors:\n" + "o: 3\n" + "e: 2\n" + "l: 1\n"
        self.assertEqual(result, expected)

class TestUserStats(unittest.TestCase):
    @patch('builtins.open', mock_open(read_data='{"sessions": []}'))
    @patch('json.dump')
    def test_save_stats(self, mock_json_dump):
        us = UserStats()
        us.user_data = {'sessions': [{'correct': 5, 'wrong': 3}]}
        us.save_stats()
        mock_json_dump.assert_called_once()

    @patch('builtins.open', mock_open(read_data='{"sessions": []}'))
    def test_load_stats_found(self):
        us = UserStats()
        self.assertEqual(us.user_data, {'sessions': []})

class TestTypingTrainer(unittest.TestCase):
    def setUp(self):
        self.root = Tk()
        self.app = TypingTrainer(self.root)

    @patch('speed.TypingTrainer.set_new_word')
    def test_play_game_correct_word(self, mock_set_new_word):
        self.app.word_list_Label.config(text="hello")
        self.app.wordEntry.insert(0, "hello")
        self.app.play_game(Mock(type='2'))
        self.assertEqual(self.app.correct_word, 1)

    @patch('speed.TypingTrainer.set_new_word')
    def test_play_game_wrong_word(self, mock_set_new_word):
        self.app.word_list_Label.config(text="hello")
        self.app.wordEntry.insert(0, "hallo")
        self.app.play_game(Mock(type='2'))
        self.assertEqual(self.app.wrong_word, 1)

    def tearDown(self):
        self.root.destroy()

if __name__ == '__main__':
    unittest.main()
