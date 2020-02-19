import random
import math
from collections import Counter
from treesearch.max_node import MaxNode 

class Gridentify():
    NUMBERS = [1, 2, 3]
    GRID_X = 5
    GRID_Y = 5

    def __init__(self, board = "random", score = 0, highlighted = None):
        if board == "random":
            self.board = [random.choices(self.NUMBERS, k=self.GRID_X) for y in range(self.GRID_Y)]  
        else:
            self.board = board

        self.score = score

        if not highlighted:
            self.highlighted = []
        else:
            self.highlighted = highlighted

    def evaluate(self): # TO DO
        # return self.score
        return 7*math.log2(len(self.moves()) + 1) + self.monotonicity()

    def result(self, move):
        return sum([self.board[y][x] for x,y in move])

    def pruneable_move(self, move):
        """
        Return True if move can be removed from consideration during tree search
        """
        if len(move) > 6:
            return True
        if len(self.moves()) > 10:
            if not self.good_number(self.result(move)):
                return True
            if not self.happy_move(move):
                return True
        return False

    def good_number(self, num):
        def is_pow2(num):
            return (num & (num-1) == 0) and num != 0

        if num in self.NUMBERS:
            return True
        # if num == 4:
        #     return True
        if num % 3 == 0 and is_pow2(num // 3):
            return True
        else:
            return False 

    def happy_move(self, move):
        """
        Return true if move creates number equal to an adjacent number 
        or if move ends on an edge of the board.
        """
        end_x, end_y = move[-1]
        if end_x == 0 or end_x == self.GRID_X - 1 or end_y == 0 or end_y == self.GRID_Y - 1:
            return True
        result = self.result(move)
        for x,y in self.adjacent_coords(end_x, end_y):
            if self.board[y][x] == result:
                return True
        return False

    def monotonicity(self):
        """
        Returns a more negative number for squares on the edge 
        not in increasing or decreasing order.

        e.g. 
        48 24 12 6 3
        is a monotic row but 
        3 12 6 24 1
        is not
        """
        score = 0
        for x in range(1, self.GRID_X-1):
            if self.board[0][x] not in self.NUMBERS: # top edge
                if self.board[0][x-1] < self.board[0][x] and self.board[0][x] > self.board[0][x+1]:
                    score += math.log2(self.board[0][x]**2/(self.board[0][x-1]*self.board[0][x+1]))
                if self.board[0][x-1] > self.board[0][x] and self.board[0][x] < self.board[0][x+1]:
                    score -= math.log2(self.board[0][x]**2/(self.board[0][x-1]*self.board[0][x+1]))

            if self.board[self.GRID_Y-1][x] not in self.NUMBERS: # bottom edge
                if self.board[self.GRID_Y-1][x-1] < self.board[self.GRID_Y-1][x] and self.board[self.GRID_Y-1][x] > self.board[self.GRID_Y-1][x+1]:
                    score += math.log2(self.board[self.GRID_Y-1][x]**2/(self.board[self.GRID_Y-1][x-1]*self.board[self.GRID_Y-1][x+1]))
                if self.board[self.GRID_Y-1][x-1] > self.board[self.GRID_Y-1][x] and self.board[self.GRID_Y-1][x] < self.board[self.GRID_Y-1][x+1]:
                    score -= math.log2(self.board[self.GRID_Y-1][x]**2/(self.board[self.GRID_Y-1][x-1]*self.board[self.GRID_Y-1][x+1]))
        
        for y in range(1, self.GRID_Y-1):
            if self.board[y][0] not in self.NUMBERS: # left edge
                if self.board[y-1][0] < self.board[y][0] and self.board[y][0] > self.board[y+1][0]:
                    score += math.log2(self.board[y][0]**2/(self.board[y-1][0]*self.board[y+1][0]))
                if self.board[y-1][0] > self.board[y][0] and self.board[y][0] < self.board[y+1][0]:
                    score -= math.log2(self.board[y][0]**2/(self.board[y-1][0]*self.board[y+1][0]))

            if self.board[y][self.GRID_X-1] not in self.NUMBERS: # right edge
                if self.board[y-1][self.GRID_X-1] < self.board[y][self.GRID_X-1] and self.board[y][self.GRID_X-1] > self.board[y+1][self.GRID_X-1]:
                    score += math.log2(self.board[y][self.GRID_X-1]**2/(self.board[y-1][self.GRID_X-1]*self.board[y+1][self.GRID_X-1]))
                if self.board[y-1][self.GRID_X-1] > self.board[y][self.GRID_X-1] and self.board[y][self.GRID_X-1] < self.board[y+1][self.GRID_X-1]:
                    score -= math.log2(self.board[y][self.GRID_X-1]**2/(self.board[y-1][self.GRID_X-1]*self.board[y+1][self.GRID_X-1]))

        return -score

    def make_move(self, coords, fill = "random"):
        self.highlight_coords(coords)
        self.connect(fill)

    def make_indices_move(self, indices, fill = "random"):
        self.highlight_indices(indices)
        self.connect(fill)      

    def make_random_move(self):
        indices = self.random_move()
        self.make_indices_move(indices)

    def connect(self, fill = "random"):
        if not self.valid_connection():
            print("Invalid connection")
            self.highlighted = []
            return
        result = sum([self.board[y][x] for x,y in self.highlighted])
        end_x, end_y = self.highlighted.pop()
        self.board[end_y][end_x] = result
        self.score += result
        while self.highlighted:
            curr_x, curr_y = self.highlighted.pop()
            if fill == "random":
                self.board[curr_y][curr_x] = random.choice(self.NUMBERS)
            else:
                self.board[curr_y][curr_x] = fill.pop()

    def valid_connection(self, verbose=False):
        if len(self.highlighted) <= 1:
            if verbose:
                print("Must connect at least 2 squares")
            return False

        for i in range(len(self.highlighted) - 1):
            curr_x, curr_y = self.highlighted[i]
            next_x, next_y = self.highlighted[i+1]

            if not self.valid_coords(curr_y, curr_x) or not self.valid_coords(next_y, next_x):
                if verbose:
                    print("Coordinate out of bounds")
                return False

            if abs(curr_x - next_x,) + abs(curr_y - next_y) != 1:
                if verbose:
                    print("Must connect adjacent squares")
                return False
                
            curr_val = self.board[curr_y][curr_x]
            next_val = self.board[next_y][next_x]
            if curr_val != next_val:
                if verbose:
                    print("Must connect equal values")
                return False

        return True

    def highlight_coords(self, coords):
        """
        >>> g = Gridentify()
        >>> g.highlighted
        []
        >>> g.highlight_coords("A1 A2 B2")
        >>> g.highlighted
        [(0, 0), (0, 1), (1,1)]
        """
        if self.highlighted:
            raise RuntimeError("Attempted to highlight when squares already highlighted")

        coords = coords.split(' ')
        self.highlighted += list(map(self.coords_to_indices, coords))

    def highlight_indices(self, indices):
        if self.highlighted:
            raise RuntimeError("Attempted to highlight when squares already highlighted")

        self.highlighted += indices

    def is_finished(self):
        for x in range(self.GRID_X):
            for y in range(self.GRID_Y):
                if y < self.GRID_Y - 1 and self.board[y][x] == self.board[y+1][x]:
                    return False
                if x < self.GRID_X - 1 and self.board[y][x] == self.board[y][x+1]:
                    return False
        return True

    def random_move(self):
        # pick starting point
        comp_sizes = self.component_sizes()
        starting_points = []
        for y in range(len(comp_sizes)):
            for x in range(len(comp_sizes[0])):
                if comp_sizes[y][x] > 1:
                    starting_points.append((x, y))
        
        start_x, start_y = random.choice(starting_points)
        comp = self.component(start_x, start_y)
        highlighted = [(start_x, start_y)]

        self.random_highlight_next(highlighted, comp)
        while len(highlighted) < len(comp) and random.random() > 1/len(comp):
        # while len(highlighted) < len(comp) and random.random() > 1/2:
            curr_len = len(highlighted)
            self.random_highlight_next(highlighted, comp)
            if curr_len == len(highlighted):
                break
        return highlighted

    def random_highlight_next(self, highlighted, comp):
        curr_x, curr_y = highlighted[-1]
        curr_number = self.board[curr_y][curr_x]
        possible_coords = list(set(self.adjacent_coords(curr_x, curr_y)) & set(comp) - set(highlighted))
        # possible_coords = [(x,y) for (x,y) in comp if abs(curr_x - x) + abs(curr_y - y) == 1 and (x,y) not in highlighted]
        if possible_coords:
            highlighted.append(random.choice(possible_coords))

    def random_playout(self):
        while not self.is_finished():
            self.make_random_move()
        return self.score

    def uniform_random_move(self, pruned=False):
        moves = self.moves()
        if pruned:
            pruned_moves = set(m for m in moves if not self.pruneable_move(m))
            if pruned_moves:
                moves = pruned_moves
        return random.sample(moves, 1)[0]

    def uniform_random_playout(self, pruned=False):
        while not self.is_finished():
            m = self.uniform_random_move(pruned)
            self.make_indices_move(m)
        return self.score

    def minimax_move(self, max_depth):
        root = MaxNode(self.copy(), 0, max_depth, 0)
        root.get_value()
        # print("children: " + str(len(root.get_children())))
        return list(root.best_child.move)

    def minimax_playout(self, max_depth):
        while not self.is_finished():
            # print(self)
            # print("moves: " + str(len(self.moves())))
            m = self.minimax_move(max_depth)
            self.make_indices_move(m)
        return self.score

    def expectimax_move(self, max_depth):
        root = MaxNode(self.copy(), 0, max_depth, 1)
        root.get_value()
        # print("children: " + str(len(root.get_children())))
        return list(root.best_child.move)

    def expectimax_playout(self, max_depth):
        while not self.is_finished():
            # print(self)
            # print("moves: " + str(len(self.moves())))
            m = self.expectimax_move(max_depth)
            self.make_indices_move(m)
        return self.score

    def dumb_monte_move(self, num_samples, pruned, playout_type):
        move_scores = Counter()
        move_counts = Counter()
        moves = self.moves()
        for i in range(num_samples):
            if pruned:
                m = tuple(self.uniform_random_move(True))
            else:
                m = tuple(self.random_move())

            branch = self.copy()
            branch.highlight_indices(m)
            branch.connect()

            if playout_type == 0:
                move_scores[m] += branch.random_playout()
            elif playout_type == 1:
                move_scores[m] += branch.uniform_random_playout(pruned)
            elif playout_type == 2:
                move_scores[m] += branch.minimax_playout(2)
            elif playout_type == 3:
                move_scores[m] += branch.expectimax_playout(2)
            else:
                raise RuntimeError("Invalid playout type")
            move_counts[m] += 1

        best_move = max(move_scores, key=lambda m: move_scores[m]/move_counts[m])
        return best_move

    def dumb_monte_playout(self, num_samples, pruned, playout_type):
        while not self.is_finished():
            m = self.dumb_monte_move(num_samples, pruned, playout_type)
            self.make_indices_move(m)
        return self.score

    def components(self):
        """
        List of all components.
        """
        comps = []
        done = set()
        for y in range(len(self.board)):
            for x in range(len(self.board[0])):
                if (x,y) not in done:
                    comp = self.component(x,y)
                    for curr_x, curr_y in comp:
                        done.add((curr_x, curr_y))
                    comps.append(comp)

        return comps

    def component_sizes(self):
        """
        Board mapping each square to the size of the component
        of that square.
        """
        comp_sizes = [list(row) for row in self.board]
        done = set()

        for y in range(len(comp_sizes)):
            for x in range(len(comp_sizes[0])):
                if (x,y) not in done:
                    comp = self.component(x,y)
                    for curr_x, curr_y in comp:
                        done.add((curr_x, curr_y))
                        comp_sizes[curr_y][curr_x] = len(comp)

        return comp_sizes

    def component(self, x, y):
        """
        Set of coordinates (as (x,y) coords) in connected component
        of square (x,y)
        """
        val = self.board[y][x]
        visited = set()
        stack = [(x,y)]

        while stack:
            curr_x, curr_y = stack.pop()

            if (curr_x, curr_y) in visited:
                continue
            if not self.valid_coords(curr_x, curr_y):
                continue
            if self.board[curr_y][curr_x] != val:
                continue

            visited.add((curr_x, curr_y))
            stack += self.adjacent_coords(curr_x, curr_y)

        return visited

    def comp_moves(self, comp):
        """
        Set of moves within a given connected component
        """
        # dynamic programming: create paths by ascending length
        paths = [set((c,) for c in comp)]
        while len(paths) < len(comp):
            prev_paths = paths[-1]
            new_paths = set()
            for p in prev_paths:
                end_x, end_y = p[-1]
                adjacent = [(end_x-1, end_y), (end_x+1, end_y), (end_x, end_y-1), (end_x, end_y+1)]
                for x,y in adjacent:
                    if self.valid_coords(x,y) and (x,y) in comp and (x,y) not in p:
                        new_p = p + ((x,y),)
                        new_paths.add(new_p)
            if not new_paths:
                break
            paths.append(new_paths)
       
        all_paths = set()
        for i in range(1, len(paths)):
            all_paths = all_paths | paths[i]

        return all_paths

    def moves(self):
        """
        Set of all moves.
        """
        comps = self.components()
        paths = set()
        for c in comps:
            paths = paths | self.comp_moves(c)
        return paths

    def copy(self):
        board_copy = [list(row) for row in self.board]
        return Gridentify(board_copy, self.score, list(self.highlighted))

    def board_with_coords(self, board):
        with_coords = [['#'] + ['X:' + chr(i+65) for i in range(self.GRID_X)]]
        with_coords += [['Y:' + str(i+1)] + board[i] for i in range(self.GRID_Y)]

        s = [[str(e) for e in row] for row in with_coords] # from https://stackoverflow.com/questions/13214809/pretty-print-2d-python-list
        lens = [max(map(len, col)) for col in zip(*s)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in s]
        return '\n'.join(table)

    def __str__(self):
        return self.board_with_coords(self.board) + '\n' + "score: " + str(self.score)

    def valid_coords(self, x, y):
        return x >= 0 and y >= 0 and x < self.GRID_X and y < self.GRID_Y

    def adjacent_coords(self, x, y):
        adj = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        return [coord for coord in adj if self.valid_coords(*coord)]

    def coords_to_indices(self, coord):
        """
        >>> cords_to_indices('A1')
        0, 0
        >>> coords_to_indices('B3')
        1, 2
        """
        x_coord, y_coord = coord
        x = ord(x_coord) - 65
        y = int(y_coord) - 1
        return x, y

    def indices_to_coords(self, x, y):
        return chr(x+65) + str(y+1)