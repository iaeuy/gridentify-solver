import itertools
from .node import Node

class ExpNode(Node):
    def __init__(self, game, depth, max_depth, move):
        super().__init__(game, depth, max_depth)
        self.move = move # move from max node; not yet executed in self.game

    def get_children(self):
        if self.children == None:
            children = []
            fill_num = len(self.move) - 1
            for fill_array in itertools.product(self.game.NUMBERS, repeat=fill_num):
                new_game = self.game.copy()
                new_game.make_indices_move(self.move, fill=list(fill_array))
                from .max_node import MaxNode
                children.append(MaxNode(new_game, self.depth+1, self.max_depth, 1))
            
            self.children = children
        return self.children

    def get_value(self):
        if self.depth >= self.max_depth:
            self.value = self.game.evaluate()
        elif self.value == None:
            val = sum([child.get_value() for child in self.get_children()])
            val /= 3**(len(self.move)-1)
            self.value = val
        return self.value