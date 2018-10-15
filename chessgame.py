from stockfish import *

sf = Stockfish('/usr/games/stockfish')



def make_move(move, game_moves):

    valid = False

    sf.set_position(game_moves)

    while not valid:
        if move=="q":
            print("Bye!")
            return "game over"

        if move == "r":
            print("reset game")
            return "game reset"

        if sf.is_move_correct(move):
            game_moves.append(move)

            return move, game_moves

        else:
            print("invalid move")
            continue


def sf_get_move(game_moves):

    sf.set_position(game_moves)

    sf_move = sf.get_best_move()

    game_moves.append(sf_move)
    sf.set_position(game_moves)

    return sf_move, game_moves



def main():


    game_moves = []
    sf.set_fen_position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    print("play a new move")
    old_move = ""

    while True:

        move = get_alexa_move()

        if move == old_move :
            continue

        move, game_moves = make_move(move, game_moves)
        old_move = move
        if move == "game_over":
            break

        if move == "game reset":
            game_moves = []
            sf.set_fen_position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
            print("play a new move")
            continue

        sf_move, game_moves = sf_get_move(game_moves)
        give_move_alexa(sf_move)


main()











