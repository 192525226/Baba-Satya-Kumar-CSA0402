"""
Unit and Regression Tests for Virtual Memory & Page Replacement (CO3)
"""

import pytest
import os
import sys

# Ensure src path is accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from page_replacement import PageReplacementSimulator, VirtualMemoryHardware, simulate_working_set_and_thrashing


@pytest.fixture
def ref_string_20():
    return [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1]


def test_hardware_bounds():
    hw = VirtualMemoryHardware(ram_gb=16.0, page_kb=4.0, logical_mb=64.0)
    assert hw.num_physical_frames == 4194304
    assert hw.num_logical_pages == 16384
    assert hw.offset_bits == 12
    assert hw.page_number_bits == 14
    assert hw.frame_number_bits == 22
    assert hw.calculate_emat(0.95) == 57.0


def test_fifo_page_faults(ref_string_20):
    sim3 = PageReplacementSimulator(ref_string_20, 3)
    faults3, hits3, _ = sim3.run_fifo()
    assert faults3 == 15
    assert hits3 == 5

    sim4 = PageReplacementSimulator(ref_string_20, 4)
    faults4, hits4, _ = sim4.run_fifo()
    assert faults4 == 10
    assert hits4 == 10


def test_lru_page_faults(ref_string_20):
    sim3 = PageReplacementSimulator(ref_string_20, 3)
    faults3, hits3, _ = sim3.run_lru()
    assert faults3 == 12
    assert hits3 == 8

    sim4 = PageReplacementSimulator(ref_string_20, 4)
    faults4, hits4, _ = sim4.run_lru()
    assert faults4 == 8
    assert hits4 == 12


def test_optimal_page_faults(ref_string_20):
    sim3 = PageReplacementSimulator(ref_string_20, 3)
    faults3, hits3, _ = sim3.run_optimal()
    assert faults3 == 9
    assert hits3 == 11

    sim4 = PageReplacementSimulator(ref_string_20, 4)
    faults4, hits4, _ = sim4.run_optimal()
    assert faults4 == 8
    assert hits4 == 12


def test_beladys_anomaly_proof():
    # Belady reference string: 1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5
    belady_str = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
    
    sim_fifo_3 = PageReplacementSimulator(belady_str, 3)
    f3, _, _ = sim_fifo_3.run_fifo()
    sim_fifo_4 = PageReplacementSimulator(belady_str, 4)
    f4, _, _ = sim_fifo_4.run_fifo()
    
    # FIFO exhibits Belady's Anomaly: 9 faults on 3 frames -> 10 faults on 4 frames!
    assert f3 == 9
    assert f4 == 10
    assert f4 > f3

    # LRU is a stack algorithm and does NOT suffer from Belady's Anomaly
    sim_lru_3 = PageReplacementSimulator(belady_str, 3)
    lru_f3, _, _ = sim_lru_3.run_lru()
    sim_lru_4 = PageReplacementSimulator(belady_str, 4)
    lru_f4, _, _ = sim_lru_4.run_lru()
    assert lru_f4 <= lru_f3


def test_working_set_thrashing_800_users():
    res = simulate_working_set_and_thrashing(800)
    assert res["is_thrashing"] is False
    assert res["total_active_memory_mb"] == 43.75 or res["total_active_memory_mb"] == 44.8
    assert res["memory_pressure_percent"] < 15.0
