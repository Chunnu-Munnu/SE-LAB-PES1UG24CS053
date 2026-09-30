import random
import pygame


class GameEngine:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        self.arm_position = 0.0
        self.target_limit = 100.0
        self.last_key = None
        
        self.stamina = 100.0
        self.max_stamina = 100.0
        self.exhaust_threshold = 10.0  # at or below this, player input is ignored...
        self.recover_threshold = 30.0  # ...until stamina climbs back to this
        self.player_exhausted = False

        self.winner = None
        self.game_state = "PLAYING"
        self.ai_strength = 0.35

        # AI surge cycle: BUILDING -> SURGE -> EXHAUSTED -> BUILDING (timers in frames @ 60 FPS)
        self.ai_force_multipliers = {"BUILDING": 1.0, "SURGE": 2.5, "EXHAUSTED": 0.3}
        self.ai_max_energy = 100.0
        self.ai_energy = 0.0
        self.ai_state = "BUILDING"
        self.ai_state_timer = 0

        self.font_big = pygame.font.SysFont(None, 44)
        self.font_med = pygame.font.SysFont(None, 26)

    def handle_event(self, event):
        if self.game_state != "PLAYING":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset()
            return

        if event.type == pygame.KEYDOWN:
            if self.is_exhausted():
                return
            
            # Player wins at -target_limit, so player force must decrease arm_position
            # (the AI in update() adds positive force toward the computer's side).
            if event.key == pygame.K_LEFT:
                if self.last_key != pygame.K_LEFT:
                    self.arm_position -= 4.2
                    self.stamina = max(0.0, self.stamina - 2.0)
                    self.last_key = pygame.K_LEFT
            elif event.key == pygame.K_RIGHT:
                if self.last_key != pygame.K_RIGHT:
                    self.arm_position -= 4.2
                    self.stamina = max(0.0, self.stamina - 2.0)
                    self.last_key = pygame.K_RIGHT

            if self.stamina <= self.exhaust_threshold:
                self.player_exhausted = True

    def is_exhausted(self):
        return self.player_exhausted

    def update(self):
        if self.game_state != "PLAYING":
            return

        self.update_ai_state()

        ai_variance = random.uniform(0.3, 1.0)
        multiplier = self.ai_force_multipliers[self.ai_state]
        self.arm_position += self.ai_strength * ai_variance * multiplier

        if self.stamina < self.max_stamina:
            self.stamina = min(self.max_stamina, self.stamina + 0.25)

        if self.player_exhausted and self.stamina >= self.recover_threshold:
            self.player_exhausted = False

        if self.arm_position <= -self.target_limit:
            self.winner = "PLAYER"
            self.game_state = "GAME_OVER"
        elif self.arm_position >= self.target_limit:
            self.winner = "COMPUTER"
            self.game_state = "GAME_OVER"

    def update_ai_state(self):
        if self.ai_state == "BUILDING":
            # Charges to full in roughly 2-3 seconds
            self.ai_energy = min(self.ai_max_energy, self.ai_energy + random.uniform(0.55, 0.85))
            if self.ai_energy >= self.ai_max_energy:
                self.ai_state = "SURGE"
                self.ai_state_timer = random.randint(60, 120)  # 1-2 seconds
        elif self.ai_state == "SURGE":
            self.ai_state_timer -= 1
            self.ai_energy = self.ai_max_energy * max(0, self.ai_state_timer) / 120
            if self.ai_state_timer <= 0:
                self.ai_state = "EXHAUSTED"
                self.ai_energy = 0.0
                self.ai_state_timer = random.randint(60, 120)  # 1-2 seconds
        elif self.ai_state == "EXHAUSTED":
            self.ai_state_timer -= 1
            if self.ai_state_timer <= 0:
                self.ai_state = "BUILDING"
                self.ai_state_timer = 0

    def reset(self):
        self.arm_position = 0.0
        self.stamina = self.max_stamina
        self.player_exhausted = False
        self.last_key = None
        self.winner = None
        self.game_state = "PLAYING"
        self.ai_energy = 0.0
        self.ai_state = "BUILDING"
        self.ai_state_timer = 0

    def render(self, screen):
        screen.fill((25, 28, 35))

        title_surf = self.font_big.render("ARM WRESTLE SHOWDOWN", True, (240, 240, 240))
        screen.blit(title_surf, (self.width // 2 - title_surf.get_width() // 2, 12))

        player_header = self.font_med.render("PLAYER", True, (80, 160, 255))
        computer_header = self.font_med.render("COMPUTER", True, (255, 100, 80))
        screen.blit(player_header, (60, 55))
        screen.blit(computer_header, (self.width - 150, 55))

        ai_state_colors = {
            "BUILDING": (230, 200, 90),
            "SURGE": (255, 60, 60),
            "EXHAUSTED": (140, 150, 170),
        }
        ai_label = "SURGE!" if self.ai_state == "SURGE" else self.ai_state
        ai_state_surf = self.font_med.render(ai_label, True, ai_state_colors[self.ai_state])
        screen.blit(ai_state_surf, (self.width - 150, 78))

        table_rect = pygame.Rect(40, 100, self.width - 80, 310)
        pygame.draw.rect(screen, (110, 50, 15), table_rect, border_radius=14)
        pygame.draw.rect(screen, (70, 30, 8), table_rect, width=5, border_radius=14)

        pygame.draw.line(screen, (45, 18, 4), (self.width // 2, 100), (self.width // 2, 410), 4)

        offset_x = (self.arm_position / self.target_limit) * 95
        hand_x = (self.width // 2) + int(offset_x)
        hand_y = 235

        p_shoulder = (70, 330)
        p_elbow = (140, 215)
        c_shoulder = (self.width - 70, 330)
        c_elbow = (self.width - 140, 215)

        exhausted = self.is_exhausted() and self.game_state == "PLAYING"
        ticks = pygame.time.get_ticks()

        # Tremble the player's arm while exhausted. The hand stays put because the
        # computer's arm is attached to it too.
        if exhausted:
            p_shoulder = (p_shoulder[0] + random.randint(-1, 1), p_shoulder[1] + random.randint(-1, 1))
            p_elbow = (p_elbow[0] + random.randint(-3, 3), p_elbow[1] + random.randint(-3, 3))

        pygame.draw.line(screen, (200, 145, 110), p_shoulder, p_elbow, 32)
        pygame.draw.line(screen, (215, 160, 125), p_elbow, (hand_x, hand_y), 26)
        pygame.draw.circle(screen, (185, 130, 95), p_elbow, 18)

        pygame.draw.line(screen, (170, 110, 85), c_shoulder, c_elbow, 32)
        pygame.draw.line(screen, (185, 125, 95), c_elbow, (hand_x, hand_y), 26)
        pygame.draw.circle(screen, (150, 95, 70), c_elbow, 18)

        pygame.draw.circle(screen, (225, 175, 140), (hand_x, hand_y), 24)
        pygame.draw.circle(screen, (160, 115, 85), (hand_x, hand_y), 24, width=3)

        stamina_label = self.font_med.render("STAMINA", True, (220, 220, 220))
        screen.blit(stamina_label, (40, 445))

        stamina_bg = pygame.Rect(140, 448, 240, 22)
        stamina_fill = pygame.Rect(140, 448, int(240 * (self.stamina / self.max_stamina)), 22)
        if exhausted:
            # Flash the whole bar, since the fill is small while exhausted
            flash_on = (ticks // 150) % 2 == 0
            bg_color = (150, 25, 25) if flash_on else (45, 50, 60)
            bar_color = (255, 70, 70) if flash_on else (120, 20, 20)
        else:
            bg_color = (45, 50, 60)
            bar_color = (60, 210, 100) if self.stamina > 25 else (220, 60, 60)
        pygame.draw.rect(screen, bg_color, stamina_bg, border_radius=6)
        pygame.draw.rect(screen, bar_color, stamina_fill, border_radius=6)

        if exhausted and (ticks // 300) % 2 == 0:
            exhausted_surf = self.font_med.render("EXHAUSTED!", True, (255, 70, 70))
            screen.blit(exhausted_surf, (stamina_bg.right + 15, 450))

        if self.game_state == "GAME_OVER":
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            screen.blit(overlay, (0, 0))

            win_text = "PLAYER WINS THE MATCH!" if self.winner == "PLAYER" else "COMPUTER WINS!"
            color = (80, 240, 100) if self.winner == "PLAYER" else (240, 80, 80)
            text_surf = self.font_big.render(win_text, True, color)
            screen.blit(
                text_surf,
                (self.width // 2 - text_surf.get_width() // 2, self.height // 2 - 45)
            )

            restart_surf = self.font_med.render(
                "Press [R] to Rematch", True, (240, 240, 240)
            )
            screen.blit(
                restart_surf,
                (self.width // 2 - restart_surf.get_width() // 2, self.height // 2 + 10)
            )