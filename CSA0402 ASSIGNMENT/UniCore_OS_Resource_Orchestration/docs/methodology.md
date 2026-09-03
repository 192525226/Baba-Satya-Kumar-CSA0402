# UniCore OS Resource Orchestration — Engineering Methodology

## 1. Executive Problem Formulation
The **UniCore Smart University Platform** represents a complex multi-tenant computing environment designed to host high-stakes examination engines, campus-wide learning management systems (LMS), high-performance computing (HPC) research simulations, and IoT telemetry ingest systems. Under baseline operating conditions, the system supports ~500 concurrent sessions, but scales dynamically during synchronized examinations to over 800+ concurrent students submitting exam records simultaneously.

To ensure deterministic execution, high responsiveness, memory isolation, and bounded disk latencies, the Operating System layer must orchestrate four interrelated subsystems:
1. **Process Management & CPU Scheduling (CO2)**
2. **Concurrency & Classical Synchronization (CO2)**
3. **Deadlock Avoidance & Safety Verification (CO2)**
4. **Virtual Memory, Paging, and Thrashing Prevention (CO3)**
5. **File Allocation & Inode Storage Organization (CO4)**
6. **Disk Arm Seek Scheduling & Fair Queuing (CO4)**

---

## 2. Mathematical Modeling & Algorithms

### A. CPU Scheduling Formulation
Process metrics are governed by discrete event simulation:
- **Turnaround Time ($TAT$):** $TAT_i = CT_i - AT_i$
- **Waiting Time ($WT$):** $WT_i = TAT_i - BT_i$
- **Response Time ($RT$):** $RT_i = ST_i - AT_i$
- **Averages:** $\bar{W} = \frac{1}{N} \sum WT_i$, $\bar{T} = \frac{1}{N} \sum TAT_i$, $\bar{R} = \frac{1}{N} \sum RT_i$

Schedulers implemented include:
- **FCFS:** Non-preemptive, FIFO arrival ordering.
- **SJF:** Shortest Job First non-preemptive selection.
- **Round Robin ($q=4\text{ms}$):** Time-sliced circular queue.
- **Preemptive Priority:** Dynamic interruption for lower numerical priority values.
- **MLFQ:** 3-tier feedback queue with demotion:
  - $Q_0$: RR ($q=2\text{ms}$)
  - $Q_1$: RR ($q=4\text{ms}$)
  - $Q_2$: FCFS batch queue

### B. Classical Synchronization: Readers-Writers Monitor
Modeled over shared examination records ($D$).
- **State Invariants:**
  - Active Writers $W_{act} \in \{0, 1\}$
  - If $W_{act} = 1 \implies R_{act} = 0$
  - If $R_{act} > 0 \implies W_{act} = 0$
- **Fairness Guarantee:** When a writer arrives ($W_{wait} > 0$), subsequent readers are blocked on condition variable `can_read` to prevent writer starvation.

### C. Banker's Deadlock Avoidance Algorithm
- Resource Types: $m = 4$ ($R_1$: DB Connections [10], $R_2$: File Locks [6], $R_3$: GPU Cores [8], $R_4$: Disk I/O [7])
- Processes: $n = 8$ ($P_0$ through $P_7$)
- **Need Computation:** $\text{Need}_{i,j} = \text{Max}_{i,j} - \text{Alloc}_{i,j}$
- **Available Computation:** $\text{Avail}_j = \text{Total}_j - \sum_{i} \text{Alloc}_{i,j}$
- **Safety Algorithm:**
  1. $\text{Work} = \text{Avail}$, $\text{Finish}[i] = \text{False} \, \forall i$
  2. Find $i$ such that $\text{Finish}[i] == \text{False}$ and $\text{Need}_i \le \text{Work}$.
  3. $\text{Work} = \text{Work} + \text{Alloc}_i$, $\text{Finish}[i] = \text{True}$. Repeat.
  4. If $\text{Finish}[i] == \text{True} \, \forall i \implies$ System is **SAFE**.

### D. Memory Management & Paging
- **Physical Memory:** $16\text{ GB} = 16 \times 2^{30}\text{ bytes} = 2^{34}\text{ bytes}$ (34-bit Physical Address)
- **Page Size:** $4\text{ KB} = 2^{12}\text{ bytes}$ (12-bit Offset)
- **Physical Frames:** $\frac{2^{34}}{2^{12}} = 2^{22} = 4,194,304\text{ frames}$
- **Logical Address Space:** $64\text{ MB} = 2^{26}\text{ bytes}$ (26-bit Logical Address)
- **Logical Pages:** $\frac{2^{26}}{2^{12}} = 2^{14} = 16,384\text{ pages}$
- **Two-Level Paging:** 14-bit page number split into 7-bit Outer Page Table ($p_1$) and 7-bit Inner Page Table ($p_2$).
- **Effective Memory Access Time (EMAT):**
  $$\text{EMAT} = \alpha (t_{TLB} + t_{MEM}) + (1 - \alpha)(t_{TLB} + 3 \cdot t_{MEM})$$
  For $\alpha = 0.95, t_{TLB} = 2\text{ns}, t_{MEM} = 50\text{ns}$:
  $$\text{EMAT} = 0.95(52) + 0.05(152) = 49.4 + 7.6 = 57.0\text{ ns}$$

### E. Disk Scheduling & Seek Optimization
200 Cylinders ($0 - 199$), Initial Head = 53, Direction = HIGH.
- **FCFS:** Direct arrival sequence.
- **SSTF:** Greedy local distance minimization ($d = \min |r_i - \text{head}|$).
- **SCAN:** Sweeps towards cylinder 199, then reverses down to lowest pending cylinder.
- **C-SCAN:** Sweeps towards cylinder 199, jumps to cylinder 0, and sweeps upwards.
- **Total Head Movement (THM):** $\text{THM} = \sum_{i=1}^{K} |\text{Seq}_i - \text{Seq}_{i-1}|$
- **Average Seek Length (ASL):** $\text{ASL} = \frac{\text{THM}}{N}$
