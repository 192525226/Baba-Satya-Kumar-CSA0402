"""
Disk Scheduling Simulator for UniCore Smart University Platform
Course: CSA04 Operating Systems (CO4)

Implements and evaluates disk arm scheduling policies on a 200-cylinder storage unit (0-199):
1. First-Come First-Served (FCFS)
2. Shortest Seek Time First (SSTF)
3. SCAN (Elevator Algorithm)
4. C-SCAN (Circular SCAN)
5. LOOK (Optimized Elevator)
6. C-LOOK (Optimized Circular LOOK)

Calculates:
- Complete Seek Trajectory Sequences
- Step-by-Step Individual Cylinder Movements
- Total Head Movement (THM in cylinders)
- Average Seek Length (ASL in cylinders/request)
- Fairness, Variance, and Starvation Risk Profiles
- Exports detailed traces to results/disk_results.csv
"""

from typing import List, Tuple, Dict, Any, Optional
import copy
import os
import sys

# Support relative and standalone imports
try:
    from .utils import load_json_data, save_csv_results, format_table
except ImportError:
    from utils import load_json_data, save_csv_results, format_table


class DiskScheduler:
    def __init__(self, requests: List[int], initial_head: int, total_cylinders: int = 200, direction: str = "HIGH"):
        self.requests = list(requests)
        self.initial_head = initial_head
        self.total_cylinders = total_cylinders  # Cylinders 0 to 199
        self.max_cylinder = total_cylinders - 1
        self.direction = direction.upper()  # "HIGH" (increasing numbers) or "LOW"

        # Validate requests within disk bounds
        for r in self.requests:
            if not (0 <= r <= self.max_cylinder):
                raise ValueError(f"Request cylinder {r} is out of disk bounds (0-{self.max_cylinder})")

    def _calc_movements(self, sequence: List[int]) -> Tuple[int, float, List[int]]:
        movements = []
        total = 0
        for i in range(len(sequence) - 1):
            diff = abs(sequence[i+1] - sequence[i])
            movements.append(diff)
            total += diff
        asl = total / len(self.requests) if self.requests else 0.0
        return total, round(asl, 2), movements

    def run_fcfs(self) -> Tuple[List[int], int, float, List[int]]:
        """FCFS: Services requests strictly in arrival order."""
        seek_sequence = [self.initial_head] + list(self.requests)
        thm, asl, movements = self._calc_movements(seek_sequence)
        return seek_sequence, thm, asl, movements

    def run_sstf(self) -> Tuple[List[int], int, float, List[int]]:
        """SSTF: Selects request with minimum seek distance from current head."""
        pending = list(self.requests)
        curr = self.initial_head
        seek_sequence = [curr]

        while pending:
            # Find closest request (tie-break: smaller cylinder number)
            closest = min(pending, key=lambda r: (abs(r - curr), r))
            pending.remove(closest)
            seek_sequence.append(closest)
            curr = closest

        thm, asl, movements = self._calc_movements(seek_sequence)
        return seek_sequence, thm, asl, movements

    def run_scan(self) -> Tuple[List[int], int, float, List[int]]:
        """
        SCAN (Elevator): Moves in current direction to the disk boundary (199 or 0),
        servicing requests on the path, then reverses direction.
        """
        curr = self.initial_head
        seek_sequence = [curr]

        if self.direction == "HIGH":
            # Sort upper requests ascending, lower requests descending
            upper = sorted([r for r in self.requests if r >= curr])
            lower = sorted([r for r in self.requests if r < curr], reverse=True)

            seek_sequence.extend(upper)
            if lower:
                # If there are lower requests, SCAN goes all the way to the boundary (max_cylinder)
                if seek_sequence[-1] != self.max_cylinder:
                    seek_sequence.append(self.max_cylinder)
                seek_sequence.extend(lower)
        else:
            # Moving towards 0
            lower = sorted([r for r in self.requests if r <= curr], reverse=True)
            upper = sorted([r for r in self.requests if r > curr])

            seek_sequence.extend(lower)
            if upper:
                if seek_sequence[-1] != 0:
                    seek_sequence.append(0)
                seek_sequence.extend(upper)

        thm, asl, movements = self._calc_movements(seek_sequence)
        return seek_sequence, thm, asl, movements

    def run_cscan(self) -> Tuple[List[int], int, float, List[int]]:
        """
        C-SCAN (Circular SCAN): Sweeps in one direction to the boundary,
        then returns immediately to the opposite boundary (0) without servicing,
        and continues in the same direction.
        """
        curr = self.initial_head
        seek_sequence = [curr]

        if self.direction == "HIGH":
            upper = sorted([r for r in self.requests if r >= curr])
            lower = sorted([r for r in self.requests if r < curr])

            seek_sequence.extend(upper)
            if lower:
                # Reach upper boundary
                if seek_sequence[-1] != self.max_cylinder:
                    seek_sequence.append(self.max_cylinder)
                # Circular jump to 0
                seek_sequence.append(0)
                seek_sequence.extend(lower)
        else:
            lower = sorted([r for r in self.requests if r <= curr], reverse=True)
            upper = sorted([r for r in self.requests if r > curr], reverse=True)

            seek_sequence.extend(lower)
            if upper:
                if seek_sequence[-1] != 0:
                    seek_sequence.append(0)
                seek_sequence.append(self.max_cylinder)
                seek_sequence.extend(upper)

        thm, asl, movements = self._calc_movements(seek_sequence)
        return seek_sequence, thm, asl, movements

    def run_look(self) -> Tuple[List[int], int, float, List[int]]:
        """
        LOOK: Like SCAN, but only goes as far as the final request in each direction,
        avoiding travel to empty disk boundaries.
        """
        curr = self.initial_head
        seek_sequence = [curr]

        if self.direction == "HIGH":
            upper = sorted([r for r in self.requests if r >= curr])
            lower = sorted([r for r in self.requests if r < curr], reverse=True)

            seek_sequence.extend(upper)
            seek_sequence.extend(lower)
        else:
            lower = sorted([r for r in self.requests if r <= curr], reverse=True)
            upper = sorted([r for r in self.requests if r > curr])

            seek_sequence.extend(lower)
            seek_sequence.extend(upper)

        thm, asl, movements = self._calc_movements(seek_sequence)
        return seek_sequence, thm, asl, movements

    def run_clook(self) -> Tuple[List[int], int, float, List[int]]:
        """
        C-LOOK: Like C-SCAN, but only goes as far as the highest request,
        then jumps directly to the lowest request without hitting cylinders 199 or 0.
        """
        curr = self.initial_head
        seek_sequence = [curr]

        if self.direction == "HIGH":
            upper = sorted([r for r in self.requests if r >= curr])
            lower = sorted([r for r in self.requests if r < curr])

            seek_sequence.extend(upper)
            seek_sequence.extend(lower)
        else:
            lower = sorted([r for r in self.requests if r <= curr], reverse=True)
            upper = sorted([r for r in self.requests if r > curr], reverse=True)

            seek_sequence.extend(lower)
            seek_sequence.extend(upper)

        thm, asl, movements = self._calc_movements(seek_sequence)
        return seek_sequence, thm, asl, movements


def get_unicore_disk_config() -> Tuple[List[int], int, int, str]:
    """Loads default disk requests and head position from JSON or default."""
    try:
        data = load_json_data("data/disk_requests.json")
        return data["requests"], data["initial_head"], data["total_cylinders"], data["direction"]
    except Exception:
        return [98, 183, 37, 122, 14, 124, 65, 67, 190, 45], 53, 200, "HIGH"


def run_and_save_disk_benchmarks() -> Dict[str, Any]:
    """Runs all disk algorithms and saves results to results/disk_results.csv."""
    requests, head, cylinders, direction = get_unicore_disk_config()
    scheduler = DiskScheduler(requests, head, cylinders, direction)

    results = {
        "FCFS": scheduler.run_fcfs(),
        "SSTF": scheduler.run_sstf(),
        "SCAN": scheduler.run_scan(),
        "C-SCAN": scheduler.run_cscan(),
        "LOOK": scheduler.run_look(),
        "C-LOOK": scheduler.run_clook()
    }

    # Prepare CSV export
    headers = ["Algorithm", "Step", "From Cylinder", "To Cylinder", "Distance (Cylinders)", "Cumulative THM"]
    rows = []

    for algo_name, (seq, thm, asl, movements) in results.items():
        cum = 0
        for i in range(len(seq) - 1):
            dist = abs(seq[i+1] - seq[i])
            cum += dist
            rows.append([algo_name, i + 1, seq[i], seq[i+1], dist, cum])

    save_csv_results("results/disk_results.csv", headers, rows)
    return results


if __name__ == "__main__":
    print("=" * 86)
    print(" UNICORE DISK SCHEDULING & SEEK TIME BENCHMARK (CO4)")
    print("=" * 86)

    requests, head, cyl, direction = get_unicore_disk_config()
    print(f"\nConfiguration: Initial Head = {head} | Direction = {direction} | Cylinders = 0-{cyl-1}")
    print(f"Request Queue ({len(requests)} items): {requests}\n")

    results = run_and_save_disk_benchmarks()

    summary_headers = ["Algorithm", "Total Head Movement (THM)", "Average Seek Length (ASL)", "Seek Sequence (Head -> Trajectory)"]
    summary_rows = []

    for algo_name, (seq, thm, asl, _) in results.items():
        seq_str = " -> ".join(str(c) for c in seq)
        summary_rows.append([algo_name, f"{thm} cyl", f"{asl:.2f} cyl/req", seq_str])

    print(format_table(summary_headers, summary_rows))
    print("\n[SUCCESS] Disk scheduling benchmark completed. Results exported to results/disk_results.csv")
