

# Example 1
#moose/tutorial/example1 #problem/poisson_equation


# Description



In this example we solve the advection-diffusion equation, given as:
$$
-\nabla\cdot\nabla u+\vec{v}\cdot\nabla u=0
$$

with same boundary conditions as previous problem. Here velocity $\vec{v}$ is a known constant with 
values $(0, 0, 1)$.  


# FEM procedure 


The weak form of the above equation is given as:
$$
(\nabla\phi_{i},\nabla u_{h})+({\vec{v}}\cdot\nabla u,\phi_{i})=0\quad\forall\phi_{i}
$$

This example is different from the previous one, by the advection term. To add the advection term, we have to add kernels to the moose files. This is done as following:




# MOOSE

## Add new kernel

```cpp
#pragma once

#include "Kernel.h"

/**
 * Define the Kernel for a convection operator that looks like:
 *
 * (V . grad(u), test)
 *
 * where V is a given constant velocity field.
 */
class ExampleConvection : public Kernel
{
public:
  /**
   * This is the constructor declaration.  This class takes a
   * string and a InputParameters object, just like other
   * Kernel-derived classes.
   */
  ExampleConvection(const InputParameters & parameters);

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
  virtual Real computeQpResidual() override;

  /**
   * Responsible for computing the diagonal block of the preconditioning matrix.
   * This is essentially the partial derivative of the residual with respect to
   * the variable this kernel operates on ("u").
   *
   * Note that this can be an approximation or linearization.  In this case it's
   * not because the Jacobian of this operator is easy to calculate.
   *
   * This function should always be defined in the .C file.
   */
  virtual Real computeQpJacobian() override;

private:
  /**
   * A vector object for storing the velocity.  Convenient for
   * computing dot products.
   */
  RealVectorValue _velocity;
};
```

```cpp
#include "ExampleConvection.h"

/**
 * All MOOSE based object classes you create must be registered using this macro.  The first
 * argument is the name of the App you entered in when running the stork.sh script with an "App"
 * suffix. If you ran "stork.sh Example", then the argument here becomes "ExampleApp". The second
 * argument is the name of the C++ class you created.
 */
registerMooseObject("ExampleApp", ExampleConvection);

/**
 * This function defines the valid parameters for
 * this Kernel and their default values
 */
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


To solve this with `moose`, we need six things to keep in mind.

1. Mesh
2. Variables
3. Kernels
4. BCs
5. Executioner
6. Outputs

With the current example, by using the internal kernels (equations) and solver, we can solve this problem with the following input file.

```
[Kernels]
  [diff]
    type = Diffusion
    variable = convected
  []

  [conv]
    type = ExampleConvection
    variable = convected
    velocity = '0.0 0.0 1.0'
  []
[]
```

The other fields stay the same.


