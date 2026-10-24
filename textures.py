import numpy as np
from OpenGL.GL import *


def create_cyber_texture(style="grid", hacked=False):
  img = np.zeros((64, 64, 3), dtype=np.uint8)

  if style == "grid":
    img[:] = [15, 18, 28]
    img[::8, :] = [0, 180, 240]
    img[:, ::8] = [0, 180, 240]
  elif style == "terminal":
    if hacked:
      img[:] = [10, 40, 20]
      img[24:40, 24:40] = [0, 255, 100]
    else:
      img[:] = [40, 10, 10]
      img[24:40, 24:40] = [255, 50, 50]
  elif style == "metal":
    noise = np.random.randint(-15, 15, (64, 64, 3), dtype=np.int16)
    base = np.array([45, 48, 55], dtype=np.int16)
    img = np.clip(base + noise, 0, 255).astype(np.uint8)
    img[:, ::8] += 10
  elif style == "hazard":
    img[:] = [30, 30, 30]
    for i in range(64):
      if (i // 8) % 2 == 0:
        img[i, :] = [200, 160, 0]
  elif style == "skin":
    # Base skin tone with facial shading details
    img[:] = [210, 172, 148]
    # Nose shadow contours (center region)
    img[28:36, 28:36] = [170, 130, 110]
    img[30:34, 30:34] = [225, 185, 160]
    # Ear helix/spiral shading (sides)
    img[20:44, 4:12] = [150, 110, 90]
    img[24:40, 6:10] = [190, 150, 125]
    img[20:44, 52:60] = [150, 110, 90]
    img[24:40, 54:58] = [190, 150, 125]
    # Mouth / Smirk shadow
    img[44:48, 26:38] = [140, 70, 70]
  elif style == "fabric":
    img[:] = [35, 40, 50]
    img[::4, :] -= 12
    img = np.clip(img, 0, 255).astype(np.uint8)
  elif style == "pants":
    img[:] = [20, 22, 30]
    img[:, ::6] -= 8
    img = np.clip(img, 0, 255).astype(np.uint8)
  elif style == "leather":
    img[:] = [25, 20, 16]
    img[::8, :] = [40, 32, 24]
  elif style == "armor":
    img[:] = [35, 38, 45]
    img[::2, ::2] = [55, 60, 70]
  elif style == "neon_cyan":
    img[:] = [0, 240, 255]
  elif style == "neon_magenta":
    img[:] = [255, 0, 180]

  tex_id = glGenTextures(1)
  glBindTexture(GL_TEXTURE_2D, tex_id)
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
  glTexImage2D(
      GL_TEXTURE_2D, 0, GL_RGB, 64, 64, 0, GL_RGB, GL_UNSIGNED_BYTE, img
  )
  return tex_id