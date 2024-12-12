# Example 1
#moose/tutorial/example1 #problem/poisson_equation


# Description

We are solving Poisson equation

$$
-\nabla\cdot\nabla u=0\in\Omega

$$

with boundary conditions, $u = 1$ on the bottom, $u = 0$ on the top and with $\nabla u \cdot \hat{n} = 0$  on the remaining boundaries.


# FEM procedure 


#problem/poisson_equation/weak_form  #fem/weak_form #diffusion/weak_form
The weak form of this equation, in the inner-product notation

$$
\left(\nabla\phi_{i},\nabla u_{h}\right)=0\quad\forall\phi_{i}
$$
where $\phi_{i}$ are the test functions and $u_h$ is the finite element solution.



# MOOSE


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



# FEniCS
