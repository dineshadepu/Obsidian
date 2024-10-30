#pybamm/create_model #pybamm/change_options #pybamm/model_options

In PyBaMM for every model it needs some specific parameters,  which can be found by executing:
```python
# Load DFN model
model = pybamm.lithium_ion.DFN(options={"SEI": "none"})
model.print_parameter_info()
```

We can create paramets



```python
import numpy as np
import pybamm
import matplotlib.pyplot as plt

# Load DFN model
model = pybamm.lithium_ion.DFN(options={"SEI": "none"})
model.print_parameter_info()

parameter_values = pybamm.ParameterValues("Chen2020")
parameter_values['Separator thickness [m]'] *= 10

# Define the experiment or set parameters for the simulation
# For example, a simple constant current discharge
experiment = pybamm.Experiment(
    ["Discharge at 1C until 3.0V", "Rest for 1 hour"]
)

# Initialize the simulation with the experiment
sim = pybamm.Simulation(model, parameter_values=parameter_values, experiment=experiment)

# Run the simulation
sim.solve()

# Plot the results
sim.plot()
```

#pybamm/validation/single_phase #pybamm/comparision/lionsimba
For the validation of the single phase DFN battery case, we have the following benchmark case
from LIONSIMBA paper #references/battery/torchio2016lionsimba :
#dfn/single_phase/benchmark/1/parameters
#dfn/single_phase/benchmark/1/table
![[Pasted image 20241022124536.png]]

The same paper is used  Ali2024 comparision paper as well #references/battery/ali2024comparison.


#pybamm/questions #battery/questions
What does single material mean? Is it LFP or NMC in cathode?


## PyBaMM validation with LIONSIMBA
#pybamm/validation/single_phase

We consider the problem #references/battery/dfn/torchio2016lionsimba and also in #references/battery/dfn/ali2024comparison. The parameters are given in the above figure. First we need to see what are the parameters required for DFN in general and in PyBaMM.

In order to see the parameters used by PyBaMM, we need to execute the following command

```python
import pybamm

# Load DFN model
model = pybamm.lithium_ion.DFN(options={"SEI": "none"})
model.print_parameter_info()
```

Which generates the following table, formatted and pasted for proper view:

#pybamm/dfn/parameters


| Parameter                                              | Type of parameter                                                                                                                                                                                             |
|--------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Lower voltage cut-off [V]                              | Parameter                                                                                                                                                                                                     |
| Reference temperature [K]                              | Parameter                                                                                                                                                                                                     |
| Positive electrode Bruggeman coefficient (electrolyte) | Parameter                                                                                                                                                                                                     |
| Nominal cell capacity [A.h]                            | Parameter                                                                                                                                                                                                     |
| Negative electrode Bruggeman coefficient (electrode)   | Parameter                                                                                                                                                                                                     |
| Negative electrode thickness [m]                       | Parameter                                                                                                                                                                                                     |
| Initial concentration in electrolyte [mol.m-3]         | Parameter                                                                                                                                                                                                     |
| Maximum concentration in negative electrode [mol.m-3]  | Parameter                                                                                                                                                                                                     |
| Initial temperature [K]                                | Parameter                                                                                                                                                                                                     |
| Negative electrode Bruggeman coefficient (electrolyte  | Parameter                                                                                                                                                                                                     |
| Faraday constant [C.mol-1]                             | Parameter                                                                                                                                                                                                     |
| Maximum concentration in positive electrode [mol.m-3]  | Parameter                                                                                                                                                                                                     |
| Ideal gas constant [J.K-1.mol-1]                       | Parameter                                                                                                                                                                                                     |
| Positive electrode thickness [m]                       | Parameter                                                                                                                                                                                                     |
| Electrode height [m]                                   | Parameter                                                                                                                                                                                                     |
| Number of electrodes connected in parallel to make a   | Parameter                                                                                                                                                                                                     |
| Electrode width [m]                                    | Parameter                                                                                                                                                                                                     |
| Positive electrode Bruggeman coefficient (electrode)   | Parameter                                                                                                                                                                                                     |
| Upper voltage cut-off [V]                              | Parameter                                                                                                                                                                                                     |
| Separator Bruggeman coefficient (electrolyte)          | Parameter                                                                                                                                                                                                     |
| Separator thickness [m]                                | Parameter                                                                                                                                                                                                     |
| Number of cells connected in series to make a battery  | Parameter                                                                                                                                                                                                     |
| Positive electrode OCP entropic change [V.K-1]         | FunctionParameter with inputs(s) 'Positive particle stoichiometry'                                                                                                                                            |
| Initial concentration in negative electrode [mol.m-3]  | FunctionParameter with inputs(s) 'Radial distance (r) [m]', 'Through-cell distance (x) [m]'│                                                                                                                  |
| Negative particle radius [m]                           | FunctionParameter with inputs(s) 'Through-cell distance (x) [m]'                                                                                                                                              |
| Cation transference number                             | FunctionParameter with inputs(s) 'Electrolyte concentration [mol.m-3]', 'Temperature [K]'                                                                                                                     |
| Negative electrode active material volume fraction     | FunctionParameter with inputs(s) 'Through-cell distance (x) [m]'                                                                                                                                              |
| Positive electrode active material volume fraction     | FunctionParameter with inputs(s) 'Through-cell distance (x) [m]'                                                                                                                                              |
| Positive particle diffusivity [m2.s-1]                 | FunctionParameter with inputs(s) 'Positive particle stoichiometry', 'Temperature [K]'                                                                                                                         |
| Negative particle diffusivity [m2.s-1]                 | FunctionParameter with inputs(s) 'Negative particle stoichiometry', 'Temperature [K]'                                                                                                                         |
| Negative electrode conductivity [S.m-1]                | FunctionParameter with inputs(s) 'Temperature [K]'                                                                                                                                                            |
| Positive particle radius [m]                           | FunctionParameter with inputs(s) 'Through-cell distance (x) [m]'                                                                                                                                              |
| Thermodynamic factor                                   | FunctionParameter with inputs(s) 'Electrolyte concentration [mol.m-3]', 'Temperature [K]'                                                                                                                     |
| Ambient temperature [K]                                | FunctionParameter with inputs(s) 'Distance across electrode width [m]', 'Distance across electrode height [m]', 'Time [s]' │                                                                                  |
| Negative electrode OCP entropic change [V.K-1]         | FunctionParameter with inputs(s) 'Negative particle stoichiometry'                                                                                                                                            |
| Positive electrode OCP [V]                             | FunctionParameter with inputs(s) 'Positive particle stoichiometry'                                                                                                                                            |
| Positive electrode porosity                            | FunctionParameter with inputs(s) 'Through-cell distance (x) [m]'                                                                                                                                              |
| Separator porosity                                     | FunctionParameter with inputs(s) 'Through-cell distance (x) [m]'                                                                                                                                              |
| Negative electrode exchange-current density [A.m-2]    | FunctionParameter with inputs(s) 'Electrolyte concentration [mol.m-3]', 'Negative particle surface concentration [mol.m-3]', 'Maximum negative particle surface concentration [mol.m-3]', 'Temperature [K]' │ |
| Negative electrode porosity                            | FunctionParameter with inputs(s) 'Through-cell distance (x) [m]'                                                                                                                                              |
| Positive electrode exchange-current density [A.m-2]    | FunctionParameter with inputs(s) 'Electrolyte concentration [mol.m-3]', 'Positive particle surface concentration [mol.m-3]', 'Maximum positive particle surface concentration [mol.m-3]', 'Temperature [K]' │ |
| Current function [A]                                   | FunctionParameter with inputs(s) 'Time [s]'                                                                                                                                                                   |
| Electrolyte conductivity [S.m-1]                       | FunctionParameter with inputs(s) 'Electrolyte concentration [mol.m-3]', 'Temperature [K]'                                                                                                                     |
| Positive electrode conductivity [S.m-1]                | FunctionParameter with inputs(s) 'Temperature [K]'                                                                                                                                                            |
| Negative electrode OCP [V]                             | FunctionParameter with inputs(s) 'Negative particle stoichiometry'                                                                                                                                            |
| Electrolyte diffusivity [m2.s-1]                       | FunctionParameter with inputs(s) 'Electrolyte concentration [mol.m-3]', 'Temperature [K]'                                                                                                                     |
| Initial concentration in positive electrode [mol.m-3]  | FunctionParameter with inputs(s) 'Radial distance (r) [m]', 'Through-cell distance (x) [m]'│                                                                                                                  |


#pybamm/dfn/parameters/capacity
Some parameters need some deeper understanding. Such as to compute the capacity we need to know the electrode height and width, which is mentioned in this 