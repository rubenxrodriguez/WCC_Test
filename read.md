[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/SKTA3WlS)
# CMSI 2130 - Homework 1
A*-y Night Awaits You

** Ivana Krajina **


As a Homework, this is an individual assignment. While you are free to discuss strategies in groups, there should be no sharing of code or detailed pseudocode. Remember, your submissions are run through similarity checking mechanisms--if you're tempted to copy, come talk to me instead!

Premise: Your trendy friend has just discovered that weird winter Olympic sport where they ski and then shoot at targets (*quick Googling*) oh it's called a Biathlon, how creative. Anyways, they want to turn that into a game that combines pathfinding and shooting, and enlist you for help at finding the optimal strategies for their mazes.

Your mission: implement A* graph search for the Maze Biathlon! Namely, finding the most efficient way to shoot all of the targets in a grid maze!

Basically, a way better version of your Classwork 2, but with the training wheels taken off!

In particular, we'll be working on Maze Pathfinder problems with:

Non-uniform cost: in which certain actions have a higher cost associated with them than others (the mud tiles from the lecture).

Multiple Sub-Goals: different ways to solve the problem, some of which may be better than others.

Possibly No Solutions: there may be well-formed problems that simply do not have a solution.

## Overview
MazeProblems in this scenario will be constructed from a list of strings (a 2D maze of characters) indicating the contents of each cell in the maze.

In particular, the following table describes what constitutes a valid / properly formatted maze in this modified version of our Pathfinder:

| Character | Definition                                                                                 | Cost of Movement Onto | A Valid Maze Has...                                                                                         |
|-----------|--------------------------------------------------------------------------------------------|-----------------------|------------------------------------------------------------------------------------------------------------|
| X         | An impassable wall -- movement cannot be made onto these tiles.                            | N/A                   | ...walls along the border, but possibly other walls inside of the maze as well.                             |
| @         | The initial state (where the agent starts the search)                                      | 1 (for stepping back-upon, not incurred at the start) | ...exactly 1 initial state.                                                                                  |
| .         | An open cell where the agent may move.                                                     | 1                     | ...no constraints on open spaces, except that they may not be found along the border.                       |
| M         | A "mud" tile into which an agent may move, but at a greater cost.                          | 3                     | ...no constraints on mud tiles, except that they may not be found along the border.                         |
| T         | Targets to shoot: the goal has been reached when ALL targets have been shot. Players may not move onto tiles containing Targets until they've been shot. | 1                     | There may be as few as ZERO targets in the maze (hey, the initial state IS the goal!), but otherwise no limit on the number of targets that may be present! A goal is only reached if all can be shot, but not all may be accessible! |

Each MazeState / location will include exactly 1 of the above categories, meaning that the initial state cannot also be a target cannot also be on a mud tile, etc. and *ALL* mazes provided as input will be validly formatted (so you need not check for validity).

In addition to the standard movement choices of ["U", "D", "L", "R"] to navigate to each Target, your agent will have the special action "S" to shoot, which has the following effects:

All targets that are in the player's line-of-sight in each of the four cardinal directions (North, South, East, and West) are destroyed, regardless of how far away they are (how do you shoot in all 4 directions at once? Practice.).

The catch: walls ("X") will block your shots, BUT your shots will penetrate targets, hitting any targets that may be behind another in the same direction.

Shooting has a cost of 2, and your agent will remain in-place in the maze while shooting.

Here is an example, valid maze configuration (more are found in the skeleton's unit tests):

  Maze elements are indexed starting at (0, 0) = (x, y) = (col, row) 
  [top left of maze]. E.g.,
  
```python
maze = [
   # 012345
    "XXXXXX", # 0
    "XT..TX", # 1
    "X..T.X", # 2
    "X....X", # 3
    "X@X..X", # 4
    "XXXXXX", # 5
]

Initial State:  (1, 4)
Target States: {(1, 1), (3, 2), (4, 1)}
Solution:      ["U", "U", "S", "U", "S"]
Total Cost:    7
```

Notes on the above:

When the player moves up twice to be at location \((1, 2)\), the next "S" action will destroy 2 Targets: \((1, 1), (3, 2)\), because they are in the same row and column as the player without any obstructing walls.

Note that the most efficient solution demands that your agent waits until it is in the position to destroy two targets at once, lest it have to use more (and thus, more costly) "S" actions like choosing to shoot first before moving.

## Important Notes:
In any maze for which there *IS* a solution, the agent MUST shoot ALL Targets.

If there are *MULTIPLE* solutions, your procedure should return any one of the *LOWEST* cost solutions, and can shoot targets in *ANY* order to solve it.

If a maze has *NO* solution, your procedure should be able to handle this and return None.

## Solution Skeleton
Start with the solution skeleton in-hand! In the following project, I've given you the outline for a Maze Pathfinder's supporting components, including a MazeProblem specification. The rest is up to you to implement the A* Pathfinding functionality to solve the given problem!

[GitHub Classroom Link](https://classroom.github.com/a/hEuuYwQ6)

In the provided solution skeleton, I have given you an outline for how to accomplish A* search through the following components:

**maze_problem.py** is used to specify the maze and will be used in your Pathfinder's pathfind method.

**pathfinder.py** implemented functionally, the pathfind method is the main work-horse for your assignment, which is parameterized by the given MazeProblem. This is the only file you may modify for your submission.

Note the provided SearchTreeNode class meant to aid you with your implementation -- this is a skeleton that you WILL amend to complete A*.

**pathfinder_tests.py** a set of sample unit tests to verify the correct functionality of your Pathfinder solution. NOTE: Now that you're working in the big-league of homeworks, the unit tests given are only a SAMPLE / SUBSET of those that will be used to grade your submission! Make sure you add to these if you wish to receive full correctness credit (or not if you're feeling lucky).

**constants.py** a set of problem constants that you shall not change (real basic stuff like what the possible movement directions are).

**mypy.ini**, **pytest.ini** configuration files for mypy, pytest respectively. Do not change these!

**.gitignore** a set of patterns for git to avoid committing. You may modify this file if your commit attempts to add any project files to the repo (e.g., VSCode .project files or pycache folders, which should not be submitted).

## Specifications
To successfully navigate the Pathfinding Biathlon as described in the previous section, we will be implementing A* graph search.

The Pathfinding game proceeds as follows:

1. The MazeProblem is formalized, including the maze layout, initial state, actions, transitions, (new!) cost function, and a goal test.
2. The Pathfinder agent is provided with the problem (i.e., knows where any targets + goals are).
3. The Pathfinder must find a sequence of actions {"U", "D", "L", "R", "S"} that takes it from the initial state to shooting all targets that minimizes total cost.

To facilitate the above, some changes have been made to your MazeProblem class compared to CW2. The interface of methods you'll find useful are given below:

```python
def __init__(self, maze: list[str]) -> None:
    """
    Constructs a new pathfinding problem (finding the locations of any
    relevant maze entities) from a maze specified as a list of string rows.
    
    Parameters:
        maze (list[str]):
            A list of string rows of a rectangular maze consisting of the
            following traits:
            - A border of walls ("X"), with possibly others in the maze
            - Exactly 1 player starting position ("@")
            - Some number [0-infinity] of targets to shoot ("T")
            - Some number [0-infinity] of mud tiles
    """

def get_initial_loc(self) -> tuple[int, int]:
    """
    Returns the player's starting position in the maze ("@").

    Returns:
        tuple[int, int]:
            The player's starting location in the maze: (col, row) = (x, y).
    """

def get_initial_targets(self) -> set[tuple[int, int]]:
    """
    Returns the (possibly empty) set of targets that the player must shoot to
    reach a goal state.
    
    [!] Note: this method ALWAYS returns the starting set of target locations;
    you must record-keep separately any *remaining* targets of those unshot
    during the course of search.
    
    Returns:
        set[tuple[int, int]]:
            A set of each target's location in the maze: (col, row) = (x, y).
    """

def get_transition_cost(self, action: str, player_loc: tuple[int, int]) -> int:
    """
    Returns the cost of the given transition, which would normally be parameterized
    by the current state, action, and next state, except that all costs in the
    current maze problem are a function of only the action and next state, and so only
    those are required.
    
    Parameters:
        action (str):
            The action being taken in the current transition.
        player_loc (tuple[int, int]):
            The next-state's location of the player in the maze, i.e., having already
            taken the given action.
    
    Returns:
        int:
            The cost associated with this transition, which will be:
                - 3 if moving ONTO a mud tile for the first time
                - 2 if shooting (whether or not you're shooting from a mud tile)
                - 1 otherwise
    """

def get_visible_targets_from_loc(self, player_loc: tuple[int, int], targets_left: set[tuple[int, int]]) -> set[tuple[int, int]]:
    """
    Returns the set of targets that would be hit by a player taking the shoot action from
    the given player_loc from amongst those targets remaining in the targets_left parameter.
    
    [!] Note: a target may only be shot if there are no walls between the player and the
    target in any of the 4 cardinal directions: Up, Down, Left, or Right (and in any number
    of tiles in those directions). Shots will also penetrate targets, possibly destroying
    multiple targets in the same direction.
    
    Parameters:
        player_loc (tuple[int, int]):
            The current location of the player / the location from which they are shooting.
        targets_left (set[tuple[int, int]]):
            A set of location tuples indicating the positions of remaining targets to shoot.
    
    Returns:
        set[tuple[int, int]]:
            The set of target locations that would be hit by taking the shoot action from the
            given player_loc.
    """

def get_transitions(self, player_loc: tuple[int, int], targets_left: set[tuple[int, int]]) -> dict:
    """
    Returns a dictionary describing all possible transitions that a player may take from their
    given position. 
    
    Parameters:
        player_loc (tuple[int, int]):
            The current location of the player / the location from which they are shooting.
        targets_left (set[tuple[int, int]]):
            A set of location tuples indicating the positions of remaining targets to shoot.
    
    Returns:
        dict:
            A dictionary whose keys are the possible actions from the given player_loc, with mapped
            values that describe the transition associated with that action, including:
                - next_loc (tuple[int, int]): the location of the player after taking that action
                - cost (int): the cost of this particular transition
                - targets_hit (set[tuple[int, int]]): the set of targets hit in this transition
    
    Example:
        For example, if only the actions "S" and "U" were possible from the current player_loc of (3,3),
        we might see an output of:
        {
            "S": {next_loc: (3,3), cost: 2, targets_hit: {(3, 1)}},
            "U": {next_loc: (3,2), cost: 1, targets_hit: {}},
        }
    """
# ...other methods that you won't need in your solution omitted here...
```

Using the methods of the MazeProblem class above, your task is to implement the pathfind method structured with the SearchTreeNode class that you will likewise amend.

```python
@dataclass
class SearchTreeNode:
    """
    SearchTreeNodes contain the following attributes to be used in generation of
    the Search tree:

    Attributes:
        player_loc (tuple[int, int]):
            The player's location in this node.
        action (str):
            The action taken to reach this node from its parent (or empty if the root).
        parent (Optional[SearchTreeNode]):
            The parent node from which this node was generated (or None if the root).
    """
    player_loc: tuple[int, int]
    action: str
    parent: Optional["SearchTreeNode"]
    # TODO: Add any other attributes and method overrides as necessary!
    
def pathfind(problem: "MazeProblem") -> Optional[list[str]]:
    """
    The main workhorse method of the package that performs A* graph search to find the optimal
    sequence of actions that takes the agent from its initial state and shoots all targets in
    the given MazeProblem's maze, or determines that the problem is unsolvable.

    Parameters:
        problem (MazeProblem):
            The MazeProblem object constructed on the maze that is to be solved or determined
            unsolvable by this method.

    Returns:
        Optional[list[str]]:
            A solution to the problem: a sequence of actions leading from the 
            initial state to the goal (a maze with all targets destroyed). If no such solution is
            possible, returns None.
    """
    # TODO: Implement A* Graph Search for the Pathfinding Biathlon!
    return None
```

All other classes are not to be modified!

Additionally, here's a good order of tasks to tackle:

1. Review your course notes and make sure you have a solid grasp on how A* Search is meant to operate, at least at a high-level. During this review, envision what attributes and data structures may be relevant in your solution, paying special attention to what is recorded in each SearchTreeNode.
2. Read through the documentation and the methods available to you in each class from the documentation above so you can envision how to proceed.
3. You should be able to use large portions of your CW2 Pathfinder to motivate the A* one, noting the important differences between BFS and A* in the hints below.
4. Remember that the skeleton's unit tests are only a subset of the final grading tests -- make sure to test your submission adequately!
5. Start early and ask questions! I'm here to help!

The rest is yours to figure out! Enjoy the puzzle!

## Hints
Note: Parts of your solution to Classwork 2 may be useful here (i.e., you can use it as a starting point, including any solution code if you so please), but there will be substantial differences between it and this assignment, chiefly:

- The addition of subgoals (the targets), optimization for non-uniform cost (the mud tiles), and optimization of possible solutions (multiple paths from initial state to goal).
- Your search strategy, search tree nodes, and frontier now have some extra recordkeeping, including the addition of a graveyard for avoiding repeated states, and Python implementations of priority (which likewise means a different data structure for the frontier).
- The MazeProblem class has a different interface to accommodate the multiple keys--make sure you read through the new documentation below!
- The goal test is now performed during expansion, not generation of nodes.

Some other challenges, tips, and hints to consider:

- Before starting any code: review the A* lecture and CW2 solutions.
- You've graduated from CMSI 2120! Feel free to use any data structures from the Python standard types in pursuit of your task; you won't need anything fancy.
- Consider the appropriate data structures that can be used in pursuit of the frontier and graveyard; you may need to examine the Python documentation and see some tutorials to use these data structures! (self-sufficiency is another take-away lesson here, though I'm happy to help if you get stuck).
- Function getting out-of-hand complicated? Remember to use ample helper methods! Be particularly conscious of repeated code if you want full style-points.
- Need to keep track of costs and prioritize which nodes to expand next? Try record-keeping costs in your SearchTreeNodes and using these to define priority!
- Struggling to keep track of the subgoals of targets? Consider incorporating a data structure into the SearchTreeNodes to track progress!
- Recall that A*'s main improvement over Best-First is its efficiency improvement, so your solution must work (quite quickly) on even large mazes. You thus *must* implement some heuristic to get maximal credit on the full grading tests.
- While you are not allowed to modify any of the existing class' *public* interfaces (except those specified above), you are free to add to the Pathfinders' and SearchTreeNodes' interfaces at will, and you may change whatever you'd like in the SearchTreeNode. This means you can add whatever helper methods or overrides that you see fit (hint: you'll probably need to), but cannot change the existing public methods in Pathfinder.

## Testing & Grading
As mentioned, the full set of grading tests will test many edge cases compared to the samples given in pathfinder_tests.py. Use these to judge the quality of your solution, but make sure to add to these so that you're confident all bugs are squashed!

Remember to practice Iterative Development while working!

This means to (1) make a change to the code that you think fixes a bug or implements a new method, (2) validate that change by running tests, and then (3) making a Git commit as a checkpoint for your change.

Your grade (out of a possible 100 points for homework exercises) will be based on the following:

Correctness: If good faith effort: -X points for each missed unit test (depending on a difficulty adjustment on the grading tests; typically, X=2 or 2.5). If incomplete or has errors: 0 / 100

Warning: your solutions must also be computationally efficient and will be tested on large mazes with a maximum of 3 seconds compute time. Running pytest will ensure that your solution is meeting this timeout, but all unit tests that do not reach a solution in this time will be considered "failed."

Style: Style grading will be assessed on homework, meaning choices like correct spacing, variable names, and simplified logic will be graded. Moreover, you'll receive a -5 point deduction if mypy . yields ANY errors on your submission.

## Submission
You will be submitting your assignments through GitHub Classroom!

**What**
Complete the required method in pathfinder.py that accomplishes the specification above, *in the exact project structure and package given* in the skeleton above.

**How**
To clone this assignment (if you need a refresher), consult the guide here:

[GitHub Classroom Tutorial](https://forns.lmu.build/classes/tutorials/github-classroom.html)

To submit this assignment:

Simply push your final, submission copy to the GitHub Classroom repository associated with your account.

Place your name at the top of *all* submitted files (in appropriate JavaDoc commenting fashion) AND in the accompanying readme file.
