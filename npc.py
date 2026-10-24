import math
from animation import HumanoidPose, line_intersects_box, walk_animation
from model import HumanoidModel
from OpenGL.GL import *


class BaseNPC:
  """Base spatial entity providing navigation, turning, vision, and rendering."""

  def __init__(
      self,
      x: float,
      y: float,
      z: float,
      model: HumanoidModel,
      walk_speed: float = 1.2,
      turn_speed: float = 220.0,
  ):
    self.base_x, self.base_y, self.base_z = x, y, z
    self.x, self.y, self.z = x, y, z
    self.yaw = 0.0
    self.target_yaw = 0.0
    self.walk_speed = walk_speed
    self.turn_speed = turn_speed
    self.walk_cycle = 0.0

    self.model = model
    self.pose = HumanoidPose()

  def reset(self):
    self.x, self.y, self.z = self.base_x, self.base_y, self.base_z
    self.yaw = 0.0
    self.target_yaw = 0.0
    self.walk_cycle = 0.0
    self.pose = HumanoidPose()

  def rotate_towards(self, target_yaw: float, dt: float) -> bool:
    """Smoothly interpolates yaw toward target_yaw. Returns True when facing target."""
    diff = ((target_yaw - self.yaw + 180.0) % 360.0) - 180.0
    step = self.turn_speed * dt
    if abs(diff) <= step:
      self.yaw = target_yaw
      return True
    self.yaw += math.copysign(step, diff)
    return False

  def move_towards(
      self, target_x: float, target_z: float, dt: float, stop_dist: float = 0.05
  ) -> bool:
    """Steers and walks toward (target_x, target_z). Returns True when arrived."""
    dx = target_x - self.x
    dz = target_z - self.z
    dist = math.hypot(dx, dz)
    if dist <= stop_dist:
      return True

    self.target_yaw = math.degrees(math.atan2(dx, dz))
    self.rotate_towards(self.target_yaw, dt)

    vx, vz = dx / dist, dz / dist
    self.x += vx * self.walk_speed * dt
    self.z += vz * self.walk_speed * dt

    self.walk_cycle += self.walk_speed * dt * 5.5
    self.pose = walk_animation(self.walk_cycle)
    return False

  def can_see_target(
      self,
      target_x: float,
      target_z: float,
      max_range: float = 5.2,
      fov_angle: float = 55.0,
      obstacles: list = None,
  ) -> bool:
    """Checks distance, FOV cone, and obstacle raycast occlusion."""
    dist = math.hypot(target_x - self.x, target_z - self.z)
    if dist > max_range:
      return False

    effective_gaze = self.yaw + self.pose.head_yaw
    dx = target_x - self.x
    dz = target_z - self.z
    angle_to_target = math.degrees(math.atan2(dx, dz))
    angle_diff = ((angle_to_target - effective_gaze + 180.0) % 360.0) - 180.0

    if abs(angle_diff) > fov_angle:
      return False

    if obstacles:
      for obs in obstacles:
        if line_intersects_box(self.x, self.z, target_x, target_z, obs):
          return False

    return True

  def draw(self):
    """Positions the NPC in world space and delegates drawing to the model."""
    glPushMatrix()
    glTranslatef(self.x, self.y, self.z)
    glRotatef(self.yaw, 0, 1, 0)
    self.model.draw(self.pose)
    glPopMatrix()