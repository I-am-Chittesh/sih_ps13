# Problem Statement & System Requirements Specification

---

## 1. Official Problem Statement Overview

* **Problem Statement ID:** PS #13
* **Track / Sector:** Defence
* **Problem Statement Title:** Autonomous Mine Detection System
* **Detailed Problem Statement:** Landmines and unexploded ordnance remain major threats to personnel. Current detection methods are slow and hazardous.
* **Expected Solution Mandate:** Multi-sensor robotic mine detection platform using Ground Penetrating Radar (GPR), computer vision, and AI.

---

## 2. Core Problem Analysis

* **Target Scope:** The operational envelope encompasses both buried anti-personnel/anti-tank landmines and surface-level Unexploded Ordnance (UXO) such as unspent shells, mortars, and cluster munitions.
* **Operational Risk:** Conventional manual clearance protocols (handheld metal detectors, prodders, and manual sapper deployment) incur high casualty rates and severe operational latency.
* **Mechanization Bottlenecks:** Existing heavy demining machinery (mine flails and heavy rollers) are cost-prohibitive, fuel-intensive, and mechanically incapable of maneuvering across confined, irregular, or densely vegetated terrain.

---

## 3. Engineering & Operational Considerations Taken

### A. Target Threat Vector Differentiation

* **Metallic vs. Non-Metallic Targets:** Modern minimum-metal and non-metallic (plastic/wood/bakelite) landmines cannot be identified via electromagnetic induction alone.
* **Buried vs. Exposed Threats:** Buried mines require subsurface dielectric profiling, whereas exposed or partially concealed UXO, surface mines, and tripwires require optical surface identification.

### B. Platform Mobility & Autonomy Requirements

* **Unsupervised Grid Traversal:** The robotic platform must execute fully autonomous path planning and coverage algorithms across designated target bounding coordinates without human teleoperation.
* **Terrain Adaptability:** Locomotion mechanics must maintain chassis stability, low ground pressure (to avoid premature mechanical triggering), and sensor alignment over unpaved, uneven, and obstacle-dense soil.
* **Failsafe Protocols:** The system must incorporate deterministic emergency braking and state-holding upon anomaly detection to prevent platform destruction.

### C. Subsurface Sensor Architecture (Ground Penetrating Radar)

* **Dielectric Discontinuity Detection:** The subsurface subsystem must utilize high-frequency radio wave pulses to measure reflections caused by differences in soil vs. object dielectric constants ($\varepsilon_r$).
* **Sensor Standoff & Clearance:** The physical radar/sensor head must maintain a regulated distance ahead of the primary vehicle footprint to identify threats before track or wheel contact occurs.

### D. Optical Computer Vision & Environmental Mapping

* **Surface Hazard Detection:** Edge-based vision models must continuously parse live optical feeds to detect exposed munitions, tripwires, and disturbed topsoil patterns.
* **Navigational Obstacle Avoidance:** Visual perception must run concurrently with path planning to bypass physical ground obstructions (boulders, trenches, dense flora) without degrading sensor sweep integrity.

### E. Sensor Fusion & AI Threat Classification

* **Multimodal Data Processing:** The processing pipeline must ingest asymmetric datastreams—subsurface GPR reflections and optical camera frames—into a unified inference pipeline.
* **Automated Target Discrimination:** The AI architecture must classify detected subsurface anomalies against historical clutter (roots, metallic scrap, mineral pockets) and assign probabilistic confidence ratings to identified threats.
* **Telemetry & Coordinate Tagging:** When an anomaly is validated, the system must log its spatial GPS/local-frame coordinates, halt autonomous traversal, and broadcast structured alert telemetry to a centralized command station.