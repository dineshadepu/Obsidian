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