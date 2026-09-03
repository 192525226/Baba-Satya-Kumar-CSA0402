"""
Visual Figure and Diagram Generator for UniCore Smart University Platform
Course: CSA04 Operating Systems

Generates crisp, high-resolution PNG (300 DPI) and SVG diagrams:
1. architecture_diagram.png & .svg (Multi-tier OS Architecture)
2. complete_system_flowchart.png (End-to-end Lifecycle Flowchart)
3. cpu_gantt_chart.png (Visual Gantt chart for FCFS, SJF, RR, Priority, MLFQ)
4. cpu_comparison.png (Waiting, Turnaround, and Response Time comparison)
5. bankers_flowchart.png (Resource-Request & Safety Algorithm flowchart)
6. memory_management_diagram.png (Two-level Paging, TLB, Page-Fault ISR)
7. page_fault_comparison.png (FIFO vs LRU vs Optimal on 3 & 4 frames + Belady Anomaly)
8. disk_trajectory.png (Seek position vs step line chart)
9. disk_movement_comparison.png (Total Head Movement bar chart)
"""

import os
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from typing import Dict, List, Any


def get_figures_dir() -> str:
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    fig_dir = os.path.join(root, "figures")
    os.makedirs(fig_dir, exist_ok=True)
    return fig_dir


def generate_architecture_diagram():
    """Generates Layered UniCore OS Architecture Diagram (PNG & SVG)."""
    fig_dir = get_figures_dir()
    png_path = os.path.join(fig_dir, "architecture_diagram.png")
    svg_path = os.path.join(fig_dir, "architecture_diagram.svg")

    fig, ax = plt.subplots(figsize=(12, 9), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    colors = {
        "user": "#E8F0FE",
        "app": "#D2E3FC",
        "kernel_core": "#CEEAD6",
        "kernel_sub": "#E6F4EA",
        "hardware": "#FCE8E6",
        "border": "#1A73E8",
        "text": "#202124"
    }

    # Title
    ax.text(50, 96, "UniCore: Integrated OS Resource Orchestration Architecture", 
            ha='center', va='center', fontsize=16, fontweight='bold', color='#1A73E8')

    # Layer 1: User / Client Layer
    rect1 = patches.FancyBboxPatch((5, 83), 90, 9, boxstyle="round,pad=0.5", 
                                   ec="#1967D2", fc=colors["user"], lw=1.5)
    ax.add_patch(rect1)
    ax.text(50, 89, "User & Client Access Tier (Normal: 500 Users | Exam Peak: 800+ Users)", 
            ha='center', va='center', fontsize=11, fontweight='bold', color=colors["text"])
    ax.text(50, 85.5, "Online Exam Portal • LMS Classroom • Digital Library • HPC Research Solver • IoT Telemetry", 
            ha='center', va='center', fontsize=9.5, style='italic', color="#3C4043")

    # Arrow Down
    ax.annotate('', xy=(50, 78), xytext=(50, 83),
                arrowprops=dict(arrowstyle="->", lw=2, color="#5F6368"))

    # Layer 2: UniCore Middleware & Security Monitor
    rect2 = patches.FancyBboxPatch((5, 69), 90, 9, boxstyle="round,pad=0.5", 
                                   ec="#188038", fc=colors["kernel_sub"], lw=1.5)
    ax.add_patch(rect2)
    ax.text(50, 75, "UniCore Synchronization & Deadlock Prevention Layer (CO2)", 
            ha='center', va='center', fontsize=11, fontweight='bold', color="#137333")
    ax.text(50, 71.5, "Fair Readers-Writers Monitor • Banker's Safety Verification • Dynamic Resource Reservation", 
            ha='center', va='center', fontsize=9.5, color="#202124")

    # Arrow Down
    ax.annotate('', xy=(50, 64), xytext=(50, 69),
                arrowprops=dict(arrowstyle="->", lw=2, color="#5F6368"))

    # Layer 3: Kernel Core Orchestration
    rect3 = patches.FancyBboxPatch((5, 33), 90, 31, boxstyle="round,pad=0.5", 
                                   ec="#1A73E8", fc="#F8F9FA", lw=2)
    ax.add_patch(rect3)
    ax.text(50, 61, "Operating System Kernel Subsystems", 
            ha='center', va='center', fontsize=13, fontweight='bold', color="#1A73E8")

    # Subsystem 3A: CPU Scheduling
    sub1 = patches.FancyBboxPatch((8, 36), 26, 21, boxstyle="round,pad=0.3", ec="#1A73E8", fc="#FFFFFF", lw=1.2)
    ax.add_patch(sub1)
    ax.text(21, 54, "Process & CPU\nManagement (CO2)", ha='center', va='center', fontsize=10, fontweight='bold', color="#1A73E8")
    ax.text(21, 45, "• Multilevel Feedback (MLFQ)\n• Preemptive Priority\n• SJF & FCFS Schedulers\n• Context Switch Dispatcher", 
            ha='center', va='center', fontsize=8.5, color="#3C4043")

    # Subsystem 3B: Virtual Memory Management
    sub2 = patches.FancyBboxPatch((37, 36), 26, 21, boxstyle="round,pad=0.3", ec="#137333", fc="#FFFFFF", lw=1.2)
    ax.add_patch(sub2)
    ax.text(50, 54, "Memory & Paging\nSubsystem (CO3)", ha='center', va='center', fontsize=10, fontweight='bold', color="#137333")
    ax.text(50, 45, "• 2-Level Hierarchical Paging\n• TLB Hit (95%) EMAT Opt\n• LRU Replacement (Stack)\n• Working-Set Thrashing Ctrl", 
            ha='center', va='center', fontsize=8.5, color="#3C4043")

    # Subsystem 3C: File System & Disk I/O
    sub3 = patches.FancyBboxPatch((66, 36), 26, 21, boxstyle="round,pad=0.3", ec="#D93025", fc="#FFFFFF", lw=1.2)
    ax.add_patch(sub3)
    ax.text(79, 54, "Storage & Disk\nSubsystem (CO4)", ha='center', va='center', fontsize=10, fontweight='bold', color="#D93025")
    ax.text(79, 45, "• Unix Inode Indexed Alloc\n• C-SCAN Circular Seek Opt\n• Dirty Page Buffer Cache\n• Starvation Elimination", 
            ha='center', va='center', fontsize=8.5, color="#3C4043")

    # Arrow Down
    ax.annotate('', xy=(50, 28), xytext=(50, 33),
                arrowprops=dict(arrowstyle="->", lw=2, color="#5F6368"))

    # Layer 4: Physical Hardware
    rect4 = patches.FancyBboxPatch((5, 14), 90, 14, boxstyle="round,pad=0.5", 
                                   ec="#D93025", fc=colors["hardware"], lw=1.5)
    ax.add_patch(rect4)
    ax.text(50, 24, "Underlying Hardware Infrastructure", 
            ha='center', va='center', fontsize=11, fontweight='bold', color="#B31412")
    ax.text(50, 18.5, "16 GB Physical RAM (4,194,304 Frames) • Multi-Core Xeon CPU • 200-Cylinder Secondary HDD/NVMe Array", 
            ha='center', va='center', fontsize=9.5, color="#3C4043")

    # Footer
    ax.text(50, 6, "UniCore Architecture — Designed for High Reliability, Green Energy (SDG 7), and Fair Access (SDG 11)", 
            ha='center', va='center', fontsize=9, style='italic', color="#70757A")

    plt.tight_layout()
    fig.savefig(png_path, dpi=300, bbox_inches='tight')
    fig.savefig(svg_path, bbox_inches='tight')
    plt.close(fig)


def generate_complete_system_flowchart():
    """Generates Complete System Operation Flowchart."""
    fig_dir = get_figures_dir()
    path = os.path.join(fig_dir, "complete_system_flowchart.png")

    fig, ax = plt.subplots(figsize=(11, 10), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    ax.text(50, 97, "UniCore End-to-End System Operation Flowchart", 
            ha='center', va='center', fontsize=15, fontweight='bold', color='#1A73E8')

    steps = [
        ("Job Arrival & Classification", "User submits Exam/LMS/Research request", 88, "#E8F0FE", "#1A73E8"),
        ("Deadlock Safety Check", "Banker's Algorithm: Is Request <= Need & Safe?", 75, "#FEF7E0", "#B06000"),
        ("CPU Scheduling & Execution", "MLFQ assigns dynamic priority (Q0 -> Q1 -> Q2)", 62, "#E6F4EA", "#137333"),
        ("Concurrency & Shared Records", "Fair Readers-Writers Monitor locks exam database", 49, "#FCE8E6", "#C5221F"),
        ("Memory Access & Page Table", "TLB lookup -> LRU Page Replacement if fault occurs", 36, "#F3E8FD", "#8430CE"),
        ("File & Disk I/O Operation", "Indexed Inode resolution -> C-SCAN disk seek", 23, "#E8F0FE", "#1A73E8"),
        ("Job Completion & Metric Export", "Free resources, update metrics & return result", 10, "#E6F4EA", "#137333"),
    ]

    for title, desc, y, bg, border in steps:
        box = patches.FancyBboxPatch((15, y - 4), 70, 8, boxstyle="round,pad=0.3", ec=border, fc=bg, lw=1.5)
        ax.add_patch(box)
        ax.text(50, y + 1, title, ha='center', va='center', fontsize=11, fontweight='bold', color=border)
        ax.text(50, y - 2, desc, ha='center', va='center', fontsize=9, color="#3C4043")

        if y > 10:
            ax.annotate('', xy=(50, y - 5), xytext=(50, y - 4),
                        arrowprops=dict(arrowstyle="->", lw=1.8, color="#5F6368"))

    plt.tight_layout()
    fig.savefig(path, dpi=300, bbox_inches='tight')
    plt.close(fig)


def generate_cpu_charts():
    """Generates cpu_gantt_chart.png and cpu_comparison.png."""
    fig_dir = get_figures_dir()

    # 1. CPU Comparison Bar Chart
    comp_path = os.path.join(fig_dir, "cpu_comparison.png")
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)

    algorithms = ["FCFS", "SJF (Non-Preempt)", "Round Robin (q=4)", "Preemptive Priority", "MLFQ (q0=2, q1=4)"]
    avg_wt = [17.25, 14.50, 24.88, 15.00, 27.25]
    avg_tat = [22.75, 21.38, 31.75, 21.88, 34.12]
    avg_rt = [17.25, 14.50, 10.12, 15.00, 3.50]

    x = np.arange(len(algorithms))
    width = 0.25

    rects1 = ax.bar(x - width, avg_wt, width, label='Avg Waiting Time (ms)', color='#4285F4')
    rects2 = ax.bar(x, avg_tat, width, label='Avg Turnaround Time (ms)', color='#EA4335')
    rects3 = ax.bar(x + width, avg_rt, width, label='Avg Response Time (ms)', color='#34A853')

    ax.set_ylabel('Time (ms)', fontsize=12, fontweight='bold')
    ax.set_title('CPU Scheduling Performance Comparison Across Algorithms', fontsize=14, fontweight='bold', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(algorithms, rotation=15, ha='right', fontsize=10)
    ax.legend(frameon=True, facecolor='#F8F9FA', edgecolor='#DADCE0')
    ax.grid(axis='y', linestyle='--', alpha=0.5)

    for rects in [rects1, rects2, rects3]:
        for r in rects:
            h = r.get_height()
            ax.annotate(f'{h:.1f}',
                        xy=(r.get_x() + r.get_width() / 2, h),
                        xytext=(0, 3), textcoords="offset points",
                        ha='center', va='bottom', fontsize=8)

    plt.tight_layout()
    fig.savefig(comp_path, dpi=300, bbox_inches='tight')
    plt.close(fig)

    # 2. Gantt Chart
    gantt_path = os.path.join(fig_dir, "cpu_gantt_chart.png")
    fig, ax = plt.subplots(figsize=(12, 7), dpi=300)

    fcfs_gantt = [('P0', 0, 8), ('P1', 8, 12), ('P2', 12, 21), ('P3', 21, 26), ('P4', 26, 28), ('P5', 28, 34), ('P6', 34, 37), ('P7', 37, 44)]
    sjf_gantt = [('P0', 0, 8), ('P4', 8, 10), ('P6', 10, 13), ('P1', 13, 17), ('P3', 17, 22), ('P5', 22, 28), ('P7', 28, 35), ('P2', 35, 44)]
    prio_gantt = [('P0', 0, 4), ('P4', 4, 6), ('P0', 6, 10), ('P1', 10, 14), ('P6', 14, 17), ('P2', 17, 26), ('P3', 26, 31), ('P7', 31, 38), ('P5', 38, 44)]

    gantts = [
        ("FCFS", fcfs_gantt),
        ("SJF", sjf_gantt),
        ("Preemptive Priority", prio_gantt)
    ]

    p_colors = {
        'P0': '#4285F4', 'P1': '#34A853', 'P2': '#FBBC05', 'P3': '#EA4335',
        'P4': '#AA46BB', 'P5': '#00ACC1', 'P6': '#FF7043', 'P7': '#795548',
        'IDLE': '#BDBDBD'
    }

    y_pos = 0
    yticks = []
    yticklabels = []

    for name, segs in gantts:
        for pid, st, end in segs:
            ax.broken_barh([(st, end - st)], (y_pos, 0.6), facecolors=p_colors.get(pid, '#757575'), edgecolor='black', lw=0.8)
            ax.text(st + (end - st)/2, y_pos + 0.3, pid, ha='center', va='center', color='white', fontweight='bold', fontsize=9)
        yticks.append(y_pos + 0.3)
        yticklabels.append(name)
        y_pos += 1.2

    ax.set_yticks(yticks)
    ax.set_yticklabels(yticklabels, fontsize=11, fontweight='bold')
    ax.set_xlabel('Timeline (Milliseconds)', fontsize=12, fontweight='bold')
    ax.set_title('Visual CPU Execution Gantt Chart Comparison', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlim(0, 46)
    ax.grid(axis='x', linestyle='--', alpha=0.5)

    legend_elements = [patches.Patch(facecolor=c, edgecolor='black', label=f'{p}') for p, c in p_colors.items() if p != 'IDLE']
    ax.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=4, frameon=True)

    plt.tight_layout()
    fig.savefig(gantt_path, dpi=300, bbox_inches='tight')
    plt.close(fig)


def generate_bankers_flowchart():
    """Generates Banker's Algorithm Decision Flowchart."""
    fig_dir = get_figures_dir()
    path = os.path.join(fig_dir, "bankers_flowchart.png")

    fig, ax = plt.subplots(figsize=(10, 11), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    ax.text(50, 97, "Banker's Deadlock Avoidance Algorithm Flowchart", 
            ha='center', va='center', fontsize=15, fontweight='bold', color='#1A73E8')

    ax.add_patch(patches.FancyBboxPatch((20, 86), 60, 6, boxstyle="round,pad=0.3", ec="#1A73E8", fc="#E8F0FE", lw=1.5))
    ax.text(50, 89, "Process P_i submits Resource Request Vector", ha='center', va='center', fontsize=10.5, fontweight='bold')

    ax.annotate('', xy=(50, 80), xytext=(50, 86), arrowprops=dict(arrowstyle="->", lw=1.8))

    ax.add_patch(patches.FancyBboxPatch((20, 72), 60, 8, boxstyle="round,pad=0.3", ec="#B06000", fc="#FEF7E0", lw=1.5))
    ax.text(50, 76, "Step 1: Is Request_i <= Need_i ?", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#B06000")

    ax.annotate('NO', xy=(85, 76), xytext=(80, 76), arrowprops=dict(arrowstyle="->", lw=1.5, color="#D93025"))
    ax.add_patch(patches.FancyBboxPatch((85, 73), 12, 6, boxstyle="round,pad=0.2", ec="#D93025", fc="#FCE8E6"))
    ax.text(91, 76, "ERROR\n(Exceed Max)", ha='center', va='center', fontsize=7.5, color="#D93025", fontweight='bold')

    ax.annotate('YES', xy=(50, 66), xytext=(50, 72), arrowprops=dict(arrowstyle="->", lw=1.8, color="#137333"))

    ax.add_patch(patches.FancyBboxPatch((20, 58), 60, 8, boxstyle="round,pad=0.3", ec="#B06000", fc="#FEF7E0", lw=1.5))
    ax.text(50, 62, "Step 2: Is Request_i <= Available ?", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#B06000")

    ax.annotate('NO', xy=(85, 62), xytext=(80, 62), arrowprops=dict(arrowstyle="->", lw=1.5, color="#D93025"))
    ax.add_patch(patches.FancyBboxPatch((85, 59), 12, 6, boxstyle="round,pad=0.2", ec="#D93025", fc="#FCE8E6"))
    ax.text(91, 62, "WAIT\n(Unavailable)", ha='center', va='center', fontsize=7.5, color="#D93025", fontweight='bold')

    ax.annotate('YES', xy=(50, 52), xytext=(50, 58), arrowprops=dict(arrowstyle="->", lw=1.8, color="#137333"))

    ax.add_patch(patches.FancyBboxPatch((15, 42), 70, 10, boxstyle="round,pad=0.3", ec="#1A73E8", fc="#E8F0FE", lw=1.5))
    ax.text(50, 48, "Step 3: Tentative Allocation State", ha='center', va='center', fontsize=11, fontweight='bold', color="#1A73E8")
    ax.text(50, 44.5, "Available' = Available - Request  |  Alloc' = Alloc + Request  |  Need' = Need - Request", 
            ha='center', va='center', fontsize=8.5, color="#3C4043")

    ax.annotate('', xy=(50, 36), xytext=(50, 42), arrowprops=dict(arrowstyle="->", lw=1.8))

    ax.add_patch(patches.FancyBboxPatch((15, 26), 70, 10, boxstyle="round,pad=0.3", ec="#137333", fc="#E6F4EA", lw=1.5))
    ax.text(50, 32, "Step 4: Execute Safety Verification Algorithm", ha='center', va='center', fontsize=11, fontweight='bold', color="#137333")
    ax.text(50, 28.5, "Find sequence where Need_k <= Work, Work = Work + Alloc_k, Finish[k] = True", 
            ha='center', va='center', fontsize=8.5, color="#3C4043")

    ax.annotate('SAFE SEQUENCE FOUND', xy=(30, 14), xytext=(35, 26), arrowprops=dict(arrowstyle="->", lw=1.8, color="#137333"))
    ax.annotate('NO SAFE SEQUENCE', xy=(70, 14), xytext=(65, 26), arrowprops=dict(arrowstyle="->", lw=1.8, color="#D93025"))

    ax.add_patch(patches.FancyBboxPatch((10, 6), 35, 8, boxstyle="round,pad=0.3", ec="#137333", fc="#CEEAD6", lw=2))
    ax.text(27.5, 10, "GRANT REQUEST\nCommit Allocation", ha='center', va='center', fontsize=10, fontweight='bold', color="#137333")

    ax.add_patch(patches.FancyBboxPatch((55, 6), 35, 8, boxstyle="round,pad=0.3", ec="#D93025", fc="#FCE8E6", lw=2))
    ax.text(72.5, 10, "REJECT / ROLLBACK\nProcess Must Wait", ha='center', va='center', fontsize=10, fontweight='bold', color="#D93025")

    plt.tight_layout()
    fig.savefig(path, dpi=300, bbox_inches='tight')
    plt.close(fig)


def generate_memory_diagrams():
    """Generates memory_management_diagram.png and page_fault_comparison.png."""
    fig_dir = get_figures_dir()

    # 1. Page Fault Comparison & Belady Anomaly Chart
    comp_path = os.path.join(fig_dir, "page_fault_comparison.png")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5), dpi=300)

    algos = ['FIFO', 'LRU', 'Optimal']
    faults_3 = [15, 12, 9]
    faults_4 = [10, 8, 8]

    x = np.arange(len(algos))
    width = 0.35

    ax1.bar(x - width/2, faults_3, width, label='3 Frames', color='#EA4335')
    ax1.bar(x + width/2, faults_4, width, label='4 Frames', color='#34A853')
    ax1.set_ylabel('Page Fault Count', fontsize=11, fontweight='bold')
    ax1.set_title('Page Faults on Standard Workload (20 Refs)', fontsize=12, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(algos, fontsize=10, fontweight='bold')
    ax1.legend()
    ax1.grid(axis='y', linestyle='--', alpha=0.5)

    for i in range(len(algos)):
        ax1.annotate(str(faults_3[i]), xy=(x[i] - width/2, faults_3[i]), xytext=(0, 3), textcoords="offset points", ha='center')
        ax1.annotate(str(faults_4[i]), xy=(x[i] + width/2, faults_4[i]), xytext=(0, 3), textcoords="offset points", ha='center')

    frames = [3, 4]
    fifo_belady = [9, 10]  # Anomaly: increases with more frames!
    lru_belady = [10, 8]   # Normal stack property behavior

    ax2.plot(frames, fifo_belady, marker='o', lw=2.5, color='#D93025', label="FIFO (Anomaly: 9 -> 10 Faults)")
    ax2.plot(frames, lru_belady, marker='s', lw=2.5, color='#1A73E8', label="LRU (Stack Property: 10 -> 8 Faults)")
    ax2.set_xlabel('Allocated Physical Frames', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Total Page Faults', fontsize=11, fontweight='bold')
    ax2.set_title("Belady's Anomaly Verification (12-Ref String)", fontsize=12, fontweight='bold')
    ax2.set_xticks([3, 4])
    ax2.legend()
    ax2.grid(True, linestyle='--', alpha=0.5)

    for f, v in zip(frames, fifo_belady):
        ax2.annotate(f'{v} Faults', xy=(f, v), xytext=(-10, 7), textcoords="offset points", fontweight='bold', color='#D93025')
    for f, v in zip(frames, lru_belady):
        ax2.annotate(f'{v} Faults', xy=(f, v), xytext=(-10, -15), textcoords="offset points", fontweight='bold', color='#1A73E8')

    plt.tight_layout()
    fig.savefig(comp_path, dpi=300, bbox_inches='tight')
    plt.close(fig)

    # 2. Memory Management Diagram
    diag_path = os.path.join(fig_dir, "memory_management_diagram.png")
    fig, ax = plt.subplots(figsize=(11, 7), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    ax.text(50, 95, "UniCore Two-Level Paging, TLB, & Page-Fault Handling Architecture", 
            ha='center', va='center', fontsize=13, fontweight='bold', color='#1A73E8')

    ax.add_patch(patches.Rectangle((10, 80), 35, 10, ec='#1A73E8', fc='#E8F0FE', lw=1.5))
    ax.text(27.5, 85, "Page Number (p: 14 bits)\n[Outer p1: 7 bits | Inner p2: 7 bits]", ha='center', va='center', fontsize=9, fontweight='bold')
    ax.add_patch(patches.Rectangle((45, 80), 20, 10, ec='#1A73E8', fc='#D2E3FC', lw=1.5))
    ax.text(55, 85, "Offset (d: 12 bits)\n4 KB Page Offset", ha='center', va='center', fontsize=9, fontweight='bold')

    ax.add_patch(patches.FancyBboxPatch((15, 55), 25, 16, boxstyle="round,pad=0.3", ec='#137333', fc='#E6F4EA', lw=1.5))
    ax.text(27.5, 65, "TLB Lookup\n(95% Hit Ratio)", ha='center', va='center', fontsize=10, fontweight='bold', color='#137333')
    ax.text(27.5, 59, "EMAT = 57.0 ns", ha='center', va='center', fontsize=8.5, color='#3C4043')

    ax.add_patch(patches.FancyBboxPatch((50, 55), 38, 16, boxstyle="round,pad=0.3", ec='#B06000', fc='#FEF7E0', lw=1.5))
    ax.text(69, 65, "Two-Level Page Table\n(RAM Translation)", ha='center', va='center', fontsize=10, fontweight='bold', color='#B06000')
    ax.text(69, 59, "Outer Table -> Inner Table -> Frame #", ha='center', va='center', fontsize=8.5, color='#3C4043')

    ax.add_patch(patches.FancyBboxPatch((30, 20), 55, 20, boxstyle="round,pad=0.3", ec='#D93025', fc='#FCE8E6', lw=1.5))
    ax.text(57.5, 33, "Physical RAM: 16 GB\n(4,194,304 Frames @ 4 KB each)", ha='center', va='center', fontsize=11, fontweight='bold', color='#D93025')
    ax.text(57.5, 25, "Frame Number (f: 22 bits) + Offset (d: 12 bits) = 34-bit Physical Address", 
            ha='center', va='center', fontsize=8.5, color='#3C4043')

    ax.annotate('', xy=(27.5, 71), xytext=(27.5, 80), arrowprops=dict(arrowstyle="->", lw=1.8))
    ax.annotate('TLB Hit (Fast Path)', xy=(35, 40), xytext=(27.5, 55), arrowprops=dict(arrowstyle="->", lw=1.8, color='#137333'))
    ax.annotate('TLB Miss', xy=(50, 63), xytext=(40, 63), arrowprops=dict(arrowstyle="->", lw=1.5, color='#B06000'))
    ax.annotate('Valid Frame Found', xy=(65, 40), xytext=(69, 55), arrowprops=dict(arrowstyle="->", lw=1.8, color='#1A73E8'))
    ax.annotate('Offset Passed Directly', xy=(65, 80), xytext=(57.5, 40), arrowprops=dict(arrowstyle="<-", lw=1.5, linestyle=':', color='#5F6368'))

    plt.tight_layout()
    fig.savefig(diag_path, dpi=300, bbox_inches='tight')
    plt.close(fig)


def generate_disk_charts():
    """Generates disk_trajectory.png and disk_movement_comparison.png."""
    fig_dir = get_figures_dir()

    # 1. Total Head Movement Bar Chart
    comp_path = os.path.join(fig_dir, "disk_movement_comparison.png")
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)

    algos = ["FCFS", "SSTF", "SCAN", "C-SCAN", "LOOK", "C-LOOK"]
    thm = [908, 215, 331, 390, 313, 344]
    colors = ['#EA4335', '#FBBC05', '#4285F4', '#34A853', '#AA46BB', '#00ACC1']

    bars = ax.bar(algos, thm, color=colors, edgecolor='black', lw=0.8, width=0.55)
    ax.set_ylabel('Total Head Movement (Cylinders)', fontsize=12, fontweight='bold')
    ax.set_title('Disk Scheduling Total Head Movement (THM) Comparison on 200 Cylinders', fontsize=13, fontweight='bold', pad=15)
    ax.grid(axis='y', linestyle='--', alpha=0.5)

    for bar in bars:
        h = bar.get_height()
        ax.annotate(f'{h} cyl',
                    xy=(bar.get_x() + bar.get_width() / 2, h),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontsize=10, fontweight='bold')

    plt.tight_layout()
    fig.savefig(comp_path, dpi=300, bbox_inches='tight')
    plt.close(fig)

    # 2. Seek Trajectory Line Chart
    traj_path = os.path.join(fig_dir, "disk_trajectory.png")
    fig, ax = plt.subplots(figsize=(11, 7), dpi=300)

    trajectories = {
        "FCFS (THM: 908)": [53, 98, 183, 37, 122, 14, 124, 65, 67, 190, 45],
        "SSTF (THM: 215)": [53, 45, 37, 14, 65, 67, 98, 122, 124, 183, 190],
        "SCAN (THM: 331)": [53, 65, 67, 98, 122, 124, 183, 190, 199, 45, 37, 14],
        "C-SCAN (THM: 390)": [53, 65, 67, 98, 122, 124, 183, 190, 199, 0, 14, 37, 45],
        "LOOK (THM: 313)": [53, 65, 67, 98, 122, 124, 183, 190, 45, 37, 14]
    }

    styles = {
        "FCFS (THM: 908)": ('#EA4335', 'o', '--'),
        "SSTF (THM: 215)": ('#FBBC05', 's', '-.'),
        "SCAN (THM: 331)": ('#4285F4', '^', '-'),
        "C-SCAN (THM: 390)": ('#34A853', 'D', '-'),
        "LOOK (THM: 313)": ('#AA46BB', 'v', ':')
    }

    for name, seq in trajectories.items():
        color, marker, lstyle = styles[name]
        steps = list(range(len(seq)))
        ax.plot(seq, steps, marker=marker, linestyle=lstyle, color=color, label=name, lw=2)

    ax.set_xlabel('Cylinder Position (0 - 199)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Seek Step Sequence', fontsize=12, fontweight='bold')
    ax.set_title('Disk Arm Trajectory Comparison Across Schedulers', fontsize=14, fontweight='bold', pad=15)
    ax.invert_yaxis()  # Steps advance downwards
    ax.set_xlim(-5, 205)
    ax.legend(loc='lower right', frameon=True, facecolor='#F8F9FA', edgecolor='#DADCE0')
    ax.grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    fig.savefig(traj_path, dpi=300, bbox_inches='tight')
    plt.close(fig)


def generate_all_figures():
    """Generates all 9 technical figures in PNG and SVG formats."""
    print("[FIGURES] Generating Architecture Diagrams (PNG & SVG)...")
    generate_architecture_diagram()

    print("[FIGURES] Generating Complete System Flowchart (PNG)...")
    generate_complete_system_flowchart()

    print("[FIGURES] Generating CPU Scheduling Charts (PNG)...")
    generate_cpu_charts()

    print("[FIGURES] Generating Banker's Algorithm Flowchart (PNG)...")
    generate_bankers_flowchart()

    print("[FIGURES] Generating Memory Management & Belady Charts (PNG)...")
    generate_memory_diagrams()

    print("[FIGURES] Generating Disk Scheduling Trajectories & Movement Charts (PNG)...")
    generate_disk_charts()

    print("[SUCCESS] All figures generated successfully in figures/")


if __name__ == "__main__":
    generate_all_figures()
