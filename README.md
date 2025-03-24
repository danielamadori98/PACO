# RESPISE
![Build Status](https://github.com/danielamadori98/PACO/actions/workflows/tests.yml/badge.svg)
![License](https://img.shields.io/github/license/danielamadori98/PACO)
![Docker Pulls](https://img.shields.io/docker/pulls/danielamadori/paco)
![Python Version](https://img.shields.io/badge/python-3.12%2B-blue)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/danielamadori98/PACO)
![GitHub issues](https://img.shields.io/github/issues/danielamadori98/PACO)
![GitHub pull requests](https://img.shields.io/github/issues-pr/danielamadori98/PACO)
![GitHub contributors](https://img.shields.io/github/contributors/danielamadori98/PACO)


## A strategy founder for *BPMN + CPI*

## Features

- Models complex business processes with probabilistic decision points
- Provides a strategy synthesis algorithm for BPMN+CPI diagrams
- Web-based interface using Dash for visualizations

## Description

In the context of increasingly complex business processes, accurately modeling decision points, their probabilities, and resource utilization is essential for optimizing operations. To tackle this challenge, we propose an extension to the Business Process Model and Notation (BPMN) called BPMN+CPI. This extension incorporates choices, probabilities, and impacts, emphasizing precise control in business process management. Our approach introduces a timeline-based semantics for BPMN+CPI, allowing for the analysis of process flows and decision points over time. Notably, we assume that all costs, energies, and resources are positive and exhibit additive characteristics, leading to favorable computational properties. Real-world examples demonstrate the role of probabilistic decision models in resource management.

### Solver
RESPISE is an algorithm that given a *BPMN + CPI*  diagram and a bound impact vector can determine if there exists a feasible strategy such that the process can be completed while remaining under the bound vector. Moreover, We explain the synthesized strategies to users by labeling choice gateways in the BPMN diagram, making the strategies more interpretable and actionable.
![alt text](image.png)

## Prerequisites

To run the application, you can use either **Python** or **Docker**. Only one of these is required.

- **Python 3.12+**
- **Docker**

To install **Python**, follow the instructions on [Python's official website](https://www.python.org/downloads/). For **Docker**, you can find installation steps on [Docker's official website](https://docs.docker.com/get-docker/).

---

## Quick Start

### Using Docker

To start the application using Docker, follow these steps:

1. Pull and start the Docker:
    ```bash
    docker pull danielamadori/paco:latest
    docker run -d -p 8000:8000 -p 8888:8888 -it --name PACO danielamadori/paco:latest
    docker logs PACO
    ```
   Note: Replace latest with a specific version number if needed.
2. Open a browser and navigate to `http://127.0.0.1:8000` to access the application via REST API.
   The docs are available at `http://127.0.0.1:8000/docs`
3. Open another browser tab and go to `http://127.0.0.1:8888` to access the Jupyter environment.  
   You will find multiple `.ipynb` notebooks available — **we recommend [starting with `tutorial.ipynb`](tutorial.ipynb)**, which provides a guided walkthrough of the main functionalities.

### Using Python
To start the application using Python, follow these steps:
1. **Environment Setup**
- **Using Conda**
    ```bash
    conda create --name paco python=3.12
    conda activate paco
    ```
- **Using venv**
  ```bash
  python3.12 -m venv paco_env
  source paco_env/bin/activate  # On macOS/Linux
  paco_env\Scripts\activate     # On Windows
  ```
2. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3. Run the **PACO server**:
    ```bash
    python3 src
    ```
   Open a browser and navigate to `http://127.0.0.1:8000` to access the application via REST API.
   The docs are available at `http://127.0.0.1:8000/docs`

3. Run the **jupyter notebook**:
    ```bash
    jupyter notebook --port=8888
    ```
4. Open another browser tab and go to `http://127.0.0.1:8888` to access the Jupyter environment.  
   You will find multiple `.ipynb` notebooks available — **we recommend [starting with `tutorial.ipynb`](tutorial.ipynb)**, which provides a guided walkthrough of the main functionalities.

---
NB! This application is currently under development. There may be some issues and bugs.


## Running Benchmark
Ensure that all dependencies are installed and the environment is correctly set up before running the tests.

**Run the script**
- Linux
    ```bash
    chmod +x run_benchmark.sh
    ./run_benchmark.sh
    ```
- Windows
    ```batch
    .\run_benchmark.bat
    ```

These scripts will execute a series of tests to validate the functionality of the application. 

## Authors

* **Daniel Amadori**
* **Emanuele Chini**
* **Pietro Sala**
* **Andrea Simonetti**
* **Omid Zare**

## Contributing

If you want to contribute to RESPISE, you can create your own branch and start programming.

## License

RESPISE is licensed under MIT license.