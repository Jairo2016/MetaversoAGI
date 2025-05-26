
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# --- PARÁMETROS DEL SISTEMA ---
gamma = 1.0
lambda_ = 0.5
x = np.linspace(0, 10, 100)
dx = x[1] - x[0]

# --- ECUACIONES DIFERENCIALES ACOPLADAS ---
def coupled_system(t, y):
    DeltaS = y[:len(x)]
    dDeltaS_dt = y[len(x):2*len(x)]
    Omega = y[-2]
    dOmega_dt = y[-1]

    DeltaS_xx = np.zeros_like(DeltaS)
    DeltaS_xx[1:-1] = (DeltaS[2:] - 2 * DeltaS[1:-1] + DeltaS[:-2]) / dx**2

    d2DeltaS_dt2 = DeltaS_xx - lambda_ * (DeltaS - Omega)
    d2Omega_dt2 = gamma * np.mean(DeltaS - Omega)

    return np.concatenate([dDeltaS_dt, d2DeltaS_dt2, [dOmega_dt, d2Omega_dt2]])

# --- CONDICIONES INICIALES ---
DeltaS_0 = np.exp(-0.5 * (x - 5)**2)
dDeltaS_dt0 = np.zeros_like(x)
Omega_0 = 0.0
dOmega_dt0 = 0.0
y0 = np.concatenate([DeltaS_0, dDeltaS_dt0, [Omega_0, dOmega_dt0]])

# --- RESOLVER EL SISTEMA ---
t_eval = np.linspace(0, 10, 300)
sol = solve_ivp(coupled_system, [0, 10], y0, t_eval=t_eval, method='RK45')

# --- EXTRAER SOLUCIONES ---
DeltaS_t = sol.y[:len(x), :]
dDeltaS_dt_t = np.gradient(DeltaS_t, axis=1) / (t_eval[1] - t_eval[0])
Omega_t = sol.y[-2, :]

# --- CALCULAR COMPONENTES DE T^{μν}_{(ΔS)} ---
T00 = np.zeros_like(DeltaS_t)
T11 = np.zeros_like(DeltaS_t)

for i in range(1, len(x)-1):
    DeltaS_x = (DeltaS_t[i+1, :] - DeltaS_t[i-1, :]) / (2 * dx)
    dS_dt = dDeltaS_dt_t[i, :]
    grad_sq = -dS_dt**2 + DeltaS_x**2
    V = 0.5 * lambda_ * (DeltaS_t[i, :] - Omega_t)**2
    T00[i, :] = dS_dt**2 + 0.5 * (grad_sq + V)
    T11[i, :] = DeltaS_x**2 - 0.5 * (grad_sq + V)

T00_mean = T00.mean(axis=0)
T11_mean = T11.mean(axis=0)

# --- VISUALIZACIÓN ---
plt.figure(figsize=(10, 4))
plt.plot(t_eval, T00_mean, label='T⁰⁰ (Energía)', color='blue')
plt.plot(t_eval, T11_mean, label='T¹¹ (Presión Espacial)', color='green')
plt.title('Componentes del Tensor Energía-Momento T^{(ΔS)}')
plt.xlabel('Tiempo t')
plt.ylabel('Densidad / Presión')
plt.legend(); plt.grid(True)
plt.tight_layout()
plt.show()
