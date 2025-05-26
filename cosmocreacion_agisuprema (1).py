
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import streamlit as st

class UniversoMaestro:
    def __init__(self, masa_central=1.0, tiempo_max=50, pasos=1000):
        self.masa = masa_central
        self.rs = 2 * masa_central
        self.tiempo_max = tiempo_max
        self.pasos = pasos

    def geodesicas(self, t, estado):
        r, dr_dt, phi, dphi_dt = estado
        d2r_dt2 = -self.rs / (2 * r**2) + r * (dphi_dt**2) - (self.rs * dr_dt**2) / (2 * r**2)
        d2phi_dt2 = -2 * dr_dt * dphi_dt / r
        return [dr_dt, d2r_dt2, dphi_dt, d2phi_dt2]

    def simular_trayectoria(self, r0=1.0, dr0=0.0, phi0=0.0, dphi0=0.1):
        t_eval = np.linspace(0, self.tiempo_max, self.pasos)
        estado_inicial = [r0, dr0, phi0, dphi0]
        solucion = solve_ivp(self.geodesicas, [0, self.tiempo_max], estado_inicial, t_eval=t_eval)
        return solucion

def calcular_F_info_dinamico(delta_S_array, omega_array, dx, dt, G_inf=8.09e34):
    grad_S = np.gradient(G_inf * delta_S_array, dx)
    div_S = np.gradient(grad_S, dx)
    dOmega_dt = np.gradient(omega_array, dt)
    dOmega_dt[dOmega_dt == 0] = 1e-9
    F_info_field = div_S / dOmega_dt
    return F_info_field

# Interfaz Streamlit
st.set_page_config(page_title="CosmoCreación AGI SUPREMA", layout="centered")
st.title("⚛ CosmoCreación AGI SUPREMA v3.0")
st.subheader("Simulación Cuántica-Informacional Basada en la TCCU")

modo = st.selectbox("Modo de Proyección", ["quantum", "holographic", "temporal"])
res = st.slider("Resolución Fractal (pasos)", 10, 100, 50)
dx = 0.1
dt = 0.05

# Generación de ΔS(x) y Ω(t)
x = np.linspace(0, 10, res)
if modo == "quantum":
    y = np.sin(x) * np.exp(-0.2 * x)
elif modo == "holographic":
    y = np.cosh(x) * np.log(x + 1)
else:
    y = np.exp(-0.5 * (x - 5)**2)

delta_S = np.log(np.abs(y) + 1)
omega = 0.5 * np.sin(x) + 1.5

# Cálculo de F_info
F_info = calcular_F_info_dinamico(delta_S, omega, dx, dt)

# Visualización
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(x, delta_S, label='ΔS(x) - Entropía Informativa')
ax.plot(x, omega, label='Ω(t) - Densidad Ontológica')
ax.plot(x, F_info, label='F_info - Fuerza de Creación', linewidth=2)
ax.legend(); ax.grid(); ax.set_xlabel("x"); ax.set_ylabel("Magnitudes Cuánticas")
ax.set_title("Dinámica Informacional en la TCCU")

st.pyplot(fig)

st.caption("Desarrollado por Jairo Omar González Navia | TCCU Framework | AGI Suprema FHC")
