from animation import HumanoidPose
from entities import draw_cube
from OpenGL.GL import *


def draw_laser_blaster():
  """Default laser blaster prop."""
  glMaterialfv(GL_FRONT, GL_EMISSION, [0.25, 0.25, 0.25, 1.0])
  glColor3f(0.82, 0.84, 0.90)

  # Grip
  glPushMatrix()
  glTranslatef(0.0, -0.06, 0.0)
  glRotatef(12, 1, 0, 0)
  glScalef(0.05, 0.14, 0.07)
  draw_cube(None)
  glPopMatrix()

  # Receiver
  glPushMatrix()
  glTranslatef(0.0, 0.02, 0.02)
  glScalef(0.06, 0.08, 0.20)
  draw_cube(None)
  glPopMatrix()

  # Barrel
  glPushMatrix()
  glTranslatef(0.0, 0.03, 0.16)
  glScalef(0.04, 0.04, 0.14)
  draw_cube(None)
  glPopMatrix()

  # Cyan Emitter Tip
  glMaterialfv(GL_FRONT, GL_EMISSION, [0.0, 0.85, 1.0, 1.0])
  glColor3f(0.0, 0.9, 1.0)
  glPushMatrix()
  glTranslatef(0.0, 0.03, 0.235)
  glScalef(0.03, 0.03, 0.02)
  draw_cube(None)
  glPopMatrix()

  glMaterialfv(GL_FRONT, GL_EMISSION, [0.0, 0.0, 0.0, 1.0])
  glColor3f(1.0, 1.0, 1.0)


class HumanoidModel:
  """Modular hierarchical renderer that can draw any humanoid NPC."""

  def __init__(
      self,
      textures: dict,
      has_visor: bool = False,
      has_core_glow: bool = False,
      has_holster: bool = False,
      hair_color: tuple = (0.12, 0.10, 0.08),
      visor_color: tuple = (1.0, 0.1, 0.1),
      prop_drawer: callable = None,
  ):
    self.textures = textures
    self.has_visor = has_visor
    self.has_core_glow = has_core_glow
    self.has_holster = has_holster
    self.hair_color = hair_color
    self.visor_color = visor_color
    self.prop_drawer = prop_drawer

  def draw(self, pose: HumanoidPose):
    bob = pose.bob

    # 1. HEAD & ACCESSORIES
    glPushMatrix()
    glTranslatef(0.0, 2.00 + bob, 0.0)
    glRotatef(pose.head_yaw, 0, 1, 0)
    glRotatef(pose.head_pitch, 1, 0, 0)
    glRotatef(pose.head_roll, 0, 0, 1)

    glPushMatrix()
    glScalef(0.32, 0.38, 0.32)
    draw_cube(self.textures.get("skin"))
    glPopMatrix()

    # Nose
    glPushMatrix()
    glTranslatef(0.0, 0.0, 0.18)
    glScalef(0.06, 0.09, 0.07)
    draw_cube(self.textures.get("skin"))
    glPopMatrix()

    # Smirk
    glPushMatrix()
    glTranslatef(0.05, -0.16, 0.17)
    glScalef(0.12, 0.04, 0.05)
    glColor3f(0.50, 0.22, 0.22)
    draw_cube(None)
    glColor3f(1, 1, 1)
    glPopMatrix()

    # Ears
    for side in [0.18, -0.18]:
      glPushMatrix()
      glTranslatef(side, 0.0, 0.0)
      glScalef(0.06, 0.14, 0.10)
      draw_cube(self.textures.get("skin"))
      glPopMatrix()

    # Hair
    glPushMatrix()
    glTranslatef(0.0, 0.21, -0.02)
    glScalef(0.34, 0.08, 0.34)
    glColor3f(*self.hair_color)
    draw_cube(None)
    glColor3f(1, 1, 1)
    glPopMatrix()

    # Optional Tactical Visor
    if self.has_visor:
      glPushMatrix()
      glTranslatef(0.0, 0.04, 0.16)
      glScalef(0.32, 0.10, 0.07)
      glMaterialfv(GL_FRONT, GL_EMISSION, [*self.visor_color, 1.0])
      glColor3f(*self.visor_color)
      draw_cube(None)
      glMaterialfv(GL_FRONT, GL_EMISSION, [0.0, 0.0, 0.0, 1.0])
      glColor3f(1, 1, 1)
      glPopMatrix()

    glPopMatrix()

    # Neck
    glPushMatrix()
    glTranslatef(0.0, 1.75 + bob, 0.0)
    glScalef(0.14, 0.12, 0.14)
    draw_cube(self.textures.get("skin"))
    glPopMatrix()

    # 2. TORSO, ARMOR & BELT
    glPushMatrix()
    glTranslatef(0.0, 1.35 + bob, 0.0)
    glScalef(0.50, 0.68, 0.30)
    draw_cube(self.textures.get("shirt"))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.0, 1.42 + bob, 0.13)
    glScalef(0.38, 0.42, 0.08)
    draw_cube(self.textures.get("armor"))
    glPopMatrix()

    # Optional Chest Core Glow
    if self.has_core_glow:
      glPushMatrix()
      glTranslatef(0.0, 1.45 + bob, 0.17)
      glScalef(0.12, 0.12, 0.02)
      glMaterialfv(GL_FRONT, GL_EMISSION, [0.0, 0.9, 1.0, 1.0])
      glColor3f(0.0, 0.9, 1.0)
      draw_cube(None)
      glMaterialfv(GL_FRONT, GL_EMISSION, [0.0, 0.0, 0.0, 1.0])
      glColor3f(1, 1, 1)
      glPopMatrix()

    # Belt
    glPushMatrix()
    glTranslatef(0.0, 0.96 + bob, 0.0)
    glScalef(0.48, 0.12, 0.28)
    draw_cube(self.textures.get("leather"))
    glPopMatrix()

    # Optional Hip Holster Box
    if self.has_holster:
      glPushMatrix()
      glTranslatef(-0.28, 0.88 + bob, 0.0)
      glScalef(0.14, 0.26, 0.18)
      draw_cube(self.textures.get("leather"))
      glPopMatrix()

    # 3. ARMS
    # Left Arm
    glPushMatrix()
    glTranslatef(0.32, 1.58 + bob, 0.0)
    glPushMatrix()
    glScalef(0.14, 0.14, 0.14)
    draw_cube(self.textures.get("armor"))
    glPopMatrix()

    glRotatef(pose.arm_l[0], 1, 0, 0)
    glRotatef(pose.arm_l[1], 0, 1, 0)
    glRotatef(pose.arm_l[2], 0, 0, 1)

    glPushMatrix()
    glTranslatef(0, -0.2, 0)
    glScalef(0.14, 0.4, 0.16)
    draw_cube(self.textures.get("skin"))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, -0.4, 0)
    glRotatef(pose.arm_l[3], 1, 0, 0)
    glTranslatef(0, -0.2, 0)
    glScalef(0.12, 0.4, 0.14)
    draw_cube(self.textures.get("shirt"))
    glPopMatrix()
    glPopMatrix()

    # Right Arm
    glPushMatrix()
    glTranslatef(-0.32, 1.58 + bob, 0.0)
    glPushMatrix()
    glScalef(0.14, 0.14, 0.14)
    draw_cube(self.textures.get("armor"))
    glPopMatrix()

    glRotatef(pose.arm_r[0], 1, 0, 0)
    glRotatef(pose.arm_r[1], 0, 1, 0)
    glRotatef(pose.arm_r[2], 0, 0, 1)

    glPushMatrix()
    glTranslatef(0, -0.2, 0)
    glScalef(0.16, 0.4, 0.18)
    draw_cube(self.textures.get("metal"))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, -0.4, 0)
    glRotatef(pose.arm_r[3], 1, 0, 0)
    glTranslatef(0, -0.2, 0)
    glScalef(0.14, 0.4, 0.16)
    draw_cube(self.textures.get("metal"))
    glPopMatrix()
    glPopMatrix()

    # 4. ATTACHED PROP (Rendered at pose-driven coords)
    if pose.has_prop and self.prop_drawer:
      glPushMatrix()
      glTranslatef(pose.prop_pos[0], pose.prop_pos[1] + bob, pose.prop_pos[2])
      glRotatef(pose.prop_rot[0], 1, 0, 0)
      glRotatef(pose.prop_rot[1], 0, 1, 0)
      glRotatef(pose.prop_rot[2], 0, 0, 1)
      self.prop_drawer()
      glPopMatrix()

    # 5. LEGS
    for side, sign, leg_angles in [(0.14, 1.0, pose.leg_l), (-0.14, -1.0, pose.leg_r)]:
      glPushMatrix()
      glTranslatef(side, 0.90 + bob, 0.0)
      glRotatef(leg_angles[0], 1, 0, 0)
      glRotatef(leg_angles[1], 0, 1, 0)

      glPushMatrix()
      glTranslatef(0, -0.22, 0)
      glScalef(0.18, 0.44, 0.20)
      draw_cube(self.textures.get("pants"))
      glPopMatrix()

      glPushMatrix()
      glTranslatef(0, -0.44, 0)
      glPushMatrix()
      glScalef(0.16, 0.12, 0.18)
      draw_cube(self.textures.get("armor"))
      glPopMatrix()

      glRotatef(max(0.0, leg_angles[2]), 1, 0, 0)
      glPushMatrix()
      glTranslatef(0, -0.20, 0)
      glScalef(0.16, 0.40, 0.18)
      draw_cube(self.textures.get("pants"))
      glPopMatrix()

      glPushMatrix()
      glTranslatef(0, -0.40, 0.04)
      glScalef(0.22, 0.24, 0.32)
      draw_cube(self.textures.get("leather"))
      glPopMatrix()
      glPopMatrix()
      glPopMatrix()