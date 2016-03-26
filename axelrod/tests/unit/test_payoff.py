import unittest
from axelrod import Game, Actions
import axelrod.payoff as ap


C, D = Actions.C, Actions.D

class TestPayoff(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.players = ('Alternator', 'TitForTat', 'Random')

        cls.interactions = {
            (0, 0): [(C, C), (D, D), (C, C), (D, D), (C, C)],
            (0, 1): [(C, C), (D, C), (C, D), (D, C), (C, D)],
            (0, 2): [(C, C), (D, C), (C, D), (D, C), (C, D)],
            (1, 1): [(C, C), (C, C), (C, C), (C, C), (C, C)],
            (1, 2): [(C, D), (D, D), (D, C), (C, D), (D, C)],
            (2, 2): [(D, C), (D, D), (D, C), (D, D), (D, D)]

        }

        cls.expected_payoff_matrix = [
            [11, 13, 13],
            [13, 15, 11],
            [13, 11, 13]
        ]

        cls.expected_payoff = [
            [[11.0, 11.0], [13, 13], [15, 12]],
            [[13, 13], [15.0, 15.0], [14, 7]],
            [[10, 12], [14, 12], [8.0, 14.5]],
        ]

        cls.expected_scores = [
            [28, 25],
            [27, 20],
            [24, 24]
        ]

        cls.expected_normalised_scores = [
            [2.8, 2.5],
            [2.7, 2.0],
            [2.4, 2.4]
        ]

        cls.expected_ranking = [0, 2, 1]
        cls.expected_ranked_names = ['Alternator', 'Random', 'TitForTat']

        cls.expected_normalised_payoff = [
            [2.2, 2.6, 2.7],
            [2.6, 3.0, 2.1],
            [2.2, 2.6, 2.25]
        ]

        cls.expected_payoff_stddevs = [
            [0.0, 0.0, 0.3],
            [0.0, 0.0, 0.7],
            [0.2, 0.2, 0.65]
        ]

        cls.expected_wins = [[1, 0], [0, 0], [0, 1]]

        cls.diff_means = [
            [0.0,  0.0,  0.5],
            [0.0,  0.0, -0.5],
            [-0.5,  0.5,  0.0]
        ]

        cls.expected_score_diffs = [
            [0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
            [-1.0, 0.0, 0.0, 1.0, 0.0, 0.0]
        ]

    def test_player_count(self):
        nplayers = ap.player_count(self.interactions)
        self.assertEqual(nplayers, 3)
        nplayers = ap.player_count({'test': 'test'})
        self.assertEqual(nplayers, 1)

    def test_payoff_matrix(self):
        payoff_matrix = ap.payoff_matrix(self.interactions, Game())
        self.assertEqual(payoff_matrix, self.expected_payoff_matrix)

    def test_interaction_payoff(self):
        payoff = ap.interaction_payoff(self.interactions[(2, 2)], Game())
        self.assertEqual(payoff, (13, 3))

    def test_scores(self):
        scores = ap.scores(self.expected_payoff)
        self.assertEqual(scores, self.expected_scores)

    def test_normalised_scores(self):
        scores = ap.normalised_scores(self.expected_scores, 5)
        self.assertEqual(scores, self.expected_normalised_scores)

    def test_normalised_scores_diff_length(self):
        scores = [[8, 9, 34], [16, 15, 32], [13, 18, 20]]
        lengths = [[4, 5, 12], [6, 7, 14], [4, 6, 8]]
        expected_normalised_scores = [[1.0, 0.9, 1.4167],
                                      [1.3333, 1.0715, 1.1429],
                                      [1.625, 1.5, 1.25]]
        normalised_scores = ap.normalised_scores_diff_length(scores, lengths)

        # Check approximate equality of all elements
        for i, row in enumerate(normalised_scores):
            for j, col in enumerate(row):
                self.assertAlmostEqual(col, expected_normalised_scores[i][j],
                                       places=3)

    def test_normalised_payoff_diff_length(self):
        scores = [[[7, 7, 4], [8, 8, 23], [0, 1, 11]],
                  [[8, 8, 23], [18, 3, 6], [8, 7, 9]],
                  [[5, 6, 6], [8, 12, 14], [8, 12, 9]]]
        lengths = [[[3, 3, 2], [3, 3, 9], [1, 2, 3]],
                   [[3, 3, 9], [6, 1, 2], [3, 4, 5]],
                   [[1, 2, 3], [3, 4, 5], [3, 6, 3]]]
        expected_payoff_matrix = [[2.2223, 2.6296, 1.3889],
                                  [2.6296, 3.0, 2.0722],
                                  [3.3334, 2.8222, 2.5556]]
        expected_payoff_stddevs = [[0.1574, 0.0524, 1.6235],
                                   [0.0524, 0.0, 0.4208],
                                   [1.2472, 0.1370, 0.4157]]
        normalised_payoff, normalised_std = ap.normalised_payoff_diff_length(scores, lengths)

        # Check approximate equality of all elements
        for i, row in enumerate(normalised_payoff):
            for j, col in enumerate(row):
                self.assertAlmostEqual(col, expected_payoff_matrix[i][j],
                                       places=3)
                self.assertAlmostEqual(normalised_std[i][j], expected_payoff_stddevs[i][j],
                                       places=3)

    def test_ranking(self):
        ranking = ap.ranking(self.expected_scores)
        self.assertEqual(ranking, self.expected_ranking)

    def test_ranked_names(self):
        ranked_names = ap.ranked_names(
            self.players, self.expected_ranking,)
        self.assertEqual(ranked_names, self.expected_ranked_names)

    def test_payoff_diffs_means(self):
        #payoff_matrix = ap.payoff_matrix(self.interactions, Game(), 3, 5)
        diff_means = ap.payoff_diffs_means(self.expected_payoff, 5)
        self.assertEqual(diff_means, self.diff_means)

    def test_score_diffs(self):
        #payoff_matrix = ap.payoff_matrix(self.interactions, Game(), 3, 5)
        score_diffs = ap.score_diffs(self.expected_payoff, 5)
        self.assertEqual(score_diffs, self.expected_score_diffs)

    @staticmethod
    def round_matrix(matrix, precision):
        return [[round(x, precision) for x in row] for row in matrix]

    def test_normalised_payoff(self):
        averages, stddevs = ap.normalised_payoff(self.expected_payoff, 5)
        self.assertEqual(
            self.round_matrix(averages, 2), self.expected_normalised_payoff)
        self.assertEqual(
            self.round_matrix(stddevs, 2), self.expected_payoff_stddevs)

    def test_winning_player(self):
        test_players = (8, 4)
        test_payoffs = (34, 44)
        winner = ap.winning_player(test_players, test_payoffs)
        self.assertEqual(winner, 4)
        test_payoffs = (54, 44)
        winner = ap.winning_player(test_players, test_payoffs)
        self.assertEqual(winner, 8)
        test_payoffs = (34, 34)
        winner = ap.winning_player(test_players, test_payoffs)
        self.assertEqual(winner, None)

    def test_wins(self):
        wins = ap.wins(self.expected_payoff)
        self.assertEqual(wins, self.expected_wins)
