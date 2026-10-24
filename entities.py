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


class Player:

  def __init__(self):
    self.reset()

  def reset(self):
    self.x, self.y, self.z = 0.0, 1.6, 6.0
    self.yaw = -90.0
    self.pitch = 0.0
    self.crouching = False
    self.stealth_meter = 0.0

  def update_height(self, dt):
    target_y = 1.0 if self.crouching else 1.6
    self.y += (target_y - self.y) * 10.0 * dt


class Terminal:

  def __init__(self, x, y, z, tex_metal, tex_locked, tex_unlocked):
    self.x, self.y, self.z = x, y, z
    self.tex_metal = tex_metal
    self.tex_locked = tex_locked
    self.tex_unlocked = tex_unlocked
    self.progress = 0.0
    self.is_hacked = False

  def reset(self):
    self.progress = 0.0
    self.is_hacked = False

  def get_bounds(self):
    # Returns (min_x, max_x, min_z, max_z) for 2D line-of-sight occlusion
    return (self.x - 1.6, self.x + 1.6, self.z - 0.6, self.z + 0.6)

  def update(self, player_x, player_z, is_e_pressed, dt):
    dist = math.hypot(player_x - self.x, player_z - self.z)
    if dist < 2.5 and is_e_pressed and not self.is_hacked:
      self.progress = min(100.0, self.progress + 40.0 * dt)
      if self.progress >= 100.0:
        self.is_hacked = True
    else:
      if not self.is_hacked:
        self.progress = max(0.0, self.progress - 20.0 * dt)

  def draw(self):
    # Reflective metallic material response
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [0.8, 0.8, 0.9, 1.0])
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 64.0)

    # Desk
    glPushMatrix()
    glTranslatef(self.x, self.y, self.z)
    glScalef(3.2, 0.9, 1.2)
    draw_cube(self.tex_metal)
    glPopMatrix()

    # Stand
    glPushMatrix()
    glTranslatef(self.x, self.y + 0.75, self.z - 0.2)
    glScalef(0.15, 0.4, 0.1)
    draw_cube(self.tex_metal)
    glPopMatrix()

    # Screen
    glPushMatrix()
    glTranslatef(self.x, self.y + 1.25, self.z - 0.2)
    glRotatef(15, 1, 0, 0)
    glScalef(1.2, 0.8, 0.08)
    draw_cube(self.tex_unlocked if self.is_hacked else self.tex_locked)
    glPopMatrix()

    # Reset default specular material
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [0.0, 0.0, 0.0, 1.0])
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 0.0)