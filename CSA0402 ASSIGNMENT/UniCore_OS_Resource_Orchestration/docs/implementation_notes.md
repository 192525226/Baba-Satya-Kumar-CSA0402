# UniCore Implementation Notes & Architecture

## 1. Modular Python Architecture
The codebase is organized into cleanly separated single-responsibility modules:
- `cpu_scheduler.py`: Contains dataclass `Process` and simulator `CPUScheduler`. State variables track execution slices, arrival, and completion times with 100% deterministic arithmetic.
- `synchronization.py`: Pure Python monitor implementing `FairReadersWritersMonitor`. Built using `threading.Lock` and `threading.Condition` variables. Avoids C-dependencies to enable cross-platform execution on Windows, Linux, and macOS.
- `bankers_algorithm.py`: Matrix safety checking engine and dynamic request verifier. Features automated tentative state cloning and rollback mechanisms.
- `page_replacement.py`: Simulates page eviction policies (FIFO, LRU, Optimal), calculates address space parameters, and performs working-set thrashing evaluations.
- `file_allocation.py`: Quantitatively benchmarks Contiguous, Linked, and Unix Inode Indexed allocation architectures.
- `disk_scheduler.py`: Implements cylinder head seek algorithms on 200-cylinder storage arrays.
- `unicore_orchestrator.py`: Master orchestration engine and end-to-end benchmark harness.
- `generate_figures.py`: Generates publication-ready 300 DPI PNG figures and vector SVGs.
- `utils.py`: Provides JSON loaders, CSV exporter, and formatted ASCII table visualizers.

---

## 2. Key Data Structures
1. **CPU Scheduler:** Uses Python `dataclass` instances, priority lists, and double-ended ready queues.
2. **Page Replacement:** Uses hash maps for $O(1)$ LRU timestamp access and lookahead scanning for optimal future distance discovery.
3. **Banker's Matrices:** Stored as 2D integer lists with deep copying for transactional tentative allocations.
4. **Disk Scheduling:** Uses sorted partitions for directional sweeps and Euclidean absolute differences for seek movement summation.
