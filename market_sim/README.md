# Market Dynamics and Trading Simulation Framework

Implements a framework for simulating, analyzing, and learning about financial markets, trading strategies, and blockchain integration.

Currently v0.

## Project Structure

```
market_sim/
├── core/                      # Core functionality and base classes
│   ├── data/                 # Data management and storage
│   ├── models/              # Core market models and entities
│   └── utils/               # Utility functions and helpers
│
├── market/                   # Market simulation components
│   ├── exchange/            # Exchange mechanisms and matching engines
│   ├── agents/              # Trading agents and strategies
│   ├── mechanisms/          # Trading mechanisms (options, warrants, etc.)
│   └── dynamics/            # Market dynamics and price formation
│
├── strategies/               # Trading strategies implementation
│   ├── traditional/         # Classical trading strategies
│   ├── hft/                 # High-frequency trading strategies
│   └── ml/                  # Machine learning based strategies
│
├── simulation/              # Simulation framework
│   ├── engine/             # Simulation engine and time management
│   ├── scenarios/          # Pre-defined simulation scenarios
│   └── results/            # Results analysis and visualization
│
├── blockchain/              # Blockchain integration
│   ├── ethereum/           # Ethereum specific implementations
│   ├── consensus/          # Consensus mechanisms
│   └── contracts/          # Smart contracts
│
├── analysis/                # Analysis tools and utilities
│   ├── metrics/            # Performance and risk metrics
│   ├── visualization/      # Data visualization tools
│   └── reports/            # Report generation
│
├── api/                     # API interfaces
│   ├── rest/               # REST API
│   └── websocket/          # WebSocket API
│
├── ui/                      # User interfaces
│   ├── web/                # Web interface
│   ├── cli/                # Command-line interface
│   └── desktop/            # Desktop application
│
└── tests/                   # Test suite
    ├── unit/               # Unit tests
    ├── integration/        # Integration tests
    └── performance/        # Performance tests
```

## Features

### Market Simulation

- Real-time market simulation with configurable parameters
- Multiple asset types and trading mechanisms
- Price formation and order book management
- Trading agent framework with customizable strategies

### Trading Mechanisms

- Stock trading with various order types
- Options and warrants simulation
- Short selling and margin trading
- Custom mechanism creation framework

### High-Frequency Trading

- Ultra-low latency framework
- Order execution optimization
- Market making strategies
- Statistical arbitrage

### Blockchain Integration

- Ethereum smart contract integration
- Consensus mechanism simulation
- Cross-chain trading strategies
- DeFi protocol integration

### Byzantine Consensus with Network Delay (∆)

- Implementation of the Dolev-Strong protocol with configurable network delay
- Custom simulation scenarios for testing how ∆ impacts consensus speed and stability
- Support for corrupt nodes simulating Byzantine failures
- Realistic integration into market scenarios for price-setting mechanisms
- Experimental framework (`delay_experiment.py`) for testing various values of ∆
- Graphical output comparing execution time and success rate across delays

### Learning Environment

- Interactive tutorials and scenarios
- Strategy backtesting framework
- Performance analytics
- Risk management tools

## Getting Started

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run tests:

```bash
# Run all tests
pytest

# Run specific test categories
pytest tests/unit/
pytest tests/integration/
pytest tests/performance/

# Run with coverage
pytest --cov=market_sim

# Run specific test file
pytest tests/integration/test_market_making.py
pytest tests/test_delay_experiment.py
```

### Run Delay Impact Experiment (∆ vs Performance)

```bash
python market_sim/consensus/delay_experiment.py
```

This generates a high-resolution plot (delay_vs_consensus.png) showing how consensus behavior changes with increasing ∆.

### Visualize Consensus Evolution

```bash
python simulation/scenarios/visualize_consensus.py --delta 500 --rounds 10
```

This script runs 10 consensus rounds for the symbol AAPL using the Dolev-Strong protocol and visualizes the evolution of consensus values under a network delay ∆ of 500 milliseconds.

You can customize:

--delta: Simulated network delay in milliseconds (e.g. 100, 500, 1000)

--rounds: Number of consensus rounds to simulate

## License

This project is licensed under the MIT License - see the LICENSE file for details.
