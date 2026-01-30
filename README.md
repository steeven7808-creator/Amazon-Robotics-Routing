# Amazon Robotics Routing (Hackathon)

A Python-based routing agent built for an Amazon Robotics–style package delivery simulation.

The goal of this project is to route packages across a network of fulfillment centers (FCs) efficiently, maximizing delivery success rate while minimizing delivery time and total time steps.

This project was completed as part of an Amazon Robotics–themed hackathon.

---

## What I Built

- Implemented a custom routing policy in `ar_hackathon/api/routing.py` (`route_package`) that determines the next fulfillment center hop for each package at every simulation step.
- Extended the baseline strategy with a graph-based shortest-path routing approach, using NetworkX when network topology information is available.
- Evaluated routing performance using provided JSON test cases and the official simulation runner.

---

## Routing Strategy

- **Baseline**: If a package is not at its destination, route it directly to the destination fulfillment center.
- **Upgraded Strategy**: When a fulfillment center network graph is available, compute the shortest path and forward the package to the next hop along that path.
- Gracefully falls back to the baseline strategy if graph or weight information is unavailable.

This approach improves delivery success rate and reduces total delivery time in multi-hop scenarios.

---

## Tech Stack

- **Language**: Python 3
- **Libraries**: NetworkX (graph shortest-path routing)
- **Tooling**: CLI simulation runner, JSON-based test cases

---

## Project Structure

```text
ar_hackathon/
├── api/
│   └── routing.py        # Custom routing policy (route_package)
├── engine/               # Simulation engine (provided by hackathon)
├── models/               # Data models for packages and network state
├── utils/                # Helper utilities
├── visualizers/          # Visualization tools for simulation output

scripts/
└── run_game.py            # CLI entry point to run simulations

test_cases/
├── level1/
├── test_case_1.json       # Simple single-package test
└── test_case_2.json       # Multi-package, multi-hop test

team.json                  # Team and participant metadata
submit.py                  # Submission script for hackathon evaluation
setup.py                   # Python package setup
README.md                  # Project documentation
```

