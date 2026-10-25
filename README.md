# Cyberduke: Tactical Infiltration

A retro-futuristic, low-poly 3D stealth and infiltration game built with **Python**, **Pygame**, and **Modern Fixed-Function OpenGL**.

Inspired by the sneaking, quick-hacking, and corporate espionage elements of *Cyberpunk 2077* combined with the grit and attitude of classic retro shooters, **Cyberduke** features an extensible hierarchical skeletal animation system, multi-sector level architecture, 2D A* pathfinding with raycast string-pulling smoothing, sensory guard AI with acoustic distraction states, security camera laser sweeps, environmental occlusion raycasting, and procedurally generated cyberpunk textures.

---

## Table of Contents

- [Features](#features)
- [Mission Objectives & Gameplay Flow](#mission-objectives--gameplay-flow)
- [Facility Layout & Sector Architecture](#facility-layout--sector-architecture)
- [Project Architecture](#project-architecture)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Controls](#controls)
- [Interactive Entities & Hazards](#interactive-entities--hazards)
  - [Security Camera](#security-camera)
  - [Vending Machine ("NEON COLD")](#vending-machine-neon-cold)
  - [Terminals & Blast Doors](#terminals--blast-doors)
- [Implementing Custom NPCs](#implementing-custom-npcs)
  - [1. Pose Generation & Keyframing](#1-pose-generation--keyframing)
  - [2. Model Configuration & Props](#2-model-configuration--props)
  - [3. Entity Behavior, Pathfinding & State Machines](#3-entity-behavior-pathfinding--state-machines)
  - [4. Step-by-Step Example: Datapad Courier](#4-step-by-step-example-datapad-courier)
- [Roadmap](#roadmap)

---

## Features

- **Intelligent A* Pathfinding & Collision Avoidance**:
  - High-performance 2D A* pathfinder (`Pathfinder` in `npc.py`) operating on an agent-inflated grid ($r = 0.35\text{m}$, $0.4\text{m}$ resolution) to calculate collision-free courses in under 1ms.
  - Greedy raycast string-pulling (path smoothing) using `line_intersects_box` to turn jagged grid paths into natural, direct trajectories around columns, server banks, and barrels.
  - Step-level physical collision detection with obstacle surface sliding, preventing NPCs from ever clipping through walls, columns, or cover props.
  - Fast-path direct line-of-sight optimization: skips grid searches entirely when the line of sight to the goal is clear.
- **Sensory Guard AI & Acoustic Distraction**:
  - State machine supporting patrol routines, configurable wall leaning (`wall_pos`, `wall_yaw`), weapon inspection, acoustic investigations, and perimeter scanning.
  - Vision cones dynamically calculate FOV and distance based on agent posture (e.g., lower awareness while inspecting gear, wide-angle scan when standing alert).
  - Ray-box line-of-sight (LOS) occlusion checks prevent detection through physical covers (desks, server racks, crates, columns) and facility walls.
  - Arrival-gated acoustic distraction routine: guards navigate around obstacles to the distraction site, reset their timer upon arrival, and inspect the machine for at least 15 seconds before returning.
  - Coordinated multi-agent stealth accumulation (`player.spotted_this_frame`) preventing detection flutter.
- **Surveillance Hazards**:
  - Wall-mounted security cameras with sweeping motor heads ($\pm 35^\circ$ sweep).
  - Ray-AABB collision-truncated laser frustum fans that dynamically collide with and terminate against walls, doorframes, and obstacles with vertical drop lines.
  - Progressive detection escalation (+65/s when upright, dampened to +18/s when crouching) with ray-box LOS checks through open doorways.
- **Multi-Sector Facility Architecture**:
  - Modular sector design separating Staging Bay, Airlock Corridor, and the multi-tiered Datacore Vault.
  - Coolant drainage trenches with emissive liquid beneath grates, elevated catwalks ($Y = 2.75\text{m}$) with flush access ramps, hazard handrails, steam pipes with pressure gauges, and central datacore monoliths.
  - Dynamic floor height interpolation (`room.get_floor_height(x, z)`) allowing the player to climb ramps and traverse catwalks.
  - Unified obstacle collision and spatial bounding across sectors.
- **Hierarchical Humanoid Skeleton**:
  - Independent rotation channels for neck, head (pitch/yaw/roll), shoulders, elbows, hips, and knees.
  - Normalized socket system for rendering dynamic, holsterable props (weapons, datapads, tools) that transition smoothly between hips, chest, and hands.
- **Stealth & Infiltration Mechanics**:
  - First-person crouching system that lowers eye-line, dampens movement profile, and minimizes camera/guard detection build-up.
  - Multi-stage terminal hacking requiring physical proximity and continuous decryption channels.
- **Atmospheric 7-Point Neon Lighting**:
  - Comprehensive 7-point hardware illumination suite (`GL_LIGHT0` through `GL_LIGHT6`) with $4\times$ boosted cyberpunk ambient/diffuse/specular lighting.
  - Sector-specific color grading: Staging Bay cyan/magenta/amber neon, Airlock industrial yellow caution lamps, and Datacore halo/catwalk floodlights.
- **Zero-Dependency Procedural Textures**:
  - NumPy bitarray generation for metal grates, floor tiles, server racks, hazard stripes, terminal UIs, beverage cans, fabric, leather, armor, and skin.

---

## Mission Objectives & Gameplay Flow

The infiltration follows a tactical two-stage penetration:

```text
 ┌────────────────────────────────────────────────────────┐
 │ Stage 1: Infiltrate Sector 1 (Staging Bay)             │
 │ - Evade Sector 1 CyberGuard patrol.                    │
 │ - Reach & hack the Netrunner Terminal (X=3.5, Z=-4.0). │
 │ - Unlock pneumatic blast door at Z=10.0.               │
 └──────────────────────────┬─────────────────────────────┘
                            │
                            ▼
 ┌────────────────────────────────────────────────────────┐
 │ Intermission: Sector Airlock Corridor                  │
 │ - Navigate corridor between Z=10.0 and Z=18.0.         │
 │ - Crouch beneath the sweeping Security Camera laser fan│
 │   mounted at Z=11.2, Y=3.6.                            │
 └──────────────────────────┬─────────────────────────────┘
                            │
                            ▼
 ┌────────────────────────────────────────────────────────┐
 │ Stage 2: Sector 2 Datacore Vault Espionage             │
 │ - Enter Datacore Vault (Z=18.0 -> 42.0).               │
 │ - Trigger "NEON COLD" Vending Machine at X=-7.5, Z=25.0│
 │   to lure Guard 2 away from the central monolith.      │
 │ - Guard 2 A* pathfinds to the machine and investigates │
 │   for 15+ seconds with back turned.                    │
 │ - Scale catwalk ramps or sneak past coolant trenches.  │
 │ - Hack Datacore Terminal (X=0.0, Z=30.0) to win!       │
 └────────────────────────────────────────────────────────┘
```

---

## Facility Layout & Sector Architecture

The facility is divided into three distinct sectors coordinated by `Room`:

```text
    Z=42.0 ┌─────────────────────────────────────────┐
           │        Sector 2: Datacore Vault         │
           │  Catwalk (Y=2.75)[===========] Catwalk  │
           │       [Trench]  [DATACORE]  [Trench]    │
           │                 Terminal 2              │
           │  [Vending]                              │
    Z=18.0 ├───────────────[Bulkhead]────────────────┤
           │      Sector Airlock Corridor            │
           │     [Camera] Steam Pipes & Grates       │
    Z=10.0 ├───────────────[Blast Door]──────────────┤
           │        Sector 1: Staging Bay            │
           │  Server Racks, Crates, Pillars          │
           │                 Terminal 1              │
    Z=-10.0└─────────────────────────────────────────┘
           X=-10.0            X=0.0            X=10.0
```

### 1. Sector 1: Staging Bay ($Z \in [-10.0, 10.0], X \in [-6.0, 6.0]$)
- Features heavy server banks, structural concrete pillars, tactical cargo crates, and a Japanese neon sign.
- Guard 1 patrols between $Z = -8.5$ and $Z = -3.0$, occasionally leaning against the left wall at $(-5.5, -6.0)$ facing $+X$ (`wall_yaw = 90.0`).
- Contains the Stage 1 Netrunner Terminal ($X=3.5, Z=-4.0$) controlling the primary blast door.

### 2. Sector Airlock: Corridor ($Z \in [10.0, 18.0], X \in [-2.5, 2.5]$)
- Pneumatic transition airlock with reinforced bulkheads, wall-mounted steam pipes, illuminated pressure gauges, and floor drainage grates.
- Overhead industrial amber caution lighting (`GL_LIGHT3` at $X=0.0, Y=3.6, Z=14.0$).
- Guarded by an active `SecurityCamera` ($Z=11.2, Y=3.6$) whose laser rays truncate cleanly against the airlock walls.

### 3. Sector 2: Datacore Vault ($Z \in [18.0, 42.0], X \in [-10.0, 10.0], Y \in [0.0, 6.0]$)
- **Central Datacore Monolith**: Rises 5.5m high at $X=0.0, Z=32.0$ with glowing data bus lines, housing the primary extraction terminal ($Z=30.0$) facing outward into the room ($180^\circ$ yaw).
- **Dual Coolant Trenches**: Recessed drainage canals at $X = \pm 3.5$ with glowing cyan/green emissive coolant fluid under heavy iron grates.
- **Elevated Perimeter Catwalks**: Raised walkways at $Y=2.75\text{m}$ (providing $>2.5\text{ feet}$ of clearance above guards' heads) with access ramps ($Z \in [18.8, 24.2]$) connecting flush with the catwalk edge at $Z = 24.2$.
- **Tactical Cover & Distractions**: Auxiliary server racks, cryogenic storage cylinders, crate clusters, and the "NEON COLD" vending machine ($X=-7.5, Z=25.0$).
- Guard 2 patrols the clear right walkway lane ($X = 2.1, Z \in [24.0, 36.0]$) and leans against the right wall at $(9.45, 30.0)$ facing $-X$ (`wall_yaw = -90.0`).

---

## Project Architecture

```text
├── animation.py      # HumanoidPose joint dataclass, lerp/smoothstep, and ray-AABB math
├── entities.py       # Player, Terminal, SecurityCamera, VendingMachine, and 3D primitives
├── guard.py          # CyberGuard NPC subclass with patrol, inspect, and A* investigate AI
├── hud.py            # Orthographic 2D interface: crosshair, stealth meter, hacking progress
├── main.py           # Application entry point: 7-point GL lighting, input, and render loop
├── model.py          # Hierarchical humanoid renderer, accessory sockets, and prop meshes
├── npc.py            # Pathfinder (A* search & string-pulling) and BaseNPC (navigation & steering)
├── textures.py       # Procedural texture generator using NumPy arrays
└── world.py          # Sector1, SectorAirlock, Sector2, and coordinator Room class
```

### Module Breakdown

| Module | Primary Responsibility |
| :--- | :--- |
| `world.py` | Implements `Sector1_StagingBay`, `SectorAirlock_Corridor`, `Sector2_DatacoreVault`, and `Room` coordinator. Manages sliding blast doors, coolant trenches, catwalk ramps, surface elevations (`get_floor_height`), and unified collision boundaries (`is_valid_position`, `get_obstacles`). |
| `entities.py` | Encapsulates interactive and hazardous world entities: `Player` controller, `Terminal` decryption volumes (with orientation `yaw`), `SecurityCamera` (laser sweep frustum with ray-AABB wall truncation & LOS detection), and `VendingMachine` (soda dispense & 22m acoustic guard pulse). |
| `guard.py` | Subclasses `BaseNPC` into `CyberGuard` with multi-route configuration (`patrol_z_min`, `patrol_z_max`, `wall_pos`, `wall_yaw`), A* pathfinding around columns and barrels, and arrival-gated 15-second investigation routines (`distract(x, z)`). |
| `npc.py` | Supplies `Pathfinder` (2D grid A* search and raycast string-pulling smoothing) and `BaseNPC` managing spatial coordinates, heading interpolation (`rotate_towards`), obstacle-avoiding navigation (`navigate_towards`), and FOV cone detection with raycast LOS checks (`can_see_target`). |
| `animation.py` | Supplies `HumanoidPose` joint transformations, procedural walking/leaning/inspecting keyframers, pose blending (`lerp_pose`), and ray-box slab intersection math (`line_intersects_aabb`, `line_intersects_box`). |
| `model.py` | Hierarchical OpenGL matrix rendering for humanoid skeletons, cybernetic visors, glowing chest cores, holsters, and prop callbacks. |
| `textures.py` | Zero-dependency procedural texture generator using NumPy bitarrays (metal, grating, hazard stripes, terminal UIs, neon signs, soda cans, fabrics, skin). |
| `hud.py` | 2D orthographic overlay displaying dynamic detection meters, terminal hacking rings, action prompts, and full-screen alert/win banners. |
| `main.py` | Initializes OpenGL context, sets up the 7-light hardware illumination grid, processes input, runs physics/AI updates, and drives the frame loop. |

---

## Getting Started

### Prerequisites

- Python 3.8+
- Pygame
- PyOpenGL
- NumPy

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/cyberduke.git
   cd cyberduke
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install pygame PyOpenGL numpy
   ```

4. Run the simulation:
   ```bash
   python main.py
   ```

### Controls

| Input | Action |
| :--- | :--- |
| **W, A, S, D** | Move forward, strafe left, move backward, strafe right |
| **Mouse** | Look around (Yaw / Pitch) |
| **C** | Toggle Crouch (lowers eye-line, dampens movement profile, reduces detection build-up) |
| **E** | Interact (Hold within 2.5m to Hack Terminals; Press within 2.5m to trigger Vending Machine distraction) |
| **R** | Reset simulation after victory or alert |
| **Esc** | Exit application |

---

## Interactive Entities & Hazards

### Security Camera
- **Mount Point**: Airlock ceiling at $X=0.0, Y=3.6, Z=11.2$.
- **Sweep Behavior**: Sine-wave oscillation across $\pm 35^\circ$ sweep angle.
- **Ray-AABB Wall Truncation**: Visual laser frustum rays raycast against all wall and prop hitboxes, truncating at the exact 3D point of contact with vertical wall seam drop lines instead of penetrating outside the facility.
- **Detection Rate**: $+65.0$/s standing; crouching dampens gain to $+18.0$/s. Fully blocked by physical walls and closed doors via slab ray-box intersection.

### Vending Machine ("NEON COLD")
- **Placement**: Datacore Vault at $X=-7.5, Z=25.0$ beneath the left catwalk.
- **Visuals**: Backlit neon marquee, glowing beverage product display, illuminated coin/cred slot, and delivery hopper.
- **Acoustic Distraction**: Pressing `[E]` within 2.5m triggers an electrical short-circuit sound and dispenses a soda can. Emits an acoustic pulse ($r = 22.0\text{m}$) that pulls nearby guards into an A*-routed 15-second investigation state.

### Terminals & Blast Doors
- **Stage 1 Terminal ($X=3.5, Z=-4.0$)**: Requires 3 seconds of sustained interaction (`[E]`). Once hacked, triggers pneumatic hydraulics that slide open the heavy blast door at $Z=10.0$.
- **Datacore Central Terminal ($X=0.0, Z=30.0$)**: Primary extraction terminal rotated $180^\circ$ outward at the base of the central monolith. Completing decryption triggers mission victory.

---

## Implementing Custom NPCs

The NPC architecture is built around three isolated layers:

```text
 ┌───────────────────────┐
 │   1. animation.py     │  Transforms & Positional Timing (HumanoidPose)
 └──────────┬────────────┘
            │ Drives
            ▼
 ┌───────────────────────┐
 │     2. model.py       │  Visual Geometry & Sockets (HumanoidModel)
 └──────────┬────────────┘
            │ Attached to
            ▼
 ┌───────────────────────┐
 │      3. npc.py        │  Spatial Positioning, A* Pathfinding & Navigation (BaseNPC)
 └───────────────────────┘
```

### 1. Pose Generation & Keyframing

To animate a character, define a function that takes a time value $t$ or walk cycle parameter and returns a `HumanoidPose`. 

Key joint vectors:
- `arm_l` / `arm_r`: `[pitch, yaw, roll, elbow_bend]` (degrees)
- `leg_l` / `leg_r`: `[hip_pitch, hip_yaw, knee_bend]` (degrees)
- `prop_pos` / `prop_rot`: Translation `[x, y, z]` and rotation `[rx, ry, rz]` relative to the character origin.

```python
from animation import HumanoidPose, smoothstep, lerp

def typing_on_datapad_animation(t: float) -> HumanoidPose:
    """NPC holds a datapad at chest height and taps it."""
    cycle = t * 4.0
    finger_tap = math.sin(cycle) * 5.0
    
    return HumanoidPose(
        bob=math.sin(t * 1.5) * 0.003,
        head_pitch=28.0,  # Looking down at datapad
        head_yaw=0.0,
        # Left arm cradles datapad
        arm_l=[-15.0, -25.0, 10.0, -90.0],
        # Right arm taps screen
        arm_r=[-10.0, 15.0, -10.0, -95.0 + finger_tap],
        leg_l=[0.0, 0.0, 0.0],
        leg_r=[0.0, 0.0, 0.0],
        has_prop=True,
        prop_pos=[0.0, 1.25, 0.32],
        prop_rot=[35.0, 0.0, 0.0],
    )
```

### 2. Model Configuration & Props

Use `HumanoidModel` to customize body textures, hair, accessories, and prop renderers:

```python
from model import HumanoidModel
from entities import draw_cube
from OpenGL.GL import *

def draw_datapad():
    """Custom prop callback."""
    glPushMatrix()
    glScalef(0.24, 0.02, 0.16)
    draw_cube(None)  # Render datapad chassis
    glPopMatrix()

custom_model = HumanoidModel(
    textures=textures_dict,
    has_visor=False,            # Disable combat visor
    has_core_glow=False,         # Disable combat core
    has_holster=False,
    hair_color=(0.8, 0.5, 0.1), # Orange hair
    prop_drawer=draw_datapad,
)
```

### 3. Entity Behavior, Pathfinding & State Machines

Subclass `BaseNPC` to build your AI:
- `self.navigate_towards(target_x, target_z, dt, obstacles=obstacles, stop_dist=0.15)`:
  - Uses the built-in `Pathfinder` to compute collision-free A* trajectories on a $0.4\text{m}$ grid.
  - Automatically performs raycast string-pulling smoothing around corners.
  - Enforces physical step collision sliding along obstacle walls.
  - Returns `True` when arrived at the destination.
- `self.move_towards(target_x, target_z, dt, stop_dist=0.05)`: Direct straight-line steering and locomotion when navigating unobstructed spaces.
- `self.rotate_towards(target_yaw, dt)`: Smooth angular interpolation without translational movement. Returns `True` when facing target heading.
- `self.can_see_target(px, pz, max_range, fov_angle, obstacles)`: Handles distance, field of view (accounting for head yaw), and ray-box obstacle occlusion.

---

### 4. Step-by-Step Example: Datapad Courier

Here is a complete, runnable NPC class implementing an oblivious corporate courier navigating around obstacles between two desks:

```python
# courier.py
import math
from animation import walk_animation, HumanoidPose
from model import HumanoidModel
from npc import BaseNPC
from entities import draw_cube
from OpenGL.GL import *

def draw_datapad():
    # Tablet chassis
    glColor3f(0.12, 0.12, 0.14)
    glPushMatrix()
    glScalef(0.22, 0.02, 0.15)
    draw_cube(None)
    glPopMatrix()

    # Glowing screen
    glMaterialfv(GL_FRONT, GL_EMISSION, [0.0, 0.8, 1.0, 1.0])
    glColor3f(0.0, 0.8, 1.0)
    glPushMatrix()
    glTranslatef(0.0, 0.015, 0.0)
    glScalef(0.19, 0.01, 0.12)
    draw_cube(None)
    glPopMatrix()
    glMaterialfv(GL_FRONT, GL_EMISSION, [0.0, 0.0, 0.0, 1.0])
    glColor3f(1.0, 1.0, 1.0)

class CorporateCourier(BaseNPC):
    def __init__(self, x, y, z, textures):
        model = HumanoidModel(
            textures=textures,
            has_visor=False,
            has_core_glow=False,
            has_holster=False,
            hair_color=(0.1, 0.1, 0.1),
            prop_drawer=draw_datapad,
        )
        super().__init__(x, y, z, model=model, walk_speed=0.9, turn_speed=180.0, collision_radius=0.35)
        self.state = "PATROLLING_A"
        self.inspect_timer = 0.0

    def update(self, player, dt, obstacles=None):
        # 1. State Machine with A* Navigation
        if self.state == "PATROLLING_A":
            # Uses A* pathfinding and physical collision avoidance around pillars/crates
            if self.navigate_towards(3.0, 2.0, dt, obstacles=obstacles):
                self.state = "READING"
                self.inspect_timer = 0.0

        elif self.state == "READING":
            self.inspect_timer += dt
            # Pose while stationary: looking at datapad
            self.pose = HumanoidPose(
                head_pitch=26.0,
                arm_l=[-10.0, -15.0, 5.0, -85.0],
                arm_r=[-10.0, 15.0, -5.0, -85.0],
                has_prop=True,
                prop_pos=[0.0, 1.22, 0.30],
                prop_rot=[30.0, 0.0, 0.0],
            )
            if self.inspect_timer > 6.0:
                self.state = "PATROLLING_B"

        elif self.state == "PATROLLING_B":
            if self.navigate_towards(-3.0, 2.0, dt, obstacles=obstacles):
                self.state = "READING"
                self.inspect_timer = 0.0

        # 2. Vision Check (Oblivious courier has narrow FOV)
        spotted = self.can_see_target(
            player.x, player.z,
            max_range=2.5,
            fov_angle=30.0,
            obstacles=obstacles
        )

        if spotted and not player.crouching:
            # Alert nearby guards or trigger alarm
            pass
```

To incorporate your new NPC into `main.py`:
1. Import `CorporateCourier`.
2. Initialize it in `main()` with your desired texture dictionary.
3. Call `courier.update(player, dt, obstacles=all_obstacles)` in the update step.
4. Call `courier.draw()` in the render step.

---

## Roadmap

- [x] **Modular Sector Architecture**: Multi-sector expansion (Staging Bay $\to$ Airlock Corridor $\to$ Datacore Vault with coolant trenches and catwalks).
- [x] **Surveillance Hazards**: Wall-mounted security cameras with dynamic laser sweep frustums and ray-AABB wall truncation.
- [x] **Environmental Distraction AI**: Interactive vending machine triggering arrival-gated 15-second guard investigation routines.
- [x] **Intelligent A* Pathfinding**: Built-in $0.4\text{m}$ grid A* navigation with raycast string-pulling smoothing and step-level obstacle sliding for NPCs.
- [x] **Master 7-Point Neon Lighting**: 4x boosted ambient, diffuse, and specular illumination across all sectors.
- [ ] **Remote Quickhacking Suite**: Direct distance raycasts against cameras, guard optics, and power grids (Distract, Ping, Blind).
- [ ] **Spatial Partitioning**: Replace linear obstacle checks with a 2D Quadtree / BVH for high NPC and obstacle density.
- [ ] **Expanded Audio Feedback**: Procedural or synthesized footstep volume thresholds, camera hums, and alarm klaxons.
- [ ] **Inventory & Cyberware**: Stash looted corporate credentials and upgrade locomotion (double jumps, optical camo).
