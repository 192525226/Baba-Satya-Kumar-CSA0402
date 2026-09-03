"""
File Allocation and Storage Architecture Simulator for UniCore Smart University Platform
Course: CSA04 Operating Systems (CO4)

Implements and evaluates the three classical file allocation strategies:
1. Contiguous Allocation
2. Linked Allocation
3. Indexed Allocation (Unix Inode-style with direct, single-indirect, and double-indirect blocks)

Evaluated across three representative university workloads:
- Workload A: Small Student Records (< 4 KB, 1-2 blocks)
- Workload B: Medium Academic Courseware Documents (500 KB - 5 MB, ~125 - 1,250 blocks)
- Workload C: Large Lecture Video Archives (500 MB - 2 GB, ~125,000 - 500,000 blocks)

Metrics Evaluated:
- Direct/Random Access Seek Complexity
- Sequential Access Seek Complexity
- External and Internal Fragmentation Vulnerability
- Metadata Overhead (bytes per file)
- Fault Tolerance / Link Failure Resilience
- Dynamic File Growth Scalability
"""

from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass
import math
import os
import sys

# Support relative and standalone imports
try:
    from .utils import format_table
except ImportError:
    from utils import format_table


@dataclass
class AllocationEvaluationResult:
    method_name: str
    workload_type: str
    file_size_kb: float
    num_blocks: int
    direct_access_complexity: str
    sequential_access_complexity: str
    metadata_overhead_bytes: int
    metadata_overhead_percent: float
    fragmentation_type: str
    dynamic_growth_support: str
    fault_tolerance: str
    suitability_score_out_of_10: int
    recommendation_verdict: str


class FileAllocationSimulator:
    def __init__(self, block_size_kb: float = 4.0, total_disk_blocks: int = 1000000):
        self.block_size_kb = block_size_kb
        self.block_size_bytes = int(block_size_kb * 1024)
        self.total_disk_blocks = total_disk_blocks

    def evaluate_contiguous(self, workload_name: str, file_size_kb: float) -> AllocationEvaluationResult:
        num_blocks = math.ceil(file_size_kb / self.block_size_kb)
        # Metadata: Start block (4 bytes) + Length (4 bytes) = 8 bytes
        metadata_bytes = 8
        overhead_pct = (metadata_bytes / (file_size_kb * 1024)) * 100.0

        if num_blocks <= 2:
            score = 8
            verdict = "Acceptable for read-only static records, but risky for updates."
        elif num_blocks <= 1500:
            score = 5
            verdict = "Poor due to heavy external fragmentation upon edits."
        else:
            score = 3
            verdict = "Unusable for large videos due to extreme continuous block allocation failures."

        return AllocationEvaluationResult(
            method_name="Contiguous Allocation",
            workload_type=workload_name,
            file_size_kb=file_size_kb,
            num_blocks=num_blocks,
            direct_access_complexity="O(1) - Single block offset calculation",
            sequential_access_complexity="O(1) - Contiguous track streaming",
            metadata_overhead_bytes=metadata_bytes,
            metadata_overhead_percent=round(overhead_pct, 4),
            fragmentation_type="Severe External Fragmentation + Compaction Overhead",
            dynamic_growth_support="Very Difficult (Requires reallocation/copying)",
            fault_tolerance="High (No pointer chains to corrupt)",
            suitability_score_out_of_10=score,
            recommendation_verdict=verdict
        )

    def evaluate_linked(self, workload_name: str, file_size_kb: float) -> AllocationEvaluationResult:
        # Each block uses 4 bytes for next-block pointer
        usable_block_bytes = self.block_size_bytes - 4
        num_blocks = math.ceil((file_size_kb * 1024) / usable_block_bytes)
        metadata_bytes = num_blocks * 4  # 4 bytes pointer per block
        overhead_pct = (metadata_bytes / (file_size_kb * 1024)) * 100.0

        if num_blocks <= 2:
            score = 6
            verdict = "Moderate for small files; pointer overhead is negligible."
        elif num_blocks <= 1500:
            score = 4
            verdict = "Inefficient: seeking page 800 requires 800 sequential disk reads."
        else:
            score = 2
            verdict = "Unacceptable for video streaming: video scrubbing requires massive pointer traversal."

        return AllocationEvaluationResult(
            method_name="Linked Allocation",
            workload_type=workload_name,
            file_size_kb=file_size_kb,
            num_blocks=num_blocks,
            direct_access_complexity=f"O(N) - Must traverse up to {num_blocks} pointer hops",
            sequential_access_complexity="O(1) per step - Follow pointer sequence",
            metadata_overhead_bytes=metadata_bytes,
            metadata_overhead_percent=round(overhead_pct, 4),
            fragmentation_type="Internal Fragmentation Only (No External)",
            dynamic_growth_support="Very Easy (Append block anywhere on free list)",
            fault_tolerance="Very Low (Single corrupted pointer breaks entire file remainder)",
            suitability_score_out_of_10=score,
            recommendation_verdict=verdict
        )

    def evaluate_indexed(self, workload_name: str, file_size_kb: float) -> AllocationEvaluationResult:
        """
        Unix Inode-style Indexed Allocation:
        - 12 Direct Pointers in Inode (covers up to 48 KB)
        - 1 Single-Indirect Pointer (index block holds 1024 pointers -> 4 MB)
        - 1 Double-Indirect Pointer (1024 * 1024 pointers -> 4 GB)
        """
        num_data_blocks = math.ceil(file_size_kb / self.block_size_kb)
        
        # Calculate Index block overhead
        pointers_per_index_block = self.block_size_bytes // 4  # 4096 / 4 = 1024 pointers
        
        index_blocks = 0
        if num_data_blocks <= 12:
            index_blocks = 0  # Contained inside inode
            metadata_bytes = 128  # Inode struct size
            access_complexity = "O(1) - Direct Inode table lookup"
        elif num_data_blocks <= 12 + pointers_per_index_block:
            index_blocks = 1  # 1 single indirect block
            metadata_bytes = 128 + (1 * self.block_size_bytes)
            access_complexity = "O(1) - 1 Indirect block memory lookup"
        else:
            remaining = num_data_blocks - (12 + pointers_per_index_block)
            second_level_blocks = math.ceil(remaining / pointers_per_index_block)
            index_blocks = 1 + 1 + second_level_blocks  # single indirect + double master + double leaf blocks
            metadata_bytes = 128 + (index_blocks * self.block_size_bytes)
            access_complexity = "O(1) - 2 Indirect block table lookups"

        overhead_pct = (metadata_bytes / (file_size_kb * 1024)) * 100.0

        if num_data_blocks <= 2:
            score = 9
            verdict = "Highly Recommended: Instant O(1) access via direct inode pointers."
        elif num_data_blocks <= 1500:
            score = 10
            verdict = "Optimal Choice: Fast random access to syllabus/slides, modular growth."
        else:
            score = 9
            verdict = "Highly Recommended: Multi-level indexing scales seamlessly to 2 GB videos with O(1) seeks."

        return AllocationEvaluationResult(
            method_name="Indexed Allocation (Unix Inode)",
            workload_type=workload_name,
            file_size_kb=file_size_kb,
            num_blocks=num_data_blocks + index_blocks,
            direct_access_complexity=access_complexity,
            sequential_access_complexity="O(1) - Read blocks via indexed pointers",
            metadata_overhead_bytes=metadata_bytes,
            metadata_overhead_percent=round(overhead_pct, 4),
            fragmentation_type="Internal Fragmentation in last block/index block only (Zero External)",
            dynamic_growth_support="Excellent (Allocate index blocks dynamically on demand)",
            fault_tolerance="High (Index isolated; lost data block does not break others)",
            suitability_score_out_of_10=score,
            recommendation_verdict=verdict
        )


def run_file_allocation_analysis() -> Dict[str, List[AllocationEvaluationResult]]:
    """Runs complete comparative simulation across all workloads and methods."""
    sim = FileAllocationSimulator(block_size_kb=4.0)

    workloads = [
        ("Small Student Record", 2.5),          # 2.5 KB
        ("Medium Academic Document", 2048.0),   # 2 MB (2048 KB)
        ("Large Lecture Video", 1048576.0)      # 1 GB (1048576 KB)
    ]

    results: Dict[str, List[AllocationEvaluationResult]] = {}

    for w_name, size_kb in workloads:
        results[w_name] = [
            sim.evaluate_contiguous(w_name, size_kb),
            sim.evaluate_linked(w_name, size_kb),
            sim.evaluate_indexed(w_name, size_kb)
        ]

    return results


if __name__ == "__main__":
    print("=" * 86)
    print(" UNICORE FILE ALLOCATION STRATEGY COMPARATIVE ANALYSIS (CO4)")
    print("=" * 86)

    benchmark_data = run_file_allocation_analysis()

    headers = ["Allocation Strategy", "Workload", "Size", "Blocks", "Random Access", "Overhead %", "Suitability", "Verdict"]
    
    for w_name, evals in benchmark_data.items():
        print(f"\n>>> WORKLOAD: {w_name.upper()} <<<")
        rows = []
        for e in evals:
            size_str = f"{e.file_size_kb} KB" if e.file_size_kb < 1024 else f"{e.file_size_kb/1024:.1f} MB" if e.file_size_kb < 1048576 else f"{e.file_size_kb/(1024**2):.1f} GB"
            rows.append([
                e.method_name,
                e.workload_type,
                size_str,
                e.num_blocks,
                e.direct_access_complexity.split(" - ")[0],
                f"{e.metadata_overhead_percent:.3f}%",
                f"{e.suitability_score_out_of_10}/10",
                e.recommendation_verdict[:40] + "..."
            ])
        print(format_table(headers, rows))

    print("\n" + "=" * 86)
    print(" ARCHITECTURAL RECOMMENDATION SUMMARY FOR UNICORE PLATFORM:")
    print(" 1. Small Student Records   -> Indexed Allocation (Stored inside 128-byte Inode direct table)")
    print(" 2. Medium Course Documents -> Indexed Allocation (Single-indirect index blocks up to 4 MB)")
    print(" 3. Large Lecture Videos    -> Multi-Level Indexed Inode + Extent Grouping (Scales to 4 GB+)")
    print("=" * 86)
