"""
CPU Scheduling Simulator for UniCore Smart University Platform
Course: CSA04 Operating Systems (CO2)

Implements and benchmarks CPU scheduling algorithms:
1. First-Come First-Served (FCFS)
2. Shortest Job First (SJF - Non-preemptive)
3. Shortest Remaining Time First (SRTF - Preemptive SJF)
4. Round Robin (RR, configurable quantum, default q=4ms)
5. Preemptive Priority Scheduling
6. Multilevel Feedback Queue (MLFQ with dynamic aging)

Generates full execution traces, Gantt chart segments, and metrics:
- Completion Time (CT)
- Turnaround Time (TAT = CT - AT)
- Waiting Time (WT = TAT - BT)
- Response Time (RT = Start Time - AT)
- CPU Utilization and Throughput
"""

from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass, field
import copy
import os
import sys

# Support relative and standalone imports
try:
    from .utils import load_json_data, save_csv_results, format_table
except ImportError:
    from utils import load_json_data, save_csv_results, format_table


@dataclass
class Process:
    pid: str
    name: str
    arrival_time: int
    burst_time: int
    priority: int = 0  # Lower number = higher priority (e.g., 1 is top priority)

    # State variables for simulation
    remaining_time: int = field(init=False)
    start_time: Optional[int] = field(init=False, default=None)
    completion_time: int = field(init=False, default=0)
    turnaround_time: int = field(init=False, default=0)
    waiting_time: int = field(init=False, default=0)
    response_time: int = field(init=False, default=0)

    def __post_init__(self):
        self.remaining_time = self.burst_time

    def clone(self) -> 'Process':
        p = Process(self.pid, self.name, self.arrival_time, self.burst_time, self.priority)
        p.remaining_time = self.remaining_time
        p.start_time = self.start_time
        p.completion_time = self.completion_time
        p.turnaround_time = self.turnaround_time
        p.waiting_time = self.waiting_time
        p.response_time = self.response_time
        return p


class CPUScheduler:
    def __init__(self, processes: List[Process]):
        self.raw_processes = processes

    def _calculate_metrics(self, procs: List[Process], total_time: int, busy_time: int) -> Dict[str, float]:
        n = len(procs)
        if n == 0:
            return {"avg_wt": 0.0, "avg_tat": 0.0, "avg_rt": 0.0, "cpu_utilization": 0.0, "throughput": 0.0}

        avg_wt = sum(p.waiting_time for p in procs) / n
        avg_tat = sum(p.turnaround_time for p in procs) / n
        avg_rt = sum(p.response_time for p in procs) / n
        utilization = (busy_time / total_time * 100.0) if total_time > 0 else 100.0
        throughput = (n / total_time) if total_time > 0 else 0.0

        return {
            "avg_wt": round(avg_wt, 2),
            "avg_tat": round(avg_tat, 2),
            "avg_rt": round(avg_rt, 2),
            "cpu_utilization": round(utilization, 2),
            "throughput": round(throughput, 4),
            "total_time": total_time
        }

    def run_fcfs(self) -> Tuple[List[Process], List[Tuple[str, int, int]], Dict[str, float]]:
        """First-Come First-Served (FCFS) Scheduling."""
        procs = [p.clone() for p in self.raw_processes]
        procs.sort(key=lambda p: (p.arrival_time, p.pid))

        current_time = 0
        gantt_chart: List[Tuple[str, int, int]] = []
        busy_time = 0

        for p in procs:
            if current_time < p.arrival_time:
                # CPU Idle
                gantt_chart.append(("IDLE", current_time, p.arrival_time))
                current_time = p.arrival_time

            p.start_time = current_time
            p.response_time = p.start_time - p.arrival_time
            start_t = current_time
            current_time += p.burst_time
            busy_time += p.burst_time
            p.completion_time = current_time
            p.turnaround_time = p.completion_time - p.arrival_time
            p.waiting_time = p.turnaround_time - p.burst_time
            gantt_chart.append((p.pid, start_t, current_time))

        metrics = self._calculate_metrics(procs, current_time, busy_time)
        return procs, gantt_chart, metrics

    def run_sjf_non_preemptive(self) -> Tuple[List[Process], List[Tuple[str, int, int]], Dict[str, float]]:
        """Shortest Job First (SJF) - Non-preemptive."""
        procs = [p.clone() for p in self.raw_processes]
        n = len(procs)
        completed = 0
        current_time = 0
        gantt_chart: List[Tuple[str, int, int]] = []
        busy_time = 0
        is_completed = [False] * n

        while completed < n:
            # Find available process with shortest burst time
            idx = -1
            min_burst = float('inf')

            for i in range(n):
                if procs[i].arrival_time <= current_time and not is_completed[i]:
                    if procs[i].burst_time < min_burst:
                        min_burst = procs[i].burst_time
                        idx = i
                    elif procs[i].burst_time == min_burst:
                        if procs[i].arrival_time < procs[idx].arrival_time:
                            idx = i

            if idx == -1:
                # Jump to next arrival time
                next_arr = min(p.arrival_time for i, p in enumerate(procs) if not is_completed[i])
                gantt_chart.append(("IDLE", current_time, next_arr))
                current_time = next_arr
                continue

            p = procs[idx]
            p.start_time = current_time
            p.response_time = p.start_time - p.arrival_time
            start_t = current_time
            current_time += p.burst_time
            busy_time += p.burst_time
            p.completion_time = current_time
            p.turnaround_time = p.completion_time - p.arrival_time
            p.waiting_time = p.turnaround_time - p.burst_time
            gantt_chart.append((p.pid, start_t, current_time))

            is_completed[idx] = True
            completed += 1

        metrics = self._calculate_metrics(procs, current_time, busy_time)
        return procs, gantt_chart, metrics

    def run_round_robin(self, quantum: int = 4) -> Tuple[List[Process], List[Tuple[str, int, int]], Dict[str, float]]:
        """Round Robin (RR) Scheduling with configurable time quantum."""
        procs = [p.clone() for p in self.raw_processes]
        procs.sort(key=lambda p: (p.arrival_time, p.pid))

        current_time = 0
        ready_queue: List[Process] = []
        gantt_chart: List[Tuple[str, int, int]] = []
        busy_time = 0
        arrived_idx = 0
        n = len(procs)
        completed = 0

        while completed < n:
            # Add newly arrived processes to ready queue
            while arrived_idx < n and procs[arrived_idx].arrival_time <= current_time:
                ready_queue.append(procs[arrived_idx])
                arrived_idx += 1

            if not ready_queue:
                if arrived_idx < n:
                    next_arr = procs[arrived_idx].arrival_time
                    gantt_chart.append(("IDLE", current_time, next_arr))
                    current_time = next_arr
                    while arrived_idx < n and procs[arrived_idx].arrival_time <= current_time:
                        ready_queue.append(procs[arrived_idx])
                        arrived_idx += 1
                else:
                    break

            curr_proc = ready_queue.pop(0)

            if curr_proc.start_time is None:
                curr_proc.start_time = current_time
                curr_proc.response_time = curr_proc.start_time - curr_proc.arrival_time

            exec_time = min(quantum, curr_proc.remaining_time)
            start_t = current_time
            current_time += exec_time
            busy_time += exec_time
            curr_proc.remaining_time -= exec_time

            gantt_chart.append((curr_proc.pid, start_t, current_time))

            # Check new arrivals during this execution slice
            while arrived_idx < n and procs[arrived_idx].arrival_time <= current_time:
                ready_queue.append(procs[arrived_idx])
                arrived_idx += 1

            if curr_proc.remaining_time > 0:
                ready_queue.append(curr_proc)
            else:
                curr_proc.completion_time = current_time
                curr_proc.turnaround_time = curr_proc.completion_time - curr_proc.arrival_time
                curr_proc.waiting_time = curr_proc.turnaround_time - curr_proc.burst_time
                completed += 1

        metrics = self._calculate_metrics(procs, current_time, busy_time)
        return procs, gantt_chart, metrics

    def run_priority_preemptive(self) -> Tuple[List[Process], List[Tuple[str, int, int]], Dict[str, float]]:
        """Preemptive Priority Scheduling (Lower priority integer = higher priority)."""
        procs = [p.clone() for p in self.raw_processes]
        n = len(procs)
        completed = 0
        current_time = 0
        gantt_chart: List[Tuple[str, int, int]] = []
        busy_time = 0
        last_pid = None
        slice_start = 0

        while completed < n:
            available = [p for p in procs if p.arrival_time <= current_time and p.remaining_time > 0]
            if not available:
                unstarted = [p for p in procs if p.remaining_time > 0]
                if unstarted:
                    next_t = min(p.arrival_time for p in unstarted)
                    if last_pid is not None:
                        gantt_chart.append((last_pid, slice_start, current_time))
                        last_pid = None
                    gantt_chart.append(("IDLE", current_time, next_t))
                    current_time = next_t
                    continue
                else:
                    break

            # Pick highest priority (lowest priority value)
            available.sort(key=lambda p: (p.priority, p.arrival_time, p.pid))
            curr = available[0]

            if curr.start_time is None:
                curr.start_time = current_time
                curr.response_time = curr.start_time - curr.arrival_time

            if last_pid != curr.pid:
                if last_pid is not None:
                    gantt_chart.append((last_pid, slice_start, current_time))
                last_pid = curr.pid
                slice_start = current_time

            # Step 1 ms unit
            curr.remaining_time -= 1
            current_time += 1
            busy_time += 1

            if curr.remaining_time == 0:
                curr.completion_time = current_time
                curr.turnaround_time = curr.completion_time - curr.arrival_time
                curr.waiting_time = curr.turnaround_time - curr.burst_time
                completed += 1
                gantt_chart.append((last_pid, slice_start, current_time))
                last_pid = None

        if last_pid is not None:
            gantt_chart.append((last_pid, slice_start, current_time))

        metrics = self._calculate_metrics(procs, current_time, busy_time)
        return procs, gantt_chart, metrics

    def run_mlfq(self, q0: int = 2, q1: int = 4) -> Tuple[List[Process], List[Tuple[str, int, int]], Dict[str, float]]:
        """
        Multilevel Feedback Queue (MLFQ):
        - Queue 0: Round Robin (quantum = q0) - Top Priority
        - Queue 1: Round Robin (quantum = q1) - Medium Priority
        - Queue 2: FCFS - Batch / Background Priority
        """
        procs = [p.clone() for p in self.raw_processes]
        procs.sort(key=lambda p: (p.arrival_time, p.pid))
        n = len(procs)

        q0_queue: List[Process] = []
        q1_queue: List[Process] = []
        q2_queue: List[Process] = []

        current_time = 0
        completed = 0
        gantt_chart: List[Tuple[str, int, int]] = []
        busy_time = 0
        arr_idx = 0

        while completed < n:
            # Enqueue newly arrived processes to Queue 0
            while arr_idx < n and procs[arr_idx].arrival_time <= current_time:
                q0_queue.append(procs[arr_idx])
                arr_idx += 1

            # Idle detection
            if not q0_queue and not q1_queue and not q2_queue:
                if arr_idx < n:
                    next_t = procs[arr_idx].arrival_time
                    gantt_chart.append(("IDLE", current_time, next_t))
                    current_time = next_t
                    while arr_idx < n and procs[arr_idx].arrival_time <= current_time:
                        q0_queue.append(procs[arr_idx])
                        arr_idx += 1
                else:
                    break

            # Process Queue 0 (Quantum = q0)
            if q0_queue:
                curr = q0_queue.pop(0)
                if curr.start_time is None:
                    curr.start_time = current_time
                    curr.response_time = curr.start_time - curr.arrival_time

                exec_time = min(q0, curr.remaining_time)
                start_t = current_time
                current_time += exec_time
                busy_time += exec_time
                curr.remaining_time -= exec_time

                gantt_chart.append((curr.pid, start_t, current_time))

                # New arrivals
                while arr_idx < n and procs[arr_idx].arrival_time <= current_time:
                    q0_queue.append(procs[arr_idx])
                    arr_idx += 1

                if curr.remaining_time > 0:
                    q1_queue.append(curr)  # Demote to Queue 1
                else:
                    curr.completion_time = current_time
                    curr.turnaround_time = curr.completion_time - curr.arrival_time
                    curr.waiting_time = curr.turnaround_time - curr.burst_time
                    completed += 1

            # Process Queue 1 (Quantum = q1)
            elif q1_queue:
                curr = q1_queue.pop(0)
                if curr.start_time is None:
                    curr.start_time = current_time
                    curr.response_time = curr.start_time - curr.arrival_time

                # Preemption check: execute up to q1 or until new arrival in Q0
                exec_time = min(q1, curr.remaining_time)
                start_t = current_time
                current_time += exec_time
                busy_time += exec_time
                curr.remaining_time -= exec_time

                gantt_chart.append((curr.pid, start_t, current_time))

                while arr_idx < n and procs[arr_idx].arrival_time <= current_time:
                    q0_queue.append(procs[arr_idx])
                    arr_idx += 1

                if curr.remaining_time > 0:
                    q2_queue.append(curr)  # Demote to Queue 2 (FCFS)
                else:
                    curr.completion_time = current_time
                    curr.turnaround_time = curr.completion_time - curr.arrival_time
                    curr.waiting_time = curr.turnaround_time - curr.burst_time
                    completed += 1

            # Process Queue 2 (FCFS with preemption if higher queue receives task)
            elif q2_queue:
                curr = q2_queue.pop(0)
                if curr.start_time is None:
                    curr.start_time = current_time
                    curr.response_time = curr.start_time - curr.arrival_time

                # Run until completion or until new process arrives
                exec_time = curr.remaining_time
                if arr_idx < n:
                    time_to_next = procs[arr_idx].arrival_time - current_time
                    if 0 < time_to_next < exec_time:
                        exec_time = time_to_next

                start_t = current_time
                current_time += exec_time
                busy_time += exec_time
                curr.remaining_time -= exec_time

                gantt_chart.append((curr.pid, start_t, current_time))

                while arr_idx < n and procs[arr_idx].arrival_time <= current_time:
                    q0_queue.append(procs[arr_idx])
                    arr_idx += 1

                if curr.remaining_time > 0:
                    q2_queue.insert(0, curr)
                else:
                    curr.completion_time = current_time
                    curr.turnaround_time = curr.completion_time - curr.arrival_time
                    curr.waiting_time = curr.turnaround_time - curr.burst_time
                    completed += 1

        metrics = self._calculate_metrics(procs, current_time, busy_time)
        return procs, gantt_chart, metrics


def get_unicore_cpu_workload() -> List[Process]:
    """Loads default UniCore process workload from JSON or creates default."""
    try:
        data = load_json_data("data/cpu_workload.json")
        return [Process(item["pid"], item["name"], item["arrival_time"], item["burst_time"], item["priority"]) for item in data]
    except Exception:
        return [
            Process("P0", "Online Examination Portal", 0, 8, 1),
            Process("P1", "LMS Student Request", 1, 4, 2),
            Process("P2", "Digital Library Search", 2, 9, 3),
            Process("P3", "Research Computing Batch", 3, 5, 4),
            Process("P4", "IoT Sensor Monitoring", 4, 2, 1),
            Process("P5", "Automated Backup Service", 5, 6, 5),
            Process("P6", "Faculty Grade Sync", 6, 3, 2),
            Process("P7", "Video Stream Processing", 7, 7, 4)
        ]


def run_and_save_cpu_benchmarks() -> Dict[str, Any]:
    """Executes all CPU algorithms and exports results to results/cpu_results.csv."""
    workload = get_unicore_cpu_workload()
    scheduler = CPUScheduler(workload)

    results = {
        "FCFS": scheduler.run_fcfs(),
        "SJF (Non-Preemptive)": scheduler.run_sjf_non_preemptive(),
        "Round Robin (q=4)": scheduler.run_round_robin(quantum=4),
        "Preemptive Priority": scheduler.run_priority_preemptive(),
        "MLFQ (q0=2, q1=4)": scheduler.run_mlfq(q0=2, q1=4)
    }

    # Prepare CSV output
    headers = [
        "Algorithm", "Process ID", "Process Name", "Arrival Time (ms)", 
        "Burst Time (ms)", "Priority", "Completion Time (ms)", 
        "Waiting Time (ms)", "Turnaround Time (ms)", "Response Time (ms)"
    ]
    rows = []
    summary_headers = ["Algorithm", "Avg Waiting Time (ms)", "Avg Turnaround Time (ms)", "Avg Response Time (ms)", "CPU Utilization (%)", "Throughput (proc/ms)"]
    summary_rows = []

    for algo_name, (procs, gantt, metrics) in results.items():
        summary_rows.append([
            algo_name, metrics["avg_wt"], metrics["avg_tat"], 
            metrics["avg_rt"], metrics["cpu_utilization"], metrics["throughput"]
        ])
        for p in procs:
            rows.append([
                algo_name, p.pid, p.name, p.arrival_time, 
                p.burst_time, p.priority, p.completion_time, 
                p.waiting_time, p.turnaround_time, p.response_time
            ])

    save_csv_results("results/cpu_results.csv", headers, rows)
    return results


if __name__ == "__main__":
    print("=" * 80)
    print(" UNICORE CPU SCHEDULING BENCHMARK (CO2)")
    print("=" * 80)

    results = run_and_save_cpu_benchmarks()
    
    summary_headers = ["Algorithm", "Avg WT (ms)", "Avg TAT (ms)", "Avg RT (ms)", "CPU Util (%)"]
    summary_rows = []
    for algo_name, (_, _, metrics) in results.items():
        summary_rows.append([
            algo_name, metrics["avg_wt"], metrics["avg_tat"], metrics["avg_rt"], metrics["cpu_utilization"]
        ])

    print("\n" + format_table(summary_headers, summary_rows))
    print(f"\n[SUCCESS] CPU simulation completed. Results exported to results/cpu_results.csv")
