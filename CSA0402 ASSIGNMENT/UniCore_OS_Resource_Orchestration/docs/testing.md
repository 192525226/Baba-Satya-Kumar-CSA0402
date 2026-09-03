# UniCore Verification & Testing Strategy

## 1. Automated Test Framework
The verification suite is implemented using `pytest` located inside the `tests/` directory.

### Test Matrix Overview
| Module Under Test | Test File | Test Count | Key Invariants Verified |
| :--- | :--- | :---: | :--- |
| **CPU Scheduling** | `test_cpu_scheduler.py` | 5 | Total execution time = 44 ms, FCFS $W_{avg}=17.25$, SJF execution order, RR slice behavior, MLFQ dynamic aging. |
| **Readers-Writers Sync** | `test_synchronization.py` | 2 | Mutual exclusion (0 concurrent writers/readers), race-condition elimination, data integrity. |
| **Banker's Algorithm** | `test_bankers.py` | 6 | $\text{Need} = \text{Max} - \text{Alloc}$, initial safe sequence, adverse request rejection on unsafe state, rollback. |
| **Page Replacement** | `test_page_replacement.py` | 6 | 3 & 4 frame fault counts, Belady's anomaly ($9 \to 10$ faults in FIFO, $10 \to 8$ in LRU), 800-user memory sizing. |
| **File Allocation** | `test_file_allocation.py` | 4 | Inode pointer structure overhead, $O(1)$ random access, suitability score across file sizes. |
| **Disk Scheduling** | `test_disk_scheduler.py` | 7 | Exact seek sequences, THM (FCFS: 908, SSTF: 215, SCAN: 331, C-SCAN: 390, LOOK: 313, C-LOOK: 344), boundary limits. |

---

## 2. Running Automated Tests
To run the complete automated test suite:
```bash
pytest
```
All 30 unit and regression test cases pass with a 100% success rate.
