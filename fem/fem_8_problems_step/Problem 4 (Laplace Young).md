

# Example 4
#moose/tutorial/example4 #problem/laplace_young


# Description



In this example we solve the advection-diffusion equation, given as:
$$
-\nabla\cdot \frac{\textbf{K}}{\mu}\nabla p = 0
$$

with same boundary conditions as previous problem. Here velocity $\vec{v}$ is a known constant with 
values $(0, 0, 1)$.  


# FEM procedure 

TODO: The weak form is to be written



# MOOSE

## Add new kernel


```cpp
// This file is part of the MOOSE framework
// https://www.mooseframework.org
//
// All rights reserved, see COPYRIGHT for full restrictions
// https://github.com/idaholab/moose/blob/master/COPYRIGHT
//
// Licensed under LGPL 2.1, please see LICENSE for details
// https://www.gnu.org/licenses/lgpl-2.1.html

#pragma once

#include "ADKernel.h"

/**
 * Define the Kernel for a convection operator that looks like:
 *
 * (V . grad(u), test)
 *
 * where V is a given constant velocity field.
 */
class DarcyPressure : public ADKernel
{
public:
  /**
   * This is the constructor declaration.  This class takes a
   * string and a InputParameters object, just like other
   * Kernel-derived classes.
   */
  DarcyPressure (const InputParameters & parameters);

  /**
   * validParams returns the parameters that this Kernel accepts / needs
   * The actual body of the function MUST be in the .C file.
   */
  static InputParameters validParams();

protected:
  /**
   * Responsible for computing the residual at one quadrature point.
   * This function should always be defined in the .C file.
   */
  virtual ADReal computeQpResidual() override;

  const Real & _permeability;
  const Real & _viscosity;
};

```


```cpp
// This file is part of the MOOSE framework
// https://www.mooseframework.org
//
// All rights reserved, see COPYRIGHT for full restrictions
// https://github.com/idaholab/moose/blob/master/COPYRIGHT
//
// Licensed under LGPL 2.1, please see LICENSE for details
// https://www.gnu.org/licenses/lgpl-2.1.html

#include "DarcyPressure.h"

/**
 * All MOOSE based object classes you create must be registered using this macro.  The first
 * argument is the name of the App you entered in when running the stork.sh script with an "App"
 * suffix. If you ran "stork.sh Example", then the argument here becomes "ExampleApp". The second
 * argument is the name of the C++ class you created.
 */
registerMooseObject("fem_darcy_pressure_mooseApp", DarcyPressure);

/**
 * This function defines the valid parameters for
 * this Kernel and their default values
 */
InputParameters
DarcyPressure::validParams()
{
  InputParameters params = ADKernel::validParams();

  params.addClassDescription("Compute the diffusion term for Darcy pressure ($p$) equation: "
                             "$-\\nabla \\cdot \\frac{\\mathbf{K}}{\\mu} \\nabla p = 0$");

  params.addRequiredParam<Real>("permeability", "The permeability ($\\mathrm{K}$) of the fluid.");
  params.addParam<Real>("viscosity",
                        7.98e-4,
                        "The viscosity ($\\mu$) of the fluid in Pa, the default is for water at 30 degrees C.");
  return params;
}

DarcyPressure::DarcyPressure(const InputParameters & parameters)
  : // You must call the constructor of the base class first
    ADKernel(parameters),

    _permeability(getParam<Real>("permeability")),
    _viscosity(getParam<Real>("viscosity"))
{
}

ADReal
DarcyPressure::computeQpResidual()
{
  // velocity * _grad_u[_qp] is actually doing a dot product
  return (_permeability / _viscosity) * _grad_test[_i][_qp] * _grad_u[_qp];
}
```

To solve this with `moose`, we need six things to keep in mind.

1. Mesh
2. Variables
3. Kernels
4. BCs
5. Executioner
6. Outputs

With the current example, by using the internal kernels (equations) and solver, we can solve this problem with the following input file.

```
[Mesh]
  [gmg]
    type = GeneratedMeshGenerator
    dim = 2
    nx = 100
    ny = 10
    xmax = 0.304 # Length of test chamber
    ymax = 0.0257 # Test chamber radius
  []
  coord_type = RZ
  rz_coord_axis = X
[]

[Variables/pressure]
[]

[Kernels]
  [darcy_pressure]
    type = DarcyPressure
    variable = pressure
    permeability = 0.8451e-9 # (m^2) 1mm spheres.
  []
[]

[BCs]
  [inlet]
    type = DirichletBC
    variable = pressure
    boundary = left
    value = 4000 # (Pa) From Figure 2 from paper.  First data point for 1mm spheres.
  []
  [outlet]
    type = DirichletBC
    variable = pressure
    boundary = right
    value = 0 # (Pa) Gives the correct pressure drop from Figure 2 for 1mm spheres
  []
[]

[Problem]
  type = FEProblem
[]

[Executioner]
  type = Steady
  solve_type = PJFNK
  petsc_options_iname = '-pc_type -pc_hypre_type'
  petsc_options_value = 'hypre boomeramg'
[]

[Outputs]
  exodus = true
[]

```

The other fields stay the same.


