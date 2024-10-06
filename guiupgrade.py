import tkinter as tk
from tkinter import *
from qiskit import QuantumCircuit
import numpy as np
from qiskit.visualization import visualize_transition
import qiskit.visualization.exceptions as qv_exception

app = tk.Tk()
app.geometry("435x490")
app.title('Quantum Visualizer')
app.resizable(0, 0)

button_font = ('Arial', 14, 'bold')
display_font = ("Arial", 20, 'bold')

background_color = '#2c3e50'
button_color = '#2980b9'
button_text_color = 'white'
display_color = '#34495e'
entry_color = '#2c3e50'

def clear():
    global circuit
    display.delete(0, END)
    initialize_circuit()

def initialize_circuit():
    global circuit 
    circuit = QuantumCircuit(1)

initialize_circuit()
theta = 0
gates_applied = []

def change_theta(num, window, circuit, key):
    global theta
    theta = num * np.pi
    if key == 'x':
        circuit.rx(theta, 0)
        theta = 0
    elif key == 'y':
        circuit.ry(theta, 0)
        theta = 0
    else:
        circuit.rz(theta, 0)
        theta = 0
    gates_applied.append(key)
    if len(gates_applied) >= 10:
        visualize_circuit(circuit, app)
        gates_applied.clear()
    window.destroy()

def display_gate(gate_input):
    display.insert(END, gate_input)

def user_input(circuit, key):
    get_input = tk.Tk()
    get_input.title('Get Theta')
    get_input.geometry('360x160')
    get_input.resizable(0, 0)

    values = [0.25, 0.5, 1.0, 2.0]
    for i, value in enumerate(values):
        button = tk.Button(get_input, text=f"PI/{value}", command=lambda val=value: change_theta(val, get_input, circuit, key))
        button.grid(row=0, column=i, padx=5, pady=5)

    entry = tk.Entry(get_input, width=10)
    entry.grid(row=1, columnspan=len(values), padx=5, pady=5)

    get_input.mainloop()

def about():
    info = tk.Tk()
    info.title('About')
    info.geometry("650x470")
    info.resizable(0, 0)

    text = tk.Text(info, height = 20, width = 20)

    label = tk.Label(info, text = "About Quantum Visualizer")
    label.config(font=('Arial',14))

    text_to_display = """
    About: Visualization tool for Single Qubit Rotation on Bloch Sphere
    
    Created by : Yash Chakraborty
    Created using: Python, Tkinter, Qiskit
    
    Info about the gate buttons and corresponding qiskit commands:
    
    X = flips the state of qubit -                                 circuit.x()
    Y = rotates the state vector about Y-axis -                    circuit.y()
    Z = flips the phase by PI radians -                            circuit.z()
    Rx = parameterized rotation about the X axis -                 circuit.rx()
    Ry = parameterized rotation about the Y axis.                  circuit.ry()
    Rz = parameterized rotation about the Z axis.                  circuit.rz()
    S = rotates the state vector about Z axis by PI/2 radians -    circuit.s()
    T = rotates the state vector about Z axis by PI/4 radians -    circuit.t()
    Sd = rotates the state vector about Z axis by -PI/2 radians -  circuit.sdg()
    Td = rotates the state vector about Z axis by -PI/4 radians -  circuit.tdg()
    H = creates the state of superposition -                       circuit.h()
    
    For Rx, Ry and Rz, 
    theta(rotation_angle) allowed range in the app is [-2*PI,2*PI]
    
    In case of a Visualization Error, the app closes automatically.
    This indicates that visualization of your circuit is not possible.
    
    At a time, only ten operations can be visualized.
    """

    label.pack()
    text.pack(fill='both',expand=True)

    text.insert(END,text_to_display)
    info.mainloop()

def visualize_circuit(circuit, window):
    try:
        visualize_transition(circuit=circuit)
    except qv_exception.VisualizationError:
        pass

display_frame = tk.LabelFrame(app, bg=background_color)
button_frame = tk.LabelFrame(app, bg=background_color)
display_frame.pack(pady=10)
button_frame.pack(fill='both', expand=True)

display = tk.Entry(display_frame, width=30, font=display_font, bg=display_color, fg='white', borderwidth=5, justify='left')
display.pack(pady=10)

gate_buttons = [
    ('X', lambda: [display_gate('x'), circuit.x(0)]),
    ('Y', lambda: [display_gate('y'), circuit.y(0)]),
    ('Z', lambda: [display_gate('z'), circuit.z(0)]),
    ('RX', lambda: [display_gate('Rx'), user_input(circuit, 'x')]),
    ('RY', lambda: [display_gate('Ry'), user_input(circuit, 'y')]),
    ('RZ', lambda: [display_gate('Rz'), user_input(circuit, 'z')]),
    ('S', lambda: [display_gate('s'), circuit.s(0)]),
    ('SD', lambda: [display_gate('SD'), circuit.sdg(0)]),
    ('H', lambda: [display_gate('H'), circuit.h(0)]),
    ('T', lambda: [display_gate('t'), circuit.t(0)]),
    ('TD', lambda: [display_gate('TD'), circuit.tdg(0)])
]

for i, (text, command) in enumerate(gate_buttons):
    button = tk.Button(button_frame, text=text, font=button_font, bg=button_color, fg=button_text_color, command=command)
    button.grid(row=i // 3, column=i % 3, padx=5, pady=5, sticky='we')

visualize_button = tk.Button(button_frame, text='Visualize', font=button_font, bg='#27ae60', fg='white', command=lambda: visualize_circuit(circuit, app))
visualize_button.grid(row=4, column=0, columnspan=3, pady=10, sticky='we')

clear_button = tk.Button(button_frame, text='Clear', font=button_font, bg='#c0392b', fg='white', command=clear)
clear_button.grid(row=5, column=0, columnspan=3, pady=10, sticky='we')

quit_button = tk.Button(button_frame, text='Quit', font=button_font, bg='#7f8c8d', fg='white', command=app.destroy)
quit_button.grid(row=6, column=0, columnspan=3, pady=10, sticky='we')

about_button = tk.Button(button_frame, text='About', font=button_font, bg='#8e44ad', fg='white', command=about)
about_button.grid(row=3, column=2, padx=5, pady=5, sticky='we')

for i in range(3):
    button_frame.grid_columnconfigure(i, weight=1)

app.mainloop()
