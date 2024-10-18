# Example 1
#moose/tutorial/example1 #problem/poisson_equation

We are solving Poisson equation

$$
-\nabla\cdot\nabla u=0\in\Omega

$$

with boundary conditions, $u = 1$ on the bottom, $u = 0$ on the top and with $\nabla u \cdot \hat{n} = 0$  on the remaining boundaries.

#problem/poisson_equation/weak_form  #fem/weak_form #diffusion/weak_form
The weak form of this equation, in the inner-product notation

$$
\left(\nabla\phi_{i},\nabla u_{h}\right)=0\quad\forall\phi_{i}
$$
where $\phi_{i}$ are the test functions and $u_h$ is the finite element solution.

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
  # We use a pre-generated mesh file (in exodus format).
  # This mesh file has 'top' and 'bottom' named boundaries defined inside it.
  file = mug.e
[]

[Variables]
  [./diffused]
    order = FIRST
    family = LAGRANGE
  [../]
[]

[Kernels]
  [./diff]
    type = Diffusion
    variable = diffused
  [../]
[]

[BCs]
  [./bottom] # arbitrary user-chosen name
    type = DirichletBC
    variable = diffused
    boundary = 'bottom' # This must match a named boundary in the mesh file
    value = 1
  [../]

  [./top] # arbitrary user-chosen name
    type = DirichletBC
    variable = diffused
    boundary = 'top' # This must match a named boundary in the mesh file
    value = 0
  [../]
[]

[Executioner]
  type = Steady
  solve_type = 'PJFNK'
[]

[Outputs]
  execute_on = 'timestep_end'
  exodus = true
[]
```

# Example 2: Adding a custom kernel
#moose/tutorial/example2 #problem/advection_diffusion #moose/add_kernel

In this example we solve the advection-diffusion equation, given as:
$$
-\nabla\cdot\nabla u+\vec{v}\cdot\nabla u=0
$$

with same boundary conditions as previous problem. Here velocity $\vec{v}$ is a known constant with 
values $(0, 0, 1)$.  The weak form of the above equation is given as:
$$
(\nabla\phi_{i},\nabla u_{h})+({\vec{v}}\cdot\nabla u,\phi_{i})=0\quad\forall\phi_{i}
$$

This example is different from the previous one, by the advection term. To add the advection term, we have to add kernels to the moose files. This is done as following:

#moose/kernel/convection #moose/kernel/advection
```cpp
#pragma once

#include "Kernel.h"

class ExampleConvection : public Kernel
{
public:
  ExampleConvection(const InputParameters & parameters);
  static InputParameters validParams();

protected:
  virtual Real computeQpResidual() override;
  virtual Real computeQpJacobian() override;

private:
  RealVectorValue _velocity;
};
```


```cpp
#include "ExampleConvection.h"

registerMooseObject("ExampleApp", ExampleConvection);


InputParameters
ExampleConvection::validParams()
{
  InputParameters params = Kernel::validParams();
  params.addRequiredParam<RealVectorValue>("velocity", "Velocity Vector");
  return params;
}

ExampleConvection::ExampleConvection(const InputParameters & parameters)
  : // You must call the constructor of the base class first
    Kernel(parameters),
    _velocity(getParam<RealVectorValue>("velocity"))
{
}

Real
ExampleConvection::computeQpResidual()
{
  // velocity * _grad_u[_qp] is actually doing a dot product
  return _test[_i][_qp] * (_velocity * _grad_u[_qp]);
}

Real
ExampleConvection::computeQpJacobian()
{
  // the partial derivative of _grad_u is just _grad_phi[_j]
  return _test[_i][_qp] * (_velocity * _grad_phi[_j][_qp]);
}
```


This is reflected in the input file as follows:
```
[Kernels]
  [./diff]
    type = Diffusion
    variable = convected
  [../]
  [./conv]
    type = ExampleConvection
    variable = convected
    velocity = '0.0 0.0 1.0'
  [../]
[]
```

# Example 3: Multiphysics coupling
#moose/tutorial/example3 #problem/advection_diffusion_variable #moose/add_kernel/convection #problem/multiphysics #moode/two_variables

Problem statement: To-be done 

In the current problem, we have two variables, where one variable has diffusion (v) and the other variable has both convection and diffusion (u). While the convection of variable (u) is driven by variable (v). To handle this problem, we need to add a new kernel, where the convection of (u) is 
while considering the other variable.

Before discussing the kernel code, lets see how the input file would look like. Define the two variables first.
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
```

Then create the kernels
```text
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

The convection part of the (u) variable is added with the use of the following kernel

```cpp
#pragma once

#include "Kernel.h"

class ExampleConvection : public Kernel
{
public:
  ExampleConvection(const InputParameters & parameters);

  static InputParameters validParams();

protected:
  virtual Real computeQpResidual() override;

  virtual Real computeQpJacobian() override;

private:
  const VariableGradient & _grad_some_variable;
};
```

And the corresponding c file would be
```cpp
#include "ExampleConvection.h"

// Don't forget to register your object with MOOSE
registerMooseObject("ExampleApp", ExampleConvection);

InputParameters
ExampleConvection::validParams()
{
  InputParameters params = Kernel::validParams();

  // Here we specify a new parameter for our kernel allowing users to indicate which other
  // variable they want to be coupled into this kernel from an input file.
  params.addRequiredCoupledVar(
      "some_variable", "The gradient of this variable will be used as the velocity vector.");

  return params;
}

ExampleConvection::ExampleConvection(const InputParameters & parameters)
  : Kernel(parameters),
    // using the user-specified name for the coupled variable, retrieve and store a reference to the
    // coupled variable.
    _grad_some_variable(coupledGradient("some_variable"))
{
}

Real
ExampleConvection::computeQpResidual()
{
  // Implement the weak form equations using the coupled variable instead of the constant
  // parameter 'velocity' used in example 2.
  return _test[_i][_qp] * (_grad_some_variable[_qp] * _grad_u[_qp]);
}

Real
ExampleConvection::computeQpJacobian()
{
  // Implement the Jacobian using the coupled variable instead of the 'velocity'
  // constant parameter used in example 2.
  return _test[_i][_qp] * (_grad_some_variable[_qp] * _grad_phi[_j][_qp]);
}
```

