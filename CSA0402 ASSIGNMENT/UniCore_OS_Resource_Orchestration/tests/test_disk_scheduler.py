"""
Unit and Boundary Tests for Disk Scheduling Algorithms (CO4)
"""

import pytest
import os
import sys

# Ensure src path is accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from disk_scheduler import DiskScheduler, get_unicore_disk_config


@pytest.fixture
def disk_scheduler_fixture():
    requests = [98, 183, 37, 122, 14, 124, 65, 67, 190, 45]
    return DiskScheduler(requests=requests, initial_head=53, total_cylinders=200, direction="HIGH")


def test_fcfs_thm(disk_scheduler_fixture):
    seq, thm, asl, mov = disk_scheduler_fixture.run_fcfs()
    assert seq == [53, 98, 183, 37, 122, 14, 124, 65, 67, 190, 45]
    assert thm == 908
    assert asl == 90.8


def test_sstf_thm(disk_scheduler_fixture):
    seq, thm, asl, mov = disk_scheduler_fixture.run_sstf()
    assert seq == [53, 45, 37, 14, 65, 67, 98, 122, 124, 183, 190]
    assert thm == 215
    assert asl == 21.5


def test_scan_thm(disk_scheduler_fixture):
    seq, thm, asl, mov = disk_scheduler_fixture.run_scan()
    # Moves up to 199 then down to 14
    assert seq == [53, 65, 67, 98, 122, 124, 183, 190, 199, 45, 37, 14]
    assert thm == 331
    assert asl == 33.1


def test_cscan_thm(disk_scheduler_fixture):
    seq, thm, asl, mov = disk_scheduler_fixture.run_cscan()
    # Moves up to 199, jumps to 0, moves up to 45
    assert seq == [53, 65, 67, 98, 122, 124, 183, 190, 199, 0, 14, 37, 45]
    assert thm == 390
    assert asl == 39.0


def test_look_thm(disk_scheduler_fixture):
    seq, thm, asl, mov = disk_scheduler_fixture.run_look()
    # Moves up to highest (190) then down to lowest (14)
    assert seq == [53, 65, 67, 98, 122, 124, 183, 190, 45, 37, 14]
    assert thm == 313
    assert asl == 31.3


def test_clook_thm(disk_scheduler_fixture):
    seq, thm, asl, mov = disk_scheduler_fixture.run_clook()
    # Moves up to 190, jumps to 14, moves up to 45
    assert seq == [53, 65, 67, 98, 122, 124, 183, 190, 14, 37, 45]
    assert thm == 344
    assert asl == 34.4


def test_boundary_requests():
    # Boundary edge requests at cylinder 0 and 199
    boundary_reqs = [0, 199, 100]
    sim = DiskScheduler(boundary_reqs, initial_head=100, total_cylinders=200, direction="HIGH")
    seq, thm, _, _ = sim.run_scan()
    assert 0 in seq
    assert 199 in seq
