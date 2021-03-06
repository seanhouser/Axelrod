"""Tests APavlov strategies."""

import axelrod
from .test_player import TestPlayer

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestAPavlov2006(TestPlayer):
    name = "Adaptive Pavlov 2006"
    player = axelrod.APavlov2006

    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        self.first_play_test(C)
        self.responses_test([C], [C] * 6, [C] * 6,
                            attrs={"opponent_class": "Cooperative"})
        self.responses_test([D], [C, D, D, D, D, D], [D] * 6,
                            attrs={"opponent_class": "ALLD"})
        self.responses_test([C, C], [C, D, C, D, C, D], [D, C, D, C, D, C],
                            attrs={"opponent_class": "STFT"})
        self.responses_test([D], [C, D, D, C, D, D], [D, D, C, D, D, C],
                            attrs={"opponent_class": "PavlovD"})
        self.responses_test([C], [C, D, D, C, D, D, C], [D, D, C, D, D, C, D],
                            attrs={"opponent_class": "PavlovD"})
        self.responses_test([D], [C, D, D, C, D, D], [C, C, C, D, D, D],
                            attrs={"opponent_class": "Random"})
        self.responses_test([D], [C, D, D, D, C, C], [D, D, D, C, C, C],
                            attrs={"opponent_class": "Random"})

    def test_reset(self):
        player = self.player()
        opponent = axelrod.Cooperator()
        [player.play(opponent) for _ in range(10)]
        player.reset()
        self.assertEqual(player.opponent_class, None)


class TestAPavlov2011(TestPlayer):
    name = "Adaptive Pavlov 2011"
    player = axelrod.APavlov2011

    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        self.first_play_test(C)
        self.responses_test([C], [C] * 6, [C] * 6,
                            attrs={"opponent_class": "Cooperative"})
        self.responses_test([D], [C, D, D, D, D, D], [D] * 6,
                            attrs={"opponent_class": "ALLD"})
        self.responses_test([D], [C, C, D, D, D, D], [C] + [D] * 5,
                            attrs={"opponent_class": "ALLD"})
        self.responses_test([D], [C, C, C, D, D, D], [C, C] + [D] * 4,
                            attrs={"opponent_class": "ALLD"})
        self.responses_test([D], [C, C, D, D, C, D], [C, D, D, C, D, D],
                            attrs={"opponent_class": "ALLD"})

        self.responses_test([C], [C, C, D, D, D, C], [C, D, D, C, C, D],
                            attrs={"opponent_class": "STFT"})
        self.responses_test([C], [C, C, D, C, D, C], [C, D, C, D, C, D],
                            attrs={"opponent_class": "STFT"})
        self.responses_test([C], [C, D, D, D, C, C], [D, D, D, C, C, C],
                            attrs={"opponent_class": "STFT"})
        self.responses_test([C], [C, D, D, D, C, C], [D, D, D, C, C, C],
                            attrs={"opponent_class": "STFT"})

        # Specific case for STFT when responding with TFT
        opponent = axelrod.Player()
        player = axelrod.APavlov2006()
        player.history = [D] * 8
        opponent.history = [D] * 8
        player.opponent_class = "STFT"
        self.assertEqual(player.strategy(opponent), D)
        opponent.history.append(C)
        self.assertEqual(player.strategy(opponent), C)

        self.responses_test([D], [C, C, C, C, C, D], [C, C, C, C, D, D],
                            attrs={"opponent_class": "Random"})
        self.responses_test([D], [C, D, D, C, C, C], [D, D, C, C, C, C],
                            attrs={"opponent_class": "Random"})

    def test_reset(self):
        player = self.player()
        opponent = axelrod.Cooperator()
        [player.play(opponent) for _ in range(10)]
        player.reset()
        self.assertEqual(player.opponent_class, None)
