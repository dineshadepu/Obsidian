
## Concentration equations:
$$
\frac{\partial c_{s}(r,t)}{\partial t}=\frac{D_{s}}{r^{2}}\,\frac{\partial}{\partial r}\left(r^{2}\frac{\partial c_{s}(r,t)}{\partial r}\right),\,\,r\in[0,R_{s}],
$$

$$
\left.\frac{\partial c_{s}(r,t)}{\partial r}\right|_{r=0}=0,\ \ \ \ \ \ \ \ \ \ \ \\

$$

$$
\left.\frac{\partial c_{s}(r,t)}{\partial r}\right|_{r=0}=0,\\
$$
$$
-D_{s}\left.\frac{\partial c_{s}(r,t)}{\partial r}\right|_{r=R_{s}}= j_{\mathrm{Li}}(x,t)
$$
$$
 \epsilon_{\mathrm{e}}\frac{\partial c_{\mathrm{e}}(x,t)}{\partial t}=\frac{\partial}{\partial x}\left(D_{\mathrm{e}}\varepsilon_{\mathrm{e}}^{\mathrm{b}}\frac{\partial c_{\mathrm{e}}(x,t)}{\partial x}\right)+a_{s}\big(1-t_{+}^{0}\big)\;j_{\mathrm{Li}}(x,t),\;x\in[0,L],
$$

$$
\frac{\partial c_{\mathrm{e}}(x,t)}{\partial x}\bigg|_{x=0}=\frac{\partial c_{\mathrm{e}}(x,t)}{\partial x}\bigg|_{x=L}=0,
$$

## Potential equations:

### Electrode potential equations

$$
{\frac{\partial}{\partial x}}\left(\sigma_{s}\varepsilon_{s}{\frac{\partial\phi_{s}(x,t)}{\partial x}}\right)=a_{s}F j_{\mathrm{Li}}(x,t),\;x\in[0,\delta_{\mathrm{n}}]\;\cup\;[L-\delta_{\mathrm{p}},L]
$$


With boundary conditions


$$
\sigma_{s}\varepsilon_{s}\frac{\partial\phi_{s}(x,t)}{\partial x}\biggr|_{x=0}=\sigma_{s}\varepsilon_{s}\frac{\partial\phi_{s}(x,t)}{\partial x}\biggr|_{x=L}=\frac{I_{\mathrm{app}}(t)}{A_{\mathrm{surf}}}
$$

$$
\left.\frac{\partial\phi_{s}(x,t)}{\partial x}\right|_{x=\delta_{n}}
=
\left.\frac{\partial\phi_{s}(x,t)}{\partial x}\right|_{x=L - \delta_{p}}
= 0
$$

### Electrolyte potential equations

$$
\frac{\partial}{\partial x}\left(\kappa_{\mathrm{e}}
\varepsilon_{\mathrm{e}}^{\mathrm{b}}
\frac{\partial\phi_{\mathrm{e}}(x,t)}{\partial x}+\kappa_{\mathrm{e}}\mathrm{e}_{\mathrm{e}}^{\mathrm{b}}\nu\frac{2R T(t)}{F}\frac{\partial\mathrm{ln}c_{\mathrm{e}}(x,t)}{\partial x}\right)=-a_{s}F j_{\mathrm{Li}}(x,t),
$$


Boundary conditions
$$
 \left.\frac{\partial\phi_{\mathrm{e}}(x,t)}{\partial x}\right|_{x=0}=\phi_{\mathrm{e}}(x,t)|_{x=L}=0
$$

## Butler-Volmer equation

Electrochemical reaction-rate
$$
j_{\mathrm{{Li}}}(x,t)={\frac{i_{0}(x,t)}{F}}\left(\exp\!\left(\alpha_{\mathrm{{a}}}{\frac{F}{R T(t)}}\eta(x,t)\right)-\exp\!\left(\alpha_{\mathrm{{c}}}{\frac{F}{R T(t)}}\eta(x,t)\right)\right)
$$


overpotential at the electrodes

$$
\eta(x,t)=\phi_{\mathrm{s}}(x,t)-\phi_{\mathrm{e}}(x,t)-U(x,t)
$$

Exchange current density

$$
i_{0}(x,t)=k_{0}{\bigl(}c_{\mathrm{e}}(x,t){\bigr)}^{\alpha_{0}}{\bigl(}c_{\mathrm{s}}^{\mathrm{max}}-c_{\mathrm{s}}^{\mathrm{sur}}{\bigl(}x,t{\bigr)}{\bigr)}^{\alpha_{0}}{\bigl(}c_{\mathrm{s}}^{\mathrm{sur}}{\bigl(}x,t{\bigr)}{\bigr)}^{\alpha_{c}}
$$
Battery voltage

$$
V(t)=\phi_{s}(L,t)-\phi_{s}(0,t)-{\frac{R_{\mathrm{ex}}}{A_{\mathrm{surf}}}}I_{\mathrm{app}}(t)~.
$$
