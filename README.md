# Blox

This repository contains the source code implementation of the Eurosys 2024 paper "Blox: A Modular Toolkit for Deep Learning Schedulers". This work was done as part of Microsoft Research's [Project Fiddle](https://https://aka.ms/msr-fiddle). This source code is available under the [MIT License](LICENSE.txt).

Blox provides a modular framework for implementing deep learning research schedulers. Blox provides modular abstractions which can be easily swapped/modified to enable researchers to implement novel scheduling and placement policies.

### Abstractions Provided
* Job Admission Policy - Allows researchers to implement any admission policy and provides an interface to accept jobs.
* Cluster Management - Handle addition or deletion of available nodes.
* Job Scheduling Policy - Implement scheduling policy, i.e., deciding which jobs to run.
* Job Placement Policy - Implement placement policy, i.e., deciding which specific GPUs to run a job.
* Job Launch and Preemption - Launch/Preempt specific jobs on any node in the cluster.
* Metric Collection - Collect any metrics needed to make informed placement or launch decisions.

### Using Blox

Components of Blox are designed to be easily swappable based on different objectives. Most existing deep learning schedulers can be implemented by adding a new scheduling policy and modifying the placement policy.

### Blox Simulator

For large scale experiments, it is common practice to simulate policy behavior under different loads. Blox provides a built-in discrete-event trace simulator implemented in `simulator.py`. Researchers can configure arrival rates, loads, and workload traces.

### Blox Utilities

Blox includes plotting and metric parsing utilities. Based on configurations, Blox will automatically output metrics like Job Completion Time (JCT) and Job Completion CDFs.

### Installation

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), clone this repository, and run the following from the repository root:

```sh
uv sync
```

uv selects Python 3.11 using `.python-version`, downloads it if needed, and creates `.venv` with the dependencies recorded in `uv.lock`.

The dependency pins recorded in `uv.lock` are a best-effort reconstruction of compatible packages when the repository was last updated.

### Running Blox

This repository contains the EuroSys artifact simulation setup. Physical cluster deployment entrypoints (`resource_manager.py` and `node_manager.py`) from the original Blox prototype are not included in this checkout.

If needed for your shell session, export the protobuf implementation once (or run `source .env`):
```sh
source .env
```

Simulation requires two processes communicating over gRPC:

1. **Terminal 1 (Workload Simulator):**
```sh
uv run python simulator.py --cluster-job-log ./cluster_job_log --sim-type trace-synthetic --jobs-per-hour 6 --exp-prefix test
```

2. **Terminal 2 (Blox Manager / Scheduler):**
```sh
uv run python blox_new_flow_multi_run.py --simulate --load 6 --exp-prefix test
```

### Reproducing Results

For detailed step-by-step instructions on reproducing each figure and experiment from the paper (Figures 6, 7, 12, 13, 14, and 15), see [REPRODUCING.md](REPRODUCING.md).
