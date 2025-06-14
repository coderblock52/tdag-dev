# TDAG City Systems Directory Structure

## Overview
This directory separates city-related systems into two primary layers:

### Root Directory (systems/cities/)
Contains city **behavioral definitions** and structural references:
- `clan_alliances_and_rivalries.full.json`: Defines how clans form alliances and rivalries
- `noble_family_roles.full.json`: Outlines roles noble families can take within cities

These files support city generation, social logic, and structural configuration. They are not directly used during simulation ticks, but inform narrative and design rules.

---

### Simulation Subdirectory (systems/cities/systems/)
Contains **simulation-driven logic** used during live ticks:
- `city_events_and_crisis.full.json`: Drives city-level crises and events
- `city_tiers.full.json`: Tier progression and rules
- `pillar_clans.full.json`, `population_system.json`, etc.: Govern city performance and governance logic

These files are actively referenced during city simulation ticks and support performance scaling, faction dynamics, and dynamic events.

---

## Usage
- Load **root files** when generating or structuring cities
- Load **simulation systems** during active simulation loops

Future expansion will support `simulation_index.json` to register simulation-active files globally.

