"""
Unit and Regression Tests for CPU Scheduling Algorithms (CO2)
"""

import pytest
import os
import sys

# Ensure src path is accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from cpu_scheduler import Process, CPUScheduler


@pytest.fixture
def standard_workload():
    return [
        Process("P0", "Online Exam", arrival_time=0, burst_time=8, priority=1),
        Process("P1", "LMS Request", arrival_time=1, burst_time=4, priority=2),
        Process("P2", "Library Search", arrival_time=2, burst_time=9, priority=3),
        Process("P3", "HPC Batch", arrival_time=3, burst_time=5, priority=4),
        Process("P4", "IoT Sensor", arrival_time=4, burst_time=2, priority=1),
        Process("P5", "Backup Service", arrival_time=5, burst_time=6, priority=5),
        Process("P6", "Grade Sync", arrival_time=6, burst_time=3, priority=2),
        Process("P7", "Video Stream", arrival_time=7, burst_time=7, priority=4),
    ]


def test_fcfs_metrics(standard_workload):
    scheduler = CPUScheduler(standard_workload)
    procs, gantt, metrics = scheduler.run_fcfs()

    assert len(procs) == 8
    assert metrics["total_time"] == 44
    assert metrics["cpu_utilization"] == 100.0
    
    # In FCFS with non-zero arrivals, P0 arrives at 0 and finishes at 8
    p0 = next(p for p in procs if p.pid == "P0")
    assert p0.completion_time == 8
    assert p0.waiting_time == 0
    assert p0.turnaround_time == 8
    assert p0.response_time == 0

    assert metrics["avg_wt"] == 17.25
    assert metrics["avg_tat"] == 22.75
    assert metrics["avg_rt"] == 17.25


def test_sjf_non_preemptive(standard_workload):
    scheduler = CPUScheduler(standard_workload)
    procs, gantt, metrics = scheduler.run_sjf_non_preemptive()

    assert len(procs) == 8
    assert metrics["total_time"] == 44
    
    # After P0 completes at 8, the ready processes (P1-P7) will be selected by shortest burst time
    # P4 (burst 2) -> P6 (burst 3) -> P1 (burst 4) -> P3 (burst 5) -> P5 (burst 6) -> P7 (burst 7) -> P2 (burst 9)
    p4 = next(p for p in procs if p.pid == "P4")
    assert p4.completion_time == 10
    assert p4.waiting_time == 4  # 8 - 4


def test_round_robin_quantum_4(standard_workload):
    scheduler = CPUScheduler(standard_workload)
    procs, gantt, metrics = scheduler.run_round_robin(quantum=4)

    assert len(procs) == 8
    assert metrics["total_time"] == 44
    assert metrics["avg_rt"] < metrics["avg_wt"]  # RR gives faster initial response time


def test_preemptive_priority(standard_workload):
    scheduler = CPUScheduler(standard_workload)
    procs, gantt, metrics = scheduler.run_priority_preemptive()

    assert len(procs) == 8
    assert metrics["total_time"] == 44
    
    p4 = next(p for p in procs if p.pid == "P4")
    assert p4.completion_time <= 10


def test_mlfq_dynamic_queues(standard_workload):
    scheduler = CPUScheduler(standard_workload)
    procs, gantt, metrics = scheduler.run_mlfq(q0=2, q1=4)

    assert len(procs) == 8
    assert metrics["total_time"] == 44
    # In MLFQ, interactive jobs (short bursts) finish in Q0 with minimal response time
    assert metrics["avg_rt"] <= 5.0
