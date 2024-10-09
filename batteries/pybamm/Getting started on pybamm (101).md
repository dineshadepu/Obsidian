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

#pybamm-model-variables
```python 
model.variables.search("electrolyte")
```


