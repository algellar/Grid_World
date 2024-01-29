# "Grid World" Experiment Report

## **Experiment name:**

Reinforcement Learning Implementation in game "Grid World"

## Experiment Objectives:

Utilize reinforcement learning algorithms based on the Bellman equation and dynamic programming to determine the optimal decision-making strategy.

## **Experiment Details:**

In a square grid maze, with specified starting and ending points, obstacles, and locations of other special cells, employ reinforcement learning algorithms to enable a robot to navigate from the starting point to the destination. Record the time taken for the robot to reach the goal.

## Experimental Principles:

The maze-solving process is treated as a Markov process, where the past history does not influence current decision-making. For the current state $S_t$ of the robot, corresponding to the action space $A_t$, the state value function $v_{\pi}(s)$ can be defined as $E_{\pi}[R_{t+1} + \gamma v_{\pi}(S_{t+1})|S_{t}=s]$, along with the state-action value function $q_\mathrm{\pi}(s,a) = E_\pi[R_{t+1} + \gamma q_\pi(S_{t+1},A_{t+1})|S_t=s,A_t=a]$. By utilizing the initial policy and the relationship $\nu_{\pi}(s) = \sum\limits_{\pi(a|s)}q_\pi(s,a)$, the state values for all cells can be computed. The process of training the robot to navigate the maze involves finding the optimal policy $π$ for each state $S$, maximizing $v_π$ and $q_π$.

The entire process is divided into policy evaluation and policy improvement. Under a randomly assigned policy $π$, policy evaluation is carried out to determine $v_π$ for each state. Subsequently, employing a greedy algorithm based on the obtained $v_π$ results in an improved policy $π^′$. This completes one iteration.

The policy evaluation process employs backward iteration using linear programming. Starting from the initial state value function, $\nu_{k}(s)$ is updated to $\nu_{k+1}(s)$ according to the Bellman expectation equation. The iteration stops when each state converges.

## Experiment Model Assumptions and Explanations:

The grid world has dimensions of 12x11, with walls forming the outer perimeter. There are six types of cells, including regular cells, endpoints, walls, boundaries, traps, and incentive cells.

- Regular Cells: Transition between regular cells results in an immediate reward of -1. If the next cell in the action is a wall, the robot remains in the current cell.
- Boundaries: The robot cannot enter boundary cells, so actions involving entering boundaries are not considered.
- Traps: If the robot enters a trap, it returns to the starting position.
- Immediate Rewards: Immediate rewards for entering endpoint, trap, and incentive cells are set to 20, -5, and 5, respectively.

## **Experimental Procedure:**

**Initialization:** Set the state values for all cells to 0 and define a policy with four possible actions. Preprocess the policies around the boundary cells, excluding actions that involve entering boundaries.

**State Value Function Update:** Utilize the formula $\nu_\pi(s)=\sum\limits_{\pi(a|s)}q_\pi(s,a)$ and iteratively update the state value function using dynamic programming.

**Policy Improvement:** After updating the state value function, use the epsilon-greedy approach to update the policy based on the state-action value functions for each action. Additionally, retain low precision during policy evaluation to prevent premature convergence to local optima.

Repeat the process of letting the robot start from the beginning, taking actions based on the current policy, and updating the policy after reaching the endpoint for nine iterations.

## **Experimental Results:**

**Grid World Map:** 

<img src="C:\Users\admin\AppData\Roaming\Typora\typora-user-images\map.png" alt="image-20240129094859923" style="zoom:67%;" />

**Initial State Values:** 

<img src="C:\Users\admin\AppData\Roaming\Typora\typora-user-images\image-20240129094829153.png" alt="image-20240129094829153" style="zoom:67%;" />

**After One Iteration until Convergence of the State Value Function:** 

<img src="C:\Users\admin\AppData\Roaming\Typora\typora-user-images\image-20240129094807196.png" alt="image-20240129094807196" style="zoom:67%;" />

(Note: Values for walls and boundaries are not updated in the state value function. Also, due to returning to the starting point after reaching the endpoint or falling into a trap, no updates are considered for these states.)

**Results After Five Iterations:** 
<div align=center>
<img src="https://github.com/algellar/Grid_world/blob/main/figure/fifth.png" width = "300" height = "200" />
</div>
It can be observed that the state value function stabilizes after four updates. Therefore, the policy is no longer updated, indicating that the policy for each cell has reached its optimum.

If the time taken by the robot to walk is considered equivalent to the number of steps, then when the policy is optimal, the number of steps should be minimized. The following graph illustrates the relationship between the number of updates and the number of steps:

Before updates, the robot's movements are entirely random, resulting in a high number of steps to reach the endpoint. As the number of updates increases, the number of steps stabilizes. Fluctuations are attributed to the epsilon-greedy strategy employed.

## **Experimental Conclusion:**

In this experiment, reinforcement learning algorithms were employed to navigate the "Grid World" game, introducing special cells to enrich the environment. The obtained optimal policy aligns well with the theoretical expectations.

## **Limitations and Recommendations for Improvement:**

1. **Adjustment of Epsilon:**
   - As the number of iterations approaches the optimal policy, consider reducing the value of epsilon to minimize fluctuations in the number of steps. This adjustment can help stabilize the convergence process.
2. **Fine-Tuning Incentive Cell Rewards:**
   - The immediate rewards for incentive cells were considered too small in the experiment. Exploring larger rewards could prevent the robot from moving back and forth between incentive cells without reaching the endpoint. It may be worth considering a mechanism where the incentive cell reward is effective only once.
3. **Experimental Sensitivity:**
   - Sensitivity to parameters such as learning rate and discount factor should be explored to ensure the robustness of the algorithm in various scenarios.

