
# Numerical Interpolation and Approximation {231024, 16:33}

#function/interpolation #function/approximation

Given data of a function at different points, i.e.,
$$
(x_1, u_1), (x_2, u_2), (x_2, u_2), (x_2, u_2), (x_2, u_2) \cdots , (x_n, u_n)
$$
we need to find a function $u$. In this regard if the function should pass through all the points then 
it is termed as an **interpolation**, while if we are trying to find an **approximate** function, then the
function need not be passing through all or any of the data points. 

In FEM, polynomial interpolation is dominantly employed in the numerical representation of the unknown functions over the elements. 

![[fig_3_1_data_with_interpolation_and_approximation_functions 1.png]]
The above figure is generated using the following code: TODO: Write comments
```python
import numpy as np
import matplotlib.pyplot as plt
import random

x = np.linspace(-1., 3., 100)
u = np.sin(x) + x**2. + 3


x_approximation = np.linspace(-1., 3., 100)
u_approximation = np.sin(x) + x**2. + 3 + np.random.uniform(low=0.01, high=0.1, size=(len(x),))
# np.random.rand(len(x))

x_data = x[10::20]
u_data = u[10::20]

plt.plot(x, u, label="Interpolation")
plt.scatter(x_data, u_data, label="Data points")
plt.plot(x_approximation, u_approximation, label="Approximation")
# plt.vlines(x_data, -10, 10)
plt.axvline(x=0, c="black")
plt.axhline(y=0, c="black")
plt.xlabel("x")
plt.ylabel("u")
plt.legend()
# plt.axes()
# plt.show()
plt.savefig("fig_3_1_data_with_interpolation_and_approximation_functions.png", dpi=300)
```
Can also be found at  https://github.com/dineshadepu/fem

## Lagrange Interpolation {231024, 16:37}

So many choices to choose as an interpolation function, few of them are:
1. Polynomial
2. Trigonometric
3. Exponential
4. Rational

Most famous one is polynomial. A polynomial interpolation function for a given data points is given as:

$$
u(x) = a_1 \cdot 1 + a_2 x + a_2 x^2 + a_3 x^3 + \cdots
$$
At given data our function value has the following values:


$$
\begin{eqnarray}
u(x_{1}) = a_1 \cdot 1 + a_2 x_{1} + a_2 x_{1}^2 + a_3 x_{1}^3 + \cdots = u_{1}\\
u(x_{2}) = a_1 \cdot 1 + a_2 x_{2} + a_2 x_{2}^2 + a_3 x_{2}^3 + \cdots = u_{2}\\
u(x_{3}) = a_1 \cdot 1 + a_2 x_{3} + a_2 x_{3}^2 + a_3 x_{3}^3 + \cdots = u_{3}\\
\end{eqnarray}
$$

This is solved for the coefficients of the polynomial basis, by forming a linear algebra equations. 
