# Real-Time System Metrics Pipeline 🐧🐳📈

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Ubuntu](https://img.shields.io/badge/Ubuntu-22.04-orange)
![WSL](https://img.shields.io/badge/WSL-2.3.26.0-brightgreen)
![Docker](https://img.shields.io/badge/Docker-🐳-brightblue)
![License](https://img.shields.io/badge/License-MIT-green)

A Python-based system metrics pipeline designed to collect, analyze, and visualize real-time system metrics for open-source servers. This project showcases **data engineering**, **Linux proficiency**, and **cloud deployment skills**, focus on open-source technologies.

---

## Table of Contents 📋
1. [Overview](#overview)
2. [Features](#features)
3. [Technologies Used](#technologies-used)
4. [System Requirements](#system-requirements)
5. [Installation](#installation)
6. [Usage Instructions](#usage-instructions)
7. [Pipeline Workflow](#pipeline-workflow)
8. [Makefile Commands](#makefile-commands)
9. [Contributing](#contributing)
10. [License](#license)

---

## Overview 📝

This project is developed using **WSL2 (Ubuntu 22.04.5 LTS)** and will be deployed on a Virtual Private Server (VPS) hosted by **OVH**. 

The system collects and processes **real-time metrics** (e.g., CPU usage, memory, and disk I/O) from open-source servers. The pipeline evolves in two phases:
1. **Phase 1**: Metrics collected via files from server logs, visualized in a dashboard.
2. **Phase 2**: Metrics are collected directly in real-time from user systems, following a legal agreement. Data is stored temporarily and deleted at midnight to optimize VPS resources.

---

## Features ✨
- **Graphical Dashboard**: Visualizes server system metrics in real-time.
- **Real-Time Data Collection**: Metrics captured directly from users.
- **Legal Compliance**: User consent is stored securely in the database.
- **Optimized for Efficiency**: Data is automatically deleted at midnight to save VPS resources.
- **Open-Source Focus**: Designed for use with open-source server systems.

---

## Technologies Used 🛠️
- **Programming Language**: Python 3.12 🐍
- **Framework**: Flask for API endpoints and consent handling 🌐
- **Database**: kdb+/q for efficient data querying 🗄️
- **Containerization**: Docker 🐳
- **Platform**: WSL2 (Ubuntu 22.04.5 LTS) 🐧
- **Dependency Management**: Poetry 🎵
- **Unit Testing**: Pytest, integrated with Makefile.

---

## System Requirements 📦
- **Operating System**: WSL2 (Ubuntu 22.04 or higher)
- **Python Version**: 3.12 or above
- **Docker**: Latest version
- **Make**: To simplify project setup and management

---

## Installation 🛠️

## Step 1: Clone the Repository
``bash

git clone https://github.com/KedarSki/sys_metric_pipeline.git
cd sys_metric_pipeline

## Step 2: Install Poetry 🎵

Use the Makefile to download Poetry for dependency management:

``bash

make poetry-download

## Step 3: Set Up a Virtual Environment 🔧

Activate the .venv and install dependencies:

``bash

poetry shell
poetry install --with dev

## Step 4: Build Docker Image 🐳
Build the container for deployment:

``bash

docker build -t sys-metric-pipeline .

---

## Usage Instructions 🚀

### For Phase 1 (Graphical Dashboard)
1. **Start the API Server**:

``bash

flask run --host=0.0.0.0 --port=5000
2. Access the Dashboard: Open your browser and navigate to:
http://<your-server-ip>:5000

### For Phase 2 (Real-Time Data Pipeline)
1. **User Legal Agreement**: Users must run the provided script and accept the agreement. The system securely stores their consent in the database.
2. **Collect Metrics**: Metrics are automatically collected and transmitted in real-time.
3. **Automated Cleanup**: Data older than 24 hours is deleted at midnight to optimize VPS resources.


---

### Pipeline Workflow 🔄

``markdown

1. **Data Collection**:
   - **Phase 1**: Collects metrics from log files.
   - **Phase 2**: Captures real-time metrics directly from user systems.
2. **Data Processing**:
   - Data is stored in **kdb+/q** for efficient querying.
3. **Visualization**:
   - Metrics visualized on the dashboard via Flask.
4. **Data Cleanup**:
   - Obsolete data is deleted at midnight to optimize the VPS.


### Makefile Commands 🛠️

The project uses a **Makefile** to simplify common tasks:

- **Download Poetry**:

``bash

make poetry-download

- **Install Dependencies**:

``bash

make poetry-install-deps

- **Run Tests**:

``bash

make check-all

- **Run Linters**:

``bash

  - Black: make black_check
  - Pylint: make pylint
  - MyPy: make mypy

---

## Contributing 🤝

Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a feature branch.
3. Submit a pull request.

## License 📜

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
