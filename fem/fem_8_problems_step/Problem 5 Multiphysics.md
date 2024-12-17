
# Example 5: Multiphysics coupling
#moose/tutorial/example4 #problem/laplace_young


# Description



In this example we solve the advection-diffusion equation, given as:
$$
\begin{aligned}
-\nabla\cdot \nabla u + -\nabla v \cdot \nabla u & = 0 \\
-\nabla\cdot \nabla v & = 0
\end{aligned}
$$

with boundary conditions:
$$
\begin{aligned}
\nabla u  \cdot \hat{n} & = 0 \\
\nabla v  \cdot \hat{n} & = 0 \\
\end{aligned}
$$

. Here velocity $\vec{v}$ is a known constant with 
values $(0, 0, 1)$.  


# FEM procedure 

The weak form is:

$$
\begin{aligned}
\left(\nabla u_{h}, \nabla\phi_{i}\right) + \left(\nabla v \cdot \nabla u, \phi_i \right) = 0\quad\forall\phi_{i}\\
\left(\nabla v, \nabla\phi_{i}\right) = 0\quad\forall\phi_{i}
\end{aligned}
$$

# MOOSE

## Add new kernel

#moose/how_to_write_a_kernel/header/multiphysics_ex_03
```cpp
#pragma once
#include "Kernel.h"

class ExampleConvection : public Kernel
{
// Elided
private:
	const VariableGradient & _grad_some_variable;
}
```


#moose/how_to_write_a_kernel/src/multiphysics_ex_03
```cpp
InputParameters
ExampleConvection::validParams()
{
  InputParameters params = Kernel::validParams();

  params.addRequiredCoupledVar(
      "some_variable", "The gradient of this variable will be used as the velocity vector.");

  return params;
}

ExampleConvection::ExampleConvection(const InputParameters & parameters)
  : // You must call the constructor of the base class first
    Kernel(parameters),
    _grad_some_variable(coupledGradient("some_variable"))
{
}

Real
ExampleConvection::computeQpResidual()
{
  // velocity * _grad_u[_qp] is actually doing a dot product
  return _test[_i][_qp] * (_grad_some_variable[_qp] * _grad_u[_qp]);
}

Real
ExampleConvection::computeQpJacobian()
{
  // the partial derivative of _grad_u is just _grad_phi[_j]
  return _test[_i][_qp] * (_velocity * _grad_phi[_j][_qp]);
}
```



## The input file
```
[Variables]
  [./convected]
    order = FIRST
    family = LAGRANGE
  [../]

  [./diffused]
    order = FIRST
    family = LAGRANGE
  [../]
[]

[Kernels]
  [./diff_convected]
    type = Diffusion
    variable = convected
  [../]

  [./conv]
    type = ExampleConvection
    variable = convected

    # Couple a variable into the convection kernel using local_name = simulationg_name syntax
    some_variable = diffused
  [../]

  [./diff_diffused]
    type = Diffusion
    variable = diffused
  [../]
[]


```