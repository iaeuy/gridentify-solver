import random
from .node import Node

class MaxNode(Node):
    MAX_CHILDREN = 10

    def __init__(self, game, depth, max_depth, node_id):
        super().__init__(game, depth, max_depth)
        self.node_id = node_id # type of node for children
        self.best_child = None

    def get_children(self):
        if self.children == None:
            children = []
            moves = self.game.moves()
            pruned = set(m for m in moves if not self.game.pruneable_move(m))
            if pruned:
                moves = pruned
            if len(moves) > self.MAX_CHILDREN:
                moves = random.sample(moves, self.MAX_CHILDREN)
            for m in moves:
                new_game = self.game.copy()
                if self.node_id == 0:
                    from .min_node import MinNode
                    children.append(MinNode(new_game, self.depth+1, self.max_depth, m))
                elif self.node_id == 1:
                    from .exp_node import ExpNode
                    children.append(ExpNode(new_game, self.depth+1, self.max_depth, m))
                else:
                    raise RuntimeError("Invalid node type.")
            self.children = children
        return self.children 

    def get_value(self):
        if self.depth >= self.max_depth or self.game.is_finished():
            self.value = self.game.evaluate()
        elif self.value == None:
            val = float("-inf")
            for child in self.get_children():
                if child.get_value() > val:
                    val = child.get_value()
                    self.best_child = child
            self.value = val
        return self.value