# FPGA-Based Microstep Controller for a Robotic Arm with Variable-Stiffness Mini Gripper via Tiny Tapeout

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Verilog](https://img.shields.io/badge/Verilog-HDL-blue)](https://en.wikipedia.org/wiki/Verilog)
[![TinyTapeout](https://img.shields.io/badge/TinyTapeout-SKY130-orange)](https://tinytapeout.com/)
[![OpenLane](https://img.shields.io/badge/OpenLane-ASIC_Flow-green)](https://github.com/The-OpenROAD-Project/OpenLane)
[![Simulation](https://img.shields.io/badge/Simulation-Icarus_Verilog-blueviolet)](http://iverilog.icarus.com/)
[![PDK](https://img.shields.io/badge/PDK-SkyWater_SKY130-red)](https://github.com/google/skywater-pdk)

*Electiva II · Ingeniería Electrónica · Universidad Pedagógica y Tecnológica de Colombia*

</div>

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Key Contributions](#-key-contributions)
- [Features](#-features)
- [System Architecture](#-system-architecture)
- [Tools & Technologies](#️-tools--technologies)
- [Repository Structure](#-repository-structure)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [RTL Simulation](#rtl-simulation)
  - [FPGA Prototyping](#fpga-prototyping)
  - [ASIC Flow (OpenLane)](#asic-flow-openlane)
- [Design Flow](#-design-flow)
- [Verification & Results](#-verification--results)
- [ASIC Physical Design](#-asic-physical-design)
- [Technical Paper](#-technical-paper)
- [Contributing](#-contributing)
- [License](#-license)
- [Acknowledgments](#-acknowledgments)

---

## 🧭 Overview

This project presents the design and validation of a digital control system for a **variable-stiffness mini gripper**, developed as part of the Elective II course in Electronic Engineering at **UPTC (Universidad Pedagógica y Tecnológica de Colombia)**.

The system was described in **Verilog HDL**, verified through functional RTL simulations, and experimentally validated on an **FPGA**. The full ASIC design flow was also completed using **open-source EDA tools** (OpenLane, Yosys, OpenROAD, Magic, Netgen) targeting the **SkyWater SKY130 PDK**, preparing the design for future fabrication through the **Tiny Tapeout** shuttle program.

> **What is a variable-stiffness gripper?**  
> A variable-stiffness gripper is a robotic end-effector capable of dynamically adjusting its mechanical compliance. This enables safe human-robot interaction and adaptable manipulation across tasks requiring different force levels — from delicate object handling to firm grasping.

---

## 🏆 Key Contributions

| # | Contribution |
|---|---|
| 1 | Modular Verilog HDL design for variable-stiffness control |
| 2 | Functional verification via testbenches and RTL simulation |
| 3 | Experimental FPGA prototyping and hardware validation |
| 4 | Complete ASIC flow: synthesis → STA → floorplanning → placement → CTS → routing |
| 5 | Successful physical verification (DRC and LVS clean) |
| 6 | Tape-out ready design for SKY130 via Tiny Tapeout |

---

## 🎯 Features

- 🔢 **Configurable stiffness levels** — up to *N* discrete levels, software-defined
- 🔄 **Finite State Machine (FSM)** — robust operation mode management
- 🔌 **Digital configuration interface** — clean digital I/O for mode selection
- ⚡ **Control signal generation** — precise PWM/step outputs for gripper actuation
- 🧩 **Modular architecture** — reusable, extensible RTL blocks
- ✅ **Dual-target synthesis** — synthesizable for both FPGA and ASIC flows

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   TOP-LEVEL MODULE                       │
│                                                         │
│  ┌──────────────┐    ┌─────────────┐    ┌────────────┐  │
│  │  Config I/F  │───▶│     FSM     │───▶│  Output    │  │
│  │  (Digital)   │    │ (State Mgr) │    │  Driver    │  │
│  └──────────────┘    └──────┬──────┘    └─────┬──────┘  │
│                             │                 │          │
│                    ┌────────▼────────┐        │          │
│                    │  Stiffness Ctrl │        │          │
│                    │   (N Levels)    │        │          │
│                    └─────────────────┘        │          │
│                                               ▼          │
│                                      ┌───────────────┐  │
│                                      │  Mini Gripper  │  │
│                                      │   Interface    │  │
│                                      └───────────────┘  │
└─────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tools & Technologies

| Category | Tool / Technology | Version / Notes |
|----------|-------------------|-----------------|
| **HDL** | Verilog HDL | IEEE 1364-2005 |
| **Simulation** | Icarus Verilog | v11+ |
| **Waveform Viewer** | GTKWave | v3.3+ |
| **Logic Synthesis** | Yosys | Open-source |
| **ASIC Flow** | OpenLane | v2.x |
| **P&R / STA** | OpenROAD | Integrated in OpenLane |
| **DRC** | Magic VLSI | v8.3+ |
| **LVS** | Netgen | v1.5+ |
| **PDK** | SkyWater SKY130 | 130 nm CMOS |
| **Fabrication Shuttle** | Tiny Tapeout | [tinytapeout.com](https://tinytapeout.com) |
| **FPGA Prototype** | Generic FPGA Board | Xilinx / Intel compatible |

---

## 📁 Repository Structure

```
.
├── rtl/                        # RTL source files (Verilog HDL)
│   ├── top.v                   # Top-level module
│   ├── fsm.v                   # Finite State Machine
│   ├── stiffness_ctrl.v        # Stiffness control logic
│   └── output_driver.v         # Output signal generation
│
├── sim/                        # Simulation testbenches
│   ├── tb_top.v                # Top-level testbench
│   ├── tb_fsm.v                # FSM-level testbench
│   └── waveforms/              # GTKWave save files (.gtkw)
│
├── fpga/                       # FPGA implementation files
│   ├── constraints/            # Timing and pin constraints (.xdc / .qsf)
│   └── bitstreams/             # Generated bitfiles (git-ignored)
│
├── asic/                       # ASIC design flow
│   ├── config.json             # OpenLane configuration
│   ├── runs/                   # OpenLane run outputs (git-ignored)
│   └── reports/                # Timing, area, and DRC/LVS reports
│
├── docs/                       # Documentation and figures
│   ├── schematic/              # Block diagrams and schematics
│   ├── timing/                 # STA reports and waveform captures
│   └── layout/                 # GDS layout screenshots
│
├── scripts/                    # Utility scripts (simulation, flow)
├── .github/                    # CI/CD workflows
├── LICENSE
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

```bash
# Clone the repository
git clone https://github.com/<your-org>/<your-repo>.git
cd <your-repo>

# Install simulation tools (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install iverilog gtkwave

# Install OpenLane (Docker-based — recommended)
# Follow: https://openlane.readthedocs.io/en/latest/getting_started/installation/index.html
```

### RTL Simulation

```bash
# Run top-level testbench
cd sim/
iverilog -o tb_top tb_top.v ../rtl/top.v ../rtl/fsm.v \
         ../rtl/stiffness_ctrl.v ../rtl/output_driver.v
vvp tb_top

# View waveforms
gtkwave waveforms/tb_top.gtkw &
```

### FPGA Prototyping

1. Open your vendor IDE (Vivado / Quartus Prime).
2. Add all sources from `rtl/` and the appropriate constraints from `fpga/constraints/`.
3. Set `top.v` as the top-level module.
4. Run synthesis, implementation, and generate the bitstream.
5. Program the target device.

### ASIC Flow (OpenLane)

```bash
# From the OpenLane installation directory
./flow.tcl -design <path-to-repo>/asic -tag run_001

# Check reports
cat <run-dir>/reports/synthesis/synthesis_pre_sta.rpt
cat <run-dir>/reports/routing/drc.rpt
```

> ⚠️ **Note:** Full ASIC runs require the SkyWater SKY130 PDK. See [OpenLane documentation](https://openlane.readthedocs.io) for PDK setup.

---

## 🔬 Design Flow

```
RTL Design (Verilog)
        │
        ▼
 Functional Simulation ──────────────────────┐
 (Icarus Verilog + GTKWave)                  │
        │                                    │
        ▼                                ✅ Pass
 Logic Synthesis                             │
 (Yosys via OpenLane)                        │
        │                                    │
        ▼                                    │
 Static Timing Analysis (STA)                │
 (OpenROAD / OpenSTA)                        │
        │                                    │
        ▼                                    │
 Floorplanning & Power Planning               │
 (OpenROAD)                                  │
        │                                    │
        ▼                                    │
 Placement & Clock Tree Synthesis (CTS)       │
 (OpenROAD)                                  │
        │                                    │
        ▼                                    │
 Routing (OpenROAD)                           │
        │                                    │
        ▼                                    │
 Physical Verification                        │
 ├── DRC (Magic)        ✅                    │
 └── LVS (Netgen)       ✅                    │
        │                                    │
        ▼                                    │
 GDSII Export  ──────────────────────────────┘
        │
        ▼
 Tiny Tapeout Submission (SKY130)
```

---

## ✅ Verification & Results

### RTL Simulation

| Test | Status | Notes |
|------|--------|-------|
| FSM state transitions | ✅ PASS | All N states verified |
| Stiffness level switching | ✅ PASS | Zero glitch transitions |
| Output signal integrity | ✅ PASS | Correct duty cycles |
| Reset behavior | ✅ PASS | Synchronous reset confirmed |
| Edge cases | ✅ PASS | Boundary inputs tested |

### FPGA Validation

- ✅ Bitstream generated and loaded successfully
- ✅ Hardware behavior matches RTL simulation
- ✅ All stiffness modes verified on physical hardware

---

## 🏭 ASIC Physical Design

### Synthesis Summary (SKY130)

| Metric | Value |
|--------|-------|
| Technology | SkyWater SKY130 (130 nm) |
| Target Frequency | TBD MHz |
| Total Cell Count | TBD |
| Core Area | TBD µm² |
| Power (estimated) | TBD µW |

### Physical Verification

| Check | Tool | Status |
|-------|------|--------|
| Design Rule Check (DRC) | Magic v8.3 | ✅ Clean |
| Layout vs. Schematic (LVS) | Netgen | ✅ Clean |

> 📐 Layout previews and detailed timing reports are available in the [`docs/`](./docs) directory.

---

## 📄 Technical Paper

> 📥 **Full document:** [`docs/informe_electiva_2.pdf`](./docs/informe_electiva_2.pdf)

This repository accompanies the IEEE-format technical article submitted for the Elective II course. The paper covers the complete RTL-to-GDSII flow and experimental validation of the system.

### Authors

| Name | Affiliation | Contact |
|------|------------|---------|
| **Elkin Felipe Leguizamón Martínez** | Ingeniería Electrónica, UPTC — Tunja, Boyacá, Colombia | elkin.leguizamon01@uptc.edu.co |
| **Juan Pablo Briceño** | Ingeniería Electrónica, UPTC — Tunja, Boyacá, Colombia | juan.briceno@uptc.edu.co |

### Abstract

> This article presents the design and validation of a digital control system for a variable-stiffness mini gripper, developed following the digital design flow studied in the Elective II course of Electronic Engineering. The system was described in Verilog HDL and verified through functional simulations, as well as through physical validation tests using an FPGA as a prototyping platform.
>
> The proposal seeks to provide a control mechanism capable of adjusting the gripper's stiffness levels, allowing the gripping force to be adapted according to the characteristics of the manipulated object. A digital architecture was developed oriented toward control signal generation and the management of different system operating states. The design was implemented following an ASIC-compatible development flow using open-source EDA tools for the stages of logic synthesis, placement, and routing.
>
> Design Rule Check (DRC) and Layout Versus Schematic (LVS) verifications were also carried out, obtaining satisfactory results that demonstrate the technical feasibility of the proposal. Currently, the project is in the validation and pre-fabrication optimization phase. As future work, integration of the design into the Tiny Tapeout fabrication flow using 130 nm SkyWater SKY130 technology is contemplated, with the goal of obtaining a physical silicon implementation.

### Development Methodology (Work Packages)

The project was organized into eight work packages (WP):

| WP | Stage | Key Deliverables |
|----|-------|-----------------|
| WP1 | Requirements & Architecture | Requirements doc, block diagrams |
| WP2 | RTL Design in Verilog HDL | Source code, RTL diagrams, module docs |
| WP3 | Functional Verification | Testbenches, simulation results, validation reports |
| WP4 | Synthesis & STA | Synthesized netlist, utilization & timing reports |
| WP5 | ASIC Physical Design | Physical layout, GDSII, area & power reports |
| WP6 | Physical Verification (DRC/LVS) | DRC report, LVS report, manufacturability evaluation |
| WP7 | FPGA Implementation & Validation | Bitstream, experimental results, hardware validation |
| WP8 | Documentation & Presentation | GitHub repository, IEEE article, final presentation |

### Key Conclusions from the Paper

1. The digital system for variable-stiffness mini gripper control was successfully developed in Verilog HDL following course methodologies.
2. The architecture was validated via functional simulation and FPGA prototyping before physical implementation.
3. The complete ASIC flow was executed using open-source EDA tools, including synthesis, STA, floorplanning, placement, CTS, routing, and physical verification.
4. The SkyWater SKY130 PDK and OpenLane flow enabled generation of the chip physical layout with all files required for 130 nm CMOS fabrication.
5. DRC and LVS verifications confirmed consistency and technological compatibility with the SKY130 process.
6. Although the circuit has not yet been submitted to fabrication via Tiny Tapeout, the project establishes a solid foundation for future MPW participation.

### References

| # | Reference |
|---|-----------|
| [1] | Tiny Tapeout — https://tinytapeout.com |
| [2] | SkyWater SKY130 Open Source PDK — https://github.com/google/skywater-pdk |
| [3] | M. Shalan & T. Edwards, "OpenLane: The open-source digital ASIC implementation flow," OSDA 2020 |
| [4] | P. P. Acarnley, *Stepping Motors: A Guide to Theory and Practice*, 4th ed., IET, 2002 |
| [5] | B. Vanderborght et al., "Variable impedance actuators: A review," *Robot. Auton. Syst.*, vol. 61, 2013 |
| [6] | S. Wolf et al., "Variable stiffness actuators: Review on design and components," *IEEE/ASME Trans. Mechatronics*, vol. 21, 2016 |
| [7] | A. Bicchi & V. Kumar, "Robotic grasping and contact: A review," *IEEE ICRA*, 2000 |
| [8] | C. Wolf, "Yosys Open SYnthesis Suite" — https://yosyshq.net/yosys/ |
| [9] | J. Ousterhout, "Magic: A VLSI layout system," *DAC*, 1984 |

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature`.
3. Commit your changes: `git commit -m 'feat: add your feature'`.
4. Push to the branch: `git push origin feature/your-feature`.
5. Open a Pull Request describing your changes.

Please ensure all RTL changes are accompanied by updated testbenches and that simulations pass before submitting.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **UPTC** — Universidad Pedagógica y Tecnológica de Colombia, Departamento de Ingeniería Electrónica y Laboratorio de Robótica y Electrónica
- **Prof. Juan David Balaguera** — for guidance and mentorship throughout the project
- **Tiny Tapeout** — for democratizing ASIC fabrication: [tinytapeout.com](https://tinytapeout.com)
- **Google + SkyWater** — for the open-source SKY130 PDK
- **The OpenROAD Project** — for open-source physical design tools
- **Yosys** — for open-source logic synthesis

---

<div align="center">

*Designed with ❤️ at UPTC · Tunja, Boyacá, Colombia*

</div>