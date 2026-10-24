import math
import sys
from entities import Player, Terminal
from guard import CyberGuard
from hud import draw_hud
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from textures import create_cyber_texture
from world import Room


def setup_lighting():
  glEnable(GL_LIGHTING)
  glEnable(GL_COLOR_MATERIAL)
  glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

  # CRITICAL: Normalize normals transformed by non-uniform glScalef
  glEnable(GL_NORMALIZE)

  # Gloomy Cyberpunk Ambient Base
  glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.08, 0.10, 0.14, 1.0])

  # Cyan Neon Light Source (Suspended over Netrunner Terminal at x=3.5, y=3.6, z=-4.0)
  glEnable(GL_LIGHT0)
  glLightfv(GL_LIGHT0, GL_POSITION, [3.5, 3.6, -4.0, 1.0])
  glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.0, 0.85, 1.0, 1.0])
  glLightfv(GL_LIGHT0, GL_SPECULAR, [0.0, 1.0, 1.0, 1.0])
  glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 1.0)
  glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)
  glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 0.015)

  # Magenta Neon Light Source (Suspended over Server Bank at x=-4.5, y=3.6, z=-7.5)
  glEnable(GL_LIGHT1)
  glLightfv(GL_LIGHT1, GL_POSITION, [-4.5, 3.6, -7.5, 1.0])
  glLightfv(GL_LIGHT1, GL_DIFFUSE, [1.0, 0.0, 0.75, 1.0])
  glLightfv(GL_LIGHT1, GL_SPECULAR, [1.0, 0.2, 0.8, 1.0])
  glLightf(GL_LIGHT1, GL_CONSTANT_ATTENUATION, 1.0)
  glLightf(GL_LIGHT1, GL_LINEAR_ATTENUATION, 0.05)
  glLightf(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, 0.015)

  # Amber Corridor Light Source (Suspended along central walkway at x=0.0, y=3.8, z=1.0)
  glEnable(GL_LIGHT2)
  glLightfv(GL_LIGHT2, GL_POSITION, [0.0, 3.8, 1.0, 1.0])
  glLightfv(GL_LIGHT2, GL_DIFFUSE, [0.75, 0.50, 0.10, 1.0])
  glLightfv(GL_LIGHT2, GL_SPECULAR, [0.50, 0.35, 0.05, 1.0])
  glLightf(GL_LIGHT2, GL_CONSTANT_ATTENUATION, 1.0)
  glLightf(GL_LIGHT2, GL_LINEAR_ATTENUATION, 0.06)
  glLightf(GL_LIGHT2, GL_QUADRATIC_ATTENUATION, 0.02)


def main():
  pygame.init()
  WIDTH, HEIGHT = 1024, 768
  pygame.display.set_mode((WIDTH, HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF)
  pygame.display.set_caption("CyberDuke: Tactical Infiltration")

  pygame.mouse.set_visible(False)
  pygame.event.set_grab(True)

  # OpenGL Setup
  glViewport(0, 0, WIDTH, HEIGHT)
  glMatrixMode(GL_PROJECTION)
  glLoadIdentity()
  gluPerspective(60, (WIDTH / HEIGHT), 0.1, 50.0)
  glMatrixMode(GL_MODELVIEW)
  glEnable(GL_DEPTH_TEST)
  glEnable(GL_BLEND)
  glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

  setup_lighting()

  # Load Complete Cyberpunk Texture Suite
  tex_wall = create_cyber_texture("wall")
  tex_floor = create_cyber_texture("floor")
  tex_metal = create_cyber_texture("metal")
  tex_locked = create_cyber_texture("terminal", hacked=False)
  tex_unlocked = create_cyber_texture("terminal", hacked=True)
  tex_hazard = create_cyber_texture("hazard")
  tex_neon_cyan = create_cyber_texture("neon_cyan")
  tex_neon_magenta = create_cyber_texture("neon_magenta")

  all_textures = {
      "wall": tex_wall,
      "floor": tex_floor,
      "metal": tex_metal,
      "terminal_locked": tex_locked,
      "terminal_unlocked": tex_unlocked,
      "hazard": tex_hazard,
      "neon_cyan": tex_neon_cyan,
      "neon_magenta": tex_neon_magenta,
      "screen_net": create_cyber_texture("screen_net"),
      "screen_radar": create_cyber_texture("screen_radar"),
      "screen_error": create_cyber_texture("screen_error"),
      "server_rack": create_cyber_texture("server_rack"),
      "crate": create_cyber_texture("crate"),
      "cardboard": create_cyber_texture("cardboard"),
      "soda_can": create_cyber_texture("soda_can"),
      "neon_sign": create_cyber_texture("neon_sign"),
      "grate": create_cyber_texture("grate"),
      "skin": create_cyber_texture("skin"),
      "shirt": create_cyber_texture("fabric"),
      "pants": create_cyber_texture("pants"),
      "leather": create_cyber_texture("leather"),
      "armor": create_cyber_texture("armor"),
  }

  guard_textures = {
      "metal": tex_metal,
      "skin": all_textures["skin"],
      "shirt": all_textures["shirt"],
      "pants": all_textures["pants"],
      "leather": all_textures["leather"],
      "armor": all_textures["armor"],
  }

  # Create World, Obstacles and Entities
  player = Player()
  room = Room(tex_wall, tex_floor, tex_hazard, tex_neon_cyan, tex_neon_magenta, textures=all_textures)
  terminal = Terminal(3.5, 0.0, -4.0, tex_metal, tex_locked, tex_unlocked, textures=all_textures)
  guard = CyberGuard(0.0, 0.0, -6.0, guard_textures)

  game_state = "PLAYING"  # "PLAYING", "CAUGHT", "WON"
  state_timer = 0.0

  clock = pygame.time.Clock()
  running = True

  def reset_game():
    nonlocal game_state, state_timer
    player.reset()
    terminal.reset()
    guard.reset()
    room.door_open = 0.0
    game_state = "PLAYING"
    state_timer = 0.0

  while running:
    dt = clock.tick(60) / 1000.0

    # Handle Events
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          running = False
        elif event.key == pygame.K_c and game_state == "PLAYING":
          player.crouching = not player.crouching
        elif event.key == pygame.K_r:
          reset_game()
      elif event.type == pygame.MOUSEMOTION and game_state == "PLAYING":
        dx, dy = event.rel
        player.yaw += dx * 0.15
        player.pitch -= dy * 0.15
        player.pitch = max(-89.0, min(89.0, player.pitch))

    keys = pygame.key.get_pressed()

    # Gameplay Logic & Movement
    if game_state == "PLAYING":
      rad = math.radians(player.yaw)
      fwd_x, fwd_z = math.cos(rad), math.sin(rad)
      strafe_x, strafe_z = math.sin(rad), -math.cos(rad)

      move_x, move_z = 0.0, 0.0
      if keys[pygame.K_w]: move_x += fwd_x; move_z += fwd_z
      if keys[pygame.K_s]: move_x -= fwd_x; move_z -= fwd_z
      if keys[pygame.K_a]: move_x += strafe_x; move_z += strafe_z
      if keys[pygame.K_d]: move_x -= strafe_x; move_z -= strafe_z

      all_obstacles = [terminal.get_bounds()] + room.get_obstacles()

      # Normalize diagonal movement speed & check physical collision
      move_len = math.hypot(move_x, move_z)
      if move_len > 0.001:
        speed = (2.0 if player.crouching else 4.5) * dt
        step_x = (move_x / move_len) * speed
        step_z = (move_z / move_len) * speed
        new_x = player.x + step_x
        new_z = player.z + step_z

        # Room bounds (Door at Z = 10.0 opens when hacked)
        can_pass_door = room.door_open > 1.8 and abs(player.x) < 1.6
        max_z = 12.0 if can_pass_door else 9.5

        # Check X movement against obstacles and perimeter walls
        if -5.5 < new_x < 5.5:
          collided_x = False
          for obs in all_obstacles:
            if (obs[0] - 0.32 <= new_x <= obs[1] + 0.32) and (obs[2] - 0.32 <= player.z <= obs[3] + 0.32):
              collided_x = True
              break
          if not collided_x:
            player.x = new_x

        # Check Z movement against obstacles and perimeter walls
        if -9.5 < new_z < max_z:
          collided_z = False
          for obs in all_obstacles:
            if (obs[0] - 0.32 <= player.x <= obs[1] + 0.32) and (obs[2] - 0.32 <= new_z <= obs[3] + 0.32):
              collided_z = True
              break
          if not collided_z:
            player.z = new_z

        # Win condition trigger
        if player.z > 10.5:
          game_state = "WON"

      # Update entities & AI vision occlusion against all room obstacles
      player.update_height(dt)
      terminal.update(player.x, player.z, keys[pygame.K_e], dt)
      guard.update(player, dt, obstacles=all_obstacles)
      room.update_door(terminal.is_hacked, dt)

      # Catch condition trigger
      if player.stealth_meter >= 100.0:
        game_state = "CAUGHT"
        state_timer = 0.0

    elif game_state == "CAUGHT":
      state_timer += dt
      if state_timer >= 1.6:
        reset_game()

    # OpenGL Render Pipeline
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    cos_p = math.cos(math.radians(player.pitch))
    sin_p = math.sin(math.radians(player.pitch))
    cos_y = math.cos(math.radians(player.yaw))
    sin_y = math.sin(math.radians(player.yaw))

    look_x = player.x + cos_p * cos_y
    look_y = player.y + sin_p
    look_z = player.z + cos_p * sin_y
    gluLookAt(player.x, player.y, player.z, look_x, look_y, look_z, 0.0, 1.0, 0.0)

    # Draw 3D Scene
    room.draw()
    terminal.draw()
    guard.draw()

    # Draw HUD & Game State Overlays
    draw_hud(player, terminal, WIDTH, HEIGHT, game_state=game_state)

    pygame.display.flip()

  pygame.quit()
  sys.exit()


if __name__ == "__main__":
  main()
