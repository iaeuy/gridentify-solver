class Node():
    def __init__(self, game, depth, max_depth):
        self.game = game
        self.depth = depth
        self.max_depth = max_depth
        self.children = None
        self.value = None

    def get_children(self):
        raise NotImplementedError

    def value(self):
        raise NotImplementedError()