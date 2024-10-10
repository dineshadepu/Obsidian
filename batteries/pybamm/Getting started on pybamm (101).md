#getting-started-pybamm #pybamm-top-view #pybamm-user-level
# How to run a model 091024
#pybamm-example #pybamm-basic-simulation  #pybamm-getting-started-01

We can load a basic model in `pybamm` using the following:

```python
import pybamm
model = pybamm.lithium_ion.DFN()
sim = pybamm.Simulation(model)
sim.solve([0, 3600])
sim.plot()
```

This can be divided as a following steps:
1. Import the required packages
2. Create a model
3. Create a simulation
4. Solve it
5. Plot it

# Compare different models 091024
#pybamm-example #pybamm-different-models #pybamm-getting-started-02

This example deals with running multiple models in `pybamm`.
```python
models = [
    pybamm.lithium_ion.SPM(),
    pybamm.lithium_ion.SPMe(),
    pybamm.lithium_ion.DFN(),
]
sims = []
for model in models:
    sim = pybamm.Simulation(model)
    sim.solve([0, 3600])
    sims.append(sim)
pybamm.dynamic_plot(sims)
```

# Plotting in `pybamm`
#pybamm-example #pybamm-plotting #pybamm-getting-started-03

First solve some problem as following:
```python
import pybamm

model = pybamm.lithium_ion.DFN()
sim = pybamm.Simulation(model)
sim.solve([0, 3600])
```

For every model we have several variables involved, which can be listed with the following command

#pybamm-model-variables
```python 
model.variable_names()
```

We can search in these variable names with a string:

#pybamm-model-variables #pybamm-model-variables-local-search
```python 
model.variables.search("electrolyte")
```

We can plot list of variables, like following

```python
output_variables = ["Electrolyte concentration [mol.m-3]", "Voltage [V]"]
sim.plot(output_variables=output_variables)
```

or a single variable, but in both the cases, the interested variable has to be provided in a list

```python
output_variables = ["Voltage [V]"]
sim.plot(output_variables=output_variables)
```

We can plot multiple variables in the same plot by nesting lists. It is achieved by

```python
sim.plot(
    [
        ["Electrode current density [A.m-2]", "Electrolyte current density [A.m-2]"],
        "Voltage [V]",
    ]
)
```


# Tutorial 4 - Setting parameter values
#pybamm-example #pybamm-parameter-values #pybamm-getting-started-04

One can load parameter values from a file using the following command:

```python
parameter_values = pybamm.ParameterValues("Chen2020")
```

Similar to parameters, this is a huge list similar to model `variables`, and one can similarly search through this list. 
```python
parameter_values.search("electrolyte")
```

Now, to run a simulation by using a particular parameter list, one has to create the simulation object with given parameter list as follows:

```python
model = pybamm.lithium_ion.DFN()
sim = pybamm.Simulation(model, parameter_values=parameter_values)
sim.solve([0, 3600])
sim.plot()
```

## Constant parameters
#pybamm-constant-parameters

Some parameters are constant in our differential equation, these are initialised by the following code:

```python
parameter_values["Current function [A]"] = 10
```

## Function parameters
#pybamm-function-parameters 

While, some parameters can be function of other variables, such as time, in that case, we define our parameters like the following

```python
def my_current(t):
    return pybamm.sin(2 * np.pi * t / 60)

parameter_values["Current function [A]"] = my_current
```


## Define a new parameter set

With all this, lets create a new parameter set from scratch

```python
def cube(t):
    return t**3

parameter_values = pybamm.ParameterValues(
    {
        "Negative electrode thickness [m]": 1e-4,
        "Positive electrode thickness [m]": 1.2e-4,
        "Current function [A]": cube,
    }
)
```
These parameter set has both constant and variable parameters.

# Tutorial 5: Running experiments
#pybamm-example #pybamm-running-experiments #pybamm-getting-started-05

The experiments in `pybamm` are run based on set of instruction which can be given:
```python
"Discharge at 1C for 0.5 hours",
"Discharge at C/20 for 0.5 hours",
"Charge at 0.5 C for 45 minutes",
"Discharge at 1 A for 90 seconds",
"Charge at 200mA for 45 minutes",
"Discharge at 1 W for 0.5 hours",
"Charge at 200 mW for 45 minutes",
"Rest for 10 minutes",
"Hold at 1 V for 20 seconds",
"Charge at 1 C until 4.1V",
"Hold at 4.1 V until 50 mA",
"Hold at 3V until C/50",
```

These instructions are put together and an experiment object is created

#pybamm-create-experiment
```python
experiment = pybamm.Experiment(
    [
        "Discharge at C/10 for 10 hours or until 3.3 V",
        "Rest for 1 hour",
        "Charge at 1 A until 4.1 V",
        "Hold at 4.1 V until 50 mA",
        "Rest for 1 hour",
    ]
)
```

We can repeat a given experiment any number of times, by creating a list of lists as follows:

```python
experiment = pybamm.Experiment(
    [
        (
            "Discharge at C/10 for 10 hours or until 3.3 V",
            "Rest for 1 hour",
            "Charge at 1 A until 4.1 V",
            "Hold at 4.1 V until 50 mA",
            "Rest for 1 hour",
        )
    ]
    * 3
    + [
        "Discharge at 1C until 3.3 V",
    ]
)
```

Using this experiment object we can create our simulation as follows:
#pybamm-simulation-with-experiment

```python
model = pybamm.lithium_ion.DFN()
sim = pybamm.Simulation(model, experiment=experiment)
sim.solve()
sim.plot()
```

As part of plotting the results, we can select a given cycle out of all the cycles. 
#pybamm-plotting-cycle

```python
sim.solution.cycles[0].plot()
```

# Tutorial 6 - Managing simulation outputs
#pybamm-example #pybamm-simulation-output #pybamm-getting-started-06

We can get the output of a given experiment as follows
```python
solution = sim.solution
```

or the `solve` command of `simulation` returns `solution`
```python
solution = sim.solve([0, 3600])
```

We use the `solution` object to plot our results, one can get the requisite variables to plot using 
solution object as follows:
```python
t = solution["Time [s]"]
V = solution["Voltage [V]"]
```
However, the `V` voltage parameter is only given at the discretised time of `t`. We can get voltage
`V` values at different times from extrapolation as follows
#pybamm-output-different-time
```python
V([200, 400, 780, 1236])  # times in seconds
```

## Load simulation and save simulation
#pybamm-load-simulation #pybamm-save-simulation

The simulation of a given experiment can be saved by
```python
sim.save("SPMe.pkl")
```
Similarly, one can load by
```python
sol2 = pybamm.load("SPMe_sol.pkl")
sol2.plot()
```
Or one can selectively save specific variables or parameters only rather than the whole
simulation
#pybamm-save-some-parameters
```python
sol = sim.solution
sol.save_data("sol_data.pkl", ["Current [A]", "Voltage [V]"])
```

Before we finish, if we need to delete any simulation data saved on the disc we can use the 
following command:

```python
import os

os.remove("SPMe.pkl")
os.remove("SPMe_sol.pkl")
os.remove("sol_data.pkl")
os.remove("sol_data.csv")
os.remove("sol_data.mat")
```
## Model options - Tutorial 7
#pybamm-example #pybamm-model-options #pybamm-getting-started-07
We have so many models in `pybamm`, we can add these multiphysics model to the models like following. Here for `SPMe` , we add thermal model
```python
options = {"thermal": "lumped"}
```

you have several options for a given model, change it!

## Model options - Tutorial 8
#pybamm-example #pybamm-solver-options #pybamm-getting-started-08

The solver in `pybamm` is similar to any other solver other softwares provide. `Tolerance`, 
`time step`, and other options a typical `solver` takes care of. As an example, here we create 
two solvers, `fast` and `slow`

```python
model = pybamm.lithium_ion.DFN()
param = model.default_parameter_values
param["Lower voltage cut-off [V]"] = 3.6
safe_solver = pybamm.CasadiSolver(atol=1e-3, rtol=1e-3, mode="safe")
fast_solver = pybamm.CasadiSolver(atol=1e-3, rtol=1e-3, mode="fast")
# create simulations
safe_sim = pybamm.Simulation(model, parameter_values=param, solver=safe_solver)
fast_sim = pybamm.Simulation(model, parameter_values=param, solver=fast_solver)

# solve
safe_sim.solve([0, 3600])
print(f"Safe mode solve time: {safe_sim.solution.solve_time}")
fast_sim.solve([0, 3600])
print(f"Fast mode solve time: {fast_sim.solution.solve_time}")

# plot solutions
pybamm.dynamic_plot([safe_sim, fast_sim])
```





















