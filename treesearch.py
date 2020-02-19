from gridentify import Gridentify
from treesearch.max_node import MaxNode 

g = Gridentify()
print(g)
n = MaxNode(g, 0, 2, 0)
print(n)
print(n.get_children())

def evaluate(node, max_depth):
	if node.depth >= max_depth:
		node.value = node.game.evaluate()
	else:
		node.get_children()
	return node.get_value()

def minimax_move(g, max_depth):
	root = MaxNode(g, 0, max_depth, 0)
	root.get_value()
	print("children: " + str(len(root.get_children())))
	return list(root.best_child.move)

def minimax_playout(g, max_depth):
	while not g.is_finished():
		print(g)
		print("moves: " + str(len(g.moves())))
		m = minimax_move(g.copy(), max_depth)
		g.make_indices_move(m)
	return g.score

def expectimax_move(g, max_depth):
	root = MaxNode(g, 0, max_depth, 1)
	root.get_value()
	print("children: " + str(len(root.get_children())))
	return list(root.best_child.move)

def expectimax_playout(g, max_depth):
	while not g.is_finished():
		print(g)
		print("moves: " + str(len(g.moves())))
		m = expectimax_move(g.copy(), max_depth)
		g.make_indices_move(m)
	return g.score
