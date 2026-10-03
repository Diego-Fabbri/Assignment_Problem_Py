# Assignment Problem

A **Mixed Integer Linear Programming (MILP)** model in **Python** for the **Assignment Problem**, built with the **[Pyomo](http://www.pyomo.org/)** optimization framework and solved via the **IBM ILOG CPLEX** solver.

## Overview

The Assignment Problem is a fundamental combinatorial optimization problem in Operations Research. A set of workers must be assigned to a set of tasks — each task performed by exactly one worker and each worker performing at most one task — at **minimum total cost**.

This implementation solves a **rectangular** variant where the number of workers ($n$) exceeds the number of tasks ($m$). Since not all workers can receive a task, the model selects the best subset of workers to assign. When $n = m$ (balanced case), every worker is assigned exactly one task.

The Assignment Problem is a special case of the Transportation Problem and can be solved in polynomial time via the Hungarian algorithm. It is widely applicable to workforce scheduling, resource allocation, and task distribution.

## Repository Contents

| File | Description |
|---|---|
| `Assignment_Problem.py` | Python script implementing and solving the Assignment Problem via Pyomo and CPLEX |
| `Assignment_Problem_Results.txt` | Solver output: execution time, optimal assignments with costs, objective value, and solver status |
| `Assignment_Problem.pdf` | Mathematical formulation of the problem |

## Mathematical Formulation

### Parameters

- $n$ = number of workers (index $i = 1, \dots, n$)
- $m$ = number of tasks (index $j = 1, \dots, m$)
- $c_{ij}$ = cost of assigning worker $i$ to task $j$; $\forall\, i = 1, \dots, n,\ j = 1, \dots, m$

### Variable

- $x_{ij}$ = binary assignment variable:

$$
x_{ij} = \begin{cases} 1 & \text{if worker } i \text{ is assigned to task } j \\ 0 & \text{otherwise} \end{cases}
$$

### Objective Function

**(1)** — Minimize total assignment cost

$$
\displaystyle \min \sum_{i=1}^{n} \sum_{j=1}^{m} c_{ij} \cdot x_{ij}
$$

### Constraints

**(2)** — Each task is performed by exactly one worker

$$
\displaystyle \sum_{i=1}^{n} x_{ij} = 1 \qquad \forall\, j = 1, \dots, m
$$

**(3)** — Each worker is assigned to at most one task

$$
\displaystyle \sum_{j=1}^{m} x_{ij} \le 1 \qquad \forall\, i = 1, \dots, n
$$

**(4)** — Binary assignment variables

$$
x_{ij} \in \{0, 1\} \qquad \forall\, i = 1, \dots, n,\ j = 1, \dots, m
$$

> **Note on the rectangular case:** Constraint (2) uses $= 1$ (every task must be covered), while constraint (3) uses $\le 1$ (a worker may be left unassigned). This asymmetry handles the case $n > m$: exactly $m$ workers are selected from the $n$ available. The script also handles the infeasibility case explicitly, printing a diagnostic message if the model has no feasible solution.

A copy of this formulation is also available as a standalone PDF in this repository.

## Example Instance

The script uses a hardcoded instance with **5 workers** and **4 tasks** ($n = 5,\ m = 4$). Since workers outnumber tasks, exactly one worker is left unassigned in the optimal solution.

**Cost matrix $C$** (rows = workers, columns = tasks):

| | Task 0 | Task 1 | Task 2 | Task 3 |
|---|---:|---:|---:|---:|
| **Worker 0** | 90 | 80 | 75 | 70 |
| **Worker 1** | 35 | 85 | 55 | 65 |
| **Worker 2** | 125 | 95 | 90 | 95 |
| **Worker 3** | 45 | 110 | 95 | 115 |
| **Worker 4** | 50 | 100 | 90 | 100 |

The **optimal total cost is 265**, found in **0.06 seconds**:

| Worker | Task | Cost |
|:---:|:---:|---:|
| 0 | 3 | 70 |
| 1 | 2 | 55 |
| 2 | 1 | 95 |
| 3 | 0 | 45 |
| 4 | — | *(unassigned)* |
| | **Total** | **265** |

Worker 4 is left unassigned — its cheapest available task (Task 0, cost 50) is outweighed by the gain from assigning Worker 3 to Task 0 instead (cost 45). The solution is identical to the Java version.

## Requirements

Install the required Python packages via pip:

```bash
pip install pyomo numpy pandas
```

**IBM ILOG CPLEX** must also be installed separately on your system. An academic license is available free of charge through the [IBM Academic Initiative](https://www.ibm.com/academic).

## Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/Diego-Fabbri/Assignment_Problem_Py.git
   cd Assignment_Problem_Py
   ```

2. Run the script:
   ```bash
   python Assignment_Problem.py
   ```

## Output

When executed, the script:
- Builds the MILP model using Pyomo's `ConcreteModel` and prints the full model structure to the console
- Solves it via CPLEX and measures execution time
- Writes the results to `Assignment_Problem_Results.txt`, including:
  - Execution time in seconds
  - Each worker-to-task assignment with its cost (for all active $x[i][j] = 1$)
  - Optimal total assignment cost (objective value)
  - Solver status and termination condition
