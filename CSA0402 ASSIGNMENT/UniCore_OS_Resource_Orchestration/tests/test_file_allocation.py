"""
Unit and Comparative Tests for File Allocation Strategies (CO4)
"""

import pytest
import os
import sys

# Ensure src path is accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from file_allocation import FileAllocationSimulator, run_file_allocation_analysis


@pytest.fixture
def allocator():
    return FileAllocationSimulator(block_size_kb=4.0)


def test_small_student_record_allocation(allocator):
    res_contig = allocator.evaluate_contiguous("Small Student Record", 2.5)
    res_linked = allocator.evaluate_linked("Small Student Record", 2.5)
    res_indexed = allocator.evaluate_indexed("Small Student Record", 2.5)

    assert res_contig.num_blocks == 1
    assert res_linked.num_blocks == 1
    assert res_indexed.num_blocks == 1
    assert res_indexed.suitability_score_out_of_10 >= 9


def test_medium_document_allocation(allocator):
    res_indexed = allocator.evaluate_indexed("Medium Document", 2048.0)
    assert res_indexed.num_blocks == 512 + 1  # 512 data blocks + 1 single indirect block
    assert "O(1)" in res_indexed.direct_access_complexity
    assert res_indexed.suitability_score_out_of_10 == 10


def test_large_video_allocation(allocator):
    res_linked = allocator.evaluate_linked("Large Video", 1048576.0)
    res_indexed = allocator.evaluate_indexed("Large Video", 1048576.0)

    # Linked allocation has O(N) access complexity (unsuitable for video streaming)
    assert "O(N)" in res_linked.direct_access_complexity
    assert res_linked.suitability_score_out_of_10 <= 3

    # Indexed allocation supports multi-level tree with O(1) seek
    assert "O(1)" in res_indexed.direct_access_complexity
    assert res_indexed.suitability_score_out_of_10 >= 9


def test_full_allocation_suite():
    results = run_file_allocation_analysis()
    assert len(results) == 3
    assert "Small Student Record" in results
    assert "Medium Academic Document" in results
    assert "Large Lecture Video" in results
