# Parameters of DFN
#battery/dfn/parameters


# Dendrite modeling 
#battery/modeling/dendrite
#references/battery/dendrite/xu2022promoting mentions that there are three methods which address the computational modelling at different scales:

1. #references/battery/dendrite/monte_carlo/aryanfar2014dynamics have employed Monte Carlo (MC) calculations to elucidate the mechanism of inhibited Li dendrite growth with a pulsed deposition mode. 
2.  #references/battery/dendrite/sph/tan2020simulating have simulated cyclic Li dendrite growth at the electrode-electrolyte interface in lithium batteries over multiple cycles based on a reactive mass transport dendrite growth smoothed-particle hydrodynamics (SPH) model, which is able to qualitatively predict the morphologies of Li deposition and the effects of fast charging on the dendrite growth rate
3.  #references/battery/dendrite/dft/li2019energy used DFT and tight binding (DFTB), similarly hybrid ab initio and reactive molecular dynamics (HAIR) is used as well. 
4. Kinetic Monte Carlo (KMC) typically simulates processes with known transition rates among states, which have to be obtained from diffusion experiments or MD (molecular dynamics) and DFT
5. PF is complex and costs more time compared to KMC.
6. SPH has no connection with microscopic simulation methods and atomic models. 
Among the theoretical methods, DFT- and MD-based computations are commonly used for revealing the thermodynamics and physicochemical properties of the SEI layer, while KMC, SPH, and PF are suitable to simulate the Li deposition behaviors. Multiscale simulation is required to ensure complementariness and obtain a more comprehensive understanding of the chemical and structural evolution of both Li deposition and SEI formation. The reliability of the results shall be further validated with experiments. To further improve our understanding of Li deposition, it is necessary to bridge the existing atomic and macroscopic simulations and establish a unified set of theoretical simulation models.

![[Pasted image 20241023015352.png]]
A more comprehensive overview of each of these methods is as follows
#battery/modeling/dendrite/dst
- Quantum mechanical (QM) calculation based on the DFT method obtains potential energy function. It can be used to calculate the reaction potential energy surface and the physical and chemical properties of materials in the SEI.
#battery/modeling/dendrite/AIMD
- ab initio molecular dynamics (AIMD) generates finite-temperature dynamical trajectories and thus allows chemical bond breaking and forming events to occur and accounts for electronic polarization effects.
#battery/modeling/dendrite/HAIR
- HAIR enables simulations of the initial chemical reactions related to SEI formation, which may take up to 1 ns, far too long for AIMD. The AIMD part of HAIR can describe the localized electrochemical reactions accurately, while ReaxFF MD could accelerate chemical reactions and mass transfer with a much more affordable cost while keeping the QM accuracy when the force field parameter is well trained.
#battery/modeling/dendrite/MC
- MC methods, as a widespread class of computational algorithms that depend on repeated random sampling to obtain numerical value, are often applied to solve unsolvable physical and mathematical problems. The side reactions and ion diffusion in the charge and discharge process may be simulated by the constant voltage simulation method based on GCMC to observe the gradual formation process of SEI film with the increase of cycles.
#battery/modeling/dendrite/PF
- PF substitutes boundary conditions at the interface of Li dendrite growth by a partial differential equation for the evolution of an auxiliary field (the phase-field) that takes the role of an order parameter. This model equation is extremely complex. Now PF has been developed into open-source software such as MOOSE, FiPy, and PRISMS.
#battery/modeling/dendrite/SPH
- SPH is a computational method used for simulating the mechanics of continuum media and has been used in lithium dendrite growth, based on building mass continuity and mass transport governing equations and solutions. A Lagrangian particle-based SPH model also simulates the cycling lithium dendrite growth in multiscale including time and space.
## Dendrite modeling of Lithium with phase field
#battery/modeling/dendrite/phase_field

## Dendrite modeling of Lithium with SPH
#battery/modeling/dendrite/SPH