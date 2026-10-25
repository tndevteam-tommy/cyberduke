import heapq
import math
from animation import HumanoidPose, line_intersects_aabb, line_intersects_box, walk_animation
from model import HumanoidModel
from OpenGL.GL import *


class Pathfinder:
  """2D A* pathfinder with line-of-sight path smoothing (string-pulling)."""

  def __init__(self, grid_size: float = 0.4, agent_radius: float = 0.35):
    self.grid_size = grid_size
    self.agent_radius = agent_radius

  def _to_grid(self, x: float, z: float):
    return int(round(x / self.grid_size)), int(round(z / self.grid_size))

  def _to_world(self, gx: int, gz: int):
    return gx * self.grid_size, gz * self.grid_size

  def is_blocked(self, x: float, z: float, obstacles: list, agent_y: float = 0.0) -> bool:
    r = self.agent_radius
    agent_feet = agent_y
    agent_top = agent_y + 1.9
    for obs in obstacles:
      obs_ymin = obs[4] if len(obs) >= 6 else 0.0
      obs_ymax = obs[5] if len(obs) >= 6 else 2.5
      if agent_feet >= obs_ymax - 0.05 or agent_top <= obs_ymin + 0.05:
        continue
      if (obs[0] - r <= x <= obs[1] + r) and (obs[2] - r <= z <= obs[3] + r):
        return True
    return False

  def line_clear(self, x1: float, z1: float, x2: float, z2: float, obstacles: list, agent_y: float = 0.0) -> bool:
    r = self.agent_radius
    agent_feet = agent_y
    agent_top = agent_y + 1.9
    for obs in obstacles:
      obs_ymin = obs[4] if len(obs) >= 6 else 0.0
      obs_ymax = obs[5] if len(obs) >= 6 else 2.5
      if agent_feet >= obs_ymax - 0.05 or agent_top <= obs_ymin + 0.05:
        continue
      inflated = (obs[0] - r, obs[1] + r, obs[2] - r, obs[3] + r)
      if line_intersects_box(x1, z1, x2, z2, inflated[:4]):
        return False
    return True

  def find_path(
      self,
      start_x: float,
      start_z: float,
      goal_x: float,
      goal_z: float,
      obstacles: list,
      agent_y: float = 0.0,
      bounds: tuple = (-11.0, 11.0, -11.0, 43.0),
  ) -> list:
    """Finds a collision-free smoothed path from (start_x, start_z) to (goal_x, goal_z)."""
    if not obstacles or self.line_clear(start_x, start_z, goal_x, goal_z, obstacles, agent_y=agent_y):
      return [(goal_x, goal_z)]

    sgx, sgz = self._to_grid(start_x, start_z)
    egx, egz = self._to_grid(goal_x, goal_z)

    min_gx, min_gz = self._to_grid(bounds[0], bounds[2])
    max_gx, max_gz = self._to_grid(bounds[1], bounds[3])

    target_cell = (egx, egz)
    wx, wz = self._to_world(egx, egz)
    if self.is_blocked(wx, wz, obstacles, agent_y=agent_y):
      best_d = float('inf')
      best_cell = None
      for dx in range(-3, 4):
        for dz in range(-3, 4):
          cand_x, cand_z = self._to_world(egx + dx, egz + dz)
          if not self.is_blocked(cand_x, cand_z, obstacles, agent_y=agent_y):
            d = math.hypot(cand_x - goal_x, cand_z - goal_z)
            if d < best_d:
              best_d = d
              best_cell = (egx + dx, egz + dz)
      if best_cell:
        target_cell = best_cell

    open_set = []
    heapq.heappush(open_set, (0.0, (sgx, sgz)))
    came_from = {}
    g_score = {(sgx, sgz): 0.0}

    neighbors = [
        (1, 0, 1.0), (-1, 0, 1.0), (0, 1, 1.0), (0, -1, 1.0),
        (1, 1, 1.414), (1, -1, 1.414), (-1, 1, 1.414), (-1, -1, 1.414)
    ]

    found = False
    iterations = 0
    max_iterations = 800

    while open_set and iterations < max_iterations:
      iterations += 1
      _, current = heapq.heappop(open_set)

      if current == target_cell:
        found = True
        break

      for dx, dz, cost in neighbors:
        nx, nz = current[0] + dx, current[1] + dz
        if not (min_gx <= nx <= max_gx and min_gz <= nz <= max_gz):
          continue

        n_wx, n_wz = self._to_world(nx, nz)
        if self.is_blocked(n_wx, n_wz, obstacles, agent_y=agent_y):
          continue

        tentative_g = g_score[current] + cost * self.grid_size
        neighbor = (nx, nz)

        if neighbor not in g_score or tentative_g < g_score[neighbor]:
          came_from[neighbor] = current
          g_score[neighbor] = tentative_g
          h = math.hypot(nx - target_cell[0], nz - target_cell[1]) * self.grid_size
          heapq.heappush(open_set, (tentative_g + h, neighbor))

    if not found:
      return [(goal_x, goal_z)]

    raw_path = []
    curr = target_cell
    while curr in came_from:
      raw_path.append(self._to_world(curr[0], curr[1]))
      curr = came_from[curr]
    raw_path.reverse()
    raw_path.append((goal_x, goal_z))

    smoothed = []
    curr_x, curr_z = start_x, start_z
    i = 0
    while i < len(raw_path):
      furthest = i
      for j in range(len(raw_path) - 1, i, -1):
        if self.line_clear(curr_x, curr_z, raw_path[j][0], raw_path[j][1], obstacles, agent_y=agent_y):
          furthest = j
          break
      smoothed.append(raw_path[furthest])
      curr_x, curr_z = raw_path[furthest][0], raw_path[furthest][1]
      i = furthest + 1

    return smoothed


class BaseNPC:
  """Base spatial entity providing navigation, A* pathfinding, turning, vision, and rendering."""

  def __init__(
      self,
      x: float,
      y: float,
      z: float,
      model: HumanoidModel,
      walk_speed: float = 1.2,
      turn_speed: float = 220.0,
      collision_radius: float = 0.35,
  ):
    self.base_x, self.base_y, self.base_z = x, y, z
    self.x, self.y, self.z = x, y, z
    self.yaw = 0.0
    self.target_yaw = 0.0
    self.walk_speed = walk_speed
    self.turn_speed = turn_speed
    self.collision_radius = collision_radius
    self.walk_cycle = 0.0

    self.path = []
    self.current_goal = None
    self.pathfinder = Pathfinder(grid_size=0.4, agent_radius=collision_radius)

    self.model = model
    self.pose = HumanoidPose()

  def reset(self):
    self.x, self.y, self.z = self.base_x, self.base_y, self.base_z
    self.yaw = 0.0
    self.target_yaw = 0.0
    self.walk_cycle = 0.0
    self.path = []
    self.current_goal = None
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
    """Steers and walks directly toward (target_x, target_z). Returns True when arrived."""
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

  def navigate_towards(
      self,
      target_x: float,
      target_z: float,
      dt: float,
      obstacles: list = None,
      stop_dist: float = 0.15,
  ) -> bool:
    """Navigates toward (target_x, target_z) using 3D A* pathfinding and physical obstacle avoidance."""
    dist_to_goal = math.hypot(target_x - self.x, target_z - self.z)
    if dist_to_goal <= stop_dist:
      self.path = []
      self.current_goal = None
      return True

    goal_key = (round(target_x, 2), round(target_z, 2))

    need_replan = (self.current_goal != goal_key) or not self.path
    if not need_replan and obstacles and self.path:
      wp = self.path[0]
      if not self.pathfinder.line_clear(self.x, self.z, wp[0], wp[1], obstacles, agent_y=self.y):
        need_replan = True

    if need_replan and obstacles:
      self.path = self.pathfinder.find_path(self.x, self.z, target_x, target_z, obstacles, agent_y=self.y)
      self.current_goal = goal_key

    if not self.path:
      self.path = [(target_x, target_z)]

    while self.path:
      wx, wz = self.path[0]
      d = math.hypot(wx - self.x, wz - self.z)
      if d <= stop_dist:
        self.path.pop(0)
      else:
        break

    if not self.path:
      return True

    tx, tz = self.path[0]
    dx = tx - self.x
    dz = tz - self.z
    d = math.hypot(dx, dz)
    if d <= 0.001:
      return True

    self.target_yaw = math.degrees(math.atan2(dx, dz))
    self.rotate_towards(self.target_yaw, dt)

    move_step = min(d, self.walk_speed * dt)
    vx = (dx / d) * move_step
    vz = (dz / d) * move_step

    new_x = self.x + vx
    new_z = self.z + vz

    # Physical collision avoidance with obstacle sliding (3D height-aware)
    if obstacles:
      collided_x = False
      collided_z = False
      r = self.collision_radius
      npc_feet = self.y
      npc_top = self.y + 1.9

      for obs in obstacles:
        obs_ymin = obs[4] if len(obs) >= 6 else 0.0
        obs_ymax = obs[5] if len(obs) >= 6 else 2.5
        if npc_feet >= obs_ymax - 0.05 or npc_top <= obs_ymin + 0.05:
          continue

        if (obs[0] - r <= new_x <= obs[1] + r) and (obs[2] - r <= self.z <= obs[3] + r):
          collided_x = True
        if (obs[0] - r <= self.x <= obs[1] + r) and (obs[2] - r <= new_z <= obs[3] + r):
          collided_z = True

      if not collided_x:
        self.x = new_x
      if not collided_z:
        self.z = new_z
    else:
      self.x = new_x
      self.z = new_z

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
      target_y: float = None,
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
      if target_y is not None:
        p1 = (self.x, self.y + 1.5, self.z)
        p2 = (target_x, target_y + 1.2, target_z)
        for obs in obstacles:
          # Handrails / catwalk railing barriers do not occlude line of sight
          if len(obs) >= 6 and abs(obs[5] - 3.70) < 1e-3:
            continue
          if line_intersects_aabb(p1, p2, obs):
            return False
      else:
        for obs in obstacles:
          # Handrails / catwalk railing barriers do not occlude line of sight
          if len(obs) >= 6 and abs(obs[5] - 3.70) < 1e-3:
            continue
          if line_intersects_box(self.x, self.z, target_x, target_z, obs[:4]):
            return False

    return True

  def draw(self):
    """Positions the NPC in world space and delegates drawing to the model."""
    glPushMatrix()
    glTranslatef(self.x, self.y, self.z)
    glRotatef(self.yaw, 0, 1, 0)
    self.model.draw(self.pose)
    glPopMatrix()