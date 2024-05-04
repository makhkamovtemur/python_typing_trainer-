import unittest
from speed import HeatmapGenerator, UserStats, TypingTrainer


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
    def test_load_stats_not_found(self):
        us = UserStats('nofile.json')
        self.assertEqual(us.user_data, {})

    def test_update_stats(self):
        us = UserStats()
        us.user_data = {'sessions': []}
        us.update_stats({'correct': 5, 'wrong': 3})
        self.assertEqual(us.user_data['sessions'], [{'correct': 5, 'wrong': 3}])



if __name__ == '__main__':
    unittest.main()
