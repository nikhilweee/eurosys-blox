"""
Plot Fig 6 (Average JCT) and Fig 7 (Average Responsiveness) reproducing
the EuroSys '24 paper figures from completed simulation data in experiments/.
"""
import json
import os
import statistics
from blox.utils import get_experiment_filepath
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
EXP_DIR = os.path.join(HERE, "experiments")
PLOT_DIR = os.path.join(HERE, "plots")
os.makedirs(PLOT_DIR, exist_ok=True)

# Digitized vector points extracted from the EuroSys '24 paper PDF
PAPER_POINTS = {
    "Fig6 JCT": {
        "Tiresias": [(1.0, 57031), (2.0, 57026), (3.0, 57030), (4.0, 57026), (5.0, 57025), (6.0, 57033), (7.0, 57072), (8.0, 189300), (9.0, 323469)],
        "Fifo": [(1.0, 57031), (2.0, 57026), (3.0, 57030), (4.0, 57026), (5.0, 57025), (6.0, 57033), (7.0, 57199), (8.0, 131709), (9.0, 281452)],
        "Optimus": [(1.0, 11660), (2.0, 19230), (3.0, 40866), (4.0, 47629), (5.0, 51934), (6.0, 57109), (7.0, 57162), (8.0, 75394), (9.0, 114820)],
    },
    "Fig7 Resp": {
        "Tiresias": [(1.0, 206847), (2.0, 735), (3.0, 742), (4.0, 736), (5.0, 734), (6.0, 742), (7.0, 738), (8.0, 741), (9.0, 742)],
        "Fifo": [(1.0, 114563), (2.0, 735), (3.0, 742), (4.0, 736), (5.0, 734), (6.0, 742), (7.0, 908), (8.0, 75394), (9.0, 225042)],
    },
}

COLORS = {
    "Tiresias": "#1f77b4",  # Blue
    "Fifo": "#ff7f0e",      # Orange
    "Optimus": "#2ca02c",   # Green
}

LOADS = list(range(1, 10))


def read_metric(scheduler, load, kind, prefix="test", start=3000, end=4000):
    path = get_experiment_filepath(
        os.path.join(EXP_DIR, prefix), start, end, scheduler, load, kind,
        acceptance_policy="AcceptAll",
    )
    with open(path) as f:
        data = json.load(f)
    return statistics.mean([v[1] - v[0] for v in data.values()]) / 3600.0


def plot_figures():
    plt.rcParams.update({"font.size": 11, "figure.autolayout": True})

    # --- Figure 6: Average JCT ---
    fig, ax = plt.subplots(figsize=(7, 5))
    for sched in ["Tiresias", "Fifo", "Optimus"]:
        ys = [read_metric(sched, lo, "job_stats") for lo in LOADS]
        ax.plot(LOADS, ys, color=COLORS[sched], lw=2, marker="o", ms=6, label=f"{sched} (Simulated)")
        paper_pts = dict(PAPER_POINTS["Fig6 JCT"].get(sched, []))
        px = sorted(paper_pts.keys())
        py = [paper_pts[x] / 3600.0 for x in px]
        ax.plot(px, py, color=COLORS[sched], lw=0, marker="s", ms=8, mfc="none", mew=1.8, label=f"{sched} (Paper Fig 6)")

    ax.set_title("Figure 6: Average JCT vs Load (Philly Trace)", fontsize=13, fontweight="bold")
    ax.set_xlabel("Jobs per Hour (Load)", fontsize=11)
    ax.set_ylabel("Average JCT (Hours)", fontsize=11)
    ax.set_xticks(LOADS)
    ax.grid(True, linestyle="--", alpha=0.6)
    ax.legend(frameon=True, fontsize=9.5)

    fig6_path = os.path.join(PLOT_DIR, "figure_6_jct.png")
    fig.savefig(fig6_path, dpi=300)
    plt.close(fig)
    print(f"Generated {fig6_path}")

    # --- Figure 7: Average Responsiveness ---
    fig, ax = plt.subplots(figsize=(7, 5))
    for sched in ["Tiresias", "Fifo"]:
        ys = [read_metric(sched, lo, "responsivness") for lo in LOADS]
        ax.plot(LOADS, ys, color=COLORS[sched], lw=2, marker="o", ms=6, label=f"{sched} (Simulated)")
        paper_pts = dict(PAPER_POINTS["Fig7 Resp"].get(sched, []))
        px = sorted(paper_pts.keys())
        py = [paper_pts[x] / 3600.0 for x in px]
        ax.plot(px, py, color=COLORS[sched], lw=0, marker="s", ms=8, mfc="none", mew=1.8, label=f"{sched} (Paper Fig 7)")

    ax.set_title("Figure 7: Average Responsiveness vs Load", fontsize=13, fontweight="bold")
    ax.set_xlabel("Jobs per Hour (Load)", fontsize=11)
    ax.set_ylabel("Average Responsiveness (Hours)", fontsize=11)
    ax.set_xticks(LOADS)
    ax.grid(True, linestyle="--", alpha=0.6)
    ax.legend(frameon=True, fontsize=9.5)

    fig7_path = os.path.join(PLOT_DIR, "figure_7_responsiveness.png")
    fig.savefig(fig7_path, dpi=300)
    plt.close(fig)
    print(f"Generated {fig7_path}")


if __name__ == "__main__":
    plot_figures()
