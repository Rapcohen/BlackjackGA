import random
from copy import deepcopy
from enum import Enum
from typing import List

from blackjack21 import Table
from blackjack21.deck import Card
from blackjack21.players import Player


class Action(Enum):
    HIT = 1
    STAND = 2
    DOUBLE_DOWN = 3

    # SPLIT = 4

    def __str__(self):
        return self.name[0]


class Result(Enum):
    PLAYER_BUST = -2
    PLAYER_LOSE = -1
    TIE = 0
    PLAYER_BLACKJACK = 1
    PLAYER_WIN = 2
    DEALER_BUST = 3


class Strategy:
    def __init__(self, hard_hands: List[List[Action]], soft_hands: List[List[Action]]):
        self.hard_hands = hard_hands
        self.soft_hands = soft_hands
        self.min_hard_hand = 4
        self.min_soft_hand_without_ace = 2
        self.min_dealer_hand = 2

    def get_action(self, dealer_card: Card, player: Player) -> Action:
        if self.is_soft(player.hand):
            action = self.get_soft_action(dealer_card, player.hand)
        else:
            action = self.get_hard_action(dealer_card, player)
        if action == Action.DOUBLE_DOWN and len(player.hand) > 2:
            action = Action.HIT
        return action

    def is_soft(self, hand: List[Card]):
        has_ace = any(card.rank == "A" for card in hand)
        return has_ace and sum([card._value for card in hand]) <= 20

    def get_hard_action(self, dealer_card: Card, player: Player) -> Action:
        return self.hard_hands[player.total - self.min_hard_hand][dealer_card._value - self.min_dealer_hand]

    def get_soft_action(self, dealer_card: Card, player_hand: List[Card]) -> Action:
        hand_value_without_ace = sum([card._value for card in player_hand if card.rank != "A"])
        return self.soft_hands[hand_value_without_ace - self.min_soft_hand_without_ace][
            dealer_card._value - self.min_dealer_hand]


def simulate_hands(n_hands: int, strategy):
    fixed_bet = 1
    cash = 0

    for hand in range(n_hands):
        table = Table((("AI", fixed_bet),))
        player = table.players[0]
        dealer_hand = table.dealer.hand[0]

        if player.total == 21:
            continue

        action = strategy.get_action(dealer_hand, player)
        if action == Action.DOUBLE_DOWN:
            player.play_double_down()

        while not (player.bust or player.stand):
            action = strategy.get_action(dealer_hand, player)
            if action == Action.HIT:
                player.play_hit()
            elif action == Action.STAND:
                player.play_stand()
            # elif action == Action.SPLIT and player.can_split:
            #     player.play_split()

        table.dealer.play_dealer()
        result = Result(player.result)
        if result in [Result.PLAYER_BLACKJACK, Result.PLAYER_WIN, Result.DEALER_BUST]:
            cash += player.bet
        elif result in [Result.PLAYER_BUST, Result.PLAYER_LOSE]:
            cash -= player.bet

    return cash


def random_action():
    return random.choice(list(Action))


if __name__ == "__main__":
    strategy = Strategy(
        [[random_action() for _ in range(10)] for _ in range(17)],
        [[random_action() for _ in range(10)] for _ in range(8)],
    )
    hard = deepcopy(strategy.hard_hands)
    hard.reverse()
    soft = deepcopy(strategy.soft_hands)
    soft.reverse()
    print("Hard Hands:")
    print(f"\t {['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'A']}")
    i = 20
    for row in hard:
        print(f'{i}\t {[str(item) for item in row]}')
        i -= 1
    print("Soft Hands:")
    for row in soft:
        print([str(item) for item in row])

    simulate_hands(3, strategy)
