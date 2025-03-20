# Typer CLI Tool

## Overview
This guide explains how to install `Typer` and run the Python CLI tool that interacts with Kubernetes using `kubectl`.

## Prerequisites
Before you begin, ensure you have the following installed:
- **Python 3.7+** (Check with `python --version` or `python3 --version`)
- **pip** (Python package manager, comes with Python)
- **kubectl** (Check with `kubectl version --client`)

## Installation
### 1. Install Typer
To install `Typer` along with its dependencies, run:

```sh
pip install typer[all]
```

This installs `typer` along with `rich` for better CLI output.

### 2. Verify Installation
You can check if `Typer` is installed correctly by running:

```sh
python -c "import typer; print(typer.__version__)"
```

## Running the CLI Tool

Once `Typer` is installed, you can run the Python script containing the CLI tool.

### 1. Save the Script
Create a new Python file, e.g., `cli.py`, and paste your Typer-based code inside it.

### 2. Run the CLI Tool
Run the script using:

```sh
python cli.py --help
```

This will display all available commands.

### 3. Example Usage
#### Get Cluster Info
```sh
python cli.py get --cluster-info
```

#### List Pods Across All Namespaces
```sh
python cli.py get --pods
```

#### List Pods in a Specific Namespace
```sh
python cli.py get --pods --namespace my-namespace
```

## Using a Virtual Environment (Optional)
To avoid conflicts with other Python packages, you can use a virtual environment:

```sh
python -m venv myenv
source myenv/bin/activate  # macOS/Linux
myenv\Scripts\activate     # Windows
pip install typer[all]
```

Then, run the CLI tool as usual:
```sh
python cli.py --help
```

## Troubleshooting
- If you get a `ModuleNotFoundError`, ensure Typer is installed in the correct Python environment.
- If `kubectl` is not found, ensure it is installed and configured correctly

## Contribution
- Raise a PR to improve this tool