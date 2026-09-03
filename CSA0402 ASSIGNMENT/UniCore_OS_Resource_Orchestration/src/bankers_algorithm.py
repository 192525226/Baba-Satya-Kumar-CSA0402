"""
Banker's Deadlock Avoidance Algorithm Simulator for UniCore Smart University Platform
Course: CSA04 Operating Systems (CO2)

Models 8 processes competing for 4 critical university resource types:
- R1: Database Connections (Total = 10)
- R2: Exam Record File Locks (Total = 6)
- R3: Compute / GPU Cores (Total = 8)
- R4: Disk I/O Channels (Total = 7)

Features:
- Matrix calculations: Allocation, Maximum, Need = Max - Allocation, Available
- Step-by-step safety sequence verification (Work vector updates)
- Resource-Request Algorithm with automatic rollback upon unsafe state
- Adverse scenario simulation: Proves rejection of unsafe requests
- Exports detailed trace to results/bankers_results.txt
"""

from typing import List, Tuple, Dict, Optional, Any
import copy
import os
import sys

# Support relative and standalone imports
try:
    from .utils import load_json_data, save_text_results, format_table
except ImportError:
    from utils import load_json_data, save_text_results, format_table


class BankersAlgorithm:
    def __init__(
        self,
        process_names: List[str],
        resource_names: List[str],
        total_resources: List[int],
        allocation: List[List[int]],
        max_matrix: List[List[int]],
    ):
        self.process_names = list(process_names)
        self.resource_names = list(resource_names)
        self.total_resources = list(total_resources)
        self.num_processes = len(process_names)
        self.num_resources = len(resource_names)

        self.allocation = copy.deepcopy(allocation)
        self.max_matrix = copy.deepcopy(max_matrix)
        self.need = self.compute_need()
        self.available = self.compute_available()

    def clone(self) -> 'BankersAlgorithm':
        return BankersAlgorithm(
            self.process_names,
            self.resource_names,
            self.total_resources,
            self.allocation,
            self.max_matrix
        )

    def compute_need(self) -> List[List[int]]:
        """Need[i][j] = Max[i][j] - Allocation[i][j]"""
        need = []
        for i in range(self.num_processes):
            row = []
            for j in range(self.num_resources):
                val = self.max_matrix[i][j] - self.allocation[i][j]
                if val < 0:
                    raise ValueError(f"Invalid state: Allocation exceeds Max for process {self.process_names[i]}, resource {self.resource_names[j]}")
                row.append(val)
            need.append(row)
        return need

    def compute_available(self) -> List[int]:
        """Available[j] = Total[j] - Sum(Allocation[i][j] for all i)"""
        avail = list(self.total_resources)
        for j in range(self.num_resources):
            allocated_sum = sum(self.allocation[i][j] for i in range(self.num_processes))
            avail[j] -= allocated_sum
            if avail[j] < 0:
                raise ValueError(f"Resource {self.resource_names[j]} over-allocated! Available would be negative ({avail[j]})")
        return avail

    def is_safe_state(self, verbose: bool = False) -> Tuple[bool, List[str], List[Dict[str, Any]]]:
        """
        Banker's Safety Algorithm:
        Returns (is_safe, safe_sequence, step_by_step_trace).
        """
        work = list(self.available)
        finish = [False] * self.num_processes
        safe_sequence = []
        trace = []

        step = 0
        while len(safe_sequence) < self.num_processes:
            found = False
            for i in range(self.num_processes):
                if not finish[i]:
                    # Check if Need[i] <= Work
                    need_i = self.need[i]
                    if all(need_i[j] <= work[j] for j in range(self.num_resources)):
                        step += 1
                        old_work = list(work)
                        # Work = Work + Allocation[i]
                        for j in range(self.num_resources):
                            work[j] += self.allocation[i][j]
                        finish[i] = True
                        p_name = self.process_names[i]
                        safe_sequence.append(p_name)
                        found = True

                        step_info = {
                            "step": step,
                            "process": p_name,
                            "need": need_i,
                            "work_before": old_work,
                            "allocation": self.allocation[i],
                            "work_after": list(work),
                            "finish_state": list(finish)
                        }
                        trace.append(step_info)
                        break

            if not found:
                # Deadlock / Unsafe state detected
                break

        is_safe = (len(safe_sequence) == self.num_processes)
        return is_safe, safe_sequence, trace

    def request_resources(self, process_idx: int, request: List[int]) -> Tuple[bool, str, List[Dict[str, Any]]]:
        """
        Banker's Resource-Request Algorithm:
        1. Check if Request <= Need
        2. Check if Request <= Available
        3. Pretend to allocate and check if state remains safe.
        4. If safe -> Grant; If unsafe -> Rollback and Reject/Delay.
        """
        p_name = self.process_names[process_idx]

        # 1. Check Request <= Need
        for j in range(self.num_resources):
            if request[j] > self.need[process_idx][j]:
                return False, f"ERROR: Process {p_name} exceeded its declared maximum claim (Request {request} > Need {self.need[process_idx]})", []

        # 2. Check Request <= Available
        for j in range(self.num_resources):
            if request[j] > self.available[j]:
                return False, f"WAIT: Process {p_name} must wait because resources are unavailable (Request {request} > Available {self.available})", []

        # 3. Tentative Allocation
        tentative = self.clone()
        for j in range(self.num_resources):
            tentative.available[j] -= request[j]
            tentative.allocation[process_idx][j] += request[j]
            tentative.need[process_idx][j] -= request[j]

        # 4. Safety Check
        is_safe, seq, trace = tentative.is_safe_state(verbose=False)
        if is_safe:
            # Commit changes
            self.available = tentative.available
            self.allocation = tentative.allocation
            self.need = tentative.need
            return True, f"SUCCESS: Request granted for {p_name}. System remains in safe state. Safe Sequence: {' -> '.join(seq)}", trace
        else:
            return False, f"REJECTED/DELAYED: Request from {p_name} would lead to an UNSAFE STATE (Deadlock vulnerability). Transaction rolled back.", trace

    def format_matrix_tables(self) -> str:
        headers = ["Process", "Allocation (R1-R4)", "Max Claim (R1-R4)", "Need (R1-R4)"]
        rows = []
        for i in range(self.num_processes):
            alloc_str = f"[{', '.join(str(x) for x in self.allocation[i])}]"
            max_str = f"[{', '.join(str(x) for x in self.max_matrix[i])}]"
            need_str = f"[{', '.join(str(x) for x in self.need[i])}]"
            rows.append([self.process_names[i], alloc_str, max_str, need_str])

        out = format_table(headers, rows)
        out += f"\n\nTotal System Resources : [{', '.join(str(x) for x in self.total_resources)}]"
        out += f"\nInitial Available Vector: [{', '.join(str(x) for x in self.available)}]"
        return out


def get_unicore_banker_instance() -> BankersAlgorithm:
    """Loads Banker configuration from JSON data or creates standard instance."""
    try:
        data = load_json_data("data/banker_resources.json")
        return BankersAlgorithm(
            data["process_names"],
            data["resource_names"],
            data["total_resources"],
            data["allocation"],
            data["max_matrix"]
        )
    except Exception:
        process_names = [
            "P0: Exam Submission Svc", "P1: Student Auth Portal", "P2: Library Query Engine", 
            "P3: AI Research Sim", "P4: Campus IoT Ingest", "P5: System Backup Daemon", 
            "P6: Auto-Grading Worker", "P7: Lecture Stream Engine"
        ]
        resource_names = ["R1 (DB)", "R2 (Lock)", "R3 (GPU)", "R4 (IO)"]
        total_resources = [10, 6, 8, 7]
        allocation = [
            [2, 1, 1, 1],
            [1, 0, 1, 0],
            [1, 1, 0, 1],
            [1, 0, 2, 1],
            [1, 0, 0, 2],
            [1, 1, 1, 0],
            [1, 1, 1, 0],
            [1, 0, 0, 1]
        ]
        max_matrix = [
            [3, 2, 2, 2],
            [2, 1, 1, 1],
            [2, 2, 1, 2],
            [4, 2, 4, 3],
            [2, 1, 1, 3],
            [3, 2, 2, 1],
            [2, 2, 2, 1],
            [3, 1, 1, 2]
        ]
        return BankersAlgorithm(process_names, resource_names, total_resources, allocation, max_matrix)


def run_and_save_bankers_results() -> str:
    banker = get_unicore_banker_instance()
    lines = []
    lines.append("=" * 84)
    lines.append(" UNICORE BANKER'S DEADLOCK AVOIDANCE & SAFETY ANALYSIS (CO2)")
    lines.append("=" * 84)
    lines.append("\n--- Initial Resource & Process Allocation Matrices ---\n")
    lines.append(banker.format_matrix_tables())

    # Step 1: Safety Evaluation
    lines.append("\n" + "=" * 84)
    lines.append(" STEP 1: SAFETY ALGORITHM EXECUTION ON INITIAL STATE")
    lines.append("=" * 84)

    is_safe, safe_seq, trace = banker.is_safe_state()
    lines.append(f"System State: {'SAFE' if is_safe else 'UNSAFE'}")
    lines.append(f"Initial Work Vector = [{', '.join(str(x) for x in banker.available)}]")
    lines.append("\nStep-by-Step Execution Sequence:")
    
    trace_headers = ["Step", "Process Selected", "Need Vector", "Work Before", "Allocation Added", "Work After"]
    trace_rows = []
    for item in trace:
        trace_rows.append([
            f"Step {item['step']}",
            item["process"],
            f"[{', '.join(str(x) for x in item['need'])}]",
            f"[{', '.join(str(x) for x in item['work_before'])}]",
            f"[{', '.join(str(x) for x in item['allocation'])}]",
            f"[{', '.join(str(x) for x in item['work_after'])}]"
        ])
    lines.append(format_table(trace_headers, trace_rows))
    lines.append(f"\nFinal Safe Execution Sequence:\n{' -> '.join(safe_seq)}")

    # Step 2: Adverse Unsafe Request Test
    lines.append("\n" + "=" * 84)
    lines.append(" STEP 2: ADVERSE UNSAFE RESOURCE-REQUEST EVALUATION")
    lines.append("=" * 84)
    adverse_pid = 3  # P3
    adverse_req = [1, 2, 0, 0]
    lines.append(f"Scenario: Process {banker.process_names[adverse_pid]} requests additional resources: {adverse_req}")
    lines.append(f"Current Available: {banker.available}")
    lines.append(f"Process Need: {banker.need[adverse_pid]}")

    test_banker = banker.clone()
    granted, msg, adv_trace = test_banker.request_resources(adverse_pid, adverse_req)
    lines.append(f"\nDecision: {'GRANTED' if granted else 'REJECTED / SUSPENDED'}")
    lines.append(f"Details: {msg}")

    # Step 3: Valid Safe Request Test
    lines.append("\n" + "=" * 84)
    lines.append(" STEP 3: BENIGN SAFE RESOURCE-REQUEST EVALUATION")
    lines.append("=" * 84)
    safe_pid = 1  # P1
    safe_req = [1, 0, 0, 1]
    lines.append(f"Scenario: Process {banker.process_names[safe_pid]} requests additional resources: {safe_req}")
    test_banker_safe = banker.clone()
    granted_safe, msg_safe, _ = test_banker_safe.request_resources(safe_pid, safe_req)
    lines.append(f"Decision: {'GRANTED' if granted_safe else 'REJECTED'}")
    lines.append(f"Details: {msg_safe}")

    full_output = "\n".join(lines)
    save_text_results("results/bankers_results.txt", full_output)
    return full_output


if __name__ == "__main__":
    out = run_and_save_bankers_results()
    print(out)
    print("\n[SUCCESS] Banker's algorithm verified. Results exported to results/bankers_results.txt")
