import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.integrate import solve_ivp
from sympy import sympify, symbols, lambdify

class ODEGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Differential Equation Solver v2.0")
        self.geometry("1200x800")
        
        # Improved layout
        self.main_frame = ttk.Frame(self, padding=15)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create components
        self.create_equation_input()
        self.create_parameter_input()
        self.create_plot_area()
        self.create_controls()
        
        # State variables
        self.current_params = {}

    def create_equation_input(self):
        frame = ttk.LabelFrame(self.main_frame, text="Equation Definition")
        frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(frame, text="Enter ODE (use y and t variables):").grid(row=0, column=0, sticky=tk.W)
        self.eq_entry = ttk.Entry(frame, width=60)
        self.eq_entry.grid(row=1, column=0, columnspan=2, sticky=tk.EW, padx=5)
        self.eq_entry.insert(0, "dy/dt = -a*y + sin(b*t)")
        
        ttk.Label(frame, text="Initial Condition y(t0):").grid(row=2, column=0, sticky=tk.W)
        self.ic_entry = ttk.Entry(frame, width=15)
        self.ic_entry.grid(row=3, column=0, sticky=tk.W, padx=5)
        self.ic_entry.insert(0, "1.0")
        
        ttk.Label(frame, text="Time Span [t0, tf]:").grid(row=2, column=1, sticky=tk.W)
        self.time_entry = ttk.Entry(frame, width=15)
        self.time_entry.grid(row=3, column=1, sticky=tk.W, padx=5)
        self.time_entry.insert(0, "0, 10")
        
        frame.columnconfigure(0, weight=1)

    def create_parameter_input(self):
        frame = ttk.LabelFrame(self.main_frame, text="Equation Parameters")
        frame.pack(fill=tk.X, pady=5)
        
        self.param_entries = {}
        default_params = {'a': 0.5, 'b': 1.0, 'c': 0.8, 'k': 1.0}
        for i, (name, val) in enumerate(default_params.items()):
            row = ttk.Frame(frame)
            row.grid(row=i//3, column=i%3, sticky=tk.W, padx=5, pady=2)
            ttk.Label(row, text=f"{name} =").pack(side=tk.LEFT)
            entry = ttk.Entry(row, width=8)
            entry.insert(0, str(val))
            entry.pack(side=tk.LEFT)
            self.param_entries[name] = entry

    def create_plot_area(self):
        frame = ttk.Frame(self.main_frame)
        frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.fig, self.ax = plt.subplots(figsize=(10, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.ax.set_title("Solution Plot")
        self.ax.grid(True)

    def create_controls(self):
        frame = ttk.Frame(self.main_frame)
        frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(frame, text="Solve", command=self.solve).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame, text="Clear", command=self.clear_plot).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame, text="Examples", command=self.show_examples).pack(side=tk.RIGHT, padx=5)
        ttk.Button(frame, text="Help", command=self.show_help).pack(side=tk.RIGHT, padx=5)

    def clear_plot(self):
        """Clear the plot area"""
        self.ax.clear()
        self.ax.set_title("Solution Plot")
        self.ax.grid(True)
        self.canvas.draw()

    def parse_equation(self):
        """Improved equation parser with error handling"""
        try:
            # Validate equation format
            eq_text = self.eq_entry.get()
            if '=' not in eq_text:
                raise ValueError("Equation must contain '=' sign")
                
            # Extract right-hand side
            rhs = eq_text.split('=')[1].strip()
            
            # Create symbols and parameters
            t_sym, y_sym = symbols('t y')
            params = {name: symbols(name) for name in self.param_entries.keys()}
            
            # Parse and substitute parameters
            expr = sympify(rhs, locals=params)
            param_values = {
                name: float(entry.get()) 
                for name, entry in self.param_entries.items() 
                if entry.get()
            }
            expr_sub = expr.subs(param_values)
            
            # Create numeric function
            return lambdify((t_sym, y_sym), expr_sub, 'numpy')
            
        except Exception as e:
            self.show_error(f"Equation parsing error: {str(e)}")
            return None

    def solve(self):
        """Improved solver with better error handling"""
        try:
            # Get time span and initial condition
            t_span = list(map(float, self.time_entry.get().split(',')))
            if len(t_span) != 2:
                raise ValueError("Time span must contain exactly two numbers")
                
            y0 = float(self.ic_entry.get())
            
            # Parse equation
            rhs_func = self.parse_equation()
            if rhs_func is None:
                return
                
            # Create ODE function with correct signature
            def ode_func(t, y):
                try:
                    return rhs_func(t, y[0])
                except Exception as e:
                    self.show_error(f"Evaluation error: {str(e)}")
                    raise

            # Solve ODE
            sol = solve_ivp(ode_func, t_span, [y0], 
                           t_eval=np.linspace(*t_span, 1000),
                           vectorized=True)

            # Update plot
            self.ax.clear()
            self.ax.plot(sol.t, sol.y[0], label='Numerical Solution')
            self.ax.set_xlabel('Time (t)')
            self.ax.set_ylabel('y(t)')
            self.ax.legend()
            self.canvas.draw()

        except ValueError as ve:
            self.show_error(f"Input error: {str(ve)}")
        except Exception as e:
            self.show_error(f"Solution error: {str(e)}")

    def show_examples(self):
        """Fixed example equations"""
        examples = [
            ("Exponential Decay", "dy/dt = -a*y", {'a': '0.5'}, "1.0", "0, 5"),
            ("Harmonic Oscillator", "dy/dt = -k*y", {'k': '1.0'}, "0.0", "0, 10"),
            ("Forced Oscillator", "dy/dt = -k*y + sin(b*t)", {'k': '1.0', 'b': '3.0'}, "0.0", "0, 20"),
            ("Logistic Growth", "dy/dt = c*y*(1 - y)", {'c': '0.8'}, "0.1", "0, 10")
        ]
        
        ex_win = tk.Toplevel(self)
        ex_win.title("Example Equations")
        
        for idx, (name, eq, params, ic, tspan) in enumerate(examples):
            frame = ttk.Frame(ex_win, padding=5)
            frame.grid(row=idx, column=0, sticky=tk.W)
            ttk.Button(frame, text=name, width=20,
                      command=lambda e=eq, p=params, i=ic, t=tspan: 
                      self.load_example(e, p, i, t)).pack(side=tk.LEFT)
            ttk.Label(frame, text=eq).pack(side=tk.LEFT, padx=10)

    def show_help(self):
        help_text = """Valid equation format:
- Use 'dy/dt' on left side
- Use standard math operations: +, -, *, /, **
- Supported functions: sin(), cos(), exp(), sqrt()
Example: dy/dt = -a*y + sin(b*t)"""
        
        help_win = tk.Toplevel(self)
        help_win.title("Help Documentation")
        ttk.Label(help_win, text=help_text, justify=tk.LEFT).pack(padx=20, pady=10)

    # Other methods remain similar with improved error messages

if __name__ == "__main__":
    app = ODEGUI()
    app.mainloop()