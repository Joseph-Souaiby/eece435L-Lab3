
# Project Title

## Description

This project contains two primary graphical user interfaces (GUIs) built using **PyQt** and **Tkinter**. It also includes data management modules and a model for handling the application’s core functionality.

The project is designed to offer a flexible and customizable user interface, where developers can easily switch between different GUI frameworks (PyQt or Tkinter) while maintaining the same backend logic. The `models.py` and `data_manager.py` scripts provide the backend logic that powers both GUIs.

## Features

- **Tkinter GUI**: A traditional lightweight GUI implemented in the `main_tkinter_updated.py` script.
- **PyQt GUI**: A more advanced interface built with PyQt, defined in the `main_PyQt.py` script.
- **Data Management**: Logic for managing data operations, available in `data_manager.py`.
- **Models**: Application logic, separated from the UI, to ensure modularity, available in `models.py` and `models_PyQt.py`.

## Installation

To run the project, you'll need to have Python installed, along with the necessary libraries such as `tkinter`, `PyQt5`, and any other required dependencies.

1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```

2. Install the dependencies:
   ```bash
   pip install pyqt5
   ```
   ```bash
   pip install tkinter
   ```

3. Run either the Tkinter or PyQt version:
   - **Tkinter version**:
     ```bash
     python main_tkinter_updated.py
     ```
   - **PyQt version**:
     ```bash
     python main_PyQt.py
     ```

## Usage

Depending on your preference, you can choose between the Tkinter or PyQt version of the application.

- To launch the **Tkinter** version, execute `main_tkinter_updated.py`.
- To launch the **PyQt** version, execute `main_PyQt.py`.

Both interfaces use the same underlying logic and functionality, which is abstracted in the `models.py` and `data_manager.py` scripts.

## File Structure

- **main_PyQt.py**: The main entry point for the PyQt GUI version.
- **main_tkinter_updated.py**: The main entry point for the Tkinter GUI version.
- **models.py**: Contains core application logic and models.
- **models_PyQt.py**: A specialized model for PyQt-based applications.
- **data_manager.py**: Handles data operations and management.
