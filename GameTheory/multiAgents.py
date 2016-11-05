# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
import math
from game import Actions
class ReflexAgent(Agent):
  """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
  """


  def getAction(self, gameState):
    """
    You do not need to change this method, but you're welcome to.

    getAction chooses among the best options according to the evaluation function.

    Just like in the previous project, getAction takes a GameState and returns
    some Directions.X for some X in the set {North, South, West, East, Stop}
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best

    "Add more of your code here if you want to"

    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
    """
    Design a better evaluation function here.

    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (newFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    newFood = successorGameState.getFood()
    walls = successorGameState.getWalls()
    newMoves = len(successorGameState.getLegalActions())
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    foodList =  newFood.asList()
    Ghost =  newGhostStates[0].getPosition()
    GhostAction = newGhostStates[0].getDirection()
    food = []
    for i in range(0, len(foodList)):
        px , py = newPos[0], newPos[1]
        dist = abs(foodList[i][0] - newPos[0]) + abs(foodList[i][1] - newPos[1])
        down_left = 0
        up_right = 0
        for dy in range(min(py, foodList[i][1]), max(py, foodList[i][1])):
          if walls[px][dy]:
           down_left += 3.5
          if walls[foodList[i][0]][dy]:
            up_right += 3.2
        for dx in range(min(px, foodList[i][0]), max(py, foodList[i][0])):
          if walls[dx][py]:
            down_left += 3.1
          if walls[dx][foodList[i][1]]:
            up_right += 3.4
        food.append(dist+ 1.18*min(up_right,down_left))
    foodDist = 0
    far = 0
    if (len(food)):
      foodDist = min(food)

    ghostDist = []
    for ghost in newGhostStates:
      GhostPosition = ghost.getPosition()
      GhostAction = ghost.getDirection()
      x, y = GhostPosition
      #dx, dy = Actions.directionToVector(action)
      #nextx, nexty = int(x + dx), int(y + dy)
      ghostDist.append(abs(newPos[0] - x) + abs(newPos[1] - y))

    if newScaredTimes[0] > 0:
      return  -min(ghostDist) - 0.7*newFood.count()
    if min(ghostDist) > 2:
      val = -15.87*foodDist - 199.7*newFood.count() + 1.59*min(ghostDist) + 0.58*newMoves
      return val
    #print ghostDist
    return  1.14*min(ghostDist)-0.078*foodDist - 1.81*newFood.count()

def scoreEvaluationFunction(currentGameState):
  """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
  """
  return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
  """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
  """

  def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
    self.index = 0 # Pacman is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (question 2)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    "*** YOUR CODE HERE ***"
    legalMoves = gameState.getLegalActions(0)
    if Directions.STOP in legalMoves:
        legalMoves.remove(Directions.STOP)
    scores = [self.min_value(gameState.generateSuccessor(0, action), self.depth, 1) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices)
    return legalMoves[chosenIndex]

  def max_value (self, gameState, depth):
      if (gameState.isLose()):
        #print "you will lose the game"
        return -999 + self.evaluationFunction(gameState)
      if (gameState.isWin()):
        #print "you will win the game"
        return 999 + self.evaluationFunction(gameState)
      legalMoves = gameState.getLegalActions(0)
      legalMoves.remove(Directions.STOP)
      best = -9999999
      for action in legalMoves:
        score = self.min_value(gameState.generateSuccessor(0, action), depth, 1)
        if score > best:
            best = score
      return best

  def min_value (self, gameState, depth, agentIndex):
      if (gameState.isLose()):
        #print "you will lose the game"
        return -999 + self.evaluationFunction(gameState)
      if (gameState.isWin()):
        #print "you will win the game"
        return 999 + self.evaluationFunction(gameState)
      agentNum = gameState.getNumAgents()
      worst = 99999
      if depth == 1:
        actions = gameState.getLegalActions(agentIndex)
        if (agentIndex == agentNum - 1):
            for action in actions:
                score = self.evaluationFunction(gameState.generateSuccessor(agentIndex, action))
                if score < worst:
                  worst = score
        else:
            for action in actions:
                score = self.min_value(gameState.generateSuccessor(agentIndex, action), depth, agentIndex+1)
                if score < worst:
                  worst = score
        return worst
      else:
          actions = gameState.getLegalActions(agentIndex)
          if (agentIndex == agentNum - 1):
              for action in actions:
                score = self.max_value(gameState.generateSuccessor(agentIndex, action), depth - 1)
                if score < worst:
                    worst = score
          else:
              for action in actions:
                  score = self.min_value(gameState.generateSuccessor(agentIndex, action), depth, agentIndex + 1)
                  if score < worst:
                    worst = score
      return worst

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    legalMoves = gameState.getLegalActions(0)
    if Directions.STOP in legalMoves:
      legalMoves.remove(Directions.STOP)
    scores = [self.min_value(gameState.generateSuccessor(0, action), self.depth, 1, -99999, 99999) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices)
    return legalMoves[chosenIndex]

  def max_value(self, gameState, depth, alpha, beta):
    if (gameState.isLose()):
      # print "you will lose the game"
      return -999 + self.evaluationFunction(gameState)
    if (gameState.isWin()):
      # print "you will win the game"
      return 999 + self.evaluationFunction(gameState)
    legalMoves = gameState.getLegalActions(0)
    legalMoves.remove(Directions.STOP)
    best = -99999
    for action in legalMoves:
      score = self.min_value(gameState.generateSuccessor(0, action), depth, 1, alpha, beta)
      if score >= beta:
        return score
      alpha = max(score, alpha)
      if score > best:
        best = score
    return best

  def min_value(self, gameState, depth, agentIndex, alpha, beta):
    if (gameState.isLose()):
      # print "you will lose the game"
      return -999 + self.evaluationFunction(gameState)
    if (gameState.isWin()):
      # print "you will win the game"
      return 999 + self.evaluationFunction(gameState)
    agentNum = gameState.getNumAgents()
    worst = 99999
    if depth == 1:
      actions = gameState.getLegalActions(agentIndex)
      if (agentIndex == agentNum - 1):
        for action in actions:
          score = self.evaluationFunction(gameState.generateSuccessor(agentIndex, action))
          if score <= alpha:
            return score
          beta = min(beta, score)
          if score < worst:
            worst = score
      else:
        for action in actions:
          score = self.min_value(gameState.generateSuccessor(agentIndex, action), depth, agentIndex + 1, alpha, beta)
          if score <= alpha:
            return score
          beta = min(beta, score)
          if score < worst:
            worst = score
      return worst
    else:
      actions = gameState.getLegalActions(agentIndex)
      if (agentIndex == agentNum - 1):
        for action in actions:
          score = self.max_value(gameState.generateSuccessor(agentIndex, action), depth - 1, alpha, beta)
          if score <= alpha:
            return score
          beta = min(beta, score)
          if score < worst:
            worst = score
      else:
        for action in actions:
          score = self.min_value(gameState.generateSuccessor(agentIndex, action), depth, agentIndex + 1, alpha, beta)
          if score <= alpha:
            return score
          beta = min(beta, score)
          if score < worst:
            worst = score
    return worst

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (question 4)
  """

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
    legalMoves = gameState.getLegalActions(0)
    if Directions.STOP in legalMoves:
        legalMoves.remove(Directions.STOP)
    scores = [self.exp_value(gameState.generateSuccessor(0, action), self.depth, 1) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices)
    return legalMoves[chosenIndex]

  def max_value(self, gameState, depth):
      if (gameState.isLose()):
          # print "you will lose the game"
          return -999 + self.evaluationFunction(gameState)
      if (gameState.isWin()):
          # print "you will win the game"
          return 999 + self.evaluationFunction(gameState)
      legalMoves = gameState.getLegalActions(0)
      legalMoves.remove(Directions.STOP)
      best = -9999999
      for action in legalMoves:
          score = self.exp_value(gameState.generateSuccessor(0, action), depth, 1)
          if score > best:
              best = score
      return best

  def exp_value(self, gameState, depth, agentIndex):
      if (gameState.isLose()):
          # print "you will lose the game"
          return -999 + self.evaluationFunction(gameState)
      if (gameState.isWin()):
          # print "you will win the game"
          return 999 + self.evaluationFunction(gameState)
      agentNum = gameState.getNumAgents()
      score = 0
      if depth == 1:
          actions = gameState.getLegalActions(agentIndex)
          if (agentIndex == agentNum - 1):
              for action in actions:
                  score += self.evaluationFunction(gameState.generateSuccessor(agentIndex, action))
          else:
              for action in actions:
                  score += self.exp_value(gameState.generateSuccessor(agentIndex, action), depth, agentIndex + 1)
      else:
          actions = gameState.getLegalActions(agentIndex)
          if (agentIndex == agentNum - 1):
              for action in actions:
                  score += self.max_value(gameState.generateSuccessor(agentIndex, action), depth - 1)
          else:
              for action in actions:
                  score += self.exp_value(gameState.generateSuccessor(agentIndex, action), depth, agentIndex + 1)
      return score/len(actions)

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
  """
  "*** YOUR CODE HERE ***"
  newPos = currentGameState.getPacmanPosition()
  newFood = currentGameState.getFood()
  walls = currentGameState.getWalls()
  newMoves = len(currentGameState.getLegalActions()) - len(Directions.STOP)
  newGhostStates = currentGameState.getGhostStates()
  newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
  score = currentGameState.getScore()

  foodList = newFood.asList()
  Ghost = newGhostStates[0].getPosition()
  GhostAction = newGhostStates[0].getDirection()
  food = []
  for i in range(0, len(foodList)):
      px, py = newPos[0], newPos[1]
      dist = abs(foodList[i][0] - newPos[0]) + abs(foodList[i][1] - newPos[1])
      down_left = 0
      up_right = 0
      for dy in range(min(py, foodList[i][1]), max(py, foodList[i][1])):
          if walls[px][dy]:
              down_left += 3.5
          if walls[foodList[i][0]][dy]:
              up_right += 3.2
      for dx in range(min(px, foodList[i][0]), max(py, foodList[i][0])):
          if walls[dx][py]:
              down_left += 3.1
          if walls[dx][foodList[i][1]]:
              up_right += 3.4
      food.append(dist + 1.18 * min(up_right, down_left))
  foodDist = 0
  far = 0
  if (len(food)):
      foodDist = min(food)

  ghostDist = []
  for ghost in newGhostStates:
      GhostPosition = ghost.getPosition()
      GhostAction = ghost.getDirection()
      x, y = GhostPosition
      # dx, dy = Actions.directionToVector(action)
      # nextx, nexty = int(x + dx), int(y + dy)
      ghostDist.append(abs(newPos[0] - x) + abs(newPos[1] - y))

  if newScaredTimes[0] > 0:
      return -min(ghostDist) - 0.7 * newFood.count() + 1.1*score
  if min(ghostDist) > 2:
      val = -25.87 * foodDist - 10.78*newFood.count() + 5.59 * min(ghostDist) +  1.1*score + 9.1*newMoves
      return val
  # print ghostDist
  return 20.14 * min(ghostDist) - 0.078 * foodDist - 1.81 * newFood.count() + score + 7*newMoves

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

