import pygame

class LCD1602:
    def __init__(self, width=300, height=150, address=0x27):  # Điều chỉnh kích thước để phù hợp với 5 dòng
        # Khởi tạo Pygame
        pygame.init()
        self.width = width
        self.height = height
        self.address = address
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("LCD1602")
        self.font = pygame.font.Font(pygame.font.match_font('courier'), 24)
        self.lines = [""] * 5  # 5 dòng
        self.backlight = True
        self.cursor_visible = False
        self.cursor_position = (0, 0)

        self.clear()

    def clear(self):
        self.lines = [""] * 5  # Xóa tất cả 5 dòng
        self.display()

    def write_string(self, text):
        # Ghi chuỗi vào các dòng còn trống
        for i in range(5):
            if self.lines[i] == "":
                self.lines[i] = text[:18]  # Chỉ ghi tối đa 16 ký tự
                break
        self.display()

    def write_char(self, char):
        row, col = self.cursor_position
        if col < 18:
            self.lines[row] = self.lines[row][:col] + char + self.lines[row][col + 1:]
            self.cursor_position = (row, col + 1)
            self.display()

    def set_cursor(self, row, col):
        if row < 5 and col < 18:  # Điều chỉnh để phù hợp với 5 dòng
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
        self.screen.fill((0, 0, 0))  # Màu nền đen
        for i in range(5):
            text = self.lines[i]
            rendered_text = self.font.render(text, True, (0, 255, 0) if self.backlight else (50, 50, 50))
            # Đặt vị trí hiển thị cho từng dòng, mỗi dòng cách nhau 30 pixel
            self.screen.blit(rendered_text, (10, i * 30)) 

        if self.cursor_visible:
            cursor_x = 10 + self.cursor_position[1] * 15
            cursor_y = self.cursor_position[0] * 30
            pygame.draw.line(self.screen, (255, 0, 0), (cursor_x, cursor_y), (cursor_x, cursor_y + 30), 2)

        pygame.display.flip()

    def close(self):
        pygame.quit()
