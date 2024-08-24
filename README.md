# Paper Replication

Students:
- Yuval Weinstein
- Ran Schreiber

This repository contains code and results of the replication of the experiments in *Can Poverty Be
Reduced by Acting on Discrimination? An Agent-based Model for Policy Making* by Aguilera et al.,
published in AAMAS 2024

It contains code from the paper's
[official repository](https://github.com/albaaguilera/Aporophobia), with a few required fixes. We
added the following files:
- `replication_notebooks/` - Jupyter notebooks that present the replications: running the
  simulations and producing measures and graphs of different types.
- `create_graphs.py` - A utility script that reads simulation results and creates the corresponding
  graphs.
- `graphs/` - Directory with the graphs produced using `create_graphs.py` over our replications.
- `Results/analyze.ipynb` - A Jupyter notebook that briefly presents a single results file to make
  its format clearer and shows a sample query over the data.

