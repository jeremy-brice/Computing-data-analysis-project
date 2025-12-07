# -*- coding: utf-8 -*-
"""
Created on Sun Nov  2 16:39:40 2025

@author: brice
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# === PARAMÈTRES PHYSIQUES ET NUMÉRIQUES ===
g  = 9.81        # gravité (m/s²)
H  = 4000.0      # profondeur moyenne (m)
nu = 1e-6        # viscosité (m²/s)
L  = 1000.0      # longueur du domaine (m)
nx = 50         # nombre de points spatiaux
dx = L / (nx - 1)
dt = 0.01         # pas de temps (s)
nt = 1500         # nombre d’itérations temporelles

# === MAILLAGE ===
x = np.linspace(0, L, nx)

# === ÉTAT INITIAL GAUSSIEN ===
A = 0.5          # amplitude max de la vague
x0 = L / 2       # centre de la vague
sigma = L / 10   # largeur de la gaussienne
eta = A * np.exp(-((x - x0)**2) / (2*sigma**2))

# --- Vitesse initiale linéaire approximative ---
u = np.sqrt(g * H) * eta / H

# === FIGURE ===
fig, ax = plt.subplots(figsize=(10, 4))
line, = ax.plot(x, eta, lw=2)
ax.set_ylim(-A*1.2, A*1.2)        # échelle centrée sur zéro
ax.set_xlabel("x (m)")
ax.set_ylabel("Surface libre η (m)")
title = ax.text(0.5, 1.05, '', transform=ax.transAxes, ha='center', fontsize=10)

# === FONCTION DE MISE À JOUR ===
def update(frame):
    global eta, u
    eta_n = eta.copy()
    u_n = u.copy()

    # --- Mise à jour de u ---
    du_dx   = (np.roll(u_n, -1) - np.roll(u_n, 1)) / (2*dx)
    deta_dx = (np.roll(eta_n, -1) - np.roll(eta_n, 1)) / (2*dx)
    d2u_dx2 = (np.roll(u_n, -1) - 2*u_n + np.roll(u_n, 1)) / dx**2
    u[:] = u_n - dt * (u_n*du_dx + g*deta_dx - nu*d2u_dx2)

    # --- Mise à jour de eta ---
    flux_plus  = (H + np.roll(eta_n, -1)) * np.roll(u_n, -1)
    flux_minus = (H + np.roll(eta_n, 1)) * np.roll(u_n, 1)
    eta[:] = eta_n - (dt / (2*dx)) * (flux_plus - flux_minus)

    # --- Mise à jour graphique ---
    line.set_ydata(eta)
    title.set_text(f"t = {frame*dt:.1f} s")
    return line, title

# === ANIMATION ===
anim = FuncAnimation(fig, update, frames=nt, interval=10, blit=True)

# === ENREGISTREMENT EN MP4 ===
output_file = "vagues_eta_gaussienne.mp4"
anim.save(output_file, fps=30, dpi=150)
print(f"✅ Animation enregistrée : {output_file}")

# === AFFICHAGE ===
plt.show()
