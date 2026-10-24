from OpenGL.GL import *
import pygame

_font_cache = {}


def draw_text(text, x, y, size=14, color=(255, 255, 255)):
  key = (text, size, color)
  if key not in _font_cache:
    font = pygame.font.SysFont("Arial", size, bold=True)
    surf = font.render(text, True, color)
    w, h = surf.get_size()
    data = pygame.image.tostring(surf, "RGBA", True)

    tex = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
    _font_cache[key] = (tex, w, h)

  tex, w, h = _font_cache[key]
  glEnable(GL_TEXTURE_2D)
  glBindTexture(GL_TEXTURE_2D, tex)
  glColor3f(1.0, 1.0, 1.0)
  glBegin(GL_QUADS)
  glTexCoord2f(0, 0); glVertex2f(x, y + h)
  glTexCoord2f(1, 0); glVertex2f(x + w, y + h)
  glTexCoord2f(1, 1); glVertex2f(x + w, y)
  glTexCoord2f(0, 1); glVertex2f(x, y)
  glEnd()
  glDisable(GL_TEXTURE_2D)


def draw_hud(player, terminal, width, height, game_state="PLAYING"):
  glDisable(GL_LIGHTING)
  glDisable(GL_DEPTH_TEST)

  glMatrixMode(GL_PROJECTION)
  glPushMatrix()
  glLoadIdentity()
  glOrtho(0, width, height, 0, -1, 1)

  glMatrixMode(GL_MODELVIEW)
  glPushMatrix()
  glLoadIdentity()

  # 1. Crosshair
  cx, cy = width / 2, height / 2
  glColor3f(0.0, 1.0, 1.0)
  glBegin(GL_QUADS)
  glVertex2f(cx - 2, cy - 8); glVertex2f(cx + 2, cy - 8)
  glVertex2f(cx + 2, cy - 2); glVertex2f(cx - 2, cy - 2)

  glVertex2f(cx - 2, cy + 2); glVertex2f(cx + 2, cy + 2)
  glVertex2f(cx + 2, cy + 8); glVertex2f(cx - 2, cy + 8)

  glVertex2f(cx - 8, cy - 2); glVertex2f(cx - 2, cy - 2)
  glVertex2f(cx - 2, cy + 2); glVertex2f(cx - 8, cy + 2)

  glVertex2f(cx + 2, cy - 2); glVertex2f(cx + 8, cy - 2)
  glVertex2f(cx + 8, cy + 2); glVertex2f(cx + 2, cy + 2)
  glEnd()

  # 2. Stealth Meter Bar
  bar_w, bar_h = 260, 14
  bar_x, bar_y = (width - bar_w) / 2, 45

  draw_text("DETECTION LEVEL", bar_x, bar_y - 18, size=13, color=(200, 240, 255))

  glColor3f(0.1, 0.1, 0.15)
  glBegin(GL_QUADS)
  glVertex2f(bar_x, bar_y); glVertex2f(bar_x + bar_w, bar_y)
  glVertex2f(bar_x + bar_w, bar_y + bar_h); glVertex2f(bar_x, bar_y + bar_h)
  glEnd()

  fill_w = (player.stealth_meter / 100.0) * bar_w
  if player.stealth_meter > 50:
    glColor3f(1.0, 0.2, 0.2)
  elif player.stealth_meter > 20:
    glColor3f(1.0, 0.8, 0.0)
  else:
    glColor3f(0.0, 0.8, 1.0)

  if fill_w > 0:
    glBegin(GL_QUADS)
    glVertex2f(bar_x, bar_y); glVertex2f(bar_x + fill_w, bar_y)
    glVertex2f(bar_x + fill_w, bar_y + bar_h); glVertex2f(bar_x, bar_y + bar_h)
    glEnd()

  glColor3f(0.0, 1.0, 1.0)
  glLineWidth(2.0)
  glBegin(GL_LINE_LOOP)
  glVertex2f(bar_x, bar_y); glVertex2f(bar_x + bar_w, bar_y)
  glVertex2f(bar_x + bar_w, bar_y + bar_h); glVertex2f(bar_x, bar_y + bar_h)
  glEnd()

  # 3. Terminal Progress Bar
  if terminal.progress > 0 or terminal.is_hacked:
    h_bar_w, h_bar_h = 220, 12
    h_bar_x, h_bar_y = (width - h_bar_w) / 2, 85

    draw_text(
        "TERMINAL HACK" if not terminal.is_hacked else "TERMINAL HACKED",
        h_bar_x,
        h_bar_y - 18,
        size=13,
        color=(100, 255, 150),
    )

    glColor3f(0.1, 0.15, 0.1)
    glBegin(GL_QUADS)
    glVertex2f(h_bar_x, h_bar_y); glVertex2f(h_bar_x + h_bar_w, h_bar_y)
    glVertex2f(h_bar_x + h_bar_w, h_bar_y + h_bar_h); glVertex2f(h_bar_x, h_bar_y + h_bar_h)
    glEnd()

    h_fill_w = (terminal.progress / 100.0) * h_bar_w
    glColor3f(0.0, 1.0, 0.4)
    if h_fill_w > 0:
      glBegin(GL_QUADS)
      glVertex2f(h_bar_x, h_bar_y); glVertex2f(h_bar_x + h_fill_w, h_bar_y)
      glVertex2f(h_bar_x + h_fill_w, h_bar_y + h_bar_h); glVertex2f(h_bar_x, h_bar_y + h_bar_h)
      glEnd()

    glColor3f(0.0, 1.0, 0.4)
    glBegin(GL_LINE_LOOP)
    glVertex2f(h_bar_x, h_bar_y); glVertex2f(h_bar_x + h_bar_w, h_bar_y)
    glVertex2f(h_bar_x + h_bar_w, h_bar_y + h_bar_h); glVertex2f(h_bar_x, h_bar_y + h_bar_h)
    glEnd()

  # 4. GAME OVER SCREEN (COMPROMISED)
  if game_state == "CAUGHT":
    glColor4f(0.9, 0.05, 0.05, 0.45)
    glBegin(GL_QUADS)
    glVertex2f(0, 0); glVertex2f(width, 0)
    glVertex2f(width, height); glVertex2f(0, height)
    glEnd()
    draw_text("ALERT! COMPROMISED!", (width - 240) / 2, height / 2 - 20, size=22, color=(255, 60, 60))
    draw_text("RESPAWNING...", (width - 120) / 2, height / 2 + 15, size=15, color=(255, 200, 200))

  # 5. VICTORY SCREEN
  elif game_state == "WON":
    glColor4f(0.0, 0.25, 0.20, 0.70)
    glBegin(GL_QUADS)
    glVertex2f(0, 0); glVertex2f(width, 0)
    glVertex2f(width, height); glVertex2f(0, height)
    glEnd()
    draw_text("MISSION ACCOMPLISHED!", (width - 290) / 2, height / 2 - 35, size=24, color=(80, 255, 170))
    draw_text("FACILITY INFILTRATED & ESCAPED", (width - 250) / 2, height / 2 + 5, size=15, color=(190, 255, 220))
    draw_text("PRESS [R] TO REPLAY OR [ESC] TO QUIT", (width - 280) / 2, height / 2 + 40, size=13, color=(150, 220, 200))

  # Restore state
  glPopMatrix()
  glMatrixMode(GL_PROJECTION)
  glPopMatrix()
  glMatrixMode(GL_MODELVIEW)

  glEnable(GL_DEPTH_TEST)
  glEnable(GL_LIGHTING)
  glColor3f(1.0, 1.0, 1.0)