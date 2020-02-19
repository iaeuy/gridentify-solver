import fileinput
import statistics
from gridentify import Gridentify
from collections import Counter

def random_average(trials):
    score = 0
    for _ in range(trials):
        g = Gridentify()
        score += g.random_playout()
    return score/trials

def uniform_random_average(trials):
    score = 0
    for _ in range(trials):
        g = Gridentify()
        score += g.uniform_random_playout()
    return score/trials

def dumb_monte_average(trials, num_samples):
    score = 0
    for _ in range(trials):
        g = Gridentify()
        score += g.dumb_monte_playout(num_samples)
    return score/trials

def branching_factor_experiment():
    g = Gridentify()
    print(g)
    while not g.is_finished():
        print(len(g.moves()))
        g.make_random_move()
    print(g)

def branching_factor_experiment2(trials):
    """
    Average branching factor of random board (i.e. starting position).
    """
    # moves = 0
    # for _ in range(trials):
    #     moves += len(Gridentify().moves())
    # return moves/trials
    moves = []
    for _ in range(trials):
        moves.append(len(Gridentify().moves()))
    print("average: " + str(statistics.mean(moves)))
    print("stdev: " + str(statistics.stdev(moves)))
    print("min: " + str(min(moves)))
    print("max: " + str(max(moves)))

def main():
    g = Gridentify()
    print(g)
    print("legal moves: " + str(len(g.moves())))
    if g.is_finished():
        print("Game over!")
        return

    for coords in fileinput.input():
        coords = coords.rstrip()

        if coords == 'exit':
            print("Game over!")
            break
        elif coords == 'random':
            g.make_random_move()
        elif coords == 'monte':
            g.make_indices_move(g.dumb_monte_move(100))
        else:
            g.make_move(coords)

        print(g)
        print("legal moves: " + str(len(g.moves())))
        if g.is_finished():
            print("Game over!")
            break


if __name__ == '__main__':
    main()