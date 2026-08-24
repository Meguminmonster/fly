*This project has been created as part of the 42 curriculum by jpedra-v.*

## Description

**Fly-Mine** is a graph-based simulation software designed to route and manage a fleet of 
autonomous drones navigating through a network of zones from a starting hub (`start_hub`)
to a destination hub (`end_hub`). 

The primary goal is to minimize the total number of turns required to transport all drones
across the network while strictly adhering to structural and operational constraints:
- **Node Capacities:** Individual zones have finite capacities (maximum number of drones
allowed simultaneously), except for the start and end hubs which have infinite capacity.
- **Link Capacities:** Connection links between zones enforce maximum throughput per turn.
- **Zone Types:**
  - `normal`: Standard zone with instant traversal (1 turn).
  - `priority`: Higher priority routing zones.
  - `restricted`: Special traversal zones requiring **2 full turns** to pass through.

---

## Instructions

To set up the Python virtual environment, install dependencies, download, and extract 
the test maps, run:
```bash
make install
```

You can run the interactive simulation menu using:
```bash
make run

```

Or execute the main script directly with a specific map file:
```bash
./venv/bin/python3 main.py maps/easy/01_linear_path.txt

```

To check code formatting (`flake8`) and strict type hinting (`mypy`), execute:
```bash
make lint

```

To remove Python cache files:
```bash
make clean

```

To perform a full cleanup (removes `venv` and `maps` directory):
```bash
make fclean

```
---

## Algorithm Choices & Implementation Strategy

### 1. Network & State Model (Object-Oriented Design)

The network is modeled using clean Object-Oriented Programming (OOP) principles:

* **`Zone`**: Represents nodes with coordinates, capacity limits, current occupancy, and type
(`normal`, `priority`, `restricted`).

* **`Connection`**: Represents bidirectional edges with specific throughput capacities.

* **`Drone`**: Tracks individual drone state, current zone, transit status, and destination zone.
Uses dynamic calculated properties (`@property`) to evaluate delivery status without redundant
state flags.

* **`Network`**: Stores nodes, edges, start, and end hubs.

### 2. Multi-Path Pathfinder & Load Balancing

Rather than sending all drones down a single shortest path (which creates severe bottlenecks at 
capacity-constrained nodes), the pathfinding algorithm (`PathFinder`):

1. **Finds Multiple Paths:** Uses graph traversal (BFS / Yen's K-Shortest Paths variant) to discover 
alternative, non-conflicting paths between `start_hub` and `end_hub`.

2. **Dynamic Load Balancing:** Assigns drones across available paths during the setup phase by 
calculating estimated traversal times based on path length and current drone queues.

### 3. Turn-Based Simulation Engine

The simulation engine (`SimulationEngine`) executes a turn-based loop where each turn processes drone 
movements in two distinct phases:

1. **In-Transit Processing:** Advance drones currently stuck in 2-turn `restricted` zones 
(`turns_remaining_in_transit`).

2. **Forward Movement Scheduling:** Process waiting drones in priority order, verifying target zone 
entry capacity (`can_enter()`) and link throughput limits (`max_link_capacity`) before executing 
moves.

---

## Visual

* **Interactive Terminal UI:** When launched without CLI arguments (`make run`), it presents a menu 
allowing users to select maps categorized by difficulty.

* **Network Summary Dashboard:** Before running the simulation, a detailed summary dashboard displays 
the network layout, hub locations, zone coordinates, zone types, and capacity parameters.

* **CLI / Checker Mode:** When passed a map path as a CLI argument, extra visual banners are 
suppressed, yielding clean turn-by-turn logs formatted strictly for automated evaluation scripts 
(`checkers`).

---

## Example Input & Expected Output

### Input Map File (`maps/easy/01_linear_path.txt`)

```text
# Map Definition
nb_drones: 2
start: start 0 0
end: goal 3 0

zone: waypoint1 1 0 normal 1
zone: waypoint2 2 0 normal 1

link: start-waypoint1 1
link: waypoint1-waypoint2 1
link: waypoint2-goal 1

```

### Expected Turn-by-Turn Output

```text
D1-waypoint1
D1-waypoint2 D2-waypoint1
D1-goal D2-waypoint2
D2-goal

```

**Output Explanation:**

* **Turn 1:** Drone `D1` enters `waypoint1`. `D2` waits at `start` because `waypoint1` has a max 
capacity of 1.
* **Turn 2:** `D1` moves to `waypoint2`, freeing `waypoint1`. `D2` immediately enters `waypoint1`.
* **Turn 3:** `D1` reaches `goal`. `D2` moves to `waypoint2`.
* **Turn 4:** `D2` reaches `goal`. Total execution time: 4 turns.

---

## Resources

### References

* **Graph Theory & Pathfinding:** [Red Blob Games - Introduction to A* and Pathfinding](https://www.redblobgames.com/pathfinding/a-star/introduction.html)
* **Yen's Algorithm for K-Shortest Paths:** Network path diversity strategies for flow routing.
* **Python Type Hints & Static Analysis:** [Mypy Documentation](https://mypy.readthedocs.io/)
* **PEP 8 Style Guide for Python:** [Python Software Foundation](https://peps.python.org/pep-0008/)

### AI

Reviewing Object-Oriented design patterns (`Drone`, `Zone`, `Connection`, `Network`)
Assisting in converting property setters/getters in `Drone` to adhere strictly to `mypy --strict` 
typing standards without runtime errors.
