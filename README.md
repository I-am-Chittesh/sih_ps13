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

# Proposed Solution
Mechanical Architecture & Hardware Innovation
1. System Overview
The physical architecture of the autonomous mine detection platform is engineered to solve three critical hardware bottlenecks in mechanized demining: minimizing ground pressure to prevent accidental detonation, ensuring continuous sensor proximity over highly irregular terrain, and maintaining rapid, modular deployability. The system utilizes a lightweight space-frame hull paired with compliant locomotion and a dynamic sensor boom.

2. Primary Mechanical Subsystems
A. Lightweight Modular Space-Frame Chassis
Architecture: The core hull is constructed using a low-weight modular space-frame (utilizing aluminum extrusions or rigid composite rods).

Engineering Advantage: This provides exceptional structural rigidity and torsional stiffness while drastically reducing the vehicle's overall mass. The modular rail system allows for rapid prototyping, enabling electronics bays, motor drivers, and battery payloads to be repositioned to perfectly balance the center of gravity without requiring complete chassis redesigns.

B. Pressure-Negating Locomotion (TPU "Tweels")
Architecture: The rover abandons traditional pneumatic rubber tires in favor of custom 3D-printed "Tweels" (airless tires) manufactured from highly flexible TPU (Thermoplastic Polyurethane) utilizing an internal collapsing honeycomb or spoke geometry.

Engineering Advantage: Standard anti-personnel mines detonate under 5kg to 15kg of concentrated downward force. If the rover accidentally rolls over an undetected fuse, the flexible internal spokes of the Tweel instantly deform around the object. Instead of transferring the weight of the chassis downward to trigger the mine, the wheel safely absorbs the shape of the obstacle, ensuring the ground pressure remains well below the detonation threshold.

C. Dynamic Sensor Deployment (Four-Bar Scissor Linkage)
Architecture: The GPR and metal detection sensors are mounted to a forward-facing, motorized four-bar scissor linkage. The linkage terminates in a semi-circular sensor mounting array.

Engineering Advantage:

The Four-Bar Sweep: By expanding and contracting the linkage, the platform achieves a massive, continuous lateral sweep across the X-Z plane without needing to constantly turn the entire vehicle.

The Semi-Circle Array: Standard straight-bar mounts create detection blind spots at the far edges of a sweep. The semi-circular geometry ensures an overlapping, unbroken detection swath, drastically reducing the time and number of passes required to clear a grid.

D. Passive Terrain Contouring (Y-Axis Compliance)
Architecture: The connection point between the primary space-frame chassis and the four-bar sensor linkage features a passive, free-floating Y-Axis hinge.

