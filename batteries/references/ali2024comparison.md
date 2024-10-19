#battery/papers/ali2024comparision #battery/papers/dfn_data
#battery/dfn_data

#battery/papers/title
Title: A comparison between physics-based Li-ion battery models

In this paper, the author has outlined several parameters used while modelling the battery
discharge with DFN and other models. The table is as follows:
#battery/dfn/parameters
#battery/dfn/ali2024comparision/parameters

| **Group**          | **Name**                                 | **Parameter**               | **SPM** | **ESPM** | **DFN** | **Latex notation** |
|--------------------|------------------------------------------|-----------------------------|---------|----------|---------|--------------------|
| **Geometric**      | Thickness                                | δ                           | ✔       | ✔        | ✔       | $\delta$           |
|                    | Electrode surface area                   | A<sub>surf</sub>            | ✔       | ✔        | ✔       | $A_{surf}$         |
|                    | Active material volume fraction          | ε<sub>s</sub>               | ✔       | ✔        | ✔       | $\epsilon_s$       |
|                    | Electrolyte volume fraction              | ε<sub>e</sub>               | ✘       | ✔        | ✔       | $\epsilon_e$       |
|                    | Radius of particle                       | R<sub>s</sub>               | ✔       | ✔        | ✔       | R_s                |
| **Transport**      | Diffusion coefficient                    | D<sub>s</sub>               | ✔       | ✔        | ✔       | D_s                |
|                    | Diffusion coefficient                    | D<sub>e</sub>               | ✘       | ✔        | ✔       | D_e                |
|                    | Solid phase electronic conductivity      | σ<sub>s</sub>               | ✘       | ✘        | ✔       | $\sigma_s$         |
|                    | Ionic conductivity                       | κ<sub>e</sub>               | ✘       | ✘        | ✔       | $\kappa_e$         |
|                    | Bruggemen exponent                       | b                           | ✘       | ✔        | ✔       | b                  |
| **Kinetic**        | Transference number                      | t<sup>0</sup><sub>+</sub>   | ✘       | ✔        | ✔       | $t_+^0$            |
|                    | Reaction rate coefficient                | k<sub>0</sub>               | ✔       | ✔        | ✔       | $k_0$              |
|                    | Contact resistance                       | R<sub>cc</sub>              | ✔       | ✔        | ✔       | $R_{cc}$           |
|                    | Charge transfer coefficient              | α                           | ✘       | ✔        | ✔       | $\alpha$           |
| **Concentration**  | Maximum concentration in the solid phase | c<sup>max</sup><sub>s</sub> | ✔       | ✔        | ✔       | $c^{max}_s$        |
|                    | Initial electrolyte concentration        | c<sub>e,0</sub>             | ✔       | ✔        | ✔       | $c_{e,0}$          |
| **Thermodynamics** | Equilibrium potential of the electrode   | U                           | ✔       | ✔        | ✔       | U                  |


Range of values from literature of LIBs
#batteries/parameters/range_values
#battery/papers/ali2024comparision/parameters_all_batteries

![[Pasted image 20241019184311.png]]

This table gives the general range of so many batteries available in the literature.
