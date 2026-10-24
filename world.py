# --- START OF FILE world.py ---

import math
from entities import draw_cube, draw_cylinder
from OpenGL.GL import *


class Room:
  """Cyberpunk Infiltration Room:

  Features industrial ceiling I-beams, HVAC ducting, hanging neon cages,
  two tactical cover pillars, server mainframe banks, mil-spec loot crates,
  a cyber-waste drum, scattered ramen/soda trash, floor cables, and wet puddle reflections.
  """

  def __init__(
      self, tex_wall, tex_floor, tex_hazard, tex_neon_cyan, tex_neon_magenta, textures=None
  ):
    self.tex_wall = tex_wall
    self.tex_floor = tex_floor
    self.tex_hazard = tex_hazard
    self.tex_neon_cyan = tex_neon_cyan
    self.tex_neon_magenta = tex_neon_magenta
    self.textures = textures or {}
    self.tex_metal = self.textures.get("metal", self.tex_wall)
    self.door_open = 0.0
    self.anim_time = 0.0

  def update_door(self, is_hacked, dt):
    self.anim_time += dt
    if is_hacked and self.door_open < 2.2:
      self.door_open += 2.0 * dt

  def get_obstacles(self):
    """Returns 2D AABB bounding boxes (xmin, xmax, zmin, zmax) for stealth LOS & collision."""
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
    ]

  def draw(self):
    no_emission = [0.0, 0.0, 0.0, 1.0]
    cyan_emission = [0.0, 0.85, 1.0, 1.0]
    magenta_emission = [1.0, 0.0, 0.75, 1.0]
    amber_emission = [1.0, 0.65, 0.0, 1.0]

    tex_metal = self.textures.get("metal", self.tex_wall)
    tex_server = self.textures.get("server_rack", self.tex_wall)
    tex_crate = self.textures.get("crate", tex_metal)
    tex_cardboard = self.textures.get("cardboard", tex_metal)
    tex_soda = self.textures.get("soda_can", tex_metal)
    tex_sign = self.textures.get("neon_sign", self.tex_neon_cyan)
    tex_grate = self.textures.get("grate", self.tex_floor)

    glMaterialfv(GL_FRONT, GL_EMISSION, no_emission)

    # -----------------------------------------------------------------------
    # 1. FLOOR & DRAINAGE GRATES
    # -----------------------------------------------------------------------
    # Main floor slab
    glPushMatrix()
    glTranslatef(0, -0.05, 0)
    glScalef(12.0, 0.1, 20.0)
    draw_cube(self.tex_floor)
    glPopMatrix()

    # Perimeter Drainage Grates along left and right base
    glColor3f(0.30, 0.32, 0.38)
    for side_x in [-5.6, 5.6]:
      glPushMatrix()
      glTranslatef(side_x, 0.005, 0.0)
      glScalef(0.6, 0.01, 19.6)
      draw_cube(tex_grate)
      glPopMatrix()

    # Dark Glossy Chemical / Water Puddle with high specular shine
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
    draw_cube(self.tex_hazard)
    glPopMatrix()

    # -----------------------------------------------------------------------
    # 2. CEILING & INDUSTRIAL INFRASTRUCTURE
    # -----------------------------------------------------------------------
    # Main ceiling slab
    glColor3f(0.20, 0.22, 0.26)
    glPushMatrix()
    glTranslatef(0, 5.05, 0)
    glScalef(12.0, 0.1, 20.0)
    draw_cube(self.tex_wall)
    glPopMatrix()

    # Structural Steel I-Beam Girders spanning room width
    glColor3f(0.15, 0.16, 0.20)
    for beam_z in [-7.5, -2.5, 2.5, 7.5]:
      # Horizontal Web
      glPushMatrix()
      glTranslatef(0.0, 4.82, beam_z)
      glScalef(12.0, 0.32, 0.12)
      draw_cube(tex_metal)
      glPopMatrix()
      # Bottom Flange Plate
      glPushMatrix()
      glTranslatef(0.0, 4.66, beam_z)
      glScalef(12.0, 0.04, 0.34)
      draw_cube(tex_metal)
      glPopMatrix()

    # Giant HVAC Ventilation Duct running lengthwise
    glColor3f(0.25, 0.27, 0.32)
    glPushMatrix()
    glTranslatef(-2.0, 4.45, 0.0)
    glScalef(1.2, 0.65, 20.0)
    draw_cube(tex_metal)
    glPopMatrix()

    # Duct Exhaust Louvers / Vents
    glColor3f(0.10, 0.12, 0.14)
    for vent_z in [-5.0, 0.0, 5.0]:
      glPushMatrix()
      glTranslatef(-1.39, 4.45, vent_z)
      glScalef(0.04, 0.45, 1.2)
      draw_cube(tex_grate)
      glPopMatrix()

    # -----------------------------------------------------------------------
    # 3. SUSPENDED INDUSTRIAL NEON LIGHT CAGES
    # -----------------------------------------------------------------------
    # Light 1: Cyan fixture over Netrunner Terminal (x=3.5, z=-4.0)
    self._draw_hanging_light(3.5, 3.6, -4.0, cyan_emission, [0.0, 0.8, 1.0], self.tex_neon_cyan, tex_metal)

    # Light 2: Magenta fixture over Server Bank (x=-4.5, z=-7.5)
    self._draw_hanging_light(-4.5, 3.6, -7.5, magenta_emission, [1.0, 0.0, 0.7], self.tex_neon_magenta, tex_metal)

    # Light 3: Amber corridor strip over center (x=0.0, z=1.0)
    self._draw_hanging_light(0.0, 3.8, 1.0, amber_emission, [1.0, 0.7, 0.0], self.tex_hazard, tex_metal)

    # -----------------------------------------------------------------------
    # 4. PERIMETER WALLS & SLIDING BLAST DOOR
    # -----------------------------------------------------------------------
    glColor3f(0.25, 0.28, 0.35)
    # Left Wall
    glPushMatrix()
    glTranslatef(-6.0, 2.5, 0)
    glScalef(0.1, 5.0, 20.0)
    draw_cube(self.tex_wall)
    glPopMatrix()

    # Right Wall
    glPushMatrix()
    glTranslatef(6.0, 2.5, 0)
    glScalef(0.1, 5.0, 20.0)
    draw_cube(self.tex_wall)
    glPopMatrix()

    # Back Wall
    glPushMatrix()
    glTranslatef(0, 2.5, -10.0)
    glScalef(12.0, 5.0, 0.1)
    draw_cube(self.tex_wall)
    glPopMatrix()

    # Front Door Frame Walls
    glPushMatrix()
    glTranslatef(-4.0, 2.5, 10.0)
    glScalef(4.0, 5.0, 0.1)
    draw_cube(self.tex_wall)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(4.0, 2.5, 10.0)
    glScalef(4.0, 5.0, 0.1)
    draw_cube(self.tex_wall)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, 4.25, 10.0)
    glScalef(4.0, 1.5, 0.1)
    draw_cube(self.tex_wall)
    glPopMatrix()

    # Sliding Blast Door
    glColor3f(0.85, 0.85, 0.85)
    glPushMatrix()
    glTranslatef(-self.door_open, 2.0, 10.0)
    glScalef(2.0, 3.5, 0.2)
    draw_cube(self.tex_hazard)
    glPopMatrix()

    # Door Status Indicator Strip
    door_color = [0.0, 0.9, 0.3, 1.0] if self.door_open > 1.8 else [0.9, 0.1, 0.1, 1.0]
    glMaterialfv(GL_FRONT, GL_EMISSION, door_color)
    glColor3f(*door_color[:3])
    glPushMatrix()
    glTranslatef(-self.door_open, 3.82, 10.11)
    glScalef(1.8, 0.08, 0.02)
    draw_cube(None)
    glPopMatrix()
    glMaterialfv(GL_FRONT, GL_EMISSION, no_emission)

    # -----------------------------------------------------------------------
    # 5. GIANT BACK WALL KATAKANA NEON SIGN ("サイバー // CYBER")
    # -----------------------------------------------------------------------
    # Steel mounting frame
    glColor3f(0.12, 0.13, 0.16)
    glPushMatrix()
    glTranslatef(0.0, 3.3, -9.92)
    glScalef(4.2, 1.4, 0.06)
    draw_cube(tex_metal)
    glPopMatrix()

    # Illuminated Katakana Face Panel
    glMaterialfv(GL_FRONT, GL_EMISSION, [0.4, 0.6, 0.9, 1.0])
    glColor3f(1.0, 1.0, 1.0)
    glPushMatrix()
    glTranslatef(0.0, 3.3, -9.88)
    glScalef(4.0, 1.2, 0.02)
    draw_cube(tex_sign)
    glPopMatrix()
    glMaterialfv(GL_FRONT, GL_EMISSION, no_emission)

    # -----------------------------------------------------------------------
    # 6. WALL NEON STRIPS & RECESSED FLOOR RUNWAY LIGHTS
    # -----------------------------------------------------------------------
    # Left Wall Cyan Runner Strip
    glMaterialfv(GL_FRONT, GL_EMISSION, cyan_emission)
    glColor3f(0.0, 0.9, 1.0)
    glPushMatrix()
    glTranslatef(-5.92, 3.8, 0.0)
    glScalef(0.06, 0.12, 18.0)
    draw_cube(self.tex_neon_cyan)
    glPopMatrix()

    # Right Wall Magenta Runner Strip
    glMaterialfv(GL_FRONT, GL_EMISSION, magenta_emission)
    glColor3f(1.0, 0.0, 0.8)
    glPushMatrix()
    glTranslatef(5.92, 3.8, 0.0)
    glScalef(0.06, 0.12, 18.0)
    draw_cube(self.tex_neon_magenta)
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

    # -----------------------------------------------------------------------
    # 7. TACTICAL COVER PILLARS (Stealth Occlusion & Cover)
    # -----------------------------------------------------------------------
    # Pillar 1 (Left Fore: x=-2.8, z=0.5)
    self._draw_pillar(-2.8, 0.5, tex_metal)

    # Pillar 2 (Right Fore: x=2.6, z=1.2)
    self._draw_pillar(2.6, 1.2, tex_metal, has_alarm=True)

    # -----------------------------------------------------------------------
    # 8. SERVER MAINFRAME BANKS
    # -----------------------------------------------------------------------
    # Server Bank 1 (Right Wall: 3-bay tall rack cabinets at x=4.85, z=-7.85)
    self._draw_server_bank(4.85, -7.85, tex_server, tex_metal)

    # Server Bank 2 (Back-Left Corner mainframe at x=-4.6, z=-8.8)
    self._draw_aux_mainframe(-4.6, -8.8, tex_server, tex_metal)

    # -----------------------------------------------------------------------
    # 9. MIL-SPEC LOOT CRATES & CONTAINERS
    # -----------------------------------------------------------------------
    # Crate Stack 1 (Left Wall near entrance: x=-4.5, z=3.0)
    self._draw_crate_stack_1(-4.5, 3.0, tex_crate, tex_metal)

    # Crate Stack 2 (Right Fore: x=4.5, z=5.2)
    self._draw_crate_stack_2(4.5, 5.2, tex_crate, tex_metal)

    # -----------------------------------------------------------------------
    # 10. CYBERPUNK CLUTTER, TRASH & ROOM PROPS
    # -----------------------------------------------------------------------
    # A. Industrial Biohazard / Waste Drum (x=-5.0, z=-2.0)
    glColor3f(0.24, 0.25, 0.28)
    glPushMatrix()
    glTranslatef(-5.0, 0.0, -2.0)
    draw_cylinder(0.38, 0.38, 0.95, slices=10, tex_id=self.tex_hazard)
    glPopMatrix()

    # Drum metal reinforcement ribs
    glColor3f(0.16, 0.17, 0.20)
    for ry in [0.32, 0.65]:
      glPushMatrix()
      glTranslatef(-5.0, ry, -2.0)
      draw_cylinder(0.39, 0.39, 0.04, slices=10, tex_id=tex_metal)
      glPopMatrix()

    # B. Crumpled Synth-Ramen Takeout Food Boxes on Floor
    glColor3f(1.0, 1.0, 1.0)
    # Box 1 near terminal
    glPushMatrix()
    glTranslatef(1.9, 0.06, -3.2)
    glRotatef(24, 0, 1, 0)
    glScalef(0.18, 0.12, 0.18)
    draw_cube(tex_cardboard)
    glPopMatrix()

    # Box 2 near left crates
    glPushMatrix()
    glTranslatef(-4.0, 0.06, 2.0)
    glRotatef(-35, 0, 1, 0)
    glScalef(0.20, 0.13, 0.20)
    draw_cube(tex_cardboard)
    glPopMatrix()

    # C. Crushed Cyber-Energy Drink Cans ("NEON CRUSH")
    # Can 1 on side near terminal
    glPushMatrix()
    glTranslatef(2.3, 0.04, -3.4)
    glRotatef(68, 0, 1, 0)
    glRotatef(90, 1, 0, 0)  # Lying horizontal
    draw_cylinder(0.035, 0.035, 0.13, slices=8, tex_id=tex_soda)
    glPopMatrix()

    # Can 2 near server bank
    glPushMatrix()
    glTranslatef(3.8, 0.04, -6.6)
    glRotatef(-42, 0, 1, 0)
    glRotatef(90, 1, 0, 0)
    draw_cylinder(0.035, 0.035, 0.13, slices=8, tex_id=tex_soda)
    glPopMatrix()

    # D. Discarded Illuminated Datachip on Floor near Servers
    glMaterialfv(GL_FRONT, GL_EMISSION, [1.0, 0.6, 0.0, 1.0])
    glColor3f(1.0, 0.7, 0.0)
    glPushMatrix()
    glTranslatef(3.6, 0.015, -7.2)
    glRotatef(18, 0, 1, 0)
    glScalef(0.12, 0.015, 0.08)
    draw_cube(None)
    glPopMatrix()
    glMaterialfv(GL_FRONT, GL_EMISSION, no_emission)

    # E. Heavy Floor Cables Secured with Hazard Tape
    glColor3f(0.08, 0.08, 0.10)
    glPushMatrix()
    glTranslatef(4.0, 0.015, -5.5)
    glRotatef(22, 0, 1, 0)
    glScalef(0.06, 0.03, 2.4)
    draw_cube(None)
    glPopMatrix()

    # Yellow hazard duct tape patch over floor cables
    glColor3f(0.8, 0.7, 0.1)
    glPushMatrix()
    glTranslatef(4.0, 0.025, -5.5)
    glScalef(0.20, 0.005, 0.12)
    draw_cube(self.tex_hazard)
    glPopMatrix()

    # F. Wall-Mounted Circuit Breaker Box (Left wall)
    glColor3f(0.20, 0.22, 0.26)
    glPushMatrix()
    glTranslatef(-5.92, 1.8, -4.0)
    glScalef(0.08, 0.85, 0.65)
    draw_cube(tex_metal)
    glPopMatrix()

    # Breaker status diodes
    glMaterialfv(GL_FRONT, GL_EMISSION, [0.0, 0.9, 0.2, 1.0])
    glColor3f(0.0, 0.9, 0.2)
    glPushMatrix()
    glTranslatef(-5.86, 2.0, -4.0)
    glScalef(0.02, 0.06, 0.16)
    draw_cube(None)
    glPopMatrix()
    glMaterialfv(GL_FRONT, GL_EMISSION, no_emission)

    glColor3f(1.0, 1.0, 1.0)

  # -------------------------------------------------------------------------
  # INTERNAL HELPER DRAWERS
  # -------------------------------------------------------------------------
  def _draw_hanging_light(self, x, y, z, emission, color, tube_tex, frame_tex):
    """Draws an industrial suspended fluorescent/neon tube light fixture."""
    # Suspension Wire Rods from ceiling (y=4.82 down to y)
    glColor3f(0.15, 0.15, 0.18)
    for offset_z in [-0.85, 0.85]:
      glPushMatrix()
      glTranslatef(x, (y + 4.82) * 0.5, z + offset_z)
      glScalef(0.02, 4.82 - y, 0.02)
      draw_cube(None)
      glPopMatrix()

    # Metal Ballast Housing
    glColor3f(0.22, 0.24, 0.28)
    glPushMatrix()
    glTranslatef(x, y + 0.08, z)
    glScalef(0.28, 0.10, 1.90)
    draw_cube(frame_tex)
    glPopMatrix()

    # Glowing Emissive Tube
    glMaterialfv(GL_FRONT, GL_EMISSION, emission)
    glColor3f(*color)
    glPushMatrix()
    glTranslatef(x, y, z)
    glScalef(0.16, 0.08, 1.76)
    draw_cube(tube_tex)
    glPopMatrix()
    glMaterialfv(GL_FRONT, GL_EMISSION, [0.0, 0.0, 0.0, 1.0])

    # Wire Safety Cage Bars
    glColor3f(0.12, 0.13, 0.16)
    glPushMatrix()
    glTranslatef(x, y - 0.05, z)
    glScalef(0.24, 0.02, 1.84)
    draw_cube(None)
    glPopMatrix()

  def _draw_pillar(self, x, z, tex_metal, has_alarm=False):
    """Draws a reinforced concrete/steel tactical cover pillar with hazard base."""
    # Base Plinth on floor with hazard stripes (y=0.0 to 0.35)
    glColor3f(0.85, 0.85, 0.85)
    glPushMatrix()
    glTranslatef(x, 0.175, z)
    glScalef(1.06, 0.35, 1.06)
    draw_cube(self.tex_hazard)
    glPopMatrix()

    # Main Column Shaft (y=0.35 to 4.70)
    glColor3f(0.26, 0.28, 0.34)
    glPushMatrix()
    glTranslatef(x, 2.525, z)
    glScalef(0.88, 4.35, 0.88)
    draw_cube(self.tex_wall)
    glPopMatrix()

    # Steel Corner Plates & Banding
    glColor3f(0.18, 0.20, 0.24)
    for by in [1.2, 2.8]:
      glPushMatrix()
      glTranslatef(x, by, z)
      glScalef(0.92, 0.12, 0.92)
      draw_cube(tex_metal)
      glPopMatrix()

    # Wall-mounted conduit pipe running up pillar
    glColor3f(0.35, 0.38, 0.45)
    glPushMatrix()
    glTranslatef(x + 0.46, 2.5, z)
    glScalef(0.04, 4.3, 0.04)
    draw_cube(tex_metal)
    glPopMatrix()

    # Emergency Terminal / Alarm Box on Pillar Face
    if has_alarm:
      glColor3f(0.18, 0.20, 0.24)
      glPushMatrix()
      glTranslatef(x, 1.5, z - 0.46)
      glScalef(0.32, 0.42, 0.06)
      draw_cube(tex_metal)
      glPopMatrix()

      glMaterialfv(GL_FRONT, GL_EMISSION, [1.0, 0.1, 0.1, 1.0])
      glColor3f(1.0, 0.1, 0.1)
      glPushMatrix()
      glTranslatef(x, 1.56, z - 0.50)
      glScalef(0.10, 0.08, 0.02)
      draw_cube(None)
      glPopMatrix()
      glMaterialfv(GL_FRONT, GL_EMISSION, [0.0, 0.0, 0.0, 1.0])

  def _draw_server_bank(self, x, z, tex_server, tex_metal):
    """Draws a bank of 3 interconnected blade server racks with blinking LEDs."""
    # Floor mounting plinth
    glColor3f(0.14, 0.15, 0.18)
    glPushMatrix()
    glTranslatef(x, 0.06, z)
    glScalef(1.15, 0.12, 2.65)
    draw_cube(tex_metal)
    glPopMatrix()

    # 3 Server Rack Cabinets
    for i, offset_z in enumerate([-0.82, 0.0, 0.82]):
      # Outer Cabinet Chassis
      glColor3f(0.18, 0.20, 0.24)
      glPushMatrix()
      glTranslatef(x, 1.68, z + offset_z)
      glScalef(1.05, 3.12, 0.78)
      draw_cube(tex_metal)
      glPopMatrix()

      # Server Blade Face (Showing flashing LED rows & fan vents)
      glColor3f(1.0, 1.0, 1.0)
      glPushMatrix()
      glTranslatef(x - 0.53, 1.68, z + offset_z)
      glScalef(0.02, 2.95, 0.72)
      draw_cube(tex_server)
      glPopMatrix()

    # Top Status Light Strip
    glMaterialfv(GL_FRONT, GL_EMISSION, [0.0, 0.8, 1.0, 1.0])
    glColor3f(0.0, 0.8, 1.0)
    glPushMatrix()
    glTranslatef(x - 0.52, 3.28, z)
    glScalef(0.03, 0.05, 2.4)
    draw_cube(None)
    glPopMatrix()
    glMaterialfv(GL_FRONT, GL_EMISSION, [0.0, 0.0, 0.0, 1.0])

    # Overhead Cable Ladder extending to ceiling
    glColor3f(0.25, 0.26, 0.30)
    glPushMatrix()
    glTranslatef(x, 4.05, z)
    glScalef(0.60, 1.50, 0.35)
    draw_cube(tex_metal)
    glPopMatrix()

  def _draw_aux_mainframe(self, x, z, tex_server, tex_metal):
    """Draws an auxiliary mainframe cabinet in the back corner."""
    glColor3f(0.18, 0.20, 0.24)
    glPushMatrix()
    glTranslatef(x, 1.55, z)
    glScalef(0.95, 3.10, 0.95)
    draw_cube(tex_metal)
    glPopMatrix()

    # Front display face
    glColor3f(1.0, 1.0, 1.0)
    glPushMatrix()
    glTranslatef(x, 1.55, z + 0.48)
    glScalef(0.85, 2.90, 0.02)
    draw_cube(tex_server)
    glPopMatrix()

  def _draw_crate_stack_1(self, x, z, tex_crate, tex_metal):
    """Draws a stack of heavy mil-spec cargo crates with an electronic lockbox."""
    # Bottom Heavy Crate (Grounded on floor: y=0.425)
    glColor3f(0.85, 0.85, 0.85)
    glPushMatrix()
    glTranslatef(x, 0.425, z)
    glScalef(1.30, 0.85, 1.10)
    draw_cube(tex_crate)
    glPopMatrix()

    # Top Stacked Crate (Resting directly on bottom crate: y=0.85 + 0.35 = 1.20)
    glPushMatrix()
    glTranslatef(x + 0.05, 1.20, z - 0.05)
    glRotatef(9, 0, 1, 0)  # Realistic imperfect stack angle
    glScalef(0.95, 0.70, 0.90)
    draw_cube(tex_crate)
    glPopMatrix()

    # Biometric Tech Lockbox resting on top crate (y=1.55 + 0.09 = 1.64)
    glColor3f(0.14, 0.15, 0.18)
    glPushMatrix()
    glTranslatef(x + 0.08, 1.64, z - 0.05)
    glRotatef(-14, 0, 1, 0)
    glScalef(0.45, 0.18, 0.35)
    draw_cube(tex_metal)
    glPopMatrix()

    # Glowing Biometric Scanner Latch on Lockbox
    glMaterialfv(GL_FRONT, GL_EMISSION, [0.0, 0.9, 1.0, 1.0])
    glColor3f(0.0, 0.9, 1.0)
    glPushMatrix()
    glTranslatef(x + 0.08, 1.64, z + 0.13)
    glScalef(0.08, 0.04, 0.02)
    draw_cube(None)
    glPopMatrix()
    glMaterialfv(GL_FRONT, GL_EMISSION, [0.0, 0.0, 0.0, 1.0])

  def _draw_crate_stack_2(self, x, z, tex_crate, tex_metal):
    """Draws a single medium cargo container with an open tech toolbox on top."""
    # Main Crate (Grounded on floor: y=0.38)
    glColor3f(0.85, 0.85, 0.85)
    glPushMatrix()
    glTranslatef(x, 0.38, z)
    glScalef(1.10, 0.76, 1.05)
    draw_cube(tex_crate)
    glPopMatrix()

    # Open Toolbox Chassis resting on top (y=0.76 + 0.10 = 0.86)
    glColor3f(0.75, 0.20, 0.10)
    glPushMatrix()
    glTranslatef(x - 0.05, 0.86, z)
    glRotatef(-18, 0, 1, 0)
    glScalef(0.55, 0.20, 0.32)
    draw_cube(tex_metal)
    glPopMatrix()

    # Toolbox Handle
    glColor3f(0.20, 0.22, 0.25)
    glPushMatrix()
    glTranslatef(x - 0.05, 0.98, z)
    glScalef(0.22, 0.04, 0.04)
    draw_cube(None)
    glPopMatrix()