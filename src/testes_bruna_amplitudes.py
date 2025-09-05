#!/usr/bin/env python
# coding: utf-8

# In[5]:


"""
Script for calculating D-meson decay amplitudes and CP asymmetry.
"""

# Importing the necessary libraries
import math
import cmath
import numpy as np
from typing import Dict, Tuple


# In[6]:


# =============================================================================
# 1. PHYSICAL CONSTANTS AND PARAMETERS
# =============================================================================

def get_physical_constants() -> Dict:
    """Returns a dictionary of physical constants and model parameters."""
    # The constants for Wilson coefficients, quark masses and meson masses are
    # all extracted from the article's sources, mainly PDG book

    # Article's values for Wilson coefficients at 2 GeV
    constants = {
        "c1": 1.18, "c2": -0.32, "c3": 0.011, "c4": -0.031,
        "c5": 0.0068, "c6": -0.032,
    }
    # Quark masses (in MeV) at 2 GeV
    constants.update({
        "m_u": 2.14, "m_d": 4.7, "m_s": 93.46, "m_c": 1097,
        "avg_light_quark_mass": 3.427, # (m_u + m_d) / 2

    # Meson masses (in MeV)
        "m_D0": 1864.84, "m_D0_star": 2343, "m_D0s_star": 2317.8,
        "m_pi": 139.57, "m_k": 496,
    })
    # CKM Wolfenstein parameters (PDG)
    constants.update({
        "lambda_d": complex(-0.22, 1.3e-4),
        "lambda_s": complex(0.22, 6.9e-6),
        "lambda_b": complex(6.1e-5, -1.4e-4),
    })
    # Other constants
    constants.update({
        "G_fermi": 1.1663788e-11,       # Fermi's Constant (MeV^-2)
        "f_k": 155.7,                   # Kaon decay constant (MeV)
        "f_d": 212.0,                   # D-meson decay constant (MeV)
        "L5": 1.2e-3,                   # Chiral low-energy constant
        "doubleL8_plus_L5": -0.15e-3,   # Chiral low-energy constant combination
        "F_D_to_pi_00": 0.612,          # Form factor for pions at q^2=0
        "F_D_to_K_00": 0.7385,          # Form factor for kaons at q^2=0
    })
    # Strong phases and scattering matrix moduli for I1 and I2
    # These values were used by the authors in the article;
    # Therefore, they were used as sample for these calculations
    # Extracted from Page 9, Table I, third row, first column
    constants.update({
        "mod_omega_1": 0.79,
        "mod_omega_2": 0.9,
        "delta_I2_zero": 0.0,
        "delta_I2_pi": math.pi,
        "delta_I1": 2.0,
    })
    return constants


# In[7]:


# =============================================================================
# 2. HELPER FUNCTIONS FOR CALCULATIONS
# =============================================================================

def calculate_bare_amplitudes(p: Dict, conjugate: bool = False) -> Dict:
    """
    Calculates the bare amplitudes (tree diagram only) for both
    D0 -> pi-pi and D0 -> K-K decays processes.
    If conjugate is True, calculates amplitudes for the anti-particle decay.
    """
    # Select appropriate CKM elements
    lambda_d = np.conj(p["lambda_d"]) if conjugate else p["lambda_d"]
    lambda_s = np.conj(p["lambda_s"]) if conjugate else p["lambda_s"]
    lambda_b = np.conj(p["lambda_b"]) if conjugate else p["lambda_b"]

    # --- Pre-computation ---
    f_pi = p["f_k"] / 1.1934

    # Corrected form factors
    corr_fdpi00 = p["F_D_to_pi_00"] / (1 - (p["m_pi"]**2 / p["m_D0_star"]**2))
    corr_fdk00 = p["F_D_to_K_00"] / (1 - (p["m_k"]**2 / p["m_D0s_star"]**2))

    # Chiral corrections for penguin diagrams
    FpiS = (1 + 16 * p["doubleL8_plus_L5"] * p["m_pi"]**2 / f_pi**2 + 8 * p["L5"] * p["m_pi"]**2 / f_pi**2)

    FkS = (1 + 16 * p["doubleL8_plus_L5"] * p["m_k"]**2 / p["f_k"]**2 + 8 * p["L5"] * p["m_k"]**2 / p["f_k"]**2)


    # Penguin contribution terms (delta_6)
    term_pi = (p["f_d"] * p["m_D0"]**2) / (f_pi * (p["m_D0"]**2 - p["m_pi"]**2)) * \
              (p["m_c"] - p["avg_light_quark_mass"]) / (p["m_c"] + p["avg_light_quark_mass"]) * FpiS / corr_fdpi00
    delta6_pi = (2 / (p["m_c"] - p["avg_light_quark_mass"])) * (p["m_pi"]**2 / (2 * p["avg_light_quark_mass"])) * (1 + term_pi)

    term_k = (p["f_d"] * p["m_D0"]**2) / (p["f_k"] * (p["m_D0"]**2 - p["m_k"]**2)) * \
             (p["m_c"] - p["m_s"]) / (p["m_c"] + p["avg_light_quark_mass"]) * FkS / corr_fdk00
    delta6_k = (2 / (p["m_c"] - p["m_s"])) * (p["m_k"]**2 / (p["m_s"] + p["avg_light_quark_mass"])) * (1 + term_k)

    # --- D0 -> pi pi bare amplitudes ---
    term_pipi_I0 = (lambda_d * (2 * p["c1"] - p["c2"]) - 3 * lambda_b * (p["c4"] - p["c6"] * delta6_pi))
    term_pipi_I2 = lambda_d * (p["c1"] + p["c2"])

    const_pi0 = -(p["G_fermi"] / math.sqrt(2)) * math.sqrt(2/3)
    const_pi2 = -(p["G_fermi"] / math.sqrt(6))
    common_factor_pi = f_pi * (p["m_D0"]**2 - p["m_pi"]**2) * corr_fdpi00

    t0_pipi_bare = const_pi0 * common_factor_pi * term_pipi_I0
    t2_pipi_bare = const_pi2 * 2 * common_factor_pi * term_pipi_I2

    # --- D0 -> K K_bar bare amplitudes ---
    term_kk_I0 = (lambda_s * p["c1"] - lambda_b * (p["c4"] - p["c6"] * delta6_k))

    const_k0 = (p["G_fermi"] / math.sqrt(2))
    common_factor_k = p["f_k"] * (p["m_D0"]**2 - p["m_k"]**2) * corr_fdk00

    t1_kk_bare = const_k0 * common_factor_k * term_kk_I0
    t0_kk_bare = -t1_kk_bare

    return {
        "t0_pipi_bare": t0_pipi_bare, "t2_pipi_bare": t2_pipi_bare,
        "t0_kk_bare": t0_kk_bare, "t1_kk_bare": t1_kk_bare,
    }

def calculate_cp_asymmetry(amp_D: float, amp_D_bar: float) -> float:
    """Calculates the CP asymmetry (Acp)."""
    return (amp_D - amp_D_bar) / (amp_D + amp_D_bar)


# In[8]:


# =============================================================================
# 3. MAIN WORKFLOW - TOTAL AMPLITUDES AND CP ASYMMETRIES FOR EACH CHANNEL
# =============================================================================

def main():
    """Main function to run the calculation and print results."""
    p = get_physical_constants()

    # --- Calculate Bare Amplitudes ---
    bare_amps_D = calculate_bare_amplitudes(p, conjugate=False)
    bare_amps_D_bar = calculate_bare_amplitudes(p, conjugate=True)

    # --- Calculate Total Amplitudes for pi-pi final state ---
    # These complex exponentials are part of the model
    # They represent rescattering effects for different Isospin values
    # Isospin I = 0 amplitudes
    t0_pipi = 0.58 * cmath.exp(1.8j) * bare_amps_D["t0_pipi_bare"] + \
              0.64 * cmath.exp(-1.74j) * bare_amps_D["t0_kk_bare"]
    bar_t0_pipi = 0.58 * cmath.exp(1.8j) * bare_amps_D_bar["t0_pipi_bare"] + \
                  0.64 * cmath.exp(-1.74j) * bare_amps_D_bar["t0_kk_bare"]

    # Isospin I = 2 amplitudes for two different strong phases
    t2_pipi_phi_zero = p["mod_omega_2"] * cmath.exp(p["delta_I2_zero"]*1j) * \
                       bare_amps_D["t2_pipi_bare"]
    t2_pipi_phi_pi = p["mod_omega_2"] * cmath.exp(p["delta_I2_pi"]*1j) * \
                     bare_amps_D["t2_pipi_bare"]

    bar_t2_pipi_phi_zero = p["mod_omega_2"] * cmath.exp(p["delta_I2_zero"]*1j) * \
                           bare_amps_D_bar["t2_pipi_bare"]
    bar_t2_pipi_phi_pi = p["mod_omega_2"] * cmath.exp(p["delta_I2_pi"]*1j) * \
                         bare_amps_D_bar["t2_pipi_bare"]

    # --- Calculate Total Amplitudes for K-K final state ---
    t0_kk = 0.58 * cmath.exp(-1.37j) * bare_amps_D["t0_pipi_bare"] + \
            0.61 * cmath.exp(2.26j) * bare_amps_D["t0_kk_bare"]
    t1_kk = p["mod_omega_1"] * cmath.exp(p["delta_I1"]*1j) * bare_amps_D["t1_kk_bare"]

    bar_t0_kk = 0.58 * cmath.exp(-1.37j) * bare_amps_D_bar["t0_pipi_bare"] + \
                0.61 * cmath.exp(2.26j) * bare_amps_D_bar["t0_kk_bare"]
    bar_t1_kk = p["mod_omega_1"] * cmath.exp(p["delta_I1"]*1j) * bare_amps_D_bar["t1_kk_bare"]

    # --- Calculate CP Asymmetry for K-K ---
    k_interference = np.conj(t1_kk) * t0_kk + np.conj(t0_kk) * t1_kk
    bar_k_interference = np.conj(bar_t1_kk) * bar_t0_kk + np.conj(bar_t0_kk) * bar_t1_kk

    amp_D_KK_sq = 0.25 * (abs(t0_kk)**2 + abs(t1_kk)**2 + k_interference)
    amp_Dbar_KK_sq = 0.25 * (abs(bar_t0_kk)**2 + abs(bar_t1_kk)**2 + bar_k_interference)

    acp_kk = calculate_cp_asymmetry(amp_D_KK_sq, amp_Dbar_KK_sq)

    # --- Calculate CP Asymmetry for pi-pi (phi=pi case) ---
    pipi_interference_pi = (np.conj(t2_pipi_phi_pi) * t0_pipi + np.conj(t0_pipi) * t2_pipi_phi_pi)
    bar_pipi_interference_pi = (np.conj(bar_t2_pipi_phi_pi) * bar_t0_pipi + np.conj(bar_t0_pipi) * bar_t2_pipi_phi_pi)

    amp_D_pipi_sq_pi = (abs(t0_pipi)**2 / 6 + abs(t2_pipi_phi_pi)**2 / 12 + pipi_interference_pi / (6 * math.sqrt(2)))
    amp_Dbar_pipi_sq_pi = (abs(bar_t0_pipi)**2 / 6 + abs(bar_t2_pipi_phi_pi)**2 / 12 + bar_pipi_interference_pi / (6 * math.sqrt(2)))

    acp_pipi_pi = calculate_cp_asymmetry(amp_D_pipi_sq_pi, amp_Dbar_pipi_sq_pi)

    # --- Calculate CP Asymmetry for pi-pi (phi=0 case) ---
    pipi_interference_zero = (np.conj(t2_pipi_phi_zero) * t0_pipi + np.conj(t0_pipi) * t2_pipi_phi_zero)
    bar_pipi_interference_zero = (np.conj(bar_t2_pipi_phi_zero) * bar_t0_pipi + np.conj(bar_t0_pipi) * bar_t2_pipi_phi_zero)

    amp_D_pipi_sq_zero = (abs(t0_pipi)**2 / 6 + abs(t2_pipi_phi_zero)**2 / 12 + pipi_interference_zero / (6 * math.sqrt(2)))
    amp_Dbar_pipi_sq_zero = (abs(bar_t0_pipi)**2 / 6 + abs(bar_t2_pipi_phi_zero)**2 / 12 + bar_pipi_interference_zero / (6 * math.sqrt(2)))

    acp_pipi_zero = calculate_cp_asymmetry(amp_D_pipi_sq_zero, amp_Dbar_pipi_sq_zero)

    # --- Print Final Results ---
    print("="*49)
    print(" "*21 + "RESULTS" + " "*21)
    print("="*49)
    print(f"CP Asymmetry Acp(K+K-):               {acp_kk.real:.6f}")
    print(f"CP Asymmetry Acp(pi+pi-) [phi=0]:     {acp_pipi_zero.real:.6f}")
    print(f"CP Asymmetry Acp(pi+pi-) [phi=pi]:    {acp_pipi_pi.real:.6f}")
    print("-"*49)
    print(f"Difference ΔAcp [phi=0]:             {(acp_kk - acp_pipi_zero).real:.6f}")
    print(f"Difference ΔAcp [phi=pi]:            {(acp_kk - acp_pipi_pi).real:.6f}")
    print("="*49)


if __name__ == "__main__":
    main()

