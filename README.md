# Cyberduke: Tactical Infiltration

A retro-futuristic, low-poly 3D stealth and infiltration prototype built with **Python**, **Pygame**, and **Modern Fixed-Function OpenGL**.

Inspired by the sneaking, quick-hacking, and corporate espionage elements of *Cyberpunk 2077* combined with the grit and attitude of classic retro shooters, **Cyberduke** features an extensible hierarchical skeletal animation system, sensory AI with dynamic field-of-view detection, environmental occlusion raycasting, and procedurally generated cyberpunk textures.

---

## Table of Contents

- [Features](#features)
- [Project Architecture](#project-architecture)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Controls](#controls)
- [Implementing Custom NPCs](#implementing-custom-npcs)
  - [1. Pose Generation & Keyframing](#1-pose-generation--keyframing)
  - [2. Model Configuration & Props](#2-model-configuration--props)
  - [3. Entity Behavior & State Machines](#3-entity-behavior--state-machines)
  - [4. Step-by-Step Example: Datapad Courier](#4-step-by-step-example-datapad-courier)
- [Roadmap](#roadmap)

---

## Features

- **Sensory Guard AI**:
  - State machine supporting patrol routines, wall leaning, weapon inspection, and perimeter scanning.
  - Vision cones dynamically calculate FOV and distance based on agent posture (e.g., lower awareness while inspecting gear, wide-angle scan when standing alert).
  - Ray-box line-of-sight (LOS) occlusion checks prevent detection through physical covers (desks, terminals, columns).
- **Hierarchical Humanoid Skeleton**:
  - Independent rotation channels for neck, head (pitch/yaw/roll), shoulders, elbows, hips, and knees.
  - Normalized socket system for rendering dynamic, holsterable props (weapons, datapads, tools) that transition smoothly between the hips, chest, and hands.
- **Stealth & Infiltration Mechanics**:
  - First-person crouching system that dampens footstep profiles, lowers camera eye-line, and dramatically reduces detection build-up.
  - Interactive terminals requiring physical proximity and time-based decryption channels to trigger environmental actions (e.g., sliding blast doors).
- **Stylized Cyberpunk Aesthetics**:
  - Atmospheric dual-point neon illumination (Cyan `GL_LIGHT0` vs. Magenta `GL_LIGHT1`) with material specular and emissive responses.
  - Zero-dependency procedural textures generated via NumPy arrays (metal grating, hazard stripes, terminal UIs, fabrics, leather, and skin).

---

## Project Architecture

```text
├── animation.py      # HumanoidPose dataclass, interpolation, and keyframe generators
├── entities.py       # Player controller, interactable Terminal, and primitive mesh drawers
├── guard.py          # CyberGuard NPC subclass implementing patrol/inspect state machines
├── hud.py            # Orthographic 2D interface: crosshairs, detection bars, hack meters
├── main.py           # Application entry point: OpenGL initialization, input, and render loop
├── model.py          # Modular HumanoidModel renderer and procedural prop meshes
├── npc.py            # BaseNPC spatial entity: navigation, smooth steering, and vision frustum
├── textures.py       # Procedural texture generator utilizing NumPy bitarrays
└── world.py          # 3D room environment, sliding blast doors, and neon strip light fixtures
```

### Module Breakdown

| Module | Primary Responsibility |
| :--- | :--- |
| `animation.py` | Defines `HumanoidPose` joint transformations and pose-blending math (`smoothstep`, `lerp`, slab ray-box intersection). |
| `model.py` | Encapsulates the OpenGL matrix stack for hierarchical humanoid rendering, customizable accessories (visors, cores, holsters), and props. |
| `npc.py` | Supplies `BaseNPC`, managing world coordinates, smooth angular interpolation (`rotate_towards`), waypoint steering (`move_towards`), and FOV cone/LOS raycasts (`can_see_target`). |
| `guard.py` | Implements game-specific AI routines (`PACING`, `WALKING_TO_WALL`, `LEANING`, `WALKING_TO_PATROL`) and detection parameters. |
| `entities.py` | Defines the `Player` state (stealth meter, crouch lerp) and `Terminal` interaction volumes. |
| `hud.py` | Handles 2D UI projection, dynamic detection colors, and GPU font caching. |

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
| **C** | Toggle Crouch (lowers profile, reduces detection gain) |
| **E** | Hack Terminal (hold within 2.5m range) |
| **R** | Reset simulation after victory or alert |
| **Esc** | Exit application |

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
 │      3. npc.py        │  Spatial Positioning & Navigation (BaseNPC)
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
    has_visor=False,           # Disable combat visor
    has_core_glow=False,        # Disable combat core
    has_holster=False,
    hair_color=(0.8, 0.5, 0.1),# Orange hair
    prop_drawer=draw_datapad,
)
```

### 3. Entity Behavior & State Machines

Subclass `BaseNPC` to build your AI:
- `self.move_towards(target_x, target_z, dt)` automatically manages target heading, steering interpolation, and walking leg animations. Returns `True` upon arrival.
- `self.rotate_towards(target_yaw, dt)` smooths rotation without translational movement. Returns `True` when aligned.
- `self.can_see_target(px, pz, max_range, fov_angle, obstacles)` handles distance, field of view (taking head yaw into account), and obstacle raycasting.

---

### 4. Step-by-Step Example: Datapad Courier

Here is a complete, runnable NPC class implementing an oblivious corporate courier patrolling between two desks:

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
        super().__init__(x, y, z, model=model, walk_speed=0.9, turn_speed=180.0)
        self.state = "PATROLLING_A"
        self.inspect_timer = 0.0

    def update(self, player, dt, obstacles=None):
        # 1. State Machine
        if self.state == "PATROLLING_A":
            if self.move_towards(3.0, 2.0, dt):
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
            if self.move_towards(-3.0, 2.0, dt):
                self.state = "READING"
                self.inspect_timer = 0.0

        # 2. Vision Check (Oblivious courier has very narrow FOV)
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
3. Call `courier.update(player, dt, obstacles=[terminal.get_bounds()])` in the update step.
4. Call `courier.draw()` in the render step.

---

## Roadmap

- [ ] **City Street Hub**: Expand `world.py` to support multi-room floor plans, alleys, and skybridge zones.
- [ ] **Spatial Partitioning**: Replace linear obstacle checks with a 2D Quadtree / BVH for high NPC density.
- [ ] **Quickhacking Suite**: Implement distance raycasts against cameras, guard optics, and power grids (Distract, Ping, Blind).
- [ ] **Expanded Audio Feedback**: Footstep volume thresholds relative to movement speed and crouching.
- [ ] **Inventory & Cyberware**: Stash looted corporate credentials and upgrade locomotion (double jumps, optical camo).