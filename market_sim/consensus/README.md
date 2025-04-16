# 🧠 Dolev-Strong Protocol Simulation

This module implements a simulation of the **Dolev-Strong consensus protocol** described in the book _Foundations of Distributed Consensus and Blockchains_ by Elaine Shi.

---

## 📁 Project Structure

```
market_sim/
├── consensus/
│   ├── dolev_strong.py         # Protocol logic
│   ├── test_dolev_strong.py    # Unit tests using unittest
│   └── visualize_consensus.py  # Visualization of results
```

---

## ⚙️ How It Works

The protocol allows a group of nodes (some potentially faulty) to reach consensus on a binary value sent by an initial node (the "sender").

- **f + 1 rounds** guarantee consensus among honest nodes.
- **Simulated digital signatures** using ID lists.
- **Byzantine faults detection** prevents message tampering.

---

## ▶️ Running the Simulation

```bash
python visualize_consensus.py
```

---

## 🧪 Running Tests

```bash
python -m unittest test_dolev_strong.py
```

---

## 📚 Based On

> **Chapter 3: Byzantine Broadcast and the Dolev-Strong Protocol**  
> Foundations of Distributed Consensus and Blockchains — Elaine Shi

---

## 📩 Contact

Simulation developed as part of the technical test for Torbellino Tech.  
For more information: [juan.diez@torbellino.tech](mailto:juan.diez@torbellino.tech)
