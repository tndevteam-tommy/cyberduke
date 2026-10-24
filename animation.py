from dataclasses import dataclass, field
import math


def smoothstep(edge0, edge1, x):
  t = max(0.0, min(1.0, (x - edge0) / (edge1 - edge0)))
  return t * t * (3.0 - 2.0 * t)


def lerp(a, b, u):
  return a + (b - a) * u


def line_intersects_box(x1, z1, x2, z2, box):
  """Slab intersection test for 2D line segment vs AABB."""
  xmin, xmax, zmin, zmax = box
  if (max(x1, x2) < xmin or min(x1, x2) > xmax or
      max(z1, z2) < zmin or min(z1, z2) > zmax):
    return False

  dx = x2 - x1
  dz = z2 - z1
  tmin, tmax = 0.0, 1.0

  if abs(dx) < 1e-6:
    if x1 < xmin or x1 > xmax:
      return False
  else:
    tx1 = (xmin - x1) / dx
    tx2 = (xmax - x1) / dx
    tmin = max(tmin, min(tx1, tx2))
    tmax = min(tmax, max(tx1, tx2))
    if tmin > tmax:
      return False

  if abs(dz) < 1e-6:
    if z1 < zmin or z1 > zmax:
      return False
  else:
    tz1 = (zmin - z1) / dz
    tz2 = (zmax - z1) / dz
    tmin = max(tmin, min(tz1, tz2))
    tmax = min(tmax, max(tz1, tz2))
    if tmin > tmax:
      return False

  return tmin <= tmax and tmax >= 0.0 and tmin <= 1.0


@dataclass
class HumanoidPose:
  """Holds skeletal rotation angles and translations for any humanoid character."""
  bob: float = 0.0

  # Head rotations (degrees)
  head_pitch: float = 0.0
  head_yaw: float = 0.0
  head_roll: float = 0.0

  # Left Arm: [pitch, yaw, roll, elbow]
  arm_l: list = field(default_factory=lambda: [0.0, 0.0, 0.0, -15.0])
  # Right Arm: [pitch, yaw, roll, elbow]
  arm_r: list = field(default_factory=lambda: [0.0, 0.0, 0.0, -15.0])

  # Left Leg: [hip_pitch, hip_yaw, knee_bend]
  leg_l: list = field(default_factory=lambda: [0.0, 0.0, 0.0])
  # Right Leg: [hip_pitch, hip_yaw, knee_bend]
  leg_r: list = field(default_factory=lambda: [0.0, 0.0, 0.0])

  # Attached Prop (weapon, datapad, tool)
  has_prop: bool = False
  prop_pos: list = field(default_factory=lambda: [0.0, 0.0, 0.0])
  prop_rot: list = field(default_factory=lambda: [0.0, 0.0, 0.0])

  def lerp(self, target: "HumanoidPose", t: float) -> "HumanoidPose":
    """Smoothly blends this pose into another pose."""
    t = max(0.0, min(1.0, t))
    l_val = lambda a, b: a + (b - a) * t
    l_lst = lambda la, lb: [l_val(a, b) for a, b in zip(la, lb)]

    return HumanoidPose(
        bob=l_val(self.bob, target.bob),
        head_pitch=l_val(self.head_pitch, target.head_pitch),
        head_yaw=l_val(self.head_yaw, target.head_yaw),
        head_roll=l_val(self.head_roll, target.head_roll),
        arm_l=l_lst(self.arm_l, target.arm_l),
        arm_r=l_lst(self.arm_r, target.arm_r),
        leg_l=l_lst(self.leg_l, target.leg_l),
        leg_r=l_lst(self.leg_r, target.leg_r),
        has_prop=target.has_prop,
        prop_pos=l_lst(self.prop_pos, target.prop_pos),
        prop_rot=l_lst(self.prop_rot, target.prop_rot),
    )


# ---------------------------------------------------------------------------
# GLOBAL REUSABLE ANIMATION GENERATORS
# ---------------------------------------------------------------------------

def walk_animation(cycle: float, arm_swing_scale: float = 1.0, prop_holstered: bool = True) -> HumanoidPose:
  """Universal humanoid walk cycle shared across guards, civilians, and thugs."""
  sin_l = math.sin(cycle)
  sin_r = math.sin(cycle + math.pi)

  hip_l = sin_l * 18.0
  hip_r = sin_r * 18.0
  knee_l = (sin_l * 38.0) if sin_l > 0 else (-sin_l * 15.0)
  knee_r = (sin_r * 38.0) if sin_r > 0 else (-sin_r * 15.0)
  bob = abs(math.sin(cycle * 2.0)) * 0.025
  arm_swing = sin_l * 16.0 * arm_swing_scale

  elbow_l = -(15.0 + abs(math.sin(cycle)) * 20.0)
  elbow_r = -(15.0 + abs(math.sin(cycle + math.pi)) * 20.0)

  prop_pos = [-0.28, 0.98, 0.0] if prop_holstered else [0.0, 0.0, 0.0]
  prop_rot = [80.0, 0.0, 0.0] if prop_holstered else [0.0, 0.0, 0.0]

  return HumanoidPose(
      bob=bob,
      arm_l=[arm_swing, 0.0, 0.0, elbow_l],
      arm_r=[-arm_swing, 0.0, 0.0, elbow_r],
      leg_l=[hip_l, 0.0, max(0.0, knee_l)],
      leg_r=[hip_r, 0.0, max(0.0, knee_r)],
      has_prop=prop_holstered,
      prop_pos=prop_pos,
      prop_rot=prop_rot,
  )


def idle_stand_animation(t: float, breathing_speed: float = 1.8) -> HumanoidPose:
  """Universal idle standing animation with gentle breathing."""
  bob = math.sin(t * breathing_speed) * 0.005
  elbow = -15.0 + math.sin(t * breathing_speed) * 2.0
  return HumanoidPose(
      bob=bob,
      arm_l=[0.0, 0.0, 0.0, elbow],
      arm_r=[0.0, 0.0, 0.0, elbow],
      leg_l=[0.0, 0.0, 0.0],
      leg_r=[0.0, 0.0, 0.0],
      has_prop=True,
      prop_pos=[-0.28, 0.98, 0.0],
      prop_rot=[80.0, 0.0, 0.0],
  )


def inspect_weapon_animation(t: float, total_duration: float = 15.0) -> HumanoidPose:
  """Guard-specific wall lean & 5-phase weapon inspection routine."""
  leg_l = [0.0, 0.0, 0.0]
  leg_r = [14.0, 0.0, 12.0]

  arm_rest_l = [0.0, 0.0, 0.0, -15.0]
  arm_rest_r = [0.0, 0.0, 0.0, -15.0]
  arm_holster_r = [0.0, 3.0, 5.0, -20.0]

  arm_hold_l = [-8.0, -32.0, 5.0, -98.0]
  arm_hold_r = [0.0, 15.0, 25.0, -95.0]

  pos_holster = [-0.28, 0.98, 0.0]
  pos_chest = [-0.02, 1.28, 0.35]

  rot_holster = [80.0, 0.0, 0.0]
  rot_chest = [10.0, 75.0, 25.0]  # Observed long-ways on its side

  head_pitch, head_yaw = 0.0, 0.0

  if t < 0.5:
    u = smoothstep(0.0, 0.5, t)
    ar = [lerp(arm_rest_r[i], arm_holster_r[i], u) for i in range(4)]
    al = list(arm_rest_l)
    gun_pos = list(pos_holster)
    gun_rot = list(rot_holster)
    head_pitch = 25.0 * u
    head_yaw = -20.0 * u

  elif t < 2.0:
    u = smoothstep(0.5, 2.0, t)
    y_arc = math.sin(u * math.pi) * 0.08
    gun_pos = [lerp(pos_holster[i], pos_chest[i], u) for i in range(3)]
    gun_pos[1] += y_arc
    gun_rot = [lerp(rot_holster[i], rot_chest[i], u) for i in range(3)]

    ar = [lerp(arm_holster_r[i], arm_hold_r[i], u) for i in range(4)]
    u_l = smoothstep(0.8, 2.0, t)
    al = [lerp(arm_rest_l[i], arm_hold_l[i], u_l) for i in range(4)]

    head_pitch = 25.0 + (32.0 - 25.0) * u
    head_yaw = -20.0 * (1.0 - u)

  elif t < 6.5:
    cycle = (t - 2.0) * 1.6
    tilt = math.sin(cycle) * 8.0
    gun_pos = list(pos_chest)
    gun_rot = [rot_chest[0] + math.cos(cycle) * 3.0, rot_chest[1] + math.sin(cycle) * 5.0, rot_chest[2] + tilt]

    ar = [arm_hold_r[0], arm_hold_r[1], arm_hold_r[2], arm_hold_r[3] + tilt * 0.3]
    al = [arm_hold_l[0], arm_hold_l[1], arm_hold_l[2], arm_hold_l[3] - tilt * 0.3]
    head_pitch = 30.0 + math.sin(cycle) * 3.0
    head_yaw = math.sin(cycle) * 7.0

  elif t < 10.5:
    scan_t = t - 6.5
    if scan_t < 0.8:
      u = smoothstep(0.0, 0.8, scan_t)
      head_pitch = 30.0 * (1.0 - u)
      head_yaw = -40.0 * u
    elif scan_t < 2.4:
      u = smoothstep(0.8, 2.4, scan_t)
      head_pitch = 0.0
      head_yaw = -40.0 + 80.0 * u
    elif scan_t < 3.5:
      u = smoothstep(2.4, 3.5, scan_t)
      head_pitch = 0.0
      head_yaw = 40.0 - 40.0 * u
    else:
      head_pitch, head_yaw = 0.0, 0.0

    gun_pos = list(pos_chest)
    gun_rot = list(rot_chest)
    ar = list(arm_hold_r)
    al = list(arm_hold_l)

  elif t < 12.8:
    u = smoothstep(10.5, 11.2, t)
    cycle = (t - 10.5) * 2.0
    tilt = math.sin(cycle) * 6.0
    gun_pos = list(pos_chest)
    gun_rot = [rot_chest[0], rot_chest[1] + math.sin(cycle) * 4.0, rot_chest[2] + tilt]
    ar = [arm_hold_r[0], arm_hold_r[1], arm_hold_r[2], arm_hold_r[3] + tilt * 0.3]
    al = [arm_hold_l[0], arm_hold_l[1], arm_hold_l[2], arm_hold_l[3] - tilt * 0.3]
    head_pitch = 32.0 * u
    head_yaw = math.sin(cycle) * 5.0

  else:
    u = smoothstep(12.8, 14.6, t)
    gun_pos = [lerp(pos_chest[i], pos_holster[i], u) for i in range(3)]
    gun_rot = [lerp(rot_chest[i], rot_holster[i], u) for i in range(3)]

    u_l = smoothstep(12.8, 13.8, t)
    al = [lerp(arm_hold_l[i], arm_rest_l[i], u_l) for i in range(4)]
    ar = [lerp(arm_hold_r[i], arm_holster_r[i], u) for i in range(4)]

    head_pitch = 32.0 + (20.0 - 32.0) * u
    head_yaw = -20.0 * u

    if t > 14.6:
      u_fin = smoothstep(14.6, 15.0, t)
      ar = [lerp(arm_holster_r[i], arm_rest_r[i], u_fin) for i in range(4)]
      head_pitch = 20.0 * (1.0 - u_fin)
      head_yaw = -20.0 * (1.0 - u_fin)

  return HumanoidPose(
      bob=0.0,
      head_pitch=head_pitch,
      head_yaw=head_yaw,
      arm_l=al,
      arm_r=ar,
      leg_l=leg_l,
      leg_r=leg_r,
      has_prop=True,
      prop_pos=gun_pos,
      prop_rot=gun_rot,
  )