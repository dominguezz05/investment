import pytest
from market_sim.consensus.delay_experiment import run_delay_experiment

def test_run_delay_experiment_returns_valid_data():
    delays, times, rates = run_delay_experiment()

    # Asegura que todo tenga el mismo tamaño
    assert len(delays) == len(times) == len(rates)

    # Asegura que los delays están en el rango esperado
    assert all(d in [0, 100, 300, 500, 700, 1000] for d in delays)

    # Asegura que los tiempos de ejecución sean positivos
    assert all(t > 0 for t in times)

    # Las tasas de éxito deben estar entre 0 y 1
    assert all(0 <= r <= 1 for r in rates)
