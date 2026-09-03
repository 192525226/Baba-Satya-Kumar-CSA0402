# UniCore Architectural Design Decisions & Trade-Offs

## 1. Multi-Criteria Engineering Decision Matrix

### Decision 1: CPU Scheduling — MLFQ over Preemptive Priority
- **Rationale:** Strict priority scheduling causes indefinite starvation for background batch tasks (e.g., Nightly DB backups, IoT log compaction). Multilevel Feedback Queue (MLFQ) provides immediate responsiveness ($R_{avg} = 3.50\text{ ms}$) for interactive exam submissions in Queue 0 ($q=2\text{ ms}$), while preventing batch starvation through dynamic aging and demotion to Queue 1 and Queue 2.

### Decision 2: Synchronization — Fair Monitor with Condition Variables
- **Rationale:** Traditional reader-preference semaphore locks allow a continuous stream of reader threads to starve writers indefinitely. In an online examination setting, student answer submissions and grade updates (writers) cannot be delayed. The fair monitor enforces writer queueing to ensure bounded wait times.

### Decision 3: Deadlock Strategy — Banker's Avoidance over Pure Prevention
- **Rationale:** Deadlock prevention (e.g., forcing processes to request all resources up front or strict linear resource ordering) severely depresses system resource utilization. Banker's avoidance dynamically evaluates safety matrices ($\text{Need} = \text{Max} - \text{Allocation}$), permitting high resource sharing while rejecting only genuinely unsafe states.

### Decision 4: Virtual Memory Replacement — LRU over FIFO
- **Rationale:** FIFO exhibits Belady's Anomaly where allocating more physical frames can paradoxically increase page faults ($9 \to 10$ on the test string). LRU is a proven stack algorithm ($M_t(n) \subseteq M_t(n+1)$) guaranteeing monotonic hit rate improvements with increased RAM.

### Decision 5: Disk Scheduling — C-SCAN over SSTF
- **Rationale:** While SSTF achieves the absolute lowest Total Head Movement (215 cylinders vs 390 for C-SCAN), it suffers from severe starvation and high latency variance for requests on outer tracks. C-SCAN delivers uniform, predictable bounded latency across all disk cylinders, which is critical for real-time exam logging.

### Decision 6: Storage Architecture — Unix Inode Indexed Allocation
- **Rationale:** Contiguous allocation suffers from crippling external fragmentation and costly compaction, while Linked allocation incurs high $O(N)$ random access penalties (crippling video scrubbing). Unix Inode indexing provides $O(1)$ direct access for small/medium files and scales up to 4 GB+ media files via multi-level indirect blocks.
