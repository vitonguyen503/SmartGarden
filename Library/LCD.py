# install pygame to run: pip install
import pygame

class LCD1602:
    def __init__(self, width=500, height=100, num_lines=2, num_cols=32, address=0x27):
        pygame.init()
        self.width = width
        self.height = height
        self.address = address
        self.num_lines = num_lines
        self.num_cols = num_cols
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("LCD")
        self.font = pygame.font.Font(pygame.font.match_font('courier'), 24)
        self.lines = ["" for _ in range(self.num_lines)]  # Support for more lines
        self.backlight = True
        self.cursor_visible = False
        self.cursor_position = (0, 0)

        self.clear()

    def clear(self):
        self.lines = ["" for _ in range(self.num_lines)]
        self.display()

    def write_string(self, text):
        for i in range(self.num_lines):
            if self.lines[i] == "":
                self.lines[i] = text[:self.num_cols]  # Write only up to num_cols characters per line
                break
        self.display()

    def write_char(self, char):
        row, col = self.cursor_position
        if col < self.num_cols:
            self.lines[row] = self.lines[row][:col] + char + self.lines[row][col + 1:]
            self.cursor_position = (row, col + 1)
            self.display()

    def set_cursor(self, row, col):
        if row < self.num_lines and col < self.num_cols:
            self.cursor_position = (row, col)

    def cursor_on(self):
        self.cursor_visible = True
        self.display()

    def cursor_off(self):
        self.cursor_visible = False
        self.display()

    def backlight_on(self):
        self.backlight = True
        self.display()

    def backlight_off(self):
        self.backlight = False
        self.display()

    def home(self):
        self.cursor_position = (0, 0)
        self.display()

    def display(self):
        self.screen.fill((0, 0, 0))  # Black background
        for i in range(self.num_lines):
            text = self.lines[i]
            rendered_text = self.font.render(text, True, (0, 255, 0) if self.backlight else (50, 50, 50))
            # Position each line vertically
            self.screen.blit(rendered_text, (10, i * 30))

        if self.cursor_visible:
            cursor_x = 10 + self.cursor_position[1] * 15
            cursor_y = self.cursor_position[0] * 30
            pygame.draw.line(self.screen, (255, 0, 0), (cursor_x, cursor_y), (cursor_x, cursor_y + 30), 2)

        pygame.display.flip()

    def close(self):
        pygame.quit()
