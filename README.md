# Extended Quantum Network
[![Tests Status](./badges/tests-badge.svg?dummy=8484744)](./reports/junit/junit.xml)
[![Coverage Status](./badges/coverage-badge.svg?dummy=8484744)](./reports/coverage/coverage.xml)
[![Flake8 Status](./badges/flake8-badge.svg?dummy=8484744)](./reports/flake8/flake8stats.txt)

![Protocol a high-level architecture](./docs/protocol-a-high-level-architecture-only.drawio.png "Protocol a high-level architecture")

For more information about the architecture (legend, port and memories mapping and swapping in the repeater), see the 2 following diagrams: 
[Protocol a](./docs/protocol-a.drawio.png) 
and
[Detailed protocol a](./docs/detailed-protocol-a.drawio.png)
----------------------------------------------------------------
This is an implementation of a Quantum Network in [python](https://www.python.org) using the [NetSquid](https://netsquid.org) library. 

The method `protocol_a` is the implementation of the example in page 4 of the following scientific paper:

[Anita Buckley](https://orcid.org/0000-0002-4493-2999), 
[Pavel Chuprikov](https://orcid.org/0000-0002-6673-1143), 
[Rodrigo Otoni](https://orcid.org/0000-0003-1097-2367), 
[Robert Soulé](https://orcid.org/0000-0002-2825-6660), 
[Robert Rand](https://orcid.org/0000-0001-6842-5505) and 
[Patrick Eugster](https://orcid.org/0000-0003-3864-9078).
[An Algebraic Language for Specifying Quantum Networks](https://dl.acm.org/doi/10.1145/3656430). 
[Proceedings of the ACM on Programming Languages 8, PLDI](https://dl.acm.org/toc/pacmpl/2024/8/PLDI), 
Article 200 (20 June 2024), 23 pages. 
[https://doi.org/10.1145/3656430](https://doi.org/10.1145/3656430).

This academic research work was founded via the 
[Undergraduate Research Opportunities Program (UROP)](https://www.inf.usi.ch/en/informatics-research/internships/students) 
program and was supervised by 
[Anita Buckley](https://orcid.org/0000-0002-4493-2999) and
[Pavel Chuprikov](https://orcid.org/0000-0002-6673-1143) 
in [Università della Svizzera Italiana (USI)](https://www.usi.ch/).

The report of the project can be found [here](./docs/Extended_Quantum_Network_Manual.pdf).

A more detailed report on the [old project](https://github.com/edoriggio/quantum-network) (method `entangle_nodes`) can be found [here](./docs/old/report.pdf).

----------------------------------------------------------------

The topology of the network is a Star topology, this means that the center of the network is a Quantum Source that generates entangled Bell pairs. 
On the other hand, the points of the star are nodes with quantum memories.

One of the points of the network is a Quantum Repeater. 
This repeater is connected to a remote node which has a Quantum Source as well as a quantum memory. 
The repeater will receive one qubit from the source, one qubit from the remote node, and will perform Entanglement Swapping on those qubits.

----------------------------------------------------------------
## Program usage:
To show the usage in the terminal use the following command
```bash
python3 main.py help
```
The usage command structure is the following:
```bash
python3 main.py <models_name> <method_name> <nodes> <debug> <experiment_num>
```
Where:
* `<models_name>` can be either: `combined` or `empty`, 
with the default value set to `empty`,
that enables/disables the quantum: loss, noise and delay models.
* `<method_name>` can be either: `protocol_a` or `entangle_nodes`,
with the default value set to `protocol_a`,
that selects the method to use to send the qubits.
* `<nodes>` is a comma separated list of numbers between 1 and 4 (both included), with 2 or 3 numbers
(2 for using `entangle_nodes` and 3 for using `protocol_a`),
with the default value set to `1,2,4`,
that represents the nodes to connect with entangled qubits.
* `<debug>` can be either: `False` or `True`,
with the default value set to `True`,
that enables/disables the print of additional debug information, in the standard output (in the terminal).
* `<experiment_num>` is a positive number (0 included),
with the default value set to 0,
that enables the execution of the program via the experiment wrapper (when not 0) 
that executes the program that amounts of times for every different channel length 
(to get an approximated statistical probability of the execution/operations) as well as
collecting data (as `csv` file format) and 
generating the corresponding plots 
about the fidelity of the qubits over different channel length (as `png` file format) 
automatically (in the folder called `out`) with name of the inputted values;
otherwise (with 0) it does not collect and generates anything (by not using the experiment wrapper) and 
simply displays the results in the standard output (in the terminal).

## Examples
Default, an unrealistic (almost perfect system) simulation for `protocol_a`:
```bash
python3 main.py
```
is equivalent to the following:
```bash
python3 main.py empty protocol_a 1,2,4 True 0
```

Realistic simulation for `protocol_a` with 1 execution and no data collection and plot generation
```bash
python3 main.py combined protocol_a 1,2,4 True 0
```
Realistic simulation for `protocol_a` with 100 execution and data collection and plot generation
```bash
python3 main.py combined protocol_a 1,2,4 True 100
```

Unrealistic (almost perfect system) simulation for `entangle_nodes`:
```bash
python3 main.py empty entangle_nodes 1,4 True 0
```
Realistic simulation for `entangle_nodes` with 1 execution and no data collection and plot generation
```bash
python3 main.py combined entangle_nodes 1,4 True 0
```
Realistic simulation for `entangle_nodes` with 100 execution and data collection and plot generation
```bash
python3 main.py combined entangle_nodes 1,4 True 100
```

On request, the used PyCharm run configuration files can be shared.
## Docker Setup

### Download (Not Recommended, limited support for scripts and libraries)
A pre-built docker image can be downloaded by running the following command:

```bash
docker pull ghcr.io/edoriggio/quantum-network:main
```

Alternatively, you can directly include the image in your Dockerfile by using the following line:

```dockerfile
FROM ghcr.io/edoriggio/quantum-network:main
```

### Build (Recommended)
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
