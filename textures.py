import numpy as np
from OpenGL.GL import *


def create_cyber_texture(style="grid", hacked=False):
  img = np.zeros((64, 64, 3), dtype=np.uint8)

  if style in ("grid", "wall"):
    # Dark grungy industrial wall plating with seam grooves, rivets, and scratches
    img[:] = [18, 20, 26]
    # Seam lines
    img[::32, :] = [36, 42, 54]
    img[:, ::32] = [36, 42, 54]
    img[1::32, :] = [8, 10, 14]
    img[:, 1::32] = [8, 10, 14]
    # Subtle panel grain noise
    np.random.seed(42)
    noise = np.random.randint(-4, 5, (64, 64, 3), dtype=np.int16)
    img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    # Rivet heads near panel corners
    for r in [4, 28, 36, 60]:
      for c in [4, 28, 36, 60]:
        img[r-1:r+2, c-1:c+2] = [70, 76, 95]
        img[r, c] = [120, 132, 160]

  elif style == "floor":
    # Scuffed concrete and industrial metal floor tiles with perimeter joint grooves
    base = np.array([28, 30, 36], dtype=np.int16)
    np.random.seed(1337)
    noise = np.random.randint(-7, 8, (64, 64, 3), dtype=np.int16)
    img = np.clip(base + noise, 0, 255).astype(np.uint8)
    # Tile seams
    img[0, :] = [12, 14, 18]
    img[63, :] = [12, 14, 18]
    img[:, 0] = [12, 14, 18]
    img[:, 63] = [12, 14, 18]
    # Scuffs & scratch marks
    img[16:20, 12:44] = np.clip(img[16:20, 12:44].astype(np.int16) - 10, 0, 255).astype(np.uint8)
    img[42:45, 22:54] = np.clip(img[42:45, 22:54].astype(np.int16) + 16, 0, 255).astype(np.uint8)

  elif style == "terminal":
    if hacked:
      # Decrypted root terminal: Matrix cyber green with status banner and code streams
      img[:] = [6, 26, 14]
      img[::2, :] = (img[::2, :] * 0.65).astype(np.uint8)
      # Header banner: "SYSTEM OVERRIDE"
      img[4:12, 4:60] = [0, 180, 80]
      img[6:10, 8:56] = [200, 255, 220]
      # Green decrypted code lines
      for row in range(16, 56, 5):
        w = (row * 13) % 45 + 10
        img[row:row+2, 6:6+w] = [0, 255, 100]
        if row % 10 == 1:
          img[row:row+2, 6+w+4:6+w+12] = [180, 255, 200]
    else:
      # Locked high-security terminal: Crimson alert with padlock icon & hex memory dumps
      img[:] = [32, 8, 10]
      img[::2, :] = (img[::2, :] * 0.65).astype(np.uint8)
      # Red warning header: "ACCESS DENIED"
      img[4:12, 4:60] = [180, 20, 20]
      img[6:10, 8:56] = [255, 180, 180]
      # Red padlock box
      img[20:44, 20:44] = [200, 30, 30]
      img[24:40, 24:40] = [60, 10, 12]
      img[28:36, 28:36] = [255, 60, 60]
      for row in [48, 54]:
        img[row:row+2, 8:56:4] = [255, 80, 80]

  elif style == "screen_net":
    # Auxiliary monitor: Blue/Cyan network diagnostic topology & data bus
    img[:] = [6, 16, 28]
    img[::2, :] = (img[::2, :] * 0.7).astype(np.uint8)
    img[::16, :] = np.clip(img[::16, :].astype(np.int16) + 24, 0, 255).astype(np.uint8)
    img[:, ::16] = np.clip(img[:, ::16].astype(np.int16) + 24, 0, 255).astype(np.uint8)
    nodes = [(16, 16), (48, 16), (32, 32), (16, 48), (48, 48)]
    for ny, nx in nodes:
      img[ny-3:ny+4, nx-3:nx+4] = [0, 200, 255]
      img[ny-1:ny+2, nx-1:nx+2] = [255, 255, 255]
    img[16, 16:48] = [0, 140, 200]
    img[48, 16:48] = [0, 140, 200]
    img[16:48, 32] = [0, 140, 200]

  elif style == "screen_radar":
    # Auxiliary monitor: Amber radar sweep & biometric oscilloscope wave
    img[:] = [26, 18, 6]
    img[::2, :] = (img[::2, :] * 0.7).astype(np.uint8)
    cy, cx = 32, 32
    y, x = np.ogrid[:64, :64]
    dist = np.sqrt((x - cx)**2 + (y - cy)**2)
    img[np.abs(dist - 22) < 1.3] = [255, 190, 0]
    img[np.abs(dist - 12) < 1.0] = [180, 130, 0]
    img[32, 10:54] = [255, 180, 0]
    img[10:54, 32] = [255, 180, 0]
    img[22:25, 40:43] = [255, 255, 180]

  elif style == "screen_error":
    # Glitch / static noise & error banner
    np.random.seed(99)
    noise = np.random.randint(20, 140, (64, 64, 3), dtype=np.uint8)
    img[:] = noise
    img[:, :, 0] = np.clip(img[:, :, 0] * 1.4, 0, 255)
    img[22:42, 4:60] = [200, 0, 100]
    img[26:38, 8:56] = [255, 255, 255]

  elif style == "server_rack":
    # High-density blade servers with arrays of flashing green/amber/cyan LEDs & fan grilles
    img[:] = [14, 15, 18]
    for row in range(0, 64, 8):
      img[row, :] = [46, 50, 58]
      img[row+1, :] = [6, 8, 10]
      img[row+2:row+4, 4:40:3] = [28, 30, 36]
      # LED status banks
      img[row+2:row+4, 44:47] = [0, 255, 120]
      img[row+2:row+4, 50:53] = [0, 220, 255]
      img[row+5:row+7, 44:47] = [255, 180, 0]
      img[row+5:row+7, 50:53] = [0, 255, 120]
      img[row+3:row+6, 56:60] = [22, 22, 26]

  elif style == "crate":
    # Militech / Arasaka reinforced alloy cargo crate with hazard stencil
    img[:] = [38, 42, 50]
    img[:6, :] = [62, 68, 80]
    img[-6:, :] = [20, 22, 26]
    img[:, :6] = [58, 64, 75]
    img[:, -6:] = [22, 24, 28]
    for r in [0, 52]:
      for c in [0, 52]:
        img[r:r+12, c:c+12] = [82, 90, 106]
        img[r+2:r+10, c+2:c+10] = [112, 122, 142]
        img[r+4:r+8, c+4:c+8] = [36, 40, 48]
    img[26:38, 12:52] = [220, 175, 0]
    for i in range(12, 52):
      if ((i + 26) // 4) % 2 == 0:
        img[26:38, i] = [25, 25, 25]

  elif style == "cardboard":
    # Crumpled synth-ramen noodle box with corporate red logo & stains
    base = np.array([170, 138, 98], dtype=np.int16)
    np.random.seed(7)
    noise = np.random.randint(-12, 13, (64, 64, 3), dtype=np.int16)
    img = np.clip(base + noise, 0, 255).astype(np.uint8)
    img[15:35, 18:42] = np.clip(img[15:35, 18:42].astype(np.int16) - 35, 0, 255).astype(np.uint8)
    img[20:30, 22:38] = [210, 30, 30]
    img[23:27, 25:35] = [255, 230, 180]

  elif style == "soda_can":
    # Metallic cyber-energy drink wrapper: cyan, magenta, barcode
    img[:] = [185, 190, 200]
    for y in range(64):
      for x in range(64):
        if (x + y) % 32 < 14:
          img[y, x] = [0, 220, 255]
        elif (x + y) % 32 < 22:
          img[y, x] = [255, 0, 128]
    img[44:58, 8:40] = [240, 240, 240]
    img[46:56, 10:38:3] = [20, 20, 20]
    img[46:56, 11:38:4] = [20, 20, 20]

  elif style == "neon_sign":
    # Dark panel with bright glowing Japanese Katakana: "サイバー" (CYBER)
    img[:] = [10, 8, 16]
    img[2:4, 2:62] = [255, 0, 180]
    img[60:62, 2:62] = [255, 0, 180]
    img[2:62, 2:4] = [255, 0, 180]
    img[2:62, 60:62] = [255, 0, 180]
    # 'サ'
    img[12:15, 12:52] = [0, 240, 255]
    img[8:30, 22:25] = [0, 240, 255]
    img[8:28, 40:43] = [0, 240, 255]
    # 'イ'
    img[26:48, 16:19] = [0, 240, 255]
    img[32:54, 24:27] = [0, 240, 255]
    # 'バ'
    img[30:33, 34:58] = [0, 240, 255]
    img[33:56, 44:47] = [0, 240, 255]
    img[26:30, 54:57] = [255, 0, 180]
    # 'ー'
    img[54:57, 12:52] = [0, 240, 255]

  elif style == "grate":
    # Industrial floor / ventilation drainage grate
    img[:] = [10, 12, 14]
    img[::4, :] = [52, 58, 68]
    img[:, ::8] = [62, 68, 78]

  elif style == "metal":
    np.random.seed(12)
    noise = np.random.randint(-15, 15, (64, 64, 3), dtype=np.int16)
    base = np.array([45, 48, 55], dtype=np.int16)
    img = np.clip(base + noise, 0, 255).astype(np.uint8)
    img[:, ::8] += 10

  elif style == "hazard":
    img[:] = [30, 30, 30]
    for i in range(64):
      if (i // 8) % 2 == 0:
        img[i, :] = [220, 180, 0]

  elif style == "skin":
    img[:] = [210, 172, 148]
    img[28:36, 28:36] = [170, 130, 110]
    img[30:34, 30:34] = [225, 185, 160]
    img[20:44, 4:12] = [150, 110, 90]
    img[24:40, 6:10] = [190, 150, 125]
    img[20:44, 52:60] = [150, 110, 90]
    img[24:40, 54:58] = [190, 150, 125]
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
  elif style == "neon_amber":
    img[:] = [255, 170, 0]
  elif style == "neon_green":
    img[:] = [0, 255, 120]
  else:
    img[:] = [45, 48, 55]

  tex_id = glGenTextures(1)
  glBindTexture(GL_TEXTURE_2D, tex_id)
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
  glTexImage2D(
      GL_TEXTURE_2D, 0, GL_RGB, 64, 64, 0, GL_RGB, GL_UNSIGNED_BYTE, img
  )
  return tex_id
