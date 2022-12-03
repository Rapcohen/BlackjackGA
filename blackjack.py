from enum import Enum
from typing import List

from blackjack21 import Table
from blackjack21.deck import Card
from blackjack21.players import Player


class Action(Enum):
    HIT = 1
    STAND = 2
    DOUBLE_DOWN = 3

    def __str__(self):
        return self.name[0]


class Result(Enum):
    PLAYER_BUST = -2
    PLAYER_LOSE = -1
    TIE = 0
    PLAYER_BLACKJACK = 1
    PLAYER_WIN = 2
    DEALER_BUST = 3

    def __str__(self):
        return self.name


class Strategy:
    hard_hands_dim = (17, 10)
    soft_hands_dim = (8, 10)
    min_hard_hand = 4  # cards 2 & 2
    min_soft_hand = 2  # cards A & 2
    min_dealer_card = 2

    def __init__(self, hard_hands: List[List[Action]], soft_hands: List[List[Action]]):
        self.hard_hands = hard_hands
        self.soft_hands = soft_hands

    def get_action(self, dealer_card: Card, player: Player) -> Action:
        if self.is_soft(player.hand):
            hand_value_without_ace = sum([card._value for card in player.hand if card.rank != "A"])
            action = self.soft_hands[hand_value_without_ace - self.min_soft_hand][
                dealer_card._value - self.min_dealer_card]
        else:
            action = self.hard_hands[player.total - self.min_hard_hand][dealer_card._value - self.min_dealer_card]
        if action == Action.DOUBLE_DOWN and not player.can_double_down:
            return Action.HIT
        return action

    def get_hard_action(self, dealer_card: Card, player: Player) -> Action:
        return self.hard_hands[player.total - self.min_hard_hand][dealer_card._value - self.min_dealer_card]

    def get_soft_action(self, dealer_card: Card, player: Player) -> Action:
        hand_value_without_ace = sum([card._value for card in player.hand if card.rank != "A"])
        return self.soft_hands[hand_value_without_ace - self.min_soft_hand][dealer_card._value - self.min_dealer_card]

    @staticmethod
    def is_soft(hand: List[Card]):
        return any(card.rank == "A" for card in hand) and sum([card._value for card in hand]) < 21


def play_hand(strategy: Strategy) -> int:
    cash = 0

    ai_player = ("", 1)
    table = Table((ai_player, ai_player, ai_player, ai_player, ai_player))
    valid_players = [player for player in table.players if player.total != 21]
    dealer_card = table.dealer.hand[0]
    for player in valid_players:
        while not (player.bust or player.stand):
            action = strategy.get_action(dealer_card, player)
            if action == Action.STAND:
                player.play_stand()
            elif action == Action.HIT:
                player.play_hit()
            elif action == Action.DOUBLE_DOWN:
                player.play_double_down()

    table.dealer.play_dealer()
    for player in valid_players:
        result = Result(player.result)
        if result in [Result.PLAYER_BLACKJACK, Result.PLAYER_WIN, Result.DEALER_BUST]:
            cash += player.bet
        elif result in [Result.PLAYER_BUST, Result.PLAYER_LOSE]:
            cash -= player.bet
        # else it's a tie and cash is split with the dealer

    return cash


def simulate_hands(n_hands: int, strategy: Strategy) -> int:
    return sum([play_hand(strategy) for _ in range(n_hands // 5)])
