import matplotlib.pyplot as plt
from dolev_strong import simulate_consensus

def run_and_visualize():
    corrupt_sets = [[], [1], [1, 2]]
    labels = ["0 corrupt", "1 corrupt", "2 corrupt"]
    sender_input = 1
    n = 7
    f = 2

    plt.figure(figsize=(10, 6))
    for corrupt_nodes, label in zip(corrupt_sets, labels):
        result = simulate_consensus(n=n, f=f, sender_input=sender_input, corrupt_nodes=corrupt_nodes)
        plt.plot(range(len(result)), result, marker='o', label=f"{label}: {result}")

    plt.title("Resultados del Protocolo Dolev-Strong")
    plt.xlabel("Nodo")
    plt.ylabel("Bit de salida")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_and_visualize()
# This code visualizes the results of the Dolev-Strong consensus protocol simulation with different corrupt node scenarios. 