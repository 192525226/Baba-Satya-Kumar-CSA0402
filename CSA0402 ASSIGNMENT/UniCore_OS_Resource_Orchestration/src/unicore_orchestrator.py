"""
UniCore: Master OS Resource Orchestration System
Course: CSA04 Operating Systems (CO2, CO3, CO4)

Design and Analysis of an OS Resource Orchestration System for a Smart University.

Integrates the full operational pipeline:
1. Process Management & CPU Scheduling (CO2)
2. Classical Synchronization: Fair Readers-Writers Exam Record Monitor (CO2)
3. Deadlock Avoidance: Banker's Safety Algorithm & Adverse Request Rejection (CO2)
4. Virtual Memory Management: Hardware Sizing, Page Replacement & Thrashing Control (CO3)
5. File Systems: Allocation Strategies & Inode In-Memory Cache (CO4)
6. Disk Scheduling: 200-Cylinder Seek Optimization & Fairness (CO4)
7. Automatic Export of CSV/TXT Results and High-Res Visual Diagrams

Usage:
    python src/unicore_orchestrator.py
"""

import sys
import os
import time
from typing import Dict, Any

# Ensure local imports work seamlessly
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from cpu_scheduler import run_and_save_cpu_benchmarks, get_unicore_cpu_workload, CPUScheduler
from synchronization import UniCoreSynchronizationSimulator
from bankers_algorithm import run_and_save_bankers_results, get_unicore_banker_instance
from page_replacement import run_and_save_memory_benchmarks, VirtualMemoryHardware, simulate_working_set_and_thrashing
from file_allocation import run_file_allocation_analysis
from disk_scheduler import run_and_save_disk_benchmarks, get_unicore_disk_config
from generate_figures import generate_all_figures
from utils import save_text_results, format_table


class UniCoreOrchestrator:
    def __init__(self):
        self.log_lines = []

    def log(self, text: str = ""):
        print(text)
        self.log_lines.append(text)

    def run_full_orchestration(self):
        start_time = time.time()
        self.log("=" * 86)
        self.log(" UNICORE: OS RESOURCE ORCHESTRATION SYSTEM FOR SMART UNIVERSITY PLATFORMS")
        self.log(" Course: CSA04 Operating Systems | Comprehensive CO2, CO3, CO4 Verification")
        self.log("=" * 86 + "\n")

        # ---------------------------------------------------------
        # MODULE 1: CPU SCHEDULING & PROCESS MANAGEMENT (CO2)
        # ---------------------------------------------------------
        self.log("#" * 86)
        self.log(" [1/6] PROCESS MANAGEMENT & CPU SCHEDULING ORCHESTRATION (CO2)")
        self.log("#" * 86)
        
        cpu_results = run_and_save_cpu_benchmarks()
        cpu_headers = ["Algorithm", "Avg WT (ms)", "Avg TAT (ms)", "Avg RT (ms)", "CPU Util (%)", "Throughput (p/ms)"]
        cpu_rows = []
        for algo_name, (_, _, m) in cpu_results.items():
            cpu_rows.append([algo_name, m["avg_wt"], m["avg_tat"], m["avg_rt"], m["cpu_utilization"], m["throughput"]])

        self.log(format_table(cpu_headers, cpu_rows))
        self.log("[INFO] CPU benchmark data saved to results/cpu_results.csv\n")

        # ---------------------------------------------------------
        # MODULE 2: CONCURRENCY & READERS-WRITERS SYNCHRONIZATION (CO2)
        # ---------------------------------------------------------
        self.log("#" * 86)
        self.log(" [2/6] CONCURRENT EXAM RECORD READERS-WRITERS SYNCHRONIZATION (CO2)")
        self.log("#" * 86)

        sync_sim = UniCoreSynchronizationSimulator()
        sync_trace = sync_sim.run_simulation()
        self.log(f"[INFO] Concurrency trace saved to results/synchronization_results.txt\n")

        # ---------------------------------------------------------
        # MODULE 3: DEADLOCK AVOIDANCE & BANKER'S ALGORITHM (CO2)
        # ---------------------------------------------------------
        self.log("#" * 86)
        self.log(" [3/6] DEADLOCK AVOIDANCE & BANKER'S ALGORITHM VERIFICATION (CO2)")
        self.log("#" * 86)

        banker_output = run_and_save_bankers_results()
        self.log(banker_output)
        self.log("[INFO] Banker's algorithm verification trace saved to results/bankers_results.txt\n")

        # ---------------------------------------------------------
        # MODULE 4: VIRTUAL MEMORY & PAGE REPLACEMENT (CO3)
        # ---------------------------------------------------------
        self.log("#" * 86)
        self.log(" [4/6] VIRTUAL MEMORY SIZING & PAGE REPLACEMENT BENCHMARK (CO3)")
        self.log("#" * 86)

        vm_hw = VirtualMemoryHardware(ram_gb=16.0, page_kb=4.0, logical_mb=64.0)
        self.log(f"• Physical Memory Sizing : 16 GB RAM -> {vm_hw.num_physical_frames:,} Frames (34-bit PA)")
        self.log(f"• Logical Address Space  : 64 MB -> {vm_hw.num_logical_pages:,} Pages (26-bit LA)")
        self.log(f"• Page Table Organization: Two-Level Hierarchical Paging (14-bit Page # = 7-bit P1 + 7-bit P2)")
        self.log(f"• EMAT (95% TLB Hit)     : {vm_hw.calculate_emat(0.95)} ns\n")

        mem_res = run_and_save_memory_benchmarks()
        n_refs = len(mem_res["ref_string"])
        mem_headers = ["Algorithm", "3-Frame Faults", "3-Frame Hit %", "4-Frame Faults", "4-Frame Hit %"]
        mem_rows = [
            ["FIFO", mem_res["fifo"]["3_frames"][0], f"{(mem_res['fifo']['3_frames'][1]/n_refs)*100:.1f}%", mem_res["fifo"]["4_frames"][0], f"{(mem_res['fifo']['4_frames'][1]/n_refs)*100:.1f}%"],
            ["LRU", mem_res["lru"]["3_frames"][0], f"{(mem_res['lru']['3_frames'][1]/n_refs)*100:.1f}%", mem_res["lru"]["4_frames"][0], f"{(mem_res['lru']['4_frames'][1]/n_refs)*100:.1f}%"],
            ["Optimal", mem_res["optimal"]["3_frames"][0], f"{(mem_res['optimal']['3_frames'][1]/n_refs)*100:.1f}%", mem_res["optimal"]["4_frames"][0], f"{(mem_res['optimal']['4_frames'][1]/n_refs)*100:.1f}%"]
        ]
        self.log(format_table(mem_headers, mem_rows))

        thrash_eval = simulate_working_set_and_thrashing(800)
        self.log(f"\n[Working-Set Analysis for 800 Concurrent Exam Takers]")
        self.log(f"Active Memory Demand: {thrash_eval['total_active_memory_mb']} MB | System Memory Pressure: {thrash_eval['memory_pressure_percent']}%")
        self.log(f"Assessment: {thrash_eval['recommendation']}")
        self.log("[INFO] Memory simulation data saved to results/memory_results.csv\n")

        # ---------------------------------------------------------
        # MODULE 5: FILE ALLOCATION & STORAGE ARCHITECTURE (CO4)
        # ---------------------------------------------------------
        self.log("#" * 86)
        self.log(" [5/6] FILE ALLOCATION STRATEGIES & INODE EVALUATION (CO4)")
        self.log("#" * 86)

        fa_results = run_file_allocation_analysis()
        fa_headers = ["Strategy", "Workload", "Size", "Blocks", "Random Access", "Overhead", "Suitability", "Verdict"]
        fa_rows = []
        for w_name, evals in fa_results.items():
            for e in evals:
                sz_str = f"{e.file_size_kb} KB" if e.file_size_kb < 1024 else f"{e.file_size_kb/1024:.1f} MB" if e.file_size_kb < 1048576 else f"{e.file_size_kb/(1024**2):.1f} GB"
                fa_rows.append([
                    e.method_name.replace(" (Unix Inode)", ""),
                    w_name, sz_str, e.num_blocks,
                    e.direct_access_complexity.split(" - ")[0],
                    f"{e.metadata_overhead_percent:.3f}%",
                    f"{e.suitability_score_out_of_10}/10",
                    e.recommendation_verdict[:32] + "..."
                ])
        self.log(format_table(fa_headers, fa_rows))
        self.log("\nStrategic Storage Decision: Unix Inode Indexed Allocation selected for all UniCore tiers.\n")

        # ---------------------------------------------------------
        # MODULE 6: DISK SCHEDULING ON 200 CYLINDERS (CO4)
        # ---------------------------------------------------------
        self.log("#" * 86)
        self.log(" [6/6] DISK SCHEDULING & SEEK TIME OPTIMIZATION (CO4)")
        self.log("#" * 86)

        disk_results = run_and_save_disk_benchmarks()
        disk_headers = ["Algorithm", "THM (Cylinders)", "Avg Seek Length", "Fairness / Starvation Profile"]
        disk_rows = [
            ["FCFS", f"{disk_results['FCFS'][1]} cyl", f"{disk_results['FCFS'][2]:.2f} cyl/req", "Fair arrival order, highly inefficient oscillation"],
            ["SSTF", f"{disk_results['SSTF'][1]} cyl", f"{disk_results['SSTF'][2]:.2f} cyl/req", "Lowest THM, but high starvation risk on outer cylinders"],
            ["SCAN", f"{disk_results['SCAN'][1]} cyl", f"{disk_results['SCAN'][2]:.2f} cyl/req", "Bidirectional elevator, moderate variance"],
            ["C-SCAN", f"{disk_results['C-SCAN'][1]} cyl", f"{disk_results['C-SCAN'][2]:.2f} cyl/req", "SELECTED: Uniform bounded latency across all cylinders"],
            ["LOOK", f"{disk_results['LOOK'][1]} cyl", f"{disk_results['LOOK'][2]:.2f} cyl/req", "Bounded elevator, avoids travel to empty disk limits"],
            ["C-LOOK", f"{disk_results['C-LOOK'][1]} cyl", f"{disk_results['C-LOOK'][2]:.2f} cyl/req", "Optimized circular sweep, zero boundary overhead"]
        ]
        self.log(format_table(disk_headers, disk_rows))
        self.log("[INFO] Disk scheduling benchmark data saved to results/disk_results.csv\n")

        # ---------------------------------------------------------
        # MODULE 7: FIGURE GENERATION
        # ---------------------------------------------------------
        self.log("#" * 86)
        self.log(" GENERATING PUBLICATION-QUALITY VECTOR FIGURES & CHARTS")
        self.log("#" * 86)
        generate_all_figures()

        elapsed = time.time() - start_time
        self.log("\n" + "=" * 86)
        self.log(f" UNICORE MASTER ORCHESTRATION PIPELINE COMPLETED IN {elapsed:.2f} SECONDS")
        self.log(" All empirical benchmark datasets and high-res figures exported successfully!")
        self.log("=" * 86 + "\n")

        # Save complete report
        save_text_results("results/integrated_results.txt", "\n".join(self.log_lines))


if __name__ == "__main__":
    orchestrator = UniCoreOrchestrator()
    orchestrator.run_full_orchestration()
