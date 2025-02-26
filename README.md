# ordinary-differential-equation-solver

A Python-based GUI application for solving ordinary differential equations (ODEs) using numerical methods.

## Features
- Solve first-order ODEs
- Interactive plotting
- Parameterized equations
- Example equations provided

## Requirements
- Python 3.x
- NumPy, SciPy, SymPy, Matplotlib

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/KarmicPiper/ordinary-differential-equation-solver.git

##Install dependencies:
- pip install numpy scipy sympy matplotlib

##Run the application:
- python ode_gui.py

##Usage
- Enter an equation in the format dy/dt = ....
- Set parameters, initial conditions, and time span.
- Click "Solve" to compute and plot the solution.

##Examples
- Exponential decay: dy/dt = -a*y
- Harmonic oscillator: dy/dt = -k*sin(y)
- Logistic growth: dy/dt = c*y*(1 - y)

##License
- This project is licensed under the MIT License. See LICENSE for details.
