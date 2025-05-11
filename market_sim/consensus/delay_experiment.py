import time
import matplotlib.pyplot as plt
from datetime import datetime
from decimal import Decimal
from market_sim.consensus.price_consensus import create_price_consensus_network

from core.models.base import Trade
from core.utils.time_utils import utc_now
from uuid import uuid4
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))


def create_test_trade(symbol: str, price: Decimal) -> Trade:
    return Trade(
        id=uuid4(),
        symbol=symbol,
        price=price,
        quantity=Decimal('100'),
        buyer_order_id=uuid4(),
        seller_order_id=uuid4(),
        timestamp=utc_now()
    )
    
    
def run_delay_experiment():
    delays = [0, 100, 300, 500, 700, 1000]
    execution_times = []
    success_rates = []

    symbol = "AAPL"
    prices = [Decimal('150.0'), Decimal('151.0'), Decimal('149.5'),
              Decimal('150.5'), Decimal('150.2')]

    for delta in delays:
        successes = 0
        total_time = 0

        for _ in range(5):  # 5 repeticiones por delay
            network = create_price_consensus_network(num_nodes=7, fault_tolerance=2)
            network.corrupt_nodes = [1, 2]  # nodos corruptos

            for price in prices:
                trade = create_test_trade(symbol, price)
                network.add_trade(trade, datetime.now())

            start = time.time()
            result = network.run_consensus_with_delay(symbol, datetime.now(), delta)
            end = time.time()

            total_time += (end - start)
            if result is not None:
                successes += 1

        execution_times.append(round(total_time / 5, 4))
        success_rates.append(round(successes / 5, 2))

    return delays, execution_times, success_rates


def plot_results(delays, execution_times, success_rates):
    fig, ax1 = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('white')

    # Primer eje: tiempo de ejecución
    ax1.set_xlabel("∆ (ms)", fontsize=12)
    ax1.set_ylabel("Avg Execution Time (s)", color='tab:blue', fontsize=12)
    ax1.plot(delays, execution_times, marker='o', color='tab:blue', linewidth=2, markersize=8, label="Execution Time")
    ax1.tick_params(axis='y', labelcolor='tab:blue')
    ax1.grid(True, linestyle='--', alpha=0.5)

    # Segundo eje: tasa de éxito
    ax2 = ax1.twinx()
    ax2.set_ylabel("Success Rate", color='tab:green', fontsize=12)
    ax2.plot(delays, success_rates, marker='s', color='tab:green', linewidth=2, markersize=8, label="Success Rate")
    ax2.tick_params(axis='y', labelcolor='tab:green')

    # Título y layout
    plt.title("Consensus Performance vs Network Delay (∆)", fontsize=14, weight='bold')
    fig.tight_layout()

    # Leyenda
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper right')

    # ✅ Guardar imagen de alta calidad
    plt.savefig("delay_vs_consensus.png", dpi=300)

    plt.show()
    plt.close(fig)
    


if __name__ == "__main__":
    delays, times, rates = run_delay_experiment()
    plot_results(delays, times, rates)
