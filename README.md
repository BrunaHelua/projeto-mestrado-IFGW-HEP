
# CP Violation in D Meson Decays: A Comparative Study of FSI Models

This repository hosts the computational tools and analysis codes for the Master's thesis project titled: "CP Symmetry Violation in charmed decays: New Physics or Non-perturbative effects?".

## Description

The violation of Charge-Parity (CP) symmetry is a crucial phenomenon in particle physics, and its observation in the decay of charmed mesons provides a unique window to probe the Standard Model and search for new physics. This project focuses on the theoretical understanding of the CP asymmetry observed in the decays of neutral D mesons ($D^0$ and $\bar{D}^0$) into final states composed of pions $\pi^+\pi^- and kaons $K^+K^-.

A significant challenge in the theoretical description of these decays is the proper treatment of Final State Interactions (FSI), which are the non-perturbative strong interactions between the decay products. These interactions can generate strong phases that are essential for the emergence of direct CP violation.

This work performs a comparative study of two prominent theoretical articles that employ Final State Interactions to describe the amplitude of CP violation in the aforementioned D meson decays. The primary goal is to understand the phenomenological implications of each FSI model and to validate the calculations presented in these papers.

## About the Codes

The codes in this repository were developed to validate the analytical calculations and theoretical predictions of the paper "Final-state interactions in the CP asymmetries
of charm-meson two-body decays", by Antonio Pich, Eleftheria Solomonidi, and Luiz Vale Silva. They are intended to serve as a transparent and reproducible record of the computational aspects of this thesis.

### Core Functionalities

* **Calculation of Decay Amplitudes:** Scripts to compute the decay amplitudes for $D^0 \to \pi\pi$ and $D^0 \to KK$ within the proposed frameworks.
* **Implementation of FSI Models:** Independent implementations of the different Final State Interaction models used in the compared papers. This includes the calculation of relevant loop diagrams, rescattering amplitudes, and the extraction of strong phases.
* **CP Asymmetry Calculation:** Code to compute the direct CP asymmetry parameter, $A_{CP}$, based on the calculated decay amplitudes for the D meson and its antiparticle.

### Technologies Used

* **Language:** Python 3.8+
* **Key Libraries:**
    * `NumPy`: For numerical operations and handling of arrays.
    * `SciPy`: For scientific computing, including integration and optimization.
    * `math`: For mathematical symbols and operations.
    * `cmath`: For complex numbers and operations. 
    * `pandas`: For data manipulation and analysis (if applicable).
    * `typing`: For different types of data, especially `key`:`value` types.

   
## How to Use

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/BrunaHelua/projeto-mestrado-IFGW-HEP.git](https://github.com/BrunaHelua/projeto-mestrado-IFGW-HEP.git)
    cd projeto-mestrado-IFGW-HEP
    ```

2.  **Set up the environment:**
    It is recommended to use a virtual environment.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Running the code:**
    The main validation scripts can be found in the `src/` or `notebooks/` directory. For example, to reproduce a key calculation from one of the papers:
    ```bash
    python src/validate_paper_1.py
    ```
    Or, you can explore the Jupyter notebooks in the `notebooks/` directory for a more interactive analysis.

## Project Structure

.
├── data/               # Experimental data or model parameters
├── notebooks/          # Jupyter notebooks for analysis and visualization
├── src/                # Source code for calculations and validations
├── plots/              # Directory to save generated plots
├── .gitignore          # Files to be ignored by Git
├── LICENSE             # Your chosen open-source license
└── README.md           # This file


## References

Here you should include the full citations for the two papers you are comparing. For example:

1.  **[Pich, A., Solomonidi, E., and Silva, L. V.]**, *[Final-state interactions in the CP asymmetries
of charm-meson two-body decays]*, [PHYSICAL REVIEW D], **[108]**, [036026] ([2023]). [DOI: 10.1103/PhysRevD.108.036026]
2.  **[Bediaga I., Frederico T., Magalhães P. C.]**, *[Enhanced Charm CP Asymmetries from Final State Interactions]*, [PHYSICAL REVIEW LETTERS], **[131]**, [051802] ([2023]). [DOI: 10.1103/PhysRevLett.131.051802]
