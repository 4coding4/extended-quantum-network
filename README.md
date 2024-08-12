# Quantum Network
[![Tests Status](./reports/junit/junit-badge.svg?dummy=8484744)](./reports/junit/report.html)
[![Coverage Status](./reports/coverage/coverage-badge.svg?dummy=8484744)](./reports/coverage/index.html)
[![Flake8 Status](./reports/flake8/flake8-badge.svg?dummy=8484744)](./reports/flake8/index.html)

This is an implementation of a Quantum Network in python using the NetSquid library. The topology of the network is a Star topology, this means that the center of the network is a Quantum Source that generates entangled Bell pairs. On the other hand, the points of the star are nodes with quantum memories.

One of the points of the network is a Quantum Repeater. This repeater is connected to a remote node which has a Quantum Source as well as a quantum memory. The repeater will receive one qubit from the source, one qubit from the remote node, and will perform Entanglement Swapping on those qubits.

A more detailed report on the project can be found [here](https://github.com/edoriggio/quantum-network/blob/main/docs/report.pdf)

## Docker

### Download
A pre-built docker image can be downloaded by running the following command:

```bash
docker pull ghcr.io/edoriggio/quantum-network:main
```

Alternatively, you can directly include the image in your Dockerfile by using the following line:

```dockerfile
FROM ghcr.io/edoriggio/quantum-network:main
```

### Build
To build the docker image, use the following line of code

```bash
docker build -t quantum_network --build-arg USERNAME=<username> --build-arg PASSWORD=<password> .
```

Where `<username>` and `<password>` are the credentials used for accessing [NetSquid](https://docs.netsquid.org)

### Using as Python Interpreter
If you're using **PyCharm**, you can do the following:

If you are using the pre-built docker image do:
1. Click on the bottom right where the python interpreter name usually is;
2. `Add New Interpreter > On Docker...`;
3. Select your docker server;
   - if you don't have one click on the drawer, then `Create new... > Docker for Mac > OK`);
4. Select `pull`;
5. Write `quantum_network` in the textfield;
6. Click on `Next`.

If you are using the built the docker image do:
1. Click on the bottom right where the python interpreter name usually is;
2. `Add New Interpreter > On Docker...`;
4. Select `Build`;
5. Keep Dockerfile as `Dockerfile` and Context folder as `.`;
6. Click on Optional;
7. Write in `Build Args` the following `USERNAME=<username> PASSWORD=<password>`
8. Click on `Next`.
9. Click on `Next`.
