import math
from entities import draw_cube, draw_cylinder
from OpenGL.GL import *


class Sector:
  """Base class for an isolated facility sector."""

  def __init__(self, name, bounds):
    self.name = name
    self.bounds = bounds  # (min_x, max_x, min_z, max_z)

  def get_obstacles(self):
    return []

  def draw(self, room, textures, anim_time):
    pass


class Sector1_StagingBay(Sector):
  """Sector 1: Tactical Infiltration Staging Bay (Z = -10.0 to 10.0).

  Features industrial ceiling I-beams, HVAC ducting, hanging neon cages,
  tactical cover pillars, server mainframe banks, mil-spec loot crates,
  a cyber-waste drum, scattered ramen/soda trash, floor cables, and sliding blast door.
  """

  def __init__(self):
    super().__init__("StagingBay", (-6.0, 6.0, -10.0, 10.0))

  def get_obstacles(self):
    return [
        # Tactical Pillar 1 (Left Fore)
        (-3.3, -2.3, 0.0, 1.0),
        # Tactical Pillar 2 (Right Fore)
        (2.1, 3.1, 0.7, 1.7),
        # Server Bank 1 (Right Wall)
        (4.2, 5.5, -9.2, -6.5),
        # Server Bank 2 (Back-Left Corner)
        (-5.2, -4.0, -9.4, -8.2),
        # Crate Stack 1 (Left Wall)
        (-5.2, -3.8, 2.3, 3.7),
        # Crate Stack 2 (Right Front)
        (3.9, 5.1, 4.6, 5.8),
        # Perimeter Walls & Bulkhead
        (-6.5, -5.95, -10.2, 10.2),  # Left wall
        (5.95, 6.5, -10.2, 10.2),    # Right wall
        (-6.2, 6.2, -10.5, -9.95),   # Back wall
        (-6.2, -1.5, 9.9, 10.2),     # Front wall (Left section)
        (1.5, 6.2, 9.9, 10.2),      # Front wall (Right section)
    ]

  def draw(self, room, textures, anim_time):
    no_emission = [0.0, 0.0, 0.0, 1.0]
    cyan_emission = [0.0, 3.4, 4.0, 1.0]
    magenta_emission = [4.0, 0.0, 3.0, 1.0]
    amber_emission = [4.0, 2.6, 0.0, 1.0]

    tex_wall = textures.get("wall", None)
    tex_floor = textures.get("floor", None)
    tex_hazard = textures.get("hazard", None)
    tex_neon_cyan = textures.get("neon_cyan", None)
    tex_neon_magenta = textures.get("neon_magenta", None)
    tex_metal = textures.get("metal", tex_wall)
    tex_server = textures.get("server_rack", tex_wall)
    tex_crate = textures.get("crate", tex_metal)
    tex_cardboard = textures.get("cardboard", tex_metal)
    tex_soda = textures.get("soda_can", tex_metal)
    tex_sign = textures.get("neon_sign", tex_neon_cyan)
    tex_grate = textures.get("grate", tex_floor)

    glMaterialfv(GL_FRONT, GL_EMISSION, no_emission)

    # 1. FLOOR & DRAINAGE GRATES
    glPushMatrix()
    glTranslatef(0, -0.05, 0)
    glScalef(12.0, 0.1, 20.0)
    draw_cube(tex_floor)
    glPopMatrix()

    # Perimeter Drainage Grates
    glColor3f(0.30, 0.32, 0.38)
    for side_x in [-5.6, 5.6]:
      glPushMatrix()
      glTranslatef(side_x, 0.005, 0.0)
      glScalef(0.6, 0.01, 19.6)
      draw_cube(tex_grate)
      glPopMatrix()

    # Glossy Chemical / Water Puddle
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [0.85, 0.90, 1.0, 1.0])
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 110.0)
    glColor3f(0.08, 0.12, 0.16)
    glPushMatrix()
    glTranslatef(-1.5, 0.008, -3.8)
    glScalef(2.2, 0.001, 1.4)
    draw_cube(None)
    glPopMatrix()
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [0.0, 0.0, 0.0, 1.0])
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 0.0)

    # Hazard Safety Perimeter Line around Server Bank
    glColor3f(0.8, 0.7, 0.1)
    glPushMatrix()
    glTranslatef(4.1, 0.006, -7.85)
    glScalef(0.12, 0.002, 2.9)
    draw_cube(tex_hazard)
    glPopMatrix()

    # 2. CEILING & INDUSTRIAL INFRASTRUCTURE
    glColor3f(0.20, 0.22, 0.26)
    glPushMatrix()
    glTranslatef(0, 5.05, 0)
    glScalef(12.0, 0.1, 20.0)
    draw_cube(tex_wall)
    glPopMatrix()

    # Steel I-Beam Girders
    glColor3f(0.15, 0.16, 0.20)
    for beam_z in [-7.5, -2.5, 2.5, 7.5]:
      glPushMatrix()
      glTranslatef(0.0, 4.82, beam_z)
      glScalef(12.0, 0.32, 0.12)
      draw_cube(tex_metal)
      glPopMatrix()
      glPushMatrix()
      glTranslatef(0.0, 4.66, beam_z)
      glScalef(12.0, 0.04, 0.34)
      draw_cube(tex_metal)
      glPopMatrix()

    # Giant HVAC Ventilation Duct
    glColor3f(0.25, 0.27, 0.32)
    glPushMatrix()
    glTranslatef(-2.0, 4.45, 0.0)
    glScalef(1.2, 0.65, 20.0)
    draw_cube(tex_metal)
    glPopMatrix()

    # Duct Exhaust Louvers
    glColor3f(0.10, 0.12, 0.14)
    for vent_z in [-5.0, 0.0, 5.0]:
      glPushMatrix()
      glTranslatef(-1.39, 4.45, vent_z)
      glScalef(0.04, 0.45, 1.2)
      draw_cube(tex_grate)
      glPopMatrix()

    # 3. SUSPENDED INDUSTRIAL NEON LIGHT CAGES
    self._draw_hanging_light(3.5, 3.6, -4.0, cyan_emission, [0.0, 0.8, 1.0], tex_neon_cyan, tex_metal)
    self._draw_hanging_light(-4.5, 3.6, -7.5, magenta_emission, [1.0, 0.0, 0.7], tex_neon_magenta, tex_metal)
    self._draw_hanging_light(0.0, 3.8, 1.0, amber_emission, [1.0, 0.7, 0.0], tex_hazard, tex_metal)

    # 4. PERIMETER WALLS & SLIDING BLAST DOOR
    glColor3f(0.25, 0.28, 0.35)
    # Left Wall
    glPushMatrix()
    glTranslatef(-6.0, 2.5, 0)
    glScalef(0.1, 5.0, 20.0)
    draw_cube(tex_wall)
    glPopMatrix()

    # Right Wall
    glPushMatrix()
    glTranslatef(6.0, 2.5, 0)
    glScalef(0.1, 5.0, 20.0)
    draw_cube(tex_wall)
    glPopMatrix()

    # Back Wall
    glPushMatrix()
    glTranslatef(0, 2.5, -10.0)
    glScalef(12.0, 5.0, 0.1)
    draw_cube(tex_wall)
    glPopMatrix()

    # Front Door Frame Walls (Door opening at x in [-1.5, 1.5], z=10.0)
    # Left Wall section (x in [-6.0, -1.5])
    glPushMatrix()
    glTranslatef(-3.75, 2.5, 10.0)
    glScalef(4.5, 5.0, 0.2)
    draw_cube(tex_wall)
    glPopMatrix()

    # Right Wall section (x in [1.5, 6.0])
    glPushMatrix()
    glTranslatef(3.75, 2.5, 10.0)
    glScalef(4.5, 5.0, 0.2)
    draw_cube(tex_wall)
    glPopMatrix()

    # Top Lintel section (x in [-1.5, 1.5], y in [3.5, 5.0])
    glPushMatrix()
    glTranslatef(0.0, 4.25, 10.0)
    glScalef(3.0, 1.5, 0.2)
    draw_cube(tex_wall)
    glPopMatrix()

    # Heavy Pneumatic Door Jambs & Bulkhead Casing
    glColor3f(0.18, 0.20, 0.24)
    # Left Jamb
    glPushMatrix()
    glTranslatef(-1.5, 1.75, 10.0)
    glScalef(0.25, 3.5, 0.28)
    draw_cube(tex_metal)
    glPopMatrix()
    # Right Jamb
    glPushMatrix()
    glTranslatef(1.5, 1.75, 10.0)
    glScalef(0.25, 3.5, 0.28)
    draw_cube(tex_metal)
    glPopMatrix()
    # Overhead Header Beam with Hazard Trim
    glColor3f(0.85, 0.85, 0.85)
    glPushMatrix()
    glTranslatef(0.0, 3.55, 10.0)
    glScalef(3.25, 0.20, 0.28)
    draw_cube(tex_hazard)
    glPopMatrix()

    # Sliding Blast Door (Width 3.1 covers [-1.55, 1.55], height 3.55 sits on floor y=0.0)
    glColor3f(0.85, 0.85, 0.85)
    glPushMatrix()
    glTranslatef(-room.door_open, 1.75, 10.0)
    glScalef(3.1, 3.55, 0.22)
    draw_cube(tex_hazard)
    glPopMatrix()

    # Door Status Indicator Strip (Visible from both Sector 1 and Airlock sides)
    door_color = [0.0, 3.6, 1.2, 1.0] if room.door_open > 1.5 else [3.6, 0.4, 0.4, 1.0]
    glMaterialfv(GL_FRONT, GL_EMISSION, door_color)
    glColor3f(*door_color[:3])
    # Sector 1 side strip
    glPushMatrix()
    glTranslatef(-room.door_open, 3.30, 9.88)
    glScalef(2.6, 0.08, 0.02)
    draw_cube(None)
    glPopMatrix()
    # Airlock side strip
    glPushMatrix()
    glTranslatef(-room.door_open, 3.30, 10.12)
    glScalef(2.6, 0.08, 0.02)
    draw_cube(None)
    glPopMatrix()
    glMaterialfv(GL_FRONT, GL_EMISSION, no_emission)

    # 5. GIANT BACK WALL KATAKANA NEON SIGN ("サイバー // CYBER")
    glColor3f(0.12, 0.13, 0.16)
    glPushMatrix()
    glTranslatef(0.0, 3.3, -9.92)
    glScalef(4.2, 1.4, 0.06)
    draw_cube(tex_metal)
    glPopMatrix()

    glMaterialfv(GL_FRONT, GL_EMISSION, [1.6, 2.4, 3.6, 1.0])
    glColor3f(1.0, 1.0, 1.0)
    glPushMatrix()
    glTranslatef(0.0, 3.3, -9.88)
    glScalef(4.0, 1.2, 0.02)
    draw_cube(tex_sign)
    glPopMatrix()
    glMaterialfv(GL_FRONT, GL_EMISSION, no_emission)

    # 6. WALL NEON STRIPS & RECESSED FLOOR RUNWAY LIGHTS
    glMaterialfv(GL_FRONT, GL_EMISSION, cyan_emission)
    glColor3f(0.0, 0.9, 1.0)
    glPushMatrix()
    glTranslatef(-5.92, 3.8, 0.0)
    glScalef(0.06, 0.12, 18.0)
    draw_cube(tex_neon_cyan)
    glPopMatrix()

    glMaterialfv(GL_FRONT, GL_EMISSION, magenta_emission)
    glColor3f(1.0, 0.0, 0.8)
    glPushMatrix()
    glTranslatef(5.92, 3.8, 0.0)
    glScalef(0.06, 0.12, 18.0)
    draw_cube(tex_neon_magenta)
    glPopMatrix()
    glMaterialfv(GL_FRONT, GL_EMISSION, no_emission)

    # Recessed Floor Guide Lights
    for fz in range(-8, 9, 4):
      glMaterialfv(GL_FRONT, GL_EMISSION, cyan_emission)
      glColor3f(0.0, 0.8, 1.0)
      glPushMatrix()
      glTranslatef(-2.2, 0.008, float(fz))
      glScalef(0.10, 0.005, 0.20)
      draw_cube(None)
      glPopMatrix()

      glMaterialfv(GL_FRONT, GL_EMISSION, amber_emission)
      glColor3f(1.0, 0.6, 0.0)
      glPushMatrix()
      glTranslatef(2.2, 0.008, float(fz))
      glScalef(0.10, 0.005, 0.20)
      draw_cube(None)
      glPopMatrix()
    glMaterialfv(GL_FRONT, GL_EMISSION, no_emission)

    # 7. TACTICAL COVER PILLARS
    self._draw_pillar(-2.8, 0.5, tex_hazard, tex_wall, tex_metal)
    self._draw_pillar(2.6, 1.2, tex_hazard, tex_wall, tex_metal, has_alarm=True)

    # 8. SERVER MAINFRAME BANKS
    self._draw_server_bank(4.85, -7.85, tex_server, tex_metal)
    self._draw_aux_mainframe(-4.6, -8.8, tex_server, tex_metal)

    # 9. MIL-SPEC LOOT CRATES
    self._draw_crate_stack_1(-4.5, 3.0, tex_crate, tex_metal)
    self._draw_crate_stack_2(4.5, 5.2, tex_crate, tex_metal)

    # 10. CYBERPUNK CLUTTER
    # Biohazard Drum
    glColor3f(0.24, 0.25, 0.28)
    glPushMatrix()
    glTranslatef(-5.0, 0.0, -2.0)
    draw_cylinder(0.38, 0.38, 0.95, slices=10, tex_id=tex_hazard)
    glPopMatrix()

    # Crumpled Takeout Food Boxes
    glColor3f(1.0, 1.0, 1.0)
    glPushMatrix()
    glTranslatef(1.9, 0.06, -3.2)
    glRotatef(24, 0, 1, 0)
    glScalef(0.18, 0.12, 0.18)
    draw_cube(tex_cardboard)
    glPopMatrix()

    # Crushed Energy Drink Cans
    glPushMatrix()
    glTranslatef(2.3, 0.04, -3.4)
    glRotatef(68, 0, 1, 0)
    glRotatef(90, 1, 0, 0)
    draw_cylinder(0.035, 0.035, 0.13, slices=8, tex_id=tex_soda)
    glPopMatrix()

    # Discarded Datachip
    glMaterialfv(GL_FRONT, GL_EMISSION, [4.0, 2.4, 0.0, 1.0])
    glColor3f(1.0, 0.7, 0.0)
    glPushMatrix()
    glTranslatef(3.6, 0.015, -7.2)
    glRotatef(18, 0, 1, 0)
    glScalef(0.12, 0.015, 0.08)
    draw_cube(None)
    glPopMatrix()
    glMaterialfv(GL_FRONT, GL_EMISSION, no_emission)

    # Wall Breaker Box
    glColor3f(0.20, 0.22, 0.26)
    glPushMatrix()
    glTranslatef(-5.92, 1.8, -4.0)
    glScalef(0.08, 0.85, 0.65)
    draw_cube(tex_metal)
    glPopMatrix()

    glMaterialfv(GL_FRONT, GL_EMISSION, [0.0, 3.6, 0.8, 1.0])
    glColor3f(0.0, 0.9, 0.2)
    glPushMatrix()
    glTranslatef(-5.86, 2.0, -4.0)
    glScalef(0.02, 0.06, 0.16)
    draw_cube(None)
    glPopMatrix()
    glMaterialfv(GL_FRONT, GL_EMISSION, no_emission)
    glColor3f(1.0, 1.0, 1.0)

  def _draw_hanging_light(self, x, y, z, emission, color, tube_tex, frame_tex):
    glColor3f(0.15, 0.15, 0.18)
    for offset_z in [-0.85, 0.85]:
      glPushMatrix()
      glTranslatef(x, (y + 4.82) * 0.5, z + offset_z)
      glScalef(0.02, 4.82 - y, 0.02)
      draw_cube(None)
      glPopMatrix()

    glColor3f(0.22, 0.24, 0.28)
    glPushMatrix()
    glTranslatef(x, y + 0.08, z)
    glScalef(0.28, 0.10, 1.90)
    draw_cube(frame_tex)
    glPopMatrix()

    glMaterialfv(GL_FRONT, GL_EMISSION, emission)
    glColor3f(*color)
    glPushMatrix()
    glTranslatef(x, y, z)
    glScalef(0.16, 0.08, 1.76)
    draw_cube(tube_tex)
    glPopMatrix()
    glMaterialfv(GL_FRONT, GL_EMISSION, [0.0, 0.0, 0.0, 1.0])

    glColor3f(0.12, 0.13, 0.16)
    glPushMatrix()
    glTranslatef(x, y - 0.05, z)
    glScalef(0.24, 0.02, 1.84)
    draw_cube(None)
    glPopMatrix()

  def _draw_pillar(self, x, z, tex_hazard, tex_wall, tex_metal, has_alarm=False):
    glColor3f(0.85, 0.85, 0.85)
    glPushMatrix()
    glTranslatef(x, 0.175, z)
    glScalef(1.06, 0.35, 1.06)
    draw_cube(tex_hazard)
    glPopMatrix()

    glColor3f(0.26, 0.28, 0.34)
    glPushMatrix()
    glTranslatef(x, 2.525, z)
    glScalef(0.88, 4.35, 0.88)
    draw_cube(tex_wall)
    glPopMatrix()

    glColor3f(0.18, 0.20, 0.24)
    for by in [1.2, 2.8]:
      glPushMatrix()
      glTranslatef(x, by, z)
      glScalef(0.92, 0.12, 0.92)
      draw_cube(tex_metal)
      glPopMatrix()

    if has_alarm:
      glMaterialfv(GL_FRONT, GL_EMISSION, [4.0, 0.4, 0.4, 1.0])
      glColor3f(1.0, 0.1, 0.1)
      glPushMatrix()
      glTranslatef(x, 1.56, z - 0.50)
      glScalef(0.10, 0.08, 0.02)
      draw_cube(None)
      glPopMatrix()
      glMaterialfv(GL_FRONT, GL_EMISSION, [0.0, 0.0, 0.0, 1.0])

  def _draw_server_bank(self, x, z, tex_server, tex_metal):
    glColor3f(0.14, 0.15, 0.18)
    glPushMatrix()
    glTranslatef(x, 0.06, z)
    glScalef(1.15, 0.12, 2.65)
    draw_cube(tex_metal)
    glPopMatrix()

    for offset_z in [-0.82, 0.0, 0.82]:
      glColor3f(0.18, 0.20, 0.24)
      glPushMatrix()
      glTranslatef(x, 1.68, z + offset_z)
      glScalef(1.05, 3.12, 0.78)
      draw_cube(tex_metal)
      glPopMatrix()

      glColor3f(1.0, 1.0, 1.0)
      glPushMatrix()
      glTranslatef(x - 0.53, 1.68, z + offset_z)
      glScalef(0.02, 2.95, 0.72)
      draw_cube(tex_server)
      glPopMatrix()

    glMaterialfv(GL_FRONT, GL_EMISSION, [0.0, 3.2, 4.0, 1.0])
    glColor3f(0.0, 0.8, 1.0)
    glPushMatrix()
    glTranslatef(x - 0.52, 3.28, z)
    glScalef(0.03, 0.05, 2.4)
    draw_cube(None)
    glPopMatrix()
    glMaterialfv(GL_FRONT, GL_EMISSION, [0.0, 0.0, 0.0, 1.0])

  def _draw_aux_mainframe(self, x, z, tex_server, tex_metal):
    glColor3f(0.18, 0.20, 0.24)
    glPushMatrix()
    glTranslatef(x, 1.55, z)
    glScalef(0.95, 3.10, 0.95)
    draw_cube(tex_metal)
    glPopMatrix()

    glColor3f(1.0, 1.0, 1.0)
    glPushMatrix()
    glTranslatef(x, 1.55, z + 0.48)
    glScalef(0.85, 2.90, 0.02)
    draw_cube(tex_server)
    glPopMatrix()

  def _draw_crate_stack_1(self, x, z, tex_crate, tex_metal):
    glColor3f(0.85, 0.85, 0.85)
    glPushMatrix()
    glTranslatef(x, 0.425, z)
    glScalef(1.30, 0.85, 1.10)
    draw_cube(tex_crate)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(x + 0.05, 1.20, z - 0.05)
    glRotatef(9, 0, 1, 0)
    glScalef(0.95, 0.70, 0.90)
    draw_cube(tex_crate)
    glPopMatrix()

    glMaterialfv(GL_FRONT, GL_EMISSION, [0.0, 3.6, 4.0, 1.0])
    glColor3f(0.0, 0.9, 1.0)
    glPushMatrix()
    glTranslatef(x + 0.08, 1.64, z + 0.13)
    glScalef(0.08, 0.04, 0.02)
    draw_cube(None)
    glPopMatrix()
    glMaterialfv(GL_FRONT, GL_EMISSION, [0.0, 0.0, 0.0, 1.0])

  def _draw_crate_stack_2(self, x, z, tex_crate, tex_metal):
    glColor3f(0.85, 0.85, 0.85)
    glPushMatrix()
    glTranslatef(x, 0.38, z)
    glScalef(1.10, 0.76, 1.05)
    draw_cube(tex_crate)
    glPopMatrix()

    glColor3f(0.75, 0.20, 0.10)
    glPushMatrix()
    glTranslatef(x - 0.05, 0.86, z)
    glRotatef(-18, 0, 1, 0)
    glScalef(0.55, 0.20, 0.32)
    draw_cube(tex_metal)
    glPopMatrix()


class SectorAirlock_Corridor(Sector):
  """Sector Transition Airlock Corridor (Z = 10.0 to 18.0).

  Features heavy pneumatic doorframes, yellow hazard safety lines,
  industrial wall conduit pipes, floor grates, and overhead caution lighting.
  """

  def __init__(self):
    super().__init__("AirlockCorridor", (-2.5, 2.5, 10.0, 18.0))

  def get_obstacles(self):
    return [
        # Left Wall Conduit Enclosure
        (-2.5, -2.0, 12.0, 16.0),
        # Right Wall Conduit Enclosure
        (2.0, 2.5, 12.0, 16.0),
        # Perimeter Side Walls (x=-2.5 and x=2.5)
        (-3.5, -2.48, 9.8, 18.2),  # Left side wall
        (2.48, 3.5, 9.8, 18.2),   # Right side wall
    ]

  def draw(self, room, textures, anim_time):
    no_emission = [0.0, 0.0, 0.0, 1.0]
    tex_wall = textures.get("wall", None)
    tex_floor = textures.get("floor", None)
    tex_hazard = textures.get("hazard", None)
    tex_metal = textures.get("metal", tex_wall)
    tex_grate = textures.get("grate", tex_floor)

    # 1. Floor & Grates (z=10 to 18, width x=-2.5 to 2.5)
    glPushMatrix()
    glTranslatef(0.0, -0.05, 14.0)
    glScalef(5.0, 0.10, 8.0)
    draw_cube(tex_floor)
    glPopMatrix()

    # Center Grate Runway
    glColor3f(0.35, 0.36, 0.40)
    glPushMatrix()
    glTranslatef(0.0, 0.005, 14.0)
    glScalef(1.2, 0.01, 8.0)
    draw_cube(tex_grate)
    glPopMatrix()

    # Hazard Safety Trim Lines along walls
    glColor3f(0.9, 0.8, 0.1)
    for sx in [-2.35, 2.35]:
      glPushMatrix()
      glTranslatef(sx, 0.008, 14.0)
      glScalef(0.18, 0.005, 8.0)
      draw_cube(tex_hazard)
      glPopMatrix()

    # 2. Ceiling (Height y=4.2)
    glColor3f(0.18, 0.20, 0.24)
    glPushMatrix()
    glTranslatef(0.0, 4.25, 14.0)
    glScalef(5.0, 0.10, 8.0)
    draw_cube(tex_wall)
    glPopMatrix()

    # Structural Rib Arches spanning corridor
    glColor3f(0.14, 0.15, 0.18)
    for rz in [10.2, 12.5, 15.0, 17.5]:
      # Top beam
      glPushMatrix()
      glTranslatef(0.0, 4.12, rz)
      glScalef(5.0, 0.25, 0.25)
      draw_cube(tex_metal)
      glPopMatrix()
      # Left pillar
      glPushMatrix()
      glTranslatef(-2.4, 2.1, rz)
      glScalef(0.20, 4.2, 0.25)
      draw_cube(tex_metal)
      glPopMatrix()
      # Right pillar
      glPushMatrix()
      glTranslatef(2.4, 2.1, rz)
      glScalef(0.20, 4.2, 0.25)
      draw_cube(tex_metal)
      glPopMatrix()

    # 3. Perimeter Side Walls
    glColor3f(0.22, 0.24, 0.28)
    # Left Wall (x=-2.5)
    glPushMatrix()
    glTranslatef(-2.5, 2.1, 14.0)
    glScalef(0.10, 4.2, 8.0)
    draw_cube(tex_wall)
    glPopMatrix()
    # Right Wall (x=2.5)
    glPushMatrix()
    glTranslatef(2.5, 2.1, 14.0)
    glScalef(0.10, 4.2, 8.0)
    draw_cube(tex_wall)
    glPopMatrix()

    # 4. Industrial Wall Conduits & High-Pressure Steam Pipes
    glColor3f(0.35, 0.38, 0.45)
    # Left wall pipe cluster
    for py in [1.2, 1.8, 2.4]:
      glPushMatrix()
      glTranslatef(-2.35, py, 14.0)
      glScalef(0.12, 0.12, 7.8)
      draw_cube(tex_metal)
      glPopMatrix()
    # Right wall cable conduit
    glPushMatrix()
    glTranslatef(2.35, 2.0, 14.0)
    glScalef(0.14, 0.35, 7.8)
    draw_cube(tex_metal)
    glPopMatrix()

    # Glowing Pressure Gauge Dials
    glMaterialfv(GL_FRONT, GL_EMISSION, [0.0, 3.4, 4.0, 1.0])
    glColor3f(0.0, 0.9, 1.0)
    glPushMatrix()
    glTranslatef(-2.28, 1.8, 13.5)
    glScalef(0.04, 0.16, 0.16)
    draw_cube(None)
    glPopMatrix()

    glMaterialfv(GL_FRONT, GL_EMISSION, [4.0, 2.0, 0.0, 1.0])
    glColor3f(1.0, 0.6, 0.0)
    glPushMatrix()
    glTranslatef(-2.28, 1.8, 15.0)
    glScalef(0.04, 0.16, 0.16)
    draw_cube(None)
    glPopMatrix()
    glMaterialfv(GL_FRONT, GL_EMISSION, no_emission)

    # 5. Overhead Caution Warning Lamp Fixture (z=14.0, y=3.6)
    glMaterialfv(GL_FRONT, GL_EMISSION, [4.0, 2.6, 0.0, 1.0])
    glColor3f(1.0, 0.7, 0.0)
    glPushMatrix()
    glTranslatef(0.0, 3.65, 14.0)
    glScalef(0.24, 0.10, 1.4)
    draw_cube(tex_hazard)
    glPopMatrix()
    glMaterialfv(GL_FRONT, GL_EMISSION, no_emission)
    glColor3f(1.0, 1.0, 1.0)


class Sector2_DatacoreVault(Sector):
  """Sector 2: High-Security Datacore Vault (Z = 18.0 to 42.0).

  Features dual recessed neon coolant trenches, elevated perimeter catwalks,
  access stair ramps, massive Central Datacore Monolith, auxiliary server banks,
  high-voltage overhead floodlights, and tactical cover containers.
  """

  def __init__(self):
    super().__init__("DatacoreVault", (-10.0, 10.0, 18.0, 42.0))

  def get_obstacles(self):
    return [
        # Central Datacore Monolith (full vertical height)
        (-1.4, 1.4, 30.8, 33.2, 0.0, 6.0),
        # Left Catwalk Support Columns (under catwalk: y=0.0 to 2.65)
        (-6.4, -5.6, 23.8, 24.6, 0.0, 2.65),
        (-6.4, -5.6, 32.1, 32.9, 0.0, 2.65),
        (-6.4, -5.6, 40.1, 40.9, 0.0, 2.65),
        # Right Catwalk Support Columns (under catwalk: y=0.0 to 2.65)
        (5.6, 6.4, 23.8, 24.6, 0.0, 2.65),
        (5.6, 6.4, 32.1, 32.9, 0.0, 2.65),
        (5.6, 6.4, 40.1, 40.9, 0.0, 2.65),
        # Vault Floor Server Cluster 1 (Right Fore, floor level y=0.0 to 2.50)
        (3.5, 5.0, 23.5, 25.8, 0.0, 2.50),
        # Vault Floor Server Cluster 2 (Left Rear, floor level y=0.0 to 2.50)
        (-5.0, -3.5, 35.5, 37.8, 0.0, 2.50),
        # Vault Cover Crate Stack (floor level y=0.0 to 1.65)
        (-5.2, -3.8, 27.5, 29.5, 0.0, 1.65),
        # Cryogenic Coolant Cylinders (Right Rear, floor level y=0.0 to 2.40)
        (3.8, 5.2, 33.2, 34.8, 0.0, 2.40),
        # Entrance Partition Wall from Airlock (z=18.0, doorway at x in [-1.6, 1.6])
        (-10.2, -1.6, 17.95, 18.3, 0.0, 6.0),
        (1.6, 10.2, 17.95, 18.3, 0.0, 6.0),
        # Perimeter Walls (full height)
        (-10.5, -9.95, 17.8, 42.2, 0.0, 6.0),
        (9.95, 10.5, 17.8, 42.2, 0.0, 6.0),
        (-10.2, 10.2, 41.95, 42.5, 0.0, 6.0),
        # Catwalk Railing Barriers (block player on catwalk from falling: y=2.65 to 3.70)
        (-6.18, -5.82, 24.2, 39.5, 2.65, 3.70),  # Left catwalk inner railing
        (5.82, 6.18, 24.2, 39.5, 2.65, 3.70),   # Right catwalk inner railing
        (-6.0, 6.0, 39.30, 39.70, 2.65, 3.70),   # Skybridge front railing
        (-6.18, -5.82, 18.8, 24.2, 0.0, 3.70),  # Left ramp inner railing
        (5.82, 6.18, 18.8, 24.2, 0.0, 3.70),   # Right ramp inner railing
    ]

  def draw(self, room, textures, anim_time):
    no_emission = [0.0, 0.0, 0.0, 1.0]
    cyan_emission = [0.0, 3.8, 4.0, 1.0]
    magenta_emission = [4.0, 0.0, 3.4, 1.0]

    tex_wall = textures.get("wall", None)
    tex_floor = textures.get("floor", None)
    tex_hazard = textures.get("hazard", None)
    tex_metal = textures.get("metal", tex_wall)
    tex_server = textures.get("server_rack", tex_wall)
    tex_crate = textures.get("crate", tex_metal)
    tex_grate = textures.get("grate", tex_floor)
    tex_neon_cyan = textures.get("neon_cyan", None)
    tex_neon_magenta = textures.get("neon_magenta", None)

    # 1. MAIN VAULT FLOOR SLAB (Width x in [-10, 10], z in [18, 42])
    glPushMatrix()
    glTranslatef(0.0, -0.05, 30.0)
    glScalef(20.0, 0.10, 24.0)
    draw_cube(tex_floor)
    glPopMatrix()

    # 2. DUAL RECESSED COOLANT TRENCHES (x=-3.5 and x=3.5, z=22 to 38)
    for tx in [-3.5, 3.5]:
      # Glowing coolant fluid base in trench
      glMaterialfv(GL_FRONT, GL_EMISSION, cyan_emission)
      glColor3f(0.0, 0.9, 1.0)
      glPushMatrix()
      glTranslatef(tx, -0.02, 30.0)
      glScalef(1.2, 0.01, 16.0)
      draw_cube(tex_neon_cyan)
      glPopMatrix()
      glMaterialfv(GL_FRONT, GL_EMISSION, no_emission)

      # Heavy Drainage Grating covering the trench
      glColor3f(0.28, 0.30, 0.34)
      glPushMatrix()
      glTranslatef(tx, 0.005, 30.0)
      glScalef(1.25, 0.01, 16.2)
      draw_cube(tex_grate)
      glPopMatrix()

      # Hazard warning borders along trenches
      glColor3f(0.85, 0.85, 0.85)
      for off_x in [-0.7, 0.7]:
        glPushMatrix()
        glTranslatef(tx + off_x, 0.006, 30.0)
        glScalef(0.12, 0.005, 16.2)
        draw_cube(tex_hazard)
        glPopMatrix()

    # 3. ELEVATED PERIMETER CATWALKS (Height y=2.75 - reaches far back wall at z=42.0)
    glColor3f(0.18, 0.20, 0.24)
    # Left Catwalk Walkway (x in [-9.5, -6.0], z in [24.2, 42.0])
    glPushMatrix()
    glTranslatef(-7.75, 2.70, 33.10)
    glScalef(3.5, 0.10, 17.80)
    draw_cube(tex_metal)
    glPopMatrix()

    # Right Catwalk Walkway (x in [6.0, 9.5], z in [24.2, 42.0])
    glPushMatrix()
    glTranslatef(7.75, 2.70, 33.10)
    glScalef(3.5, 0.10, 17.80)
    draw_cube(tex_metal)
    glPopMatrix()

    # Rear Transverse Skybridge (z in [39.5, 42.0], width x in [-9.5, 9.5])
    glPushMatrix()
    glTranslatef(0.0, 2.70, 40.75)
    glScalef(19.0, 0.10, 2.50)
    draw_cube(tex_metal)
    glPopMatrix()

    # Catwalk Access Stair Ramps (z=18.8 to 24.2, rising from y=0.0 to flush deck at y=2.75)
    for sx in [-7.75, 7.75]:
      glPushMatrix()
      glTranslatef(sx, 1.375, 21.50)
      glRotatef(-27.0, 1, 0, 0)
      glScalef(3.2, 0.10, 6.06)
      draw_cube(tex_metal)
      glPopMatrix()

    # Catwalk Structural Support Columns (y=0.0 to 2.65 underside)
    glColor3f(0.14, 0.15, 0.18)
    for cx in [-6.0, 6.0]:
      for cz in [24.2, 32.5, 40.5]:
        glPushMatrix()
        glTranslatef(cx, 1.325, cz)
        glScalef(0.35, 2.65, 0.35)
        draw_cube(tex_metal)
        glPopMatrix()

    # Safety Handrails with Hazard Trim along Catwalk Edges
    glColor3f(0.8, 0.7, 0.1)
    # Left catwalk handrail (z in [24.2, 39.5])
    glPushMatrix()
    glTranslatef(-6.02, 3.20, 31.85)
    glScalef(0.04, 0.90, 15.30)
    draw_cube(tex_hazard)
    glPopMatrix()

    # Right catwalk handrail (z in [24.2, 39.5])
    glPushMatrix()
    glTranslatef(6.02, 3.20, 31.85)
    glScalef(0.04, 0.90, 15.30)
    draw_cube(tex_hazard)
    glPopMatrix()

    # Left & Right Ramp Incline Handrails (sloping with the ramp)
    for sx in [-6.02, 6.02]:
      glPushMatrix()
      glTranslatef(sx, 1.825, 21.50)
      glRotatef(-27.0, 1, 0, 0)
      glScalef(0.04, 0.90, 6.06)
      draw_cube(tex_hazard)
      glPopMatrix()

    # Rear Skybridge Front Handrail (spanning x in [-6.0, 6.0] at z=39.48)
    glPushMatrix()
    glTranslatef(0.0, 3.20, 39.48)
    glScalef(12.0, 0.90, 0.04)
    draw_cube(tex_hazard)
    glPopMatrix()

    # 4. HIGH CEILING & INDUSTRIAL STRUCTURAL TRUSSES (Height y=6.0)
    glColor3f(0.20, 0.22, 0.26)
    glPushMatrix()
    glTranslatef(0.0, 6.05, 30.0)
    glScalef(20.0, 0.10, 24.0)
    draw_cube(tex_wall)
    glPopMatrix()

    # Massive Cross-Room Steel Trusses
    glColor3f(0.14, 0.15, 0.18)
    for tz in [24.0, 30.0, 36.0]:
      glPushMatrix()
      glTranslatef(0.0, 5.82, tz)
      glScalef(20.0, 0.38, 0.20)
      draw_cube(tex_metal)
      glPopMatrix()

    # 5. PERIMETER WALLS
    glColor3f(0.24, 0.26, 0.32)
    # Left Wall (x=-10.0)
    glPushMatrix()
    glTranslatef(-10.0, 3.0, 30.0)
    glScalef(0.10, 6.0, 24.0)
    draw_cube(tex_wall)
    glPopMatrix()

    # Right Wall (x=10.0)
    glPushMatrix()
    glTranslatef(10.0, 3.0, 30.0)
    glScalef(0.10, 6.0, 24.0)
    draw_cube(tex_wall)
    glPopMatrix()

    # Far Back Vault Wall (z=42.0)
    glPushMatrix()
    glTranslatef(0.0, 3.0, 42.0)
    glScalef(20.0, 6.0, 0.10)
    draw_cube(tex_wall)
    glPopMatrix()

    # Entrance Partition Wall from Airlock (z=18.0, with door opening at x in [-1.6, 1.6])
    glPushMatrix()
    glTranslatef(-5.8, 3.0, 18.0)
    glScalef(8.4, 6.0, 0.10)
    draw_cube(tex_wall)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(5.8, 3.0, 18.0)
    glScalef(8.4, 6.0, 0.10)
    draw_cube(tex_wall)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.0, 5.1, 18.0)
    glScalef(3.2, 1.8, 0.10)
    draw_cube(tex_wall)
    glPopMatrix()

    # 6. CENTRAL DATACORE MONOLITH (x=0, z=32.0)
    # Main Tower Hexagonal / Rectangular Blade Cabinet
    glColor3f(0.16, 0.18, 0.22)
    glPushMatrix()
    glTranslatef(0.0, 2.75, 32.0)
    glScalef(2.6, 5.5, 2.6)
    draw_cube(tex_metal)
    glPopMatrix()

    # Server Blade Display Faces on Monolith Sides
    glColor3f(1.0, 1.0, 1.0)
    for mx, mz, mrot in [(-1.31, 0, -90), (1.31, 0, 90), (0, 1.31, 0)]:
      glPushMatrix()
      glTranslatef(mx, 2.75, 32.0 + mz)
      glRotatef(mrot, 0, 1, 0)
      glScalef(2.2, 5.0, 0.02)
      draw_cube(tex_server)
      glPopMatrix()

    # Glowing Cyan Core Ring Conduits on Monolith
    glMaterialfv(GL_FRONT, GL_EMISSION, cyan_emission)
    glColor3f(0.0, 0.9, 1.0)
    for ry in [1.5, 3.0, 4.5]:
      glPushMatrix()
      glTranslatef(0.0, ry, 32.0)
      glScalef(2.7, 0.12, 2.7)
      draw_cube(tex_neon_cyan)
      glPopMatrix()
    glMaterialfv(GL_FRONT, GL_EMISSION, no_emission)

    # 7. TACTICAL VAULT COVER & PROPS
    # Server Cluster 1 (Right Fore)
    glColor3f(0.18, 0.20, 0.24)
    glPushMatrix()
    glTranslatef(4.25, 1.5, 24.65)
    glScalef(1.4, 3.0, 2.2)
    draw_cube(tex_metal)
    glPopMatrix()
    glColor3f(1.0, 1.0, 1.0)
    glPushMatrix()
    glTranslatef(3.54, 1.5, 24.65)
    glScalef(0.02, 2.8, 2.0)
    draw_cube(tex_server)
    glPopMatrix()

    # Server Cluster 2 (Left Rear)
    glColor3f(0.18, 0.20, 0.24)
    glPushMatrix()
    glTranslatef(-4.25, 1.5, 36.65)
    glScalef(1.4, 3.0, 2.2)
    draw_cube(tex_metal)
    glPopMatrix()
    glColor3f(1.0, 1.0, 1.0)
    glPushMatrix()
    glTranslatef(-3.54, 1.5, 36.65)
    glScalef(0.02, 2.8, 2.0)
    draw_cube(tex_server)
    glPopMatrix()

    # Cover Crate Stack
    glColor3f(0.85, 0.85, 0.85)
    glPushMatrix()
    glTranslatef(-4.5, 0.55, 28.5)
    glScalef(1.4, 1.1, 1.8)
    draw_cube(tex_crate)
    glPopMatrix()

    # Cryogenic Coolant Tanks
    glColor3f(0.35, 0.38, 0.44)
    for cz in [33.6, 34.4]:
      glPushMatrix()
      glTranslatef(4.5, 0.0, cz)
      draw_cylinder(0.35, 0.35, 2.4, slices=10, tex_id=tex_hazard)
      glPopMatrix()

    # 8. SUSPENDED OVERHEAD VAULT FLOODLIGHTS
    # Datacore Central Halo (x=0.0, y=5.2, z=32.0)
    glMaterialfv(GL_FRONT, GL_EMISSION, cyan_emission)
    glColor3f(0.0, 0.85, 1.0)
    glPushMatrix()
    glTranslatef(0.0, 5.2, 32.0)
    glScalef(3.0, 0.10, 3.0)
    draw_cube(tex_neon_cyan)
    glPopMatrix()

    # Catwalk Magenta Floodlight (x=-7.5, y=4.5, z=28.0)
    glMaterialfv(GL_FRONT, GL_EMISSION, magenta_emission)
    glColor3f(1.0, 0.0, 0.8)
    glPushMatrix()
    glTranslatef(-7.5, 4.5, 28.0)
    glScalef(0.30, 0.12, 2.0)
    draw_cube(tex_neon_magenta)
    glPopMatrix()
    glMaterialfv(GL_FRONT, GL_EMISSION, no_emission)
    glColor3f(1.0, 1.0, 1.0)


class Room:
  """Master Facility World Coordinator:

  Orchestrates Sector 1 (Staging Bay), Transition Airlock Corridor,
  and Sector 2 (Datacore Vault). Manages dynamic sector collision,
  blast door animations, and rendering.
  """

  def __init__(self, tex_wall, tex_floor, tex_hazard, tex_neon_cyan, tex_neon_magenta, textures=None):
    self.tex_wall = tex_wall
    self.tex_floor = tex_floor
    self.tex_hazard = tex_hazard
    self.tex_neon_cyan = tex_neon_cyan
    self.tex_neon_magenta = tex_neon_magenta
    self.textures = textures or {}
    self.door_open = 0.0
    self.anim_time = 0.0

    # Initialize modular sectors
    self.sector1 = Sector1_StagingBay()
    self.airlock = SectorAirlock_Corridor()
    self.vault = Sector2_DatacoreVault()
    self.sectors = [self.sector1, self.airlock, self.vault]

  def reset(self):
    self.door_open = 0.0
    self.anim_time = 0.0

  def update_door(self, is_hacked, dt):
    self.anim_time += dt
    if is_hacked and self.door_open < 3.2:
      self.door_open += 2.4 * dt

  def is_valid_position(self, x, z, radius=0.32):
    """Verifies that an agent's bounding cylinder is inside the facility boundaries."""
    # Sector 1: Staging Bay (x in [-5.6, 5.6], z in [-9.6, 9.56])
    # Allows player to walk right up to the closed blast door (front face at z=9.88)
    if (-5.6 + radius) <= x <= (5.6 - radius) and (-9.6 + radius) <= z <= (9.88 - radius):
      return True

    # Door 1 Transition (z in [9.2, 10.8]) - seamlessly passable when door is slid open
    if self.door_open > 1.5 and (-1.5 + radius) <= x <= (1.5 - radius) and 9.2 <= z <= 10.8:
      return True

    # Airlock Corridor (x in [-2.5, 2.5], z in [10.0, 18.0])
    airlock_min_z = 10.0 if self.door_open > 1.5 else (10.12 + radius)
    if (-2.5 + radius) <= x <= (2.5 - radius) and airlock_min_z <= z <= 18.0:
      return True

    # Door 2 Transition into Vault (x in [-1.6, 1.6], z in [17.5, 18.5])
    if (-1.6 + radius) <= x <= (1.6 - radius) and 17.5 <= z <= 18.5:
      return True

    # Sector 2: Datacore Vault (x in [-9.65, 9.65], z in [18.0, 41.95])
    if (-9.65 + radius) <= x <= (9.65 - radius) and 18.0 <= z <= (41.95 - radius):
      return True

    return False

  def get_obstacles(self):
    """Collects 2D AABB bounding boxes from all sectors for LOS occlusion & entity collision."""
    obs = []
    for sec in self.sectors:
      obs.extend(sec.get_obstacles())
    # If blast door is closed or partially open, block the doorway for LOS and movement
    if self.door_open < 1.5:
      obs.append((-1.55, 1.55, 9.88, 10.12))
    return obs

  def get_floor_height(self, player_or_x, z=None, on_catwalk=False):
    """Calculates physical floor surface elevation for ground vs elevated catwalk navigation."""
    if hasattr(player_or_x, 'x') and hasattr(player_or_x, 'z'):
      p = player_or_x
      x, z = p.x, p.z
      on_catwalk = getattr(p, 'on_catwalk', False)
      ramp_climbing = getattr(p, 'ramp_climbing', False)

      on_ramp = (6.0 <= abs(x) <= 9.6) and (18.8 <= z <= 24.2)
      on_catwalk_area = ((6.0 <= abs(x) <= 9.6) and (24.2 < z <= 42.0)) or (abs(x) <= 9.6 and 39.5 <= z <= 42.0)

      if on_ramp:
        t = (z - 18.8) / (24.2 - 18.8)
        if on_catwalk:
          if t <= 0.05:
            p.on_catwalk = False
          return max(0.0, min(1.0, t)) * 2.75
        else:
          # Only start climbing if entering from bottom of ramp (t <= 0.25)
          if ramp_climbing or t <= 0.25:
            p.ramp_climbing = True
            if t >= 0.95:
              p.on_catwalk = True
              p.ramp_climbing = False
            return max(0.0, min(1.0, t)) * 2.75
          else:
            return 0.0
      elif on_catwalk_area:
        p.ramp_climbing = False
        if on_catwalk:
          return 2.75
        else:
          # Walking on ground level underneath the catwalk!
          return 0.0
      else:
        p.on_catwalk = False
        p.ramp_climbing = False
        return 0.0
    else:
      x = player_or_x
      on_ramp = (6.0 <= abs(x) <= 9.6) and (18.8 <= z <= 24.2)
      on_catwalk_area = ((6.0 <= abs(x) <= 9.6) and (24.2 < z <= 42.0)) or (abs(x) <= 9.6 and 39.5 <= z <= 42.0)
      if on_ramp:
        t = (z - 18.8) / (24.2 - 18.8)
        return max(0.0, min(1.0, t)) * 2.75
      elif on_catwalk_area and on_catwalk:
        return 2.75
      return 0.0

  def draw(self):
    # Render all sectors
    for sec in self.sectors:
      sec.draw(self, self.textures, self.anim_time)
