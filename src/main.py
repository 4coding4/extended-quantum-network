from src.network.StarNetwork import StarNetwork


if __name__ == "__main__":
    # Initialize Network
    star_network: StarNetwork = StarNetwork()

    # Send entangled pairs to nodes 1 and 3
    entanglement_dict = star_network.entangle_nodes(1, 3)
    print(f"Qubit in Node1: {entanglement_dict['qubits'][0]}")
    print(f"Qubit in Node3: {entanglement_dict['qubits'][1]}")
    print("-------------------------------------------")
    print(f"Fidelity of the entanglement: {float(str(entanglement_dict['fidelity'])[:5]) * 100}%")
