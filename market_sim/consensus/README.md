# Market Simulation with Price Consensus

This project implements a simulated financial market environment featuring:

- A **market maker** strategy that adjusts bid-ask spreads based on price volatility and inventory risk.
- Multiple **random traders** that simulate market pressure.
- An integrated **Byzantine fault-tolerant price consensus mechanism**.
- Support for **corrupted nodes manipulating prices**.
- **Price updates via market events** using consensus output.
- Visualization of **price consensus evolution over time** with matplotlib.

---

## 🧠 Features & Architecture

### ✅ Matching Engine

- Handles both **limit** and **market orders**.
- Implements **order book management** and **trade execution**.
- Updates order status (partial, filled, cancelled).

### ✅ Market Maker Strategy

- Maintains market liquidity on both sides.
- Adapts spread based on **volatility** and **inventory skew**.
- Receives and uses **consensus prices** as mid-price inputs.
- Can dynamically adjust order sizes to reduce inventory risk.

### ✅ Market Simulation Engine

- Manages:
  - **Time steps**
  - **Order events**
  - **Market events**
- Records:
  - Trades
  - Order book snapshots
  - Agent and market metrics

### ✅ Price Consensus Integration

- Each simulation tick can trigger a **consensus round**.
- The **agreed price** is set as the new mid-price via `set_initial_price`.
- Market makers receive the updated price with `update_consensus_price()`.

### ✅ Fault Tolerance Simulation

- You can specify a number of **Byzantine (corrupted) nodes**.
- These nodes can inject **manipulated prices**.
- Honest nodes still reach **correct consensus** based on majority.

### ✅ Visualization

- Real-time consensus evolution can be plotted with:

```python
plot_consensus_evolution("AAPL", history)
```

---

## 📁 Folder Structure

```
.
├── core/
│   └── models/
│       └── base.py
├── market/
│   ├── agents/
│   │   ├── base_agent.py
│   │   └── market_maker.py
│   └── exchange/
│       └── matching_engine.py
├── simulation/
│   └── engine/
│       └── simulation_engine.py
├── consensus/
│   └── price_consensus.py
├── scenarios/
│   └── market_making_scenario.py
└── README.md
```

---

## 🧪 How to Run

```bash
python scenarios/market_making_scenario.py
```

This will:

- Create a market with 3 symbols (`AAPL`, `MSFT`, `GOOGL`).
- Run consensus every 15 minutes.
- Inject initial price with consensus.
- Simulate random trades and order book activity.
- Show statistics + a matplotlib graph of price consensus over time.

---

## 🧠 Example Output

```
Creating market making scenario...
Running simulation...

Simulation completed!
Total trades: 324
Number of market events: 15

AAPL Statistics:
Number of trades: 115
Average price: $149.62
Price volatility: 0.0178
...

[Matplotlib plot showing evolution of consensus price]
```

---

## ✅ Implemented Improvements

- [x] `set_initial_price()` with bid/ask adjustment.
- [x] `update_consensus_price()` for strategy input.
- [x] Fault-injected consensus with `corrupt_nodes`.
- [x] Graphical visualization of consensus rounds.
- [x] Integration of `run_consensus()` into simulation loop.
- [x] Realistic market making behavior adapting to consensus.
