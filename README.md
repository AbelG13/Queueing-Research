# Processor Sharing Queue Simulator (M/M/1/PS)

This repository contains a simulation of a processor-sharing (PS) queueing system developed as part of an ongoing machine learning research project on fairness in job scheduling and queue management.

The simulator models an **single-server queue with processor-sharing discipline**, allowing for experimentation with key system features such as **job abandonment**, **infection spread**, and **shared service dynamics**.

## 🔍 Project Context

This code was developed during my time as a **Research Assistant** at Cornell University. The broader research explores fairness in scheduling policies within cloud computing and data center environments.

Key goals of the project include:
- Understanding how queue disciplines affect job abandonment and infection propagation.
- Using queue simulations to generate datasets for predictive modeling and fairness analysis.
- Exploring realistic constraints faced in large-scale computing systems.

## 🛠️ Features

- Discrete-event simulation of an M/M/1/PS queue
- Supports:
  - Random inter-arrival and service times
  - Job abandonment after a fixed timeout
  - Infection propagation via overlapping queue presence
- Outputs per-job statistics including:
  - Response time
  - Abandonment status
  - Queue length at arrival
  - Time of infection and overlap exposure

## 🚀 Example Usage

To run the simulator using exponential arrival and service times (M/M/1/PS), see the provided example in:

**`main.py`**

This script initializes the simulation with random parameters, runs the queue, and prints per-job statistics to the console.
