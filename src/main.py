from src.network.StarNetwork import StarNetwork


if __name__ == "__main__":
    # Initialize Network
    star_network: StarNetwork = StarNetwork()

    # Send entangled pairs to nodes 1 and 4
    entanglement_dict = star_network.entangle_nodes(1, 4)

    print(f"Qubit in Node1: {entanglement_dict['qubits'][0]}")
    print(f"Qubit in RemoteNode: {entanglement_dict['qubits'][1]}")
    print("-------------------------------------------")
    print(f"Fidelity of the entanglement: {float(round(entanglement_dict['fidelity'], 2)) * 100}%")
