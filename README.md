# gridentify-solver
Python implementation of Gridentify, and a simple solver.

`play.py` - run in Python console to start a game of Gridentify. Input moves as a list of coordinates, e.g. A1 A2 A3 to connect the first three tiles of the top row.

`gridentify.py` - contains the Gridentify class and several types of playouts. 
  - `random_playout`: generates random moves; not uniformly random
  - `uniform_random_playout`: selects moves uniformly at random. Can be expensive for boards with large connected components.
  - `minimax_playout`/`expectimax_playout`: minimax/expectimax tree search up to specificed depth evaluation function given by `Gridentify.evaluate`. Setting `max_children` takes a random sample of `max_children` nodes at each step to limit the branching factor.  
  - `flat_monte_playout`: uses flat Monte Carlo to select moves. `playout_type` specifies which of the above playout types is used during rollouts.
  
TO DO: better MCTS (SP-MCTS with determinization), frontend with Django, better documention   

