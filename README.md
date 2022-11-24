# Quantum Network

## Docker

### Build
To build the docker image, use the following line of code

```bash
docker build -t quantum_network --build-arg USERNAME=<username> --build-arg PASSWORD=<password> .
```

Where `<username>` and `<password>` are the credentials used for accessing [NetSquid](https://docs.netsquid.org)

### Using as Python Interpreter
If you're using **PyCharm**, you can do the following:

1. Click on the bottom right where the python interpreter name usually is;
2. `Add New Interpreter > On Docker...`;
3. Select your docker server;
   - if you don't have one click on the drawer, then `Create new... > Docker for Mac > OK`);
4. Select `pull`;
5. Write `quantum_network` in the textfield;
6. Click on `Next`.
