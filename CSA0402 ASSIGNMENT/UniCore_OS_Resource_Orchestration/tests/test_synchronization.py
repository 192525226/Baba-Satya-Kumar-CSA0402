"""
Unit and Concurrency Tests for Readers-Writers Synchronization (CO2)
"""

import pytest
import threading
import time
import os
import sys

# Ensure src path is accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from synchronization import FairReadersWritersMonitor, ExamRecordDatabase, UniCoreSynchronizationSimulator


def test_monitor_mutual_exclusion():
    monitor = FairReadersWritersMonitor()
    state = {"readers": 0, "writers": 0, "violation": False}
    lock = threading.Lock()

    def dummy_log(msg):
        pass

    def reader_worker():
        monitor.start_read("Reader-T", dummy_log)
        with lock:
            if state["writers"] > 0:
                state["violation"] = True
            state["readers"] += 1
        time.sleep(0.02)
        with lock:
            state["readers"] -= 1
        monitor.end_read("Reader-T", dummy_log)

    def writer_worker():
        monitor.start_write("Writer-T", dummy_log)
        with lock:
            if state["readers"] > 0 or state["writers"] > 0:
                state["violation"] = True
            state["writers"] = 1
        time.sleep(0.03)
        with lock:
            state["writers"] = 0
        monitor.end_write("Writer-T", dummy_log)

    threads = []
    for _ in range(5):
        threads.append(threading.Thread(target=reader_worker))
    for _ in range(2):
        threads.append(threading.Thread(target=writer_worker))
    for _ in range(5):
        threads.append(threading.Thread(target=reader_worker))

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert state["violation"] is False


def test_full_synchronization_simulation():
    sim = UniCoreSynchronizationSimulator()
    log_output = sim.run_simulation()

    assert "STARTING UNICORE FAIR READERS-WRITERS SYNCHRONIZATION SIMULATION" in log_output
    assert "ZERO RACE CONDITIONS DETECTED" in log_output
    # Assert database records were updated correctly
    assert sim.db.records["STU_102"].score == 92.0
    assert sim.db.records["STU_104"].score == 89.5
    assert sim.db.records["STU_105"].score == 75.0
