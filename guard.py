import math
from animation import HumanoidPose, inspect_weapon_animation, walk_animation
from model import draw_laser_blaster, HumanoidModel
from npc import BaseNPC


class CyberGuard(BaseNPC):
  """Tactical guard AI: patrols, leans on wall, inspects gun, investigates noises, and alerts on players."""

  def __init__(
      self,
      x,
      y,
      z,
      textures,
      patrol_z_min=-8.5,
      patrol_z_max=-3.0,
      wall_pos=(-5.5, -6.0),
      wall_yaw=90.0,
      pacing_duration=6.0,
      lean_duration=12.0,
      investigate_duration=15.0,
  ):
    model = HumanoidModel(
        textures=textures,
        has_visor=True,
        has_core_glow=True,
        has_holster=True,
        prop_drawer=draw_laser_blaster,
    )
    super().__init__(x, y, z, model=model, walk_speed=1.2, collision_radius=0.35)

    self.home_x = x
    self.patrol_z_min = patrol_z_min
    self.patrol_z_max = patrol_z_max
    self.wall_pos = wall_pos
    self.wall_yaw = wall_yaw

    self.patrol_dir = 1.0
    self.state = "PACING"
    self.state_timer = 0.0
    self.pacing_duration = pacing_duration
    self.lean_duration = lean_duration
    self.investigate_target = None
    self.investigate_duration = investigate_duration
    self.arrived_at_distraction = False

  def reset(self):
    super().reset()
    self.patrol_dir = 1.0
    self.state = "PACING"
    self.state_timer = 0.0
    self.investigate_target = None
    self.arrived_at_distraction = False

  def distract(self, target_x, target_z):
    """Lures guard out of routine to investigate an acoustic/spark distraction."""
    self.investigate_target = (target_x, target_z)
    self.state = "INVESTIGATING"
    self.arrived_at_distraction = False
    self.state_timer = 0.0
    self.path = []
    self.current_goal = None

  def update(self, player, dt, obstacles=None):
    self.state_timer += dt

    # 1. Finite State Machine
    if self.state == "PACING":
      self.x = self.home_x  # Lock guard to their designated patrol lane
      step_z = self.walk_speed * self.patrol_dir * dt
      new_z = self.z + step_z

      # Reverse patrol direction if approaching bounds
      if new_z > self.patrol_z_max:
        self.patrol_dir = -1.0
        self.target_yaw = 180.0
      elif new_z < self.patrol_z_min:
        self.patrol_dir = 1.0
        self.target_yaw = 0.0
      else:
        # Collision safety check against obstacles (3D height-aware)
        blocked = False
        if obstacles:
          r = self.collision_radius
          for obs in obstacles:
            obs_ymin = obs[4] if len(obs) >= 6 else 0.0
            obs_ymax = obs[5] if len(obs) >= 6 else 2.5
            if self.y >= obs_ymax - 0.05 or (self.y + 1.9) <= obs_ymin + 0.05:
              continue
            if (obs[0] - r <= self.home_x <= obs[1] + r) and (obs[2] - r <= new_z <= obs[3] + r):
              blocked = True
              break
        if not blocked:
          self.z = new_z
        else:
          self.patrol_dir *= -1.0
          self.target_yaw = 0.0 if self.patrol_dir > 0 else 180.0

      self.walk_cycle += self.walk_speed * dt * 5.5
      self.pose = walk_animation(self.walk_cycle)
      self.rotate_towards(self.target_yaw, dt)

      if self.state_timer > self.pacing_duration:
        self.state = "WALKING_TO_WALL"
        self.state_timer = 0.0

    elif self.state == "WALKING_TO_WALL":
      wx, wz = self.wall_pos
      # A* pathfinding around columns, barrels, and server racks to reach the wall
      if self.navigate_towards(wx, wz, dt, obstacles=obstacles, stop_dist=0.15):
        self.target_yaw = self.wall_yaw
        self.state = "LEANING"
        self.state_timer = 0.0

    elif self.state == "LEANING":
      self.rotate_towards(self.target_yaw, dt)
      self.pose = inspect_weapon_animation(self.state_timer, self.lean_duration)

      if self.state_timer > self.lean_duration:
        self.state = "WALKING_TO_PATROL"
        self.state_timer = 0.0

    elif self.state == "WALKING_TO_PATROL":
      target_z = max(self.patrol_z_min, min(self.patrol_z_max, self.z))
      # A* pathfinding back to the patrol line avoiding all obstacles
      if self.navigate_towards(self.home_x, target_z, dt, obstacles=obstacles, stop_dist=0.15):
        self.target_yaw = 0.0 if self.patrol_dir > 0 else 180.0
        self.state = "PACING"
        self.state_timer = 0.0

    elif self.state == "INVESTIGATING":
      if self.investigate_target:
        tx, tz = self.investigate_target
        if not self.arrived_at_distraction:
          # A* pathfinding around the central monolith/columns to the vending machine
          if self.navigate_towards(tx, tz, dt, obstacles=obstacles, stop_dist=0.25):
            self.arrived_at_distraction = True
            self.state_timer = 0.0  # Reset timer to zero upon arrival!
            self.target_yaw = 180.0  # Face the vending machine
        else:
          # Arrived in front of distraction: inspect for at least 15 seconds
          scan_turn = math.sin(self.state_timer * 1.5) * 35.0
          self.rotate_towards(self.target_yaw + scan_turn, dt)

          # Inspecting pose: tilt head slightly downward to inspect sparks/soda dispenser
          head_pitch = 12.0 + math.sin(self.state_timer * 2.0) * 6.0
          head_yaw = math.sin(self.state_timer * 1.5) * 20.0
          self.pose = HumanoidPose(head_pitch=head_pitch, head_yaw=head_yaw)

          if self.state_timer >= self.investigate_duration:
            self.state = "WALKING_TO_PATROL"
            self.state_timer = 0.0
            self.investigate_target = None
            self.arrived_at_distraction = False
      else:
        self.state = "WALKING_TO_PATROL"
        self.state_timer = 0.0
        self.arrived_at_distraction = False

    # 2. Vision & Stealth Detection
    if self.pose.head_pitch > 20.0:
      max_range, fov = 1.8, 30.0  # Engrossed in gun
    else:
      max_range, fov = 5.2, 55.0  # Active room scan

    player_y = getattr(player, "y", 0.0)
    spotted = self.can_see_target(
        player.x,
        player.z,
        max_range=max_range,
        fov_angle=fov,
        obstacles=obstacles,
        target_y=player_y,
    )

    if spotted:
      rate = 45.0 if not player.crouching else 12.0
      player.stealth_meter = min(100.0, player.stealth_meter + rate * dt)
      player.spotted_this_frame = True
    else:
      if not getattr(player, "spotted_this_frame", False):
        player.stealth_meter = max(0.0, player.stealth_meter - 30.0 * dt)