import util

class UCSSearchProblem:
    """
    This class outlines the structure of a UCS search problem
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def search(problem: SearchProblem, algorithm: str, heuristic=nullHeuristic):
    if algorithm in ['BFS', 'DFS']:
        if algorithm == 'DFS':
            frontier = util.Stack()
        elif algorithm == 'BFS':
            frontier = util.Queue()
        initial_node = (problem.getStartState(), [])
        frontier.push(initial_node)
    elif algorithm in ['UCS', 'A*']:
        frontier = util.PriorityQueue()
        initial_node = (problem.getStartState(), [], 0)
        initial_priority = heuristic(problem.getStartState(), problem)
        if algorithm == 'A*':
            frontier.push(initial_node, initial_priority)
        elif algorithm == 'UCS':
            frontier.push(initial_node, 0)
    cost_so_far = {}
    explored = set()

    while not frontier.isEmpty():
        if algorithm in ['BFS', 'DFS']:
            current_state, path = frontier.pop()
            explored.add(current_state)
            if problem.isGoalState(current_state):
                return path
            successors = problem.getSuccessors(current_state)
            for successor_state, action, step_cost in successors:
                next_node = (successor_state, path + [action])

                if successor_state not in explored:
                    if algorithm in ['DFS']:
                        frontier.push(next_node)
                    elif algorithm in ['BFS']:
                        if successor_state not in [node[0] for node in frontier.list]:
                            frontier.push(next_node)
        elif algorithm in ['UCS', 'A*']:
            current_state, path, path_cost = frontier.pop()
            explored.add(current_state)
            if problem.isGoalState(current_state):
                return path
            successors = problem.getSuccessors(current_state)

            for successor_state, action, step_cost in successors:
                next_cost = path_cost + step_cost
                next_node = (successor_state, path + [action], next_cost)
                next_priority = next_cost + heuristic(successor_state, problem)
                if successor_state not in explored:
                    if algorithm == 'UCS':
                        if successor_state not in cost_so_far or next_cost < cost_so_far[successor_state]:
                            cost_so_far[successor_state] = next_cost
                            frontier.push(next_node, next_cost)
                    elif algorithm == 'A*':
                        if successor_state not in cost_so_far or next_priority < cost_so_far[successor_state]:
                            cost_so_far[successor_state] = next_priority
                            frontier.push(next_node, next_priority)
    return []


def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.
    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.
    """
    "*** YOUR CODE HERE ***"

    return search(problem=problem, algorithm="DFS")

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    return search(problem=problem, algorithm="BFS")

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    
    return search(problem=problem, algorithm="UCS")
    

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    return search(problem=problem, algorithm="A*", heuristic=heuristic)



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

