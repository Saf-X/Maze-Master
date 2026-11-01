# Maze Master

A Pygame maze game with two ways to play and an education mode that animates how Dijkstra's and A\* algorithms find the shortest path through a maze.

<img width="426" height="240" alt="Maze Master 2" src="https://github.com/user-attachments/assets/58d75bc6-5a38-47c4-b92f-c46e66a0ebc6" />
<img width="426" height="240" alt="Maze Master" src="https://github.com/user-attachments/assets/d11d5fd3-00d0-4a48-95d5-d81501e07333" />
<img width="426" height="240" alt="Maze Master 3" src="https://github.com/user-attachments/assets/e5b6a957-782b-4eb2-9844-dd01558187ae" />


## Features

- **Levels mode:** 45 hand-built mazes split into 15 easy, 15 medium and 15 hard levels. Each level awards up to 3 stars, giving 135 stars in total.
- **Endless mode:** a new random 20 × 20 maze every round. The game tracks your fastest solve time and your best streak of consecutive 3-star runs.
- **Darkness mode:** limits your vision to a small circle around the player. Stats and stars are tracked separately from normal mode, and it has its own theme and music.
- **Education mode:** a visualiser that animates Dijkstra's algorithm and A\* step by step on a maze you can resize (6 to 50 cells in each direction), so you can compare how each one explores.
- **Settings:** separate sound-effect and music volume (five steps each) with mute buttons. Settings and progress are saved between sessions.

## Getting started

### Requirements

- Python 3.10 or newer (the code uses `match` statements)
- [Pygame](https://www.pygame.org/)

### Install and run

```bash
git clone https://github.com/Saf-X/Maze-Master.git
cd Maze-Master
pip install pygame
python main.py
```

The game opens in a 1280 × 720 window and runs at 60 FPS. Run it from the project folder so it can find the `assets` and `data` folders.

## How to play

| Input | Action |
| --- | --- |
| Arrow keys or W A S D | Move |
| Mouse | Click buttons |
| Pause button (top left) | Pause, return home or open settings |

You don't move one square at a time. The player slides in the chosen direction until it reaches a junction or a dead end, so the puzzle is about choosing the right turns. You can queue your next direction while the player is still moving.

The goal is always the bottom-right cell, and you start in the top-left.

### Star ratings

The game works out the shortest possible route with Dijkstra's algorithm, then scores your time against it:

| Stars | Condition |
| --- | --- |
| 3 | Finish within (shortest path length ÷ 6.02) seconds |
| 2 | Finish within 5 seconds after the 3-star limit |
| 1 | Anything slower |

A level counts as completed once you earn at least one star. Your best rating for each level is saved.

## Education mode

Pick Education mode from the title screen to watch an algorithm search a maze. You can:

- Switch between **Dijkstra's** and **A\***
- Change the maze width and height, and generate a new maze with the refresh button
- Play, pause and replay the animation, and speed it up or slow it down (from 2× down to 0.25×, plus Max and Min settings)
- Open the **Info** panel for a short description of the current algorithm and its status
- Open the **Stats** panel to see the number of visited nodes, queued nodes and the shortest path length as the search runs

The colours on the maze show what the algorithm is doing:

| Colour | Meaning |
| --- | --- |
| Cyan | Start node |
| Gold | Goal node |
| Red | Node currently being examined |
| Pink | Queued nodes (the open set) |
| Light green | Visited nodes |
| Dark green | The final shortest path being retraced |

## How it works

### Maze generation

Random mazes are generated with **depth-first search** (also called recursive backtracking), implemented with an explicit stack:

1. Start at the top-left cell and mark it visited.
2. Pick a random unvisited neighbour, remove the wall between the two cells, and move to it.
3. If the current cell has no unvisited neighbours, backtrack by popping the stack.
4. Stop when the stack is empty.

This produces a "perfect" maze: every cell is reachable and there is exactly one route between any two cells.

### Pathfinding

Both algorithms treat the maze as a graph where each cell is a node and each open gap between cells is an edge with a cost of 1.

- **Dijkstra's algorithm** repeatedly visits the queued node with the lowest distance from the start. It has no sense of direction, so it spreads out evenly in all directions.
- **A\*** picks the queued node with the lowest `f(n) = g(n) + h(n)`, where `g` is the distance from the start and `h` is the Manhattan distance to the goal. The heuristic pulls the search towards the goal, so it usually visits fewer nodes.

Each algorithm has two modes of use. `run()` solves the maze instantly (used for star ratings), while `setup()` and `run_frame()` advance the search one step at a time (used for the education-mode animation).

## Code structure

The whole game is in `main.py`, organised around a simple state machine in the `Game` class. Each screen is its own class with `draw()`, `update()` and `buttons_clicked()` methods, and the game loop calls whichever is the current state.

| Class | Responsibility |
| --- | --- |
| `Game` | Window, main loop, event handling, state switching |
| `TitleScreen`, `PlayMode` | Menus, including the darkness mode toggle |
| `GameMode` | Parent class with shared timer, move counter, star rating and darkness overlay |
| `LevelsGameMode`, `EndlessGameMode` | The two ways to play, inheriting from `GameMode` |
| `EducationMode` | The algorithm visualiser |
| `Maze`, `Node` | Grid of cells with walls, DFS generation and drawing |
| `Player` | Sliding movement, queued input and the trail |
| `Dijkstra`, `AStar` | Pathfinding, with instant and step-by-step versions |
| `PauseMenu`, `Settings`, `WinScreen` (and subclasses) | Overlays and result screens |
| `Button` | Image button with pixel-accurate click detection |

Buttons check the clicked pixel against a mask of the image, so clicks on transparent parts of an icon are ignored.

### Project layout

```
Maze-Master/
├── main.py
├── data/
│   ├── levels.json     # The 45 level layouts and best star ratings
│   ├── stats.json      # Endless mode best time and best streak
│   └── settings.json   # Volume and mute settings
└── assets/
    ├── images/
    ├── sounds/
    └── fonts/
```

Progress is stored as plain JSON in the `data` folder. Delete or edit these files to reset your stars, stats or settings.

## Possible improvements

- Use a priority queue (`heapq`) instead of scanning the open set for the lowest-cost node, which would speed up both algorithms on large mazes
- Add breadth-first search and depth-first search solvers to the education mode
- Split `main.py` into separate modules for the game states, maze logic and pathfinding
- Add a keyboard shortcut for the education-mode controls

## Credits

- Built by [Safwaan Shareef](https://github.com/Saf-X)
- Fonts: Montserrat and Parkvane \[add licence details\]
- Music and sound effects: \[add sources\]

## Licence

&#91;Add a licence, for example MIT\]
