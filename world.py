from entities import draw_cube
from OpenGL.GL import *


class Room:

  def __init__(
      self, tex_wall, tex_floor, tex_hazard, tex_neon_cyan, tex_neon_magenta
  ):
    self.tex_wall = tex_wall
    self.tex_floor = tex_floor
    self.tex_hazard = tex_hazard
    self.tex_neon_cyan = tex_neon_cyan
    self.tex_neon_magenta = tex_neon_magenta
    self.door_open = 0.0

  def update_door(self, is_hacked, dt):
    if is_hacked and self.door_open < 2.2:
      self.door_open += 2.0 * dt

  def draw(self):
    # Base Materials setup
    no_emission = [0.0, 0.0, 0.0, 1.0]
    cyan_emission = [0.0, 0.8, 1.0, 1.0]
    magenta_emission = [1.0, 0.0, 0.7, 1.0]

    glMaterialfv(GL_FRONT, GL_EMISSION, no_emission)

    # Floor
    glPushMatrix()
    glTranslatef(0, 0, 0)
    glScalef(12.0, 0.1, 20.0)
    draw_cube(self.tex_floor)
    glPopMatrix()

    # Ceiling
    glPushMatrix()
    glTranslatef(0, 5.0, 0)
    glScalef(12.0, 0.1, 20.0)
    draw_cube(self.tex_wall)
    glPopMatrix()

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

    # Door Frame Walls
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

    # Sliding Door
    glPushMatrix()
    glTranslatef(-self.door_open, 2.0, 10.0)
    glScalef(2.0, 3.5, 0.2)
    draw_cube(self.tex_hazard)
    glPopMatrix()

    # --------------------------------------------------
    # GLOWING NEON WALL & CEILING LIGHT FIXTURES
    # --------------------------------------------------
    # Left Wall Cyan Light Strip
    glMaterialfv(GL_FRONT, GL_EMISSION, cyan_emission)
    glPushMatrix()
    glTranslatef(-5.9, 3.8, 0.0)
    glScalef(0.1, 0.15, 18.0)
    draw_cube(self.tex_neon_cyan)
    glPopMatrix()

    # Right Wall Magenta Light Strip
    glMaterialfv(GL_FRONT, GL_EMISSION, magenta_emission)
    glPushMatrix()
    glTranslatef(5.9, 3.8, 0.0)
    glScalef(0.1, 0.15, 18.0)
    draw_cube(self.tex_neon_magenta)
    glPopMatrix()

    # Back Wall Cyan Header Bar
    glMaterialfv(GL_FRONT, GL_EMISSION, cyan_emission)
    glPushMatrix()
    glTranslatef(0.0, 4.2, -9.9)
    glScalef(10.0, 0.15, 0.1)
    draw_cube(self.tex_neon_cyan)
    glPopMatrix()

    # Reset Emission Material
    glMaterialfv(GL_FRONT, GL_EMISSION, no_emission)