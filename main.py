from gameplay import *


def main():
    game = Gameplay()
    # game.two_players_game()
    game.set_depth(3)
    game.game_with_ai("w")


if __name__ == "__main__":
    main()
