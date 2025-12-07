# -*- coding: utf-8 -*-
"""
Created on Sat Nov  1 20:53:03 2025

@author: brice
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# === PARAMÈTRES PHYSIQUES ET NUMÉRIQUES ===
g  = 9.81       # gravité (m/s²)
H  = 4000.0     # profondeur moyenne (m)
nu = 1e-6       # viscosité (m²/s)
L  = 10000.0    # longueur du domaine (m)
nx = 500        # nombre de points spatiaux
dx = L / (nx - 1)
dt = 0.1      # pas de temps (s)
nt = 150       # nombre d’itérations temporelles

# === MAILLAGE ===
x = np.linspace(0, L, nx)

# === CONDITIONS INITIALES ===
A = 1.0
lambda_wave = 1000
eta = A * np.sin(2 * np.pi * x / lambda_wave)
u   = np.sqrt(g * H) * eta / H

# === FIGURE ===
fig, ax = plt.subplots(figsize=(10, 4))
line, = ax.plot(x, eta, lw=2)  # <- ici, on trace eta seule
ax.set_ylim(-2*A, 2*A)         # <- échelle adaptée à eta
ax.set_xlabel("x (m)")
ax.set_ylabel("Surface libre η (m)")  # <- étiquette modifiée
title = ax.text(0.5, 1.05, '', transform=ax.transAxes, ha='center', fontsize=10)

# === MISE À JOUR ===
def update(frame):
    global eta, u
    eta_n = eta.copy()
    u_n = u.copy()
    
    # --- Mise à jour de u ---
    for i in range(nx):
        ip = (i + 1) % nx
        im = (i - 1) % nx
        du_dx   = (u_n[ip] - u_n[im]) / (2*dx)
        deta_dx = (eta_n[ip] - eta_n[im]) / (2*dx)
        d2u_dx2 = (u_n[ip] - 2*u_n[i] + u_n[im]) / dx**2
        u[i] = u_n[i] - dt * (u_n[i]*du_dx + g*deta_dx - nu*d2u_dx2)
    
    # --- Mise à jour de eta ---
    for i in range(nx):
        ip = (i + 1) % nx
        im = (i - 1) % nx
        flux_plus  = (H + eta_n[ip]) * u_n[ip]
        flux_minus = (H + eta_n[im]) * u_n[im]
        eta[i] = eta_n[i] - (dt / (2*dx)) * (flux_plus - flux_minus)
    
    # --- Mise à jour du graphique ---
    line.set_ydata(eta)
    title.set_text(f"t = {frame * dt:.1f} s")
    return line, title

# === ANIMATION ===
anim = FuncAnimation(fig, update, frames=nt, interval=0.01, blit=True)

# === ENREGISTREMENT EN MP4 ===
output_file = "vagues_eta.mp4"  # <- nom modifié
anim.save(output_file, fps=30, dpi=150)
print(f"✅ Animation enregistrée avec succès : {output_file}")

# === AFFICHAGE ===
plt.show()

