import math
from OpenGL.GL import *


def draw_cube(tex_id=None):
  if tex_id:
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, tex_id)
  else:
    glDisable(GL_TEXTURE_2D)

  glBegin(GL_QUADS)
  # Front (+Z)
  glNormal3f(0.0, 0.0, 1.0)
  glTexCoord2f(0, 0); glVertex3f(-0.5, -0.5, 0.5)
  glTexCoord2f(1, 0); glVertex3f(0.5, -0.5, 0.5)
  glTexCoord2f(1, 1); glVertex3f(0.5, 0.5, 0.5)
  glTexCoord2f(0, 1); glVertex3f(-0.5, 0.5, 0.5)

  # Back (-Z)
  glNormal3f(0.0, 0.0, -1.0)
  glTexCoord2f(0, 0); glVertex3f(0.5, -0.5, -0.5)
  glTexCoord2f(1, 0); glVertex3f(-0.5, -0.5, -0.5)
  glTexCoord2f(1, 1); glVertex3f(-0.5, 0.5, -0.5)
  glTexCoord2f(0, 1); glVertex3f(0.5, 0.5, -0.5)

  # Top (+Y)
  glNormal3f(0.0, 1.0, 0.0)
  glTexCoord2f(0, 0); glVertex3f(-0.5, 0.5, -0.5)
  glTexCoord2f(1, 0); glVertex3f(0.5, 0.5, -0.5)
  glTexCoord2f(1, 1); glVertex3f(0.5, 0.5, 0.5)
  glTexCoord2f(0, 1); glVertex3f(-0.5, 0.5, 0.5)

  # Bottom (-Y)
  glNormal3f(0.0, -1.0, 0.0)
  glTexCoord2f(0, 0); glVertex3f(-0.5, -0.5, 0.5)
  glTexCoord2f(1, 0); glVertex3f(0.5, -0.5, 0.5)
  glTexCoord2f(1, 1); glVertex3f(0.5, -0.5, -0.5)
  glTexCoord2f(0, 1); glVertex3f(-0.5, -0.5, -0.5)

  # Right (+X)
  glNormal3f(1.0, 0.0, 0.0)
  glTexCoord2f(0, 0); glVertex3f(0.5, -0.5, 0.5)
  glTexCoord2f(1, 0); glVertex3f(0.5, -0.5, -0.5)
  glTexCoord2f(1, 1); glVertex3f(0.5, 0.5, -0.5)
  glTexCoord2f(0, 1); glVertex3f(0.5, 0.5, 0.5)

  # Left (-X)
  glNormal3f(-1.0, 0.0, 0.0)
  glTexCoord2f(0, 0); glVertex3f(-0.5, -0.5, -0.5)
  glTexCoord2f(1, 0); glVertex3f(-0.5, -0.5, 0.5)
  glTexCoord2f(1, 1); glVertex3f(-0.5, 0.5, 0.5)
  glTexCoord2f(0, 1); glVertex3f(-0.5, 0.5, -0.5)
  glEnd()
  glDisable(GL_TEXTURE_2D)


def draw_cylinder(r_bot, r_top, h, slices=10, tex_id=None):
  """Draws a vertical cylinder or truncated cone from y=0 to y=h."""
  if tex_id:
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, tex_id)
  else:
    glDisable(GL_TEXTURE_2D)

  # Side quads
  glBegin(GL_QUADS)
  for i in range(slices):
    u1 = i / slices
    u2 = (i + 1) / slices
    th1 = 2.0 * math.pi * u1
    th2 = 2.0 * math.pi * u2

    c1, s1 = math.cos(th1), math.sin(th1)
    c2, s2 = math.cos(th2), math.sin(th2)

    glNormal3f(c1, 0.0, s1)
    glTexCoord2f(u1, 0.0); glVertex3f(r_bot * c1, 0.0, r_bot * s1)
    glNormal3f(c2, 0.0, s2)
    glTexCoord2f(u2, 0.0); glVertex3f(r_bot * c2, 0.0, r_bot * s2)
    glTexCoord2f(u2, 1.0); glVertex3f(r_top * c2, h,   r_top * s2)
    glNormal3f(c1, 0.0, s1)
    glTexCoord2f(u1, 1.0); glVertex3f(r_top * c1, h,   r_top * s1)
  glEnd()

  # Bottom cap
  glBegin(GL_TRIANGLE_FAN)
  glNormal3f(0.0, -1.0, 0.0)
  glTexCoord2f(0.5, 0.5); glVertex3f(0.0, 0.0, 0.0)
  for i in range(slices + 1):
    th = -2.0 * math.pi * i / slices
    c, s = math.cos(th), math.sin(th)
    glTexCoord2f(0.5 + 0.5 * c, 0.5 + 0.5 * s)
    glVertex3f(r_bot * c, 0.0, r_bot * s)
  glEnd()

  # Top cap
  glBegin(GL_TRIANGLE_FAN)
  glNormal3f(0.0, 1.0, 0.0)
  glTexCoord2f(0.5, 0.5); glVertex3f(0.0, h, 0.0)
  for i in range(slices + 1):
    th = 2.0 * math.pi * i / slices
    c, s = math.cos(th), math.sin(th)
    glTexCoord2f(0.5 + 0.5 * c, 0.5 + 0.5 * s)
    glVertex3f(r_top * c, h, r_top * s)
  glEnd()
  glDisable(GL_TEXTURE_2D)


class Player:

  def __init__(self):
    self.reset()

  def reset(self):
    self.x, self.y, self.z = 0.0, 1.6, 6.0
    self.yaw = -90.0
    self.pitch = 0.0
    self.crouching = False
    self.stealth_meter = 0.0
    self.on_catwalk = False
    self.ramp_climbing = False

  def update_height(self, dt, floor_y=0.0):
    target_y = floor_y + (1.0 if self.crouching else 1.6)
    self.y += (target_y - self.y) * 10.0 * dt


class Terminal:
  """High-tech grounded Netrunner Workstation with triple curved monitors,

  ground-planted steel legs, under-desk tower PC, cable bundles, and netrunner chair.
  """

  def __init__(self, x, y, z, tex_metal, tex_locked, tex_unlocked, textures=None, yaw=0.0):
    self.x = x
    # If legacy y=0.9 offset was passed, ground cleanly to y=0.0
    self.y = 0.0 if abs(y - 0.9) < 0.1 else y
    self.z = z
    self.yaw = yaw
    self.tex_metal = tex_metal
    self.tex_locked = tex_locked
    self.tex_unlocked = tex_unlocked
    self.textures = textures or {}
    self.progress = 0.0
    self.is_hacked = False
    self.anim_time = 0.0

  def reset(self):
    self.progress = 0.0
    self.is_hacked = False
    self.anim_time = 0.0

  def get_bounds(self):
    # Returns (min_x, max_x, min_z, max_z, min_y, max_y)
    ymin = self.y
    ymax = self.y + 1.85
    if abs(self.yaw - 180.0) < 1.0:
      return (self.x - 1.4, self.x + 1.4, self.z - 0.9, self.z + 0.7, ymin, ymax)
    elif abs(self.yaw) < 1.0:
      return (self.x - 1.4, self.x + 1.4, self.z - 0.7, self.z + 0.9, ymin, ymax)
    else:
      rad = math.radians(self.yaw)
      cos_y = math.cos(rad)
      sin_y = math.sin(rad)
      corners = [(-1.4, -0.7), (1.4, -0.7), (1.4, 0.9), (-1.4, 0.9)]
      xs = [self.x + (lx * cos_y - lz * sin_y) for lx, lz in corners]
      zs = [self.z + (lx * sin_y + lz * cos_y) for lx, lz in corners]
      return (min(xs), max(xs), min(zs), max(zs), ymin, ymax)

  def update(self, player_x, player_z, is_e_pressed, dt):
    self.anim_time += dt
    dist = math.hypot(player_x - self.x, player_z - self.z)
    if dist < 2.5 and is_e_pressed and not self.is_hacked:
      self.progress = min(100.0, self.progress + 40.0 * dt)
      if self.progress >= 100.0:
        self.is_hacked = True
    else:
      if not self.is_hacked:
        self.progress = max(0.0, self.progress - 20.0 * dt)

  def draw(self):
    glPushMatrix()
    glTranslatef(self.x, self.y, self.z)
    if self.yaw != 0.0:
      glRotatef(self.yaw, 0, 1, 0)

    no_emission = [0.0, 0.0, 0.0, 1.0]
    tex_screen_net = self.textures.get("screen_net", self.tex_metal)
    tex_screen_radar = self.textures.get("screen_radar", self.tex_metal)
    tex_soda = self.textures.get("soda_can", self.tex_metal)
    tex_leather = self.textures.get("leather", self.tex_metal)

    # -----------------------------------------------------------------------
    # 1. GROUNDED STEEL DESK FRAME & LEGS (Touching y=0.0)
    # -----------------------------------------------------------------------
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [0.5, 0.5, 0.6, 1.0])
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 32.0)
    glColor3f(0.22, 0.24, 0.28)

    # Left & Right Foot Plates directly on floor
    for leg_x in [-1.15, 1.15]:
      # Floor foot skid
      glPushMatrix()
      glTranslatef(leg_x, 0.02, 0.0)
      glScalef(0.16, 0.04, 0.90)
      draw_cube(self.tex_metal)
      glPopMatrix()

      # Main vertical support column
      glPushMatrix()
      glTranslatef(leg_x, 0.43, -0.12)
      glScalef(0.08, 0.78, 0.08)
      draw_cube(self.tex_metal)
      glPopMatrix()

      # Diagonal rear brace
      glPushMatrix()
      glTranslatef(leg_x, 0.40, -0.28)
      glRotatef(-22, 1, 0, 0)
      glScalef(0.06, 0.75, 0.06)
      draw_cube(self.tex_metal)
      glPopMatrix()

    # Rear lower crossbar stretcher
    glPushMatrix()
    glTranslatef(0.0, 0.22, -0.32)
    glScalef(2.22, 0.06, 0.06)
    draw_cube(self.tex_metal)
    glPopMatrix()

    # -----------------------------------------------------------------------
    # 2. DESKTOP SURFACE (Height y=0.85)
    # -----------------------------------------------------------------------
    # Heavy beveled dark composite tabletop
    glColor3f(0.18, 0.20, 0.24)
    glPushMatrix()
    glTranslatef(0.0, 0.84, 0.0)
    glScalef(2.55, 0.05, 1.05)
    draw_cube(self.tex_metal)
    glPopMatrix()

    # Ergonomic front wrist rest edge
    glColor3f(0.12, 0.14, 0.18)
    glPushMatrix()
    glTranslatef(0.0, 0.84, 0.51)
    glScalef(2.45, 0.035, 0.06)
    draw_cube(self.tex_metal)
    glPopMatrix()

    # -----------------------------------------------------------------------
    # 3. UNDER-DESK NETRUNNER RIG & CABLE HARNESS
    # -----------------------------------------------------------------------
    # Tower chassis suspended on right floor bracket
    glColor3f(0.15, 0.16, 0.19)
    glPushMatrix()
    glTranslatef(0.85, 0.36, -0.10)
    glScalef(0.28, 0.62, 0.60)
    draw_cube(self.tex_metal)
    glPopMatrix()

    # Glowing front intake fan & LEDs
    glMaterialfv(GL_FRONT, GL_EMISSION, [0.0, 0.8, 1.0, 1.0])
    glColor3f(0.0, 0.8, 1.0)
    glPushMatrix()
    glTranslatef(0.85, 0.36, 0.21)
    glScalef(0.20, 0.45, 0.02)
    draw_cube(None)
    glPopMatrix()
    glMaterialfv(GL_FRONT, GL_EMISSION, no_emission)

    # Thick braided black & cyan power conduits pooling onto the floor
    glColor3f(0.06, 0.06, 0.08)
    # Cable from desk to floor
    glPushMatrix()
    glTranslatef(0.0, 0.42, -0.42)
    glRotatef(12, 0, 0, 1)
    glScalef(0.08, 0.84, 0.08)
    draw_cube(None)
    glPopMatrix()
    # Cable pool along floor
    glPushMatrix()
    glTranslatef(0.20, 0.02, -0.44)
    glScalef(0.60, 0.03, 0.12)
    draw_cube(None)
    glPopMatrix()

    # -----------------------------------------------------------------------
    # 4. ARTICULATED MONITOR MOUNTING MAST
    # -----------------------------------------------------------------------
    glColor3f(0.25, 0.26, 0.30)
    # Base desk clamp
    glPushMatrix()
    glTranslatef(0.0, 0.865, -0.38)
    glScalef(0.14, 0.04, 0.14)
    draw_cube(self.tex_metal)
    glPopMatrix()

    # Vertical mounting mast rising from desktop
    glPushMatrix()
    glTranslatef(0.0, 1.30, -0.38)
    glScalef(0.06, 0.82, 0.06)
    draw_cube(self.tex_metal)
    glPopMatrix()

    # Horizontal mounting crossbar arm
    glPushMatrix()
    glTranslatef(0.0, 1.36, -0.35)
    glScalef(1.90, 0.04, 0.04)
    draw_cube(self.tex_metal)
    glPopMatrix()

    # -----------------------------------------------------------------------
    # 5. TRIPLE CURVED MONITOR ARRAY
    # -----------------------------------------------------------------------
    # A. Central Interactive Terminal Monitor
    glPushMatrix()
    glTranslatef(0.0, 1.36, -0.22)
    glRotatef(10, 1, 0, 0)  # Tilted back for viewing

    # Monitor bezel housing
    glColor3f(0.14, 0.15, 0.18)
    glPushMatrix()
    glScalef(1.24, 0.76, 0.06)
    draw_cube(self.tex_metal)
    glPopMatrix()

    # Screen display face
    if self.is_hacked:
      screen_emission = [0.0, 0.85, 0.35, 1.0]
      screen_tex = self.tex_unlocked
    elif self.progress > 0.0:
      pulse = 0.5 + 0.5 * math.sin(self.anim_time * 12.0)
      screen_emission = [0.8 * pulse + 0.2, 0.4 * pulse, 0.0, 1.0]
      screen_tex = self.tex_locked
    else:
      screen_emission = [0.65, 0.08, 0.08, 1.0]
      screen_tex = self.tex_locked

    glMaterialfv(GL_FRONT, GL_EMISSION, screen_emission)
    glColor3f(1.0, 1.0, 1.0)
    glPushMatrix()
    glTranslatef(0.0, 0.0, 0.032)
    glScalef(1.18, 0.70, 0.01)
    draw_cube(screen_tex)
    glPopMatrix()
    glMaterialfv(GL_FRONT, GL_EMISSION, no_emission)
    glPopMatrix()

    # B. Left Auxiliary Monitor (Network Topology / Code)
    glPushMatrix()
    glTranslatef(-0.95, 1.36, -0.16)
    glRotatef(24, 0, 1, 0)   # Tilted inward toward netrunner
    glRotatef(6, 1, 0, 0)

    # Housing
    glColor3f(0.14, 0.15, 0.18)
    glPushMatrix()
    glScalef(0.82, 0.62, 0.05)
    draw_cube(self.tex_metal)
    glPopMatrix()

    # Screen face
    glMaterialfv(GL_FRONT, GL_EMISSION, [0.0, 0.45, 0.70, 1.0])
    glColor3f(1.0, 1.0, 1.0)
    glPushMatrix()
    glTranslatef(0.0, 0.0, 0.026)
    glScalef(0.76, 0.56, 0.01)
    draw_cube(tex_screen_net)
    glPopMatrix()
    glMaterialfv(GL_FRONT, GL_EMISSION, no_emission)
    glPopMatrix()

    # C. Right Auxiliary Monitor (Radar / Telemetry)
    glPushMatrix()
    glTranslatef(0.95, 1.36, -0.16)
    glRotatef(-24, 0, 1, 0)  # Tilted inward toward netrunner
    glRotatef(6, 1, 0, 0)

    # Housing
    glColor3f(0.14, 0.15, 0.18)
    glPushMatrix()
    glScalef(0.82, 0.62, 0.05)
    draw_cube(self.tex_metal)
    glPopMatrix()

    # Screen face
    glMaterialfv(GL_FRONT, GL_EMISSION, [0.65, 0.45, 0.05, 1.0])
    glColor3f(1.0, 1.0, 1.0)
    glPushMatrix()
    glTranslatef(0.0, 0.0, 0.026)
    glScalef(0.76, 0.56, 0.01)
    draw_cube(tex_screen_radar)
    glPopMatrix()
    glMaterialfv(GL_FRONT, GL_EMISSION, no_emission)
    glPopMatrix()

    # D. Overhead Narrow Diagnostic Ticker
    glPushMatrix()
    glTranslatef(0.0, 1.82, -0.28)
    glRotatef(-16, 1, 0, 0)  # Tilted down
    glColor3f(0.14, 0.15, 0.18)
    glPushMatrix()
    glScalef(1.05, 0.18, 0.04)
    draw_cube(self.tex_metal)
    glPopMatrix()
    glMaterialfv(GL_FRONT, GL_EMISSION, [0.0, 0.7, 0.8, 1.0])
    glColor3f(0.0, 0.8, 1.0)
    glPushMatrix()
    glTranslatef(0.0, 0.0, 0.022)
    glScalef(0.98, 0.12, 0.01)
    draw_cube(None)
    glPopMatrix()
    glMaterialfv(GL_FRONT, GL_EMISSION, no_emission)
    glPopMatrix()

    # -----------------------------------------------------------------------
    # 6. DESKTOP PERIPHERALS & NETRUNNER GEAR
    # -----------------------------------------------------------------------
    # Mechanical Backlit Cyberdeck / Keyboard
    glColor3f(0.12, 0.13, 0.15)
    glPushMatrix()
    glTranslatef(0.0, 0.88, 0.18)
    glScalef(0.62, 0.03, 0.24)
    draw_cube(self.tex_metal)
    glPopMatrix()

    # Glowing Keybed Matrix
    glMaterialfv(GL_FRONT, GL_EMISSION, [0.0, 0.6, 0.8, 1.0])
    glColor3f(0.0, 0.7, 0.9)
    glPushMatrix()
    glTranslatef(0.0, 0.896, 0.18)
    glScalef(0.56, 0.01, 0.18)
    draw_cube(None)
    glPopMatrix()
    glMaterialfv(GL_FRONT, GL_EMISSION, no_emission)

    # Left Datapad Deck
    glColor3f(0.18, 0.19, 0.22)
    glPushMatrix()
    glTranslatef(-0.65, 0.875, 0.12)
    glScalef(0.24, 0.02, 0.30)
    draw_cube(self.tex_metal)
    glPopMatrix()

    # Discarded Cyber-soda Can on right corner
    glColor3f(1.0, 1.0, 1.0)
    glPushMatrix()
    glTranslatef(0.82, 0.865, 0.25)
    draw_cylinder(0.035, 0.035, 0.12, slices=8, tex_id=tex_soda)
    glPopMatrix()

    # -----------------------------------------------------------------------
    # 7. ERGONOMIC NETRUNNER SWIVEL CHAIR (Grounded at y=0.0)
    # -----------------------------------------------------------------------
    glPushMatrix()
    # Positioned in front of desk, rotated casually
    glTranslatef(0.10, 0.0, 0.72)
    glRotatef(16, 0, 1, 0)

    # 5 Caster wheels touching the floor (y=0.0)
    glColor3f(0.12, 0.12, 0.14)
    chair_rad = 0.32
    for i in range(5):
      ang = 2.0 * math.pi * i / 5.0
      cx = math.cos(ang) * chair_rad
      cz = math.sin(ang) * chair_rad

      # Caster wheel block
      glPushMatrix()
      glTranslatef(cx, 0.02, cz)
      glScalef(0.05, 0.04, 0.05)
      draw_cube(None)
      glPopMatrix()

      # Star spoke arm from center hub to caster
      glPushMatrix()
      glTranslatef(cx * 0.5, 0.03, cz * 0.5)
      glRotatef(math.degrees(-ang), 0, 1, 0)
      glScalef(0.04, 0.025, chair_rad)
      draw_cube(self.tex_metal)
      glPopMatrix()

    # Center Hub & Hydraulic Lift Piston (y=0.03 to y=0.44)
    glColor3f(0.28, 0.30, 0.35)
    glPushMatrix()
    glTranslatef(0.0, 0.03, 0.0)
    draw_cylinder(0.035, 0.035, 0.41, slices=8, tex_id=self.tex_metal)
    glPopMatrix()

    # Seat Cushion (Height y=0.46)
    glColor3f(0.16, 0.18, 0.22)
    glPushMatrix()
    glTranslatef(0.0, 0.46, 0.0)
    glScalef(0.54, 0.07, 0.50)
    draw_cube(tex_leather)
    glPopMatrix()

    # Neon Cyan Accent Piping on seat edge
    glMaterialfv(GL_FRONT, GL_EMISSION, [0.0, 0.7, 0.9, 1.0])
    glColor3f(0.0, 0.8, 1.0)
    glPushMatrix()
    glTranslatef(0.0, 0.46, 0.252)
    glScalef(0.52, 0.015, 0.01)
    draw_cube(None)
    glPopMatrix()
    glMaterialfv(GL_FRONT, GL_EMISSION, no_emission)

    # High Bucket Seat Backrest (Rising to y=1.12)
    glColor3f(0.15, 0.16, 0.20)
    glPushMatrix()
    glTranslatef(0.0, 0.80, 0.24)
    glRotatef(-8, 1, 0, 0)  # Ergonomic recline
    glScalef(0.48, 0.62, 0.06)
    draw_cube(tex_leather)
    glPopMatrix()

    # Headrest cushion
    glColor3f(0.12, 0.13, 0.16)
    glPushMatrix()
    glTranslatef(0.0, 1.15, 0.28)
    glScalef(0.32, 0.14, 0.08)
    draw_cube(tex_leather)
    glPopMatrix()

    # Left & Right Armrests
    glColor3f(0.18, 0.20, 0.24)
    for side in [-0.28, 0.28]:
      # Upright stem
      glPushMatrix()
      glTranslatef(side, 0.56, 0.05)
      glScalef(0.04, 0.18, 0.04)
      draw_cube(self.tex_metal)
      glPopMatrix()
      # Arm pad
      glPushMatrix()
      glTranslatef(side, 0.66, 0.05)
      glScalef(0.07, 0.03, 0.28)
      draw_cube(tex_leather)
      glPopMatrix()

    glPopMatrix()  # End Chair

    glPopMatrix()  # End Workstation

    # Reset default specular material
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [0.0, 0.0, 0.0, 1.0])
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 0.0)
    glColor3f(1.0, 1.0, 1.0)


def line_intersects_aabb(p1, p2, box):
  """Checks if 2D line segment (p1 -> p2) intersects 2D AABB box (xmin, xmax, zmin, zmax)."""
  x1, z1 = p1
  x2, z2 = p2
  xmin, xmax, zmin, zmax = box[:4]
  dx = x2 - x1
  dz = z2 - z1
  t0, t1 = 0.0, 1.0
  for p, q in [(-dx, x1 - xmin), (dx, xmax - x1), (-dz, z1 - zmin), (dz, zmax - z1)]:
    if p == 0:
      if q < 0:
        return False
    else:
      t = q / p
      if p < 0:
        if t > t1: return False
        if t > t0: t0 = t
      else:
        if t < t0: return False
        if t < t1: t1 = t
  return t0 <= t1


def ray_cast_aabb(p1, p2, box):
  """Returns entry fraction t in [0, 1] if line segment p1->p2 intersects box, else None."""
  x1, z1 = p1
  x2, z2 = p2
  xmin, xmax, zmin, zmax = box[:4]
  dx = x2 - x1
  dz = z2 - z1
  t0, t1 = 0.0, 1.0
  for p, q in [(-dx, x1 - xmin), (dx, xmax - x1), (-dz, z1 - zmin), (dz, zmax - z1)]:
    if p == 0:
      if q < 0:
        return None
    else:
      t = q / p
      if p < 0:
        if t > t1: return None
        if t > t0: t0 = t
      else:
        if t < t0: return None
        if t < t1: t1 = t
  if t0 <= t1 and t0 >= 0.0:
    return t0
  return None


class SecurityCamera:
  """Ceiling-mounted surveillance camera with sweeping detection cone and laser frustum."""

  def __init__(self, x, y, z, mount_yaw=0.0, sweep_angle=35.0, sweep_speed=1.2, max_range=8.5, fov_deg=45.0):
    self.x = x
    self.y = y
    self.z = z
    self.mount_yaw = mount_yaw
    self.sweep_angle = sweep_angle
    self.sweep_speed = sweep_speed
    self.max_range = max_range
    self.fov_deg = fov_deg
    self.obstacles = []
    self.reset()

  def reset(self):
    self.anim_time = 0.0
    self.current_yaw = self.mount_yaw
    self.is_alerted = False
    self.alert_pulse = 0.0

  def get_bounds(self):
    # Ceiling mounted at y=3.6 - no ground footprint
    return None

  def update(self, player, dt, obstacles=None):
    self.anim_time += dt
    self.obstacles = obstacles or []
    # Smooth sine sweep
    self.current_yaw = self.mount_yaw + math.sin(self.anim_time * self.sweep_speed) * self.sweep_angle

    dx = player.x - self.x
    dz = player.z - self.z
    dist = math.hypot(dx, dz)

    self.is_alerted = False

    if 0.2 < dist <= self.max_range:
      # Yaw check: 0 deg = +Z, 90 deg = +X
      angle_to_player = math.degrees(math.atan2(dx, dz))
      diff = (angle_to_player - self.current_yaw + 180.0) % 360.0 - 180.0

      if abs(diff) <= (self.fov_deg * 0.5):
        # Ray-box occlusion check against walls and obstacles
        occluded = False
        if self.obstacles:
          for obs in self.obstacles:
            if line_intersects_aabb((self.x, self.z), (player.x, player.z), obs):
              occluded = True
              break

        if not occluded:
          self.is_alerted = True
          self.alert_pulse += dt * 8.0
          # Detection accumulation
          rate = 65.0 if not player.crouching else 18.0
          player.stealth_meter = min(100.0, player.stealth_meter + rate * dt)
          player.spotted_this_frame = True

  def draw(self, obstacles=None):
    obs = obstacles if obstacles is not None else self.obstacles
    glPushMatrix()
    glTranslatef(self.x, self.y, self.z)

    no_emission = [0.0, 0.0, 0.0, 1.0]

    # 1. Base Mounting Plate attached to ceiling
    glColor3f(0.20, 0.22, 0.25)
    glPushMatrix()
    glTranslatef(0.0, 0.18, 0.0)
    glScalef(0.40, 0.06, 0.40)
    draw_cube(None)
    glPopMatrix()

    # 2. Swivel Neck & Pivot Ball
    glColor3f(0.12, 0.14, 0.16)
    glPushMatrix()
    glTranslatef(0.0, 0.08, 0.0)
    draw_cylinder(0.08, 0.08, 0.12, slices=8, tex_id=None)
    glPopMatrix()

    # 3. Pivoting Camera Body & Lens
    glRotatef(self.current_yaw, 0, 1, 0)
    glRotatef(22, 1, 0, 0)  # Tilted downward towards corridor floor

    # Camera Chassis
    glColor3f(0.16, 0.18, 0.22)
    glPushMatrix()
    glTranslatef(0.0, -0.05, 0.0)
    glScalef(0.24, 0.18, 0.42)
    draw_cube(None)
    glPopMatrix()

    # Top Sun-shield Visor
    glColor3f(0.10, 0.11, 0.13)
    glPushMatrix()
    glTranslatef(0.0, 0.06, 0.06)
    glScalef(0.28, 0.03, 0.48)
    draw_cube(None)
    glPopMatrix()

    # Camera Optical Lens Ring
    glColor3f(0.25, 0.26, 0.30)
    glPushMatrix()
    glTranslatef(0.0, -0.05, 0.22)
    glRotatef(90, 1, 0, 0)
    draw_cylinder(0.07, 0.07, 0.05, slices=10, tex_id=None)
    glPopMatrix()

    # Glowing Optical Eye Sensor
    if self.is_alerted:
      pulse = 0.5 + 0.5 * math.sin(self.alert_pulse)
      lens_color = [4.0, 0.2 * pulse, 0.2 * pulse, 1.0]
    else:
      lens_color = [0.0, 3.4, 4.0, 1.0]

    glMaterialfv(GL_FRONT, GL_EMISSION, lens_color)
    glColor3f(*lens_color[:3])
    glPushMatrix()
    glTranslatef(0.0, -0.05, 0.24)
    glScalef(0.10, 0.10, 0.02)
    draw_cube(None)
    glPopMatrix()
    glMaterialfv(GL_FRONT, GL_EMISSION, no_emission)

    glPopMatrix()  # End camera transforms

    # 4. Projected Ground Laser Cone (Frustum Visualizer, blocked by walls & obstacles)
    glDisable(GL_LIGHTING)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    if self.is_alerted:
      glColor4f(1.0, 0.15, 0.15, 0.45)
    else:
      glColor4f(0.0, 0.85, 1.0, 0.22)

    rad_pitch = math.radians(22.0)
    t = self.y / math.sin(rad_pitch)  # Distance along ray to floor y=0

    half_fov = self.fov_deg * 0.5
    num_slices = 12
    fan_pts = []
    y_lens = self.y - 0.1

    for i in range(num_slices + 1):
      ang = -half_fov + (self.fov_deg * i / num_slices)
      tot_rad = math.radians(self.current_yaw + ang)
      gx = self.x + math.sin(tot_rad) * math.cos(rad_pitch) * t
      gz = self.z + math.cos(tot_rad) * math.cos(rad_pitch) * t

      # Clamp to max_range
      dist = math.hypot(gx - self.x, gz - self.z)
      if dist > self.max_range:
        s = self.max_range / dist
        gx = self.x + (gx - self.x) * s
        gz = self.z + (gz - self.z) * s

      # Raycast against wall & obstacle hitboxes
      t_min = 1.0
      if obs:
        for b in obs:
          th = ray_cast_aabb((self.x, self.z), (gx, gz), b)
          if th is not None and 0.001 < th < t_min:
            t_min = th

      hx = self.x + t_min * (gx - self.x)
      hz = self.z + t_min * (gz - self.z)
      hy = y_lens + t_min * (0.02 - y_lens)
      fan_pts.append((hx, hy, hz))

    glBegin(GL_LINES)
    # Direct laser beam rays from lens to perimeter endpoints
    for idx in [0, 3, 6, 9, 12]:
      pt = fan_pts[idx]
      glVertex3f(self.x, y_lens, self.z)
      glVertex3f(pt[0], pt[1], pt[2])

    # Perimeter boundary connecting adjacent endpoints
    for i in range(len(fan_pts) - 1):
      p1 = fan_pts[i]
      p2 = fan_pts[i + 1]
      glVertex3f(p1[0], p1[1], p1[2])
      glVertex3f(p2[0], p2[1], p2[2])

    # Vertical drop seam line when striking a wall above ground
    for pt in fan_pts:
      if pt[1] > 0.05:
        glVertex3f(pt[0], pt[1], pt[2])
        glVertex3f(pt[0], 0.02, pt[2])
    glEnd()

    glEnable(GL_LIGHTING)
    glColor3f(1.0, 1.0, 1.0)


class VendingMachine:
  """High-tech cyberpunk soda dispenser with illuminated marquee,

  beverage cabinet, cred slot, and interactable electrical distraction spark.
  """

  def __init__(self, x, y, z, textures=None, yaw=0.0):
    self.x = x
    self.y = y
    self.z = z
    self.yaw = yaw
    self.textures = textures or {}
    self.reset()

  def reset(self):
    self.is_sparking = False
    self.spark_timer = 0.0
    self.cooldown = 0.0
    self.anim_time = 0.0

  def get_bounds(self):
    # Returns (min_x, max_x, min_z, max_z, min_y, max_y)
    return (self.x - 0.65, self.x + 0.65, self.z - 0.55, self.z + 0.55, self.y, self.y + 2.30)

  def update(self, player_x, player_z, is_e_pressed, dt, guards=None):
    self.anim_time += dt
    if self.cooldown > 0.0:
      self.cooldown = max(0.0, self.cooldown - dt)

    if self.is_sparking:
      self.spark_timer -= dt
      if self.spark_timer <= 0.0:
        self.is_sparking = False

    dist = math.hypot(player_x - self.x, player_z - self.z)
    if dist < 2.5 and is_e_pressed and self.cooldown <= 0.0:
      self.trigger_distraction(guards)

  def trigger_distraction(self, guards=None):
    self.is_sparking = True
    self.spark_timer = 5.0
    self.cooldown = 22.0

    if guards:
      for g in guards:
        # Distract guards within acoustic range (up to 22 meters)
        dist = math.hypot(g.x - self.x, g.z - self.z)
        if dist < 22.0:
          g.distract(self.x, self.z + 1.2)

  def draw(self):
    glPushMatrix()
    glTranslatef(self.x, self.y, self.z)
    if self.yaw != 0.0:
      glRotatef(self.yaw, 0, 1, 0)

    no_emission = [0.0, 0.0, 0.0, 1.0]
    tex_metal = self.textures.get("metal", None)
    tex_hazard = self.textures.get("hazard", None)
    tex_soda = self.textures.get("soda_can", None)
    tex_sign = self.textures.get("neon_sign", None)

    # 1. Main Outer Chassis (W=1.2, H=2.3, D=0.9)
    glColor3f(0.18, 0.20, 0.24)
    glPushMatrix()
    glTranslatef(0.0, 1.15, 0.0)
    glScalef(1.20, 2.30, 0.90)
    draw_cube(tex_metal)
    glPopMatrix()

    # 2. Base Kickplate with hazard caution stripes
    glColor3f(0.85, 0.85, 0.85)
    glPushMatrix()
    glTranslatef(0.0, 0.10, 0.02)
    glScalef(1.22, 0.20, 0.92)
    draw_cube(tex_hazard)
    glPopMatrix()

    # 3. Illuminated Top Header Marquee ("NEON COLD")
    if self.is_sparking:
      flicker = 0.5 + 0.5 * math.sin(self.anim_time * 35.0)
      marquee_emission = [4.0 * flicker, 0.5 * flicker, 3.5 * flicker, 1.0]
    else:
      marquee_emission = [4.0, 0.0, 3.2, 1.0]

    glMaterialfv(GL_FRONT, GL_EMISSION, marquee_emission)
    glColor3f(1.0, 1.0, 1.0)
    glPushMatrix()
    glTranslatef(0.0, 2.05, 0.46)
    glScalef(1.05, 0.35, 0.04)
    draw_cube(tex_sign)
    glPopMatrix()
    glMaterialfv(GL_FRONT, GL_EMISSION, no_emission)

    # 4. Beverage Display Window & Shelves
    glColor3f(0.08, 0.10, 0.12)
    glPushMatrix()
    glTranslatef(0.0, 1.30, 0.46)
    glScalef(1.02, 1.05, 0.03)
    draw_cube(None)
    glPopMatrix()

    # Cans on Display Shelves
    glMaterialfv(GL_FRONT, GL_EMISSION, [0.0, 2.0, 2.5, 1.0] if not self.is_sparking else [3.0, 2.0, 0.0, 1.0])
    glColor3f(1.0, 1.0, 1.0)
    for row_y in [1.05, 1.35, 1.62]:
      for col_x in [-0.35, -0.12, 0.12, 0.35]:
        glPushMatrix()
        glTranslatef(col_x, row_y, 0.45)
        draw_cylinder(0.035, 0.035, 0.11, slices=8, tex_id=tex_soda)
        glPopMatrix()
    glMaterialfv(GL_FRONT, GL_EMISSION, no_emission)

    # 5. Keypad, Coin / Cred Acceptor Slot
    glColor3f(0.12, 0.14, 0.16)
    glPushMatrix()
    glTranslatef(0.38, 0.65, 0.46)
    glScalef(0.24, 0.42, 0.03)
    draw_cube(tex_metal)
    glPopMatrix()

    # Cred Slot Status LED
    if self.is_sparking:
      slot_emission = [4.0, 0.2, 0.2, 1.0]
    elif self.cooldown > 0.0:
      slot_emission = [2.5, 2.0, 0.0, 1.0]
    else:
      slot_emission = [0.0, 3.6, 0.8, 1.0]

    glMaterialfv(GL_FRONT, GL_EMISSION, slot_emission)
    glColor3f(*slot_emission[:3])
    glPushMatrix()
    glTranslatef(0.38, 0.76, 0.48)
    glScalef(0.14, 0.03, 0.02)
    draw_cube(None)
    glPopMatrix()
    glMaterialfv(GL_FRONT, GL_EMISSION, no_emission)

    # 6. Dispense Hopper Tray at Bottom
    glColor3f(0.10, 0.11, 0.14)
    glPushMatrix()
    glTranslatef(0.0, 0.35, 0.46)
    glScalef(0.72, 0.22, 0.08)
    draw_cube(tex_metal)
    glPopMatrix()

    # Dispensed Soda Can sitting in tray
    if self.is_sparking or self.cooldown > 4.0:
      glColor3f(1.0, 1.0, 1.0)
      glPushMatrix()
      glTranslatef(0.0, 0.30, 0.48)
      glRotatef(90, 1, 0, 0)
      draw_cylinder(0.035, 0.035, 0.11, slices=8, tex_id=tex_soda)
      glPopMatrix()

    glPopMatrix()  # End Vending Machine
    glColor3f(1.0, 1.0, 1.0)
