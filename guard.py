import math
from animation import inspect_weapon_animation, walk_animation
from model import draw_laser_blaster, HumanoidModel
from npc import BaseNPC


class CyberGuard(BaseNPC):
  """Tactical guard AI: patrols, leans on the wall, inspects gun, and alerts on players."""

  def __init__(self, x, y, z, textures):
    model = HumanoidModel(
        textures=textures,
        has_visor=True,
        has_core_glow=True,
        has_holster=True,
        prop_drawer=draw_laser_blaster,
    )
    super().__init__(x, y, z, model=model, walk_speed=1.2)

    self.patrol_dir = 1.0
    self.state = "PACING"
    self.state_timer = 0.0
    self.pacing_duration = 5.0
    self.lean_duration = 15.0

  def reset(self):
    super().reset()
    self.patrol_dir = 1.0
    self.state = "PACING"
    self.state_timer = 0.0

  def update(self, player, dt, obstacles=None):
    self.state_timer += dt

    # 1. Finite State Machine
    if self.state == "PACING":
      self.z += self.walk_speed * self.patrol_dir * dt
      self.walk_cycle += self.walk_speed * dt * 5.5
      self.pose = walk_animation(self.walk_cycle)

      if self.z > -3.0:
        self.patrol_dir = -1.0
        self.target_yaw = 180.0
      elif self.z < -8.5:
        self.patrol_dir = 1.0
        self.target_yaw = 0.0

      self.rotate_towards(self.target_yaw, dt)

      if self.state_timer > self.pacing_duration:
        self.state = "WALKING_TO_WALL"
        self.state_timer = 0.0

    elif self.state == "WALKING_TO_WALL":
      if self.move_towards(-5.5, -6.0, dt):
        self.target_yaw = 90.0
        self.state = "LEANING"
        self.state_timer = 0.0

    elif self.state == "LEANING":
      self.rotate_towards(self.target_yaw, dt)
      self.pose = inspect_weapon_animation(self.state_timer, self.lean_duration)

      if self.state_timer > self.lean_duration:
        self.state = "WALKING_TO_PATROL"
        self.state_timer = 0.0

    elif self.state == "WALKING_TO_PATROL":
      if self.move_towards(0.0, self.z, dt):
        self.target_yaw = 0.0 if self.patrol_dir > 0 else 180.0
        self.state = "PACING"
        self.state_timer = 0.0

    # 2. Vision & Stealth Detection
    if self.pose.head_pitch > 20.0:
      max_range, fov = 1.8, 30.0  # Engrossed in gun
    else:
      max_range, fov = 5.2, 55.0  # Active room scan

    spotted = self.can_see_target(
        player.x, player.z, max_range=max_range, fov_angle=fov, obstacles=obstacles
    )

    if spotted:
      rate = 45.0 if not player.crouching else 12.0
      player.stealth_meter = min(100.0, player.stealth_meter + rate * dt)
    else:
      player.stealth_meter = max(0.0, player.stealth_meter - 30.0 * dt)