# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first
    [2nd Edition: p 75, 3rd Edition: p 87]

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm
    [2nd Edition: Fig. 3.18, 3rd Edition: Fig 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    graph = util.Stack()
    root = (problem.getStartState(), [])
    graph.push(root)
    visited = set(root[1])
    while not graph.isEmpty():
        node = graph.pop()
     #   print "node is" , node
        direction = node[1]
        #print "direction is ", direction
        if problem.isGoalState(node[0]):
           # print "find the solution: "
            #print "the solution is ", direction
            return direction
        suss = problem.getSuccessors(node[0])
        for s in suss:
            if s[0] not in visited:
                visited.add(s[0])
                new_direction = direction + [s[1]]
                cur = (s[0], new_direction)
                graph.push(cur)
    print "failure, can't fine the path"
    return []


def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    [2nd Edition: p 73, 3rd Edition: p 82]
    """
    "*** YOUR CODE HERE ***"
    frontier = util.Queue()
    root = problem.getStartState(), []
    frontier.push(root)
    explored = set(root[1])
    while not frontier.isEmpty():
        node = frontier.pop()
        path = node[1]
       # print "the path is ", path
        if problem.isGoalState(node[0]):
            return path
        suss = problem.getSuccessors(node[0])
        for s in suss:
            if s[0] not in explored:
                explored.add(s[0])
                new_path = path + [s[1]]
                cur = s[0], new_path
                frontier.push(cur)
    print "failure, can't fine the path"
    return []



def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    frontier = util.PriorityQueue()
    root = problem.getStartState(), [], 0
    frontier.push(root, 0)
    visited = set()
    while not frontier.isEmpty():
        node = frontier.pop()
        visited.add(node[0])
        path = node[1]
        cost = node[2]
       # print "the path is ", path
        if problem.isGoalState(node[0]):
            return path
        suss = problem.getSuccessors(node[0])
        for s in suss:
            if s[0] not in visited:
                new_path = path + [s[1]]
                new_cost = cost + s[2]
                cur = s[0], new_path, new_cost
                frontier.push(cur, new_cost)
    print "failure, can't fine the path"
    return []


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"
    frontier = util.PriorityQueue()
    root = problem.getStartState(), [], 0
    frontier.push(root, 0)
    visited = set()
    while not frontier.isEmpty():
        node = frontier.pop()
        visited.add(node[0])
        path = node[1]
        cost = node[2]
       # print "the path is ", path
        if problem.isGoalState(node[0]):
            return path
        suss = problem.getSuccessors(node[0])
        for s in suss:
            if s[0] not in visited:
                new_path = path + [s[1]]
                new_cost = cost + s[2]
                h= heuristic(s[0], problem)
                cur = s[0], new_path, new_cost
                frontier.push(cur, new_cost + h)
                print new_cost + h
    print "failure, can't fine the path"
    return []



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
