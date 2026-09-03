# UniCore: OS Resource Orchestration System for a Smart University

**Course:** CSA04 – Operating Systems  
**Assignment Title:** Design and Analysis of an OS Resource Orchestration System for a Smart University (UniCore)

---

## 1. Project Overview & Problem Statement

**UniCore** is an integrated, mathematically verified Operating System resource management and simulation platform designed to orchestrate computing resources in a smart university infrastructure. The system manages heterogeneous workloads across:
- **Baseline Operations:** ~500 concurrent users running learning management systems (LMS), digital library catalog queries, and campus IoT telemetry.
- **High-Stakes Examination Peaks:** 800+ concurrent students submitting exams with strict latency, memory isolation, and fault-tolerance constraints.

UniCore provides a complete, empirical, Python-based implementation covering:
1. **Process Management & CPU Scheduling (CO2):** Comparative analysis of FCFS, SJF (Non-Preemptive), Round Robin ($q=4\text{ms}$), Preemptive Priority, and Multilevel Feedback Queue (MLFQ).
2. **Concurrency & Synchronization (CO2):** Fair Readers-Writers Monitor preventing race conditions on shared student examination records while eliminating writer starvation.
3. **Deadlock Avoidance (CO2):** Complete Banker's Safety Algorithm implementation with 8 processes, 4 resource types, dynamic Need matrix calculation, and adverse unsafe request detection and rollback.
4. **Virtual Memory & Page Replacement (CO3):** Hardware sizing for 16 GB RAM (4,194,304 physical frames) and 64 MB logical address space (16,384 pages), 2-level paging, 95% TLB hit EMAT modeling, step-by-step FIFO vs LRU vs Optimal simulations across 3 and 4 frames, Belady's anomaly proof, and working-set thrashing evaluation for 800 users.
5. **File Allocation & Storage Systems (CO4):** Quantitative benchmarking of Contiguous, Linked, and Unix Inode Indexed allocation across small student records (< 4 KB), medium course documents (2 MB), and large lecture video archives (1 GB).
6. **Disk Scheduling & Seek Optimization (CO4):** Trajectory and Total Head Movement (THM) analysis for FCFS, SSTF, SCAN, C-SCAN, LOOK, and C-LOOK on a 200-cylinder drive (0–199).
7. **End-to-End Master Orchestration:** Unified pipeline generating empirical CSV/TXT logs and high-resolution visual diagrams.

---

## 2. Project Directory Structure

```text
UniCore_OS_Resource_Orchestration/
│
├── README.md                          # Project documentation and execution instructions
├── requirements.txt                   # Minimal Python package dependencies
├── .gitignore                         # Git exclusion rules
│
├── src/                               # Core Python implementation modules
│   ├── __init__.py
│   ├── cpu_scheduler.py               # FCFS, SJF, RR, Priority, MLFQ simulators
│   ├── synchronization.py             # Pure Python Fair Readers-Writers monitor
│   ├── bankers_algorithm.py           # Banker's Safety & Resource-Request algorithm
│   ├── page_replacement.py            # FIFO, LRU, Optimal, Belady Anomaly & Thrashing
│   ├── file_allocation.py             # Contiguous, Linked, and Indexed Inode evaluation
│   ├── disk_scheduler.py              # FCFS, SSTF, SCAN, C-SCAN, LOOK, C-LOOK on 200 cyl
│   ├── unicore_orchestrator.py        # Master end-to-end orchestration entry point
│   ├── generate_figures.py            # High-resolution PNG & SVG diagram generator
│   └── utils.py                       # JSON loaders, CSV exporters, formatted table display
│
├── tests/                             # Automated Pytest suite (30 test cases)
│   ├── __init__.py
│   ├── test_cpu_scheduler.py          # CPU metrics & Gantt verification
│   ├── test_synchronization.py        # Race-condition & mutual exclusion verification
│   ├── test_bankers.py                # Need matrix, safe sequence & adverse request tests
│   ├── test_page_replacement.py       # Exact fault counts, Belady anomaly, hardware bounds
│   ├── test_file_allocation.py        # Inode overhead & random access complexity tests
│   └── test_disk_scheduler.py         # Seek trajectories, THM, and boundary tests
│
├── data/                              # Workload input JSON datasets
│   ├── cpu_workload.json              # Process burst times, arrival times, priorities
│   ├── banker_resources.json          # Allocation, Max claim, and Available matrices
│   ├── page_reference_string.json     # Page reference sequence and hardware parameters
│   └── disk_requests.json             # 200-cylinder request queue & head position
│
├── results/                           # Program-generated empirical output files
│   ├── cpu_results.csv                # Per-process CT, WT, TAT, RT, and averages
│   ├── memory_results.csv             # Step-by-step frame contents and page faults
│   ├── disk_results.csv               # Seek steps, cylinder jumps, and cumulative THM
│   ├── bankers_results.txt            # Work vectors, safe sequence & adverse trace
│   ├── synchronization_results.txt    # Concurrency timeline & thread access verification
│   └── integrated_results.txt         # Consolidated master orchestration log
│
├── figures/                           # High-resolution technical figures (PNG & SVG)
│   ├── architecture_diagram.png       # Layered OS architecture diagram
│   ├── architecture_diagram.svg       # Vector architecture diagram
│   ├── complete_system_flowchart.png  # Lifecycle flowchart from job to storage
│   ├── cpu_gantt_chart.png            # Visual Gantt chart comparing CPU schedulers
│   ├── cpu_comparison.png             # Waiting / Turnaround / Response time bar chart
│   ├── bankers_flowchart.png          # Safety & resource-request algorithm logic
│   ├── memory_management_diagram.png  # 2-level paging, TLB translation, page faults
│   ├── page_fault_comparison.png      # 3 vs 4 frame fault comparison & Belady curve
│   ├── disk_trajectory.png            # Cylinder position vs seek step line chart
│   └── disk_movement_comparison.png   # Total head movement (THM) comparison
│
├── docs/                              # Detailed technical documentation
│   ├── methodology.md                 # Mathematical models and algorithmic formulations
│   ├── implementation_notes.md        # Python design patterns and data structures
│   ├── testing.md                     # Pytest suite strategy and test cases
│   └── design_decisions.md            # Multi-criteria engineering trade-offs
│
└── report/                            # Publication-ready academic assignment reports
    ├── UniCore_OS_Assignment_Report.docx # Formatted academic report with Calibri typography
    └── UniCore_OS_Assignment_Report.pdf  # PDF report compiled directly from source
```

---

## 3. Technologies Used

- **Programming Language:** Python 3.8+
- **Standard Library Modules:** `threading`, `queue`, `collections`, `dataclasses`, `typing`, `csv`, `json`, `math`, `time`, `random`
- **External Packages:**
  - `matplotlib` (Vector diagrams & publication-quality charts)
  - `pytest` (Automated unit and regression test suite)
  - `python-docx` (Structured Microsoft Word document generator)
  - `reportlab` (Direct PDF compilation engine)

---

## 4. Installation & Environment Setup

1. **Clone or Navigate to the Project Directory:**
   ```bash
   cd UniCore_OS_Resource_Orchestration
   ```

2. **Install Required Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 5. Running the System

### A. Run Master Orchestration Pipeline
To execute all simulation modules, export CSV/TXT results, and regenerate high-resolution figures:
```bash
python src/unicore_orchestrator.py
```

### B. Run Individual Simulation Modules
- **CPU Scheduling Benchmark:**
  ```bash
  python src/cpu_scheduler.py
  ```
- **Readers-Writers Synchronization:**
  ```bash
  python src/synchronization.py
  ```
- **Banker's Deadlock Avoidance Simulator:**
  ```bash
  python src/bankers_algorithm.py
  ```
- **Virtual Memory & Page Replacement:**
  ```bash
  python src/page_replacement.py
  ```
- **File Allocation Strategies:**
  ```bash
  python src/file_allocation.py
  ```
- **Disk Scheduling Benchmark:**
  ```bash
  python src/disk_scheduler.py
  ```

---

## 6. Running Automated Tests

To execute the full `pytest` verification suite across all 30 test cases:
```bash
pytest
```

---

## 7. Summary of Quantitative Benchmark Results

### 1. CPU Scheduling Performance (8 Representative Processes)
| Algorithm | Avg Waiting Time ($\bar{W}$) | Avg Turnaround Time ($\bar{T}$) | Avg Response Time ($\bar{R}$) | CPU Utilization | Architectural Assessment |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **FCFS** | 17.25 ms | 22.75 ms | 17.25 ms | 100.0% | Convoy effect on long bursts |
| **SJF (Non-Preemptive)** | 14.50 ms | 21.38 ms | 14.50 ms | 100.0% | Minimizes average waiting time |
| **Round Robin ($q=4\text{ms}$)** | 24.88 ms | 31.75 ms | 10.12 ms | 100.0% | Eliminates starvation |
| **Preemptive Priority** | 15.00 ms | 21.88 ms | 15.00 ms | 100.0% | Strict priority for exam tasks |
| **MLFQ ($q_0=2, q_1=4$)** | 27.25 ms | 34.12 ms | **3.50 ms** | 100.0% | **Optimal interactive responsiveness** |

### 2. Page Replacement Performance (20 References: `7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1`)
| Algorithm | 3 Frames (Faults / Hit %) | 4 Frames (Faults / Hit %) | Belady's Anomaly Immunity |
| :--- | :---: | :---: | :---: |
| **FIFO** | 15 faults (25.0%) | 10 faults (50.0%) | ❌ No ($9 \to 10$ faults on Belady string) |
| **LRU (Selected)** | **12 faults (40.0%)** | **8 faults (60.0%)** | ✅ **Yes (Stack Property Guaranteed)** |
| **Optimal (OPT Bound)** | 9 faults (55.0%) | 8 faults (60.0%) | ✅ Yes (Clairvoyant Lower Bound) |

### 3. Disk Scheduling Performance (200 Cylinders: Initial Head = 53, Direction = HIGH)
| Algorithm | Total Head Movement (THM) | Average Seek Length (ASL) | Fairness & Starvation Profile |
| :--- | :---: | :---: | :--- |
| **FCFS** | 908 cylinders | 90.80 cyl/req | Fair arrival order, excessive oscillation |
| **SSTF** | 215 cylinders | 21.50 cyl/req | Lowest THM, but high starvation risk on outer cylinders |
| **SCAN (Elevator)** | 331 cylinders | 33.10 cyl/req | Bidirectional elevator, moderate variance |
| **C-SCAN (Selected)** | **390 cylinders** | **39.00 cyl/req** | **Uniform, predictable bounded latency** |
| **LOOK** | 313 cylinders | 31.30 cyl/req | Bounded elevator, skips empty boundaries |
| **C-LOOK** | 344 cylinders | 34.40 cyl/req | Optimized circular sweep, zero boundary overhead |

---

## 8. Academic Report & Documentation

The complete academic assignment report is available in the `report/` directory:
- **Microsoft Word Document:** [`report/UniCore_OS_Assignment_Report.docx`](file:///d:/CSA0402%20ASSIGNMENT/UniCore_OS_Resource_Orchestration/report/UniCore_OS_Assignment_Report.docx)
- **Publication-Ready PDF:** [`report/UniCore_OS_Assignment_Report.pdf`](file:///d:/CSA0402%20ASSIGNMENT/UniCore_OS_Resource_Orchestration/report/UniCore_OS_Assignment_Report.pdf)
