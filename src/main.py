from netsquid import qubits, b00

from src.network.StarNetwork import StarNetwork


if __name__ == "__main__":
    # Initialize Network
    star_network: StarNetwork = StarNetwork()

    # Send entangled pairs to nodes 1 and 3
    # entanglement_dict = star_network.entangle_nodes(1, 3)
    entanglement_dict = star_network.entangle_nodes(1, 4)

    print(f"Qubit in Node1: {star_network.network.subcomponents['Node1'].qmemory.peek(0)}")
    print(f"Qubit in Node2: {star_network.network.subcomponents['Node2'].qmemory.peek(0)}")
    print(f"Qubit in Node3: {star_network.network.subcomponents['Node3'].qmemory.peek(0)}")
    print(f"Qubit in Repeater: {star_network.network.subcomponents['Repeater'].qmemory.peek(0)}")
    print(f"Qubit in Repeater: {star_network.network.subcomponents['Repeater'].qmemory.peek(1)}")
    print(f"Qubit in Remote Node: {star_network.network.subcomponents['RemoteNode'].qmemory.peek(0)}")
    print(f"Fidelity Node-Repeater: {1-(qubits.fidelity([star_network.network.subcomponents['Node1'].qmemory.peek(0)[0], star_network.network.subcomponents['RemoteNode'].qmemory.peek(0)[0]], b00))}")
    # print(f"Fidelity Repeater-Node: {qubits.fidelity([star_network.network.subcomponents['RemoteNode'].qmemory.peek(0)[0], star_network.network.subcomponents['Repeater'].qmemory.peek(1)[0]], b00)}")

    # print(f"Qubit in Node1: {entanglement_dict['qubits'][0]}")
    # print(f"Qubit in Node3: {entanglement_dict['qubits'][1]}")
    # print("-------------------------------------------")
    # print(f"Fidelity of the entanglement: {float(str(entanglement_dict['fidelity'])[:5]) * 100}%")
