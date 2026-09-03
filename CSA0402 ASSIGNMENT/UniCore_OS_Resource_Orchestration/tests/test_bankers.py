"""
Unit and Adversarial Tests for Banker's Deadlock Avoidance Algorithm (CO2)
"""

import pytest
import os
import sys

# Ensure src path is accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from bankers_algorithm import BankersAlgorithm, get_unicore_banker_instance


@pytest.fixture
def banker_fixture():
    return get_unicore_banker_instance()


def test_banker_need_matrix(banker_fixture):
    # Need[i][j] = Max[i][j] - Allocation[i][j]
    for i in range(banker_fixture.num_processes):
        for j in range(banker_fixture.num_resources):
            assert banker_fixture.need[i][j] == banker_fixture.max_matrix[i][j] - banker_fixture.allocation[i][j]


def test_banker_available_vector(banker_fixture):
    # Total = [10, 6, 8, 7]
    # Sum of Alloc = [9, 4, 6, 6] -> Available = [1, 2, 2, 1]
    assert banker_fixture.available == [1, 2, 2, 1]


def test_banker_initial_safe_state(banker_fixture):
    is_safe, safe_seq, trace = banker_fixture.is_safe_state()
    assert is_safe is True
    assert len(safe_seq) == 8


def test_banker_adverse_unsafe_request_rejected(banker_fixture):
    # P3 requests [1, 2, 0, 0]
    # If tentatively granted, available becomes [0, 0, 2, 1], causing deadlock (unsafe state)
    test_banker = banker_fixture.clone()
    granted, msg, trace = test_banker.request_resources(3, [1, 2, 0, 0])
    
    assert granted is False
    assert "UNSAFE STATE" in msg or "REJECTED" in msg
    # Verify rollback: available and allocation are untouched
    assert test_banker.available == [1, 2, 2, 1]


def test_banker_valid_request_granted(banker_fixture):
    # P1 requests [1, 0, 0, 1] which is <= Need [1, 1, 0, 1] and <= Available [1, 2, 2, 1]
    test_banker = banker_fixture.clone()
    granted, msg, trace = test_banker.request_resources(1, [1, 0, 0, 1])
    
    assert granted is True
    assert test_banker.available == [0, 2, 2, 0]


def test_banker_exceed_max_claim(banker_fixture):
    # P0 asks for more than its Need
    test_banker = banker_fixture.clone()
    granted, msg, _ = test_banker.request_resources(0, [10, 10, 10, 10])
    assert granted is False
    assert "exceeded its declared maximum claim" in msg
