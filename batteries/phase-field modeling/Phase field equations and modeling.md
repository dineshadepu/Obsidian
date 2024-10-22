The road-map to model the dendrite modelling with phase-field is as follows

1. Equations of Li-Ion phase field modelling
2. Variational form of these governing equations
3. Implementation in different software packages, such as, FEniCS, MOOSE etc.

# Equations of Li-Ion phase field modelling

Equations from few papers from the literature are listed here. 

## Equations from Rebecca2020FEniCS 
#references/battery/phase_field/Rebecca2020FEniCS 

#battery/phase_field/Rebecca2020FEniCS/equations 
#battery/phase_field/equations 
From paper, we have the following equations:

#battery/phase_field/Rebecca2020FEniCS/equations/phase_evolution 
From paper, we have the following equations:
The equation of the temporal evolution of the order parameter $\xi$ is:
$$
\begin{aligned}\frac{\partial\xi}{\partial t} =
-L_\sigma\left(\frac{\partial g(\xi)}{\partial\xi}-\kappa\nabla^2\xi\right)-
L_\eta\frac{\partial h(\xi)}{\partial\xi}\left(\exp\left[\frac{(1-
\alpha)nF\eta_a(\phi)}{RT}\right]-\frac{c_{Li^+}}{c_0}\exp\left[\frac{-\alpha nF\eta_a(\phi)}{RT}\right]\right)\end{aligned}
$$
where $L_{\sigma}$ and $L_{\eta}$ are the interfacial mobility and electrochemical reaction coefficient. $g(\xi)=W\xi^2 (1-\xi)^2$  is the double well function and $h(\xi)=\xi^3 (6\xi^2 - 15\xi + 10)$  is the interpolation function. $\kappa, \alpha, n, F, R, t  \text{ and } T$  are the gradient coefficient, charge transfer coefficient, number of electrons transferred, Faraday constant, gas constant, evolution time and temperature. W sets the height of the energy barrier between the phases. The switching barrier and gradient coefficient are further related to the surface tension $\gamma$  and interfacial thickness $\delta$, i.e., $W=\frac{3\gamma}{\delta}$ and $\kappa=6\gamma\delta$. $\eta_{\alpha} = \phi - E^{\theta}$ is the activation overpotential, $E^\theta$ is the standard equilibrium half cell potential and $\phi$ is the applied overpotential. $c_{{Li}^+}$ and $c_0$ are the local and initial lithium-ion molar ratio.


The total concentration is an interpolation between the two equilibrium concentrations: $c=c^{l}\left(1-h\left(\xi\right)\right)+c^{s}h\left(\xi\right)\frac{C_{m}^{s}}{C_{m}^{l}}.c^{l}$ and $c^s$ are the molar fraction of lithium in the electrolyte and electrode phases and $C_m^{l}$ y $C_m^{s}$ are the site density of the electrode and electrolyte phases (inverse of molar volume). In a two phase model, the local lithium ion molar-fraction is defined as:

#battery/phase_field/Rebecca2020FEniCS/equations/molar_fraction
$$c_{Li^+}\left(\xi,\mu\right)=\frac{\exp\left[\frac{\mu-\epsilon^l}{RT}\right]}{1+\exp\left[\frac{\mu-\epsilon^l}{RT}\right]}\left(1-h\left(\xi\right)\right)$$


where $\mu$ is the chemical potential of lithium. $\epsilon^l=\mu^{0l}-\mu^{0N}$ is the difference in the chemical potential of lithium and neutral components on the electrolyte phase at initial equilibrium state.
The diffusion of the species can be rearranged to express the time evolution of the chemical potential $\mu:$

#battery/phase_field/Rebecca2020FEniCS/equations/chemical_potential_evolution
$$\dfrac{\partial\mu}{\partial t}=\dfrac{1}{\chi}\left[\nabla\cdot\dfrac{D\left(\xi\right)c_{Li^{+}}\left(\xi,\mu\right)}{RT}\left(\nabla\mu+nF\nabla\phi\right)-\dfrac{\partial h(\xi)}{\partial t}\left(c^{s}\dfrac{C_{m}^{s}}{C_{m}^{l}}-c^{l}\right)\right]$$

where the susceptibility factor $\chi = \frac {\partial c}{\partial \mu }= \frac {\partial c^{l}}{\partial \mu }\left [ 1- h( \xi ) \right ] + \frac {\partial c^{s}}{\partial \mu }h( \xi ) \frac {C_{m}^{s}}{C_{m}^{l}}. D\left ( \xi \right ) =$ $D^{l}(1-h\left(\xi\right))$ is the diffusivity concentration and $D^l$ the diffusivity coefficient of lithium ion in the electrolyte.
The spatial distribution of the electrical overpotential $\phi$ can be obtained
by solving the conduction equation:
#battery/phase_field/Rebecca2020FEniCS/equations/electric_overpotential_spatial_distribution
$$\nabla\cdot\sigma\left(\xi\right)\nabla\phi=nFC_{m}^{s}\frac{\partial\xi}{\partial t}$$

where $\sigma(\xi)=\sigma^{s}h(\xi)+\sigma^{l}[1-h(\xi)]$ is the effective conductivity and $\sigma^{s}$ and
$\sigma^{l}$ the conductivity of the electrode and electrolyte phases.

## Equations from arguello2022dendrite 
#battery/phase_field/Rebecca2020FEniCS/equations
#references/battery/phase_field/arguello2022dendrite  
 Title: Dendrite formation in rechargeable lithium-metal batteries: Phase-field modeling using open-source finite element library