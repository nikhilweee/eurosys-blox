# Reproducing Paper Results

This guide provides instructions for reproducing the simulation results and figures from the EuroSys 2024 paper *"Blox: A Modular Toolkit for Deep Learning Schedulers"*.

Each experiment runs two communicating processes over gRPC (ports `50050` and `50051`):
1. **Simulator (Terminal 1)**: Ingests the trace and feeds jobs/advances time.
2. **Scheduler / Blox Manager (Terminal 2)**: Runs the scheduling, admission, and placement logic.

Ensure dependencies are installed via `uv sync` before running experiments. Run all commands from the repository root, and run `source .env` if needed for your shell session.

---

### Figure 6 & Figure 7: Scheduler Evaluation (FIFO, Tiresias, LAS, Optimus)

Evaluates FIFO, Tiresias, LAS, and Optimus policies on the Microsoft Philly trace.

**Terminal 1 (Workload Simulator):**
```sh
uv run python simulator.py --cluster-job-log ./cluster_job_log --sim-type trace-synthetic --jobs-per-hour 6 --exp-prefix test
```

**Terminal 2 (Blox Manager):**
```sh
uv run python blox_new_flow_multi_run.py --simulate --load 6 --exp-prefix test
```

*Output:* Generates responsiveness, JCT CDFs, and run-time statistics for each scheduler.

---

### Figure 12: Admission Control Policies

Evaluates LAS scheduler with different admission control policies (AcceptAll vs. LoadBasedAccept).

**Terminal 1 (Simulator with Admission Policy):**
```sh
uv run python simulator_acceptance_policy.py --cluster-job-log ./cluster_job_log --sim-type trace-synthetic --jobs-per-hour 6 --exp-prefix test
```

**Terminal 2 (Blox Manager):**
```sh
uv run python blox_new_flow_multi_run.py --simulate --load 6 --exp-prefix test
```

*Output:* Generates average JCTs comparing admission policies under load.

---

### Figure 12 & Figure 13: Dual-Load Evaluation

Evaluates schedulers and admission policies under dual-load synthetic bursts.

**Terminal 1 (Dual-Load Simulator):**
```sh
uv run python simulator_dual_load.py --cluster-job-log ./cluster_job_log --sim-type trace-synthetic --jobs-per-hour 6 --exp-prefix test
```

**Terminal 2 (Blox Manager):**
```sh
uv run python blox_new_flow_multi_run.py --simulate --load 6 --exp-prefix test
```

*Output:* Generates JCT CDFs, GPU demand, and free GPU metrics under variable load.

---

### Figure 14 & Figure 15(b): Dynamic Policy Scheduler

Evaluates dynamic policy switching under fluctuating cluster load.

**Terminal 1 (Dual-Load Simulator):**
```sh
uv run python simulator_dual_load.py --cluster-job-log ./cluster_job_log --sim-type trace-synthetic --jobs-per-hour 6 --exp-prefix test
```

**Terminal 2 (Dynamic Policy Runner):**
```sh
uv run python blox_new_flow_dynamic_policy.py --cluster-job-log ./cluster_job_log --sim-type trace-synthetic --jobs-per-hour 6 --exp-prefix test
```

*Output:* Generates run-time statistics and policy transition logs.

---

### Figure 15(a): Small vs. Large Job Mix Dynamic Scheduling

Evaluates dynamic policy adaptations with skewed small vs. large job distributions.

**Terminal 1 (Small/Large Dual-Load Simulator):**
```sh
uv run python simulator_dual_load_small_large.py --cluster-job-log ./cluster_job_log --sim-type trace-synthetic --jobs-per-hour 6 --exp-prefix test
```

**Terminal 2 (Dynamic Policy Runner):**
```sh
uv run python blox_new_flow_dynamic_policy.py --cluster-job-log ./cluster_job_log --sim-type trace-synthetic --jobs-per-hour 6 --exp-prefix test
```
