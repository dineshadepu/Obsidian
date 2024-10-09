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







