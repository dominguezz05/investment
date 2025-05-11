"""
Visualize consensus evolution under network delay (∆).
This script isolates the consensus simulation for plotting purposes.
"""

import argparse
from consensus.price_consensus import run_consensus_with_delay
from simulation.scenarios.market_making_scenario import plot_consensus_evolution

def main():
    parser = argparse.ArgumentParser(description="Run consensus visualization with network delay (∆).")
    parser.add_argument("--delta", type=int, default=500, help="Network delay in milliseconds (∆)")
    parser.add_argument("--rounds", type=int, default=10, help="Number of consensus rounds to simulate")
    args = parser.parse_args()

    print(f"\n📊 Running consensus simulation for AAPL (∆ = {args.delta}ms)...")
    history = []
    for _ in range(args.rounds):
        consensus_round = run_consensus_with_delay(
            symbol='AAPL',
            n=7,
            f=2,
            sender_input=150,
            corrupt_nodes=[1, 2],
            delta_ms=args.delta
        )
        history.append(consensus_round)

    plot_consensus_evolution("AAPL", history)
    print("✅ Consensus simulation completed. Plot generated.\n")

if __name__ == "__main__":
    main()
    # Execute the main function
    # to run the script directly from the command line.