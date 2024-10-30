# src/gui/gui.py
import pygame
from sources.algorithms import *
from sources.helpers import *

class MazeGUI:
    def __init__(self, grid, stone_weights):
        pygame.init()

        # Thiết lập kích thước của mỗi ô và cửa sổ
        self.cell_size = 80
        self.grid = grid
        self.stone_weights = stone_weights
        self.maze_width = len(grid[0]) * self.cell_size
        self.maze_height = len(grid) * self.cell_size
        self.sidebar_width = 150  # Chiều rộng của phần chứa nút
        self.width = self.maze_width + self.sidebar_width
        self.height = self.maze_height

        # Khởi tạo màn hình pygame với kích thước mới
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Ares's Adventure Maze")

        # Định nghĩa các nút cho các thuật toán ở bên trái
        self.buttons = {
            "BFS": pygame.Rect(10, 10, 80, 40),
            "DFS": pygame.Rect(10, 60, 80, 40),
            "UCS": pygame.Rect(10, 110, 80, 40),
            "A*": pygame.Rect(10, 160, 80, 40)
        }

        # Biến để lưu số bước và tổng trọng lượng
        self.steps = 0
        self.total_weight = 0

    def draw_grid(self):
        # Vẽ các ô của lưới mê cung
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                x = self.sidebar_width + j * self.cell_size  # Cộng thêm `sidebar_width` để đẩy mê cung sang phải
                y = i * self.cell_size

                # Chọn màu sắc phù hợp cho từng loại ô
                if cell == '#':
                    color = (139, 69, 19)  # Màu đen cho tường
                elif cell == ' ':
                    color = (255, 255, 255)  # Màu trắng cho ô trống
                elif cell == '$':
                    color = (169, 169, 169)  # Màu xám cho viên đá
                elif cell == '.':
                    color = (0, 0, 255)  # Màu xanh nước biển cho công tắc
                elif cell == '@':
                    color = (255, 0, 0)  # Màu đỏ cho Ares
                else:
                    color = (255, 255, 255)  # Mặc định là màu trắng

                # Vẽ ô vuông trên màn hình
                pygame.draw.rect(self.screen, color, (x, y, self.cell_size, self.cell_size))

                # Nếu là viên đá, hiển thị trọng lượng của nó
                if cell == '$':
                    font = pygame.font.Font(None, 24)
                    stone_weight = self.stone_weights.get((i, j), 1)
                    text = font.render(str(stone_weight), True, (255, 255, 255))
                    text_rect = text.get_rect(center=(x + self.cell_size / 2, y + self.cell_size / 2))
                    self.screen.blit(text, text_rect)

    def draw_buttons(self):
        # Thiết lập phông chữ cho văn bản của nút
        font = pygame.font.Font(None, 24)
        for name, rect in self.buttons.items():
            pygame.draw.rect(self.screen, (100, 100, 100), rect)  # Nền nút màu xám
            text = font.render(name, True, (255, 255, 255))  # Văn bản màu trắng
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)

    def draw_statistics(self):
        # Hiển thị số bước và tổng trọng lượng đã đẩy
        font = pygame.font.Font(None, 24)
        steps_text = font.render(f"Steps: {self.steps}", True, (255, 255, 255))
        weight_text = font.render(f"Total Weight: {self.total_weight}", True, (255, 255, 255))
        self.screen.blit(steps_text, (10, self.height - 80))
        self.screen.blit(weight_text, (10, self.height - 50))

    def animate_path(self, path):
        # Dùng để chạy animation đường đi của Ares
        previous_position = path[0]
        for position in path:
            x = self.sidebar_width + position[1] * self.cell_size
            y = position[0] * self.cell_size

            # Đánh dấu vị trí trước đó màu xanh lá
            if previous_position != position:
                prev_x = self.sidebar_width + previous_position[1] * self.cell_size
                prev_y = previous_position[0] * self.cell_size
                pygame.draw.rect(self.screen, (0, 255, 0), (prev_x, prev_y, self.cell_size, self.cell_size))

            # Kiểm tra nếu vị trí tiếp theo là đá và có thể đẩy
            if self.grid[position[0]][position[1]] == '$':
                dx = position[0] - previous_position[0]
                dy = position[1] - previous_position[1]
                stone_next_pos = (position[0] + dx, position[1] + dy)

                # Đẩy đá đến vị trí mới
                if self.grid[stone_next_pos[0]][stone_next_pos[1]] == ' ':
                    # Cập nhật lưới và vẽ đá ở vị trí mới
                    self.grid[stone_next_pos[0]][stone_next_pos[1]] = '$'
                    self.grid[position[0]][position[1]] = ' '
                    stone_x = self.sidebar_width + stone_next_pos[1] * self.cell_size
                    stone_y = stone_next_pos[0] * self.cell_size
                    pygame.draw.rect(self.screen, (169, 169, 169), (stone_x, stone_y, self.cell_size, self.cell_size))

            # Vẽ Ares tại vị trí hiện tại
            self.draw_grid()  # Vẽ lại lưới để cập nhật trạng thái hiện tại
            self.draw_buttons()
            self.draw_statistics()
            pygame.draw.rect(self.screen, (255, 0, 0), (x, y, self.cell_size, self.cell_size))  # Màu đỏ cho Ares

            pygame.display.flip()
            pygame.time.delay(200)  # Độ trễ giữa mỗi bước di chuyển

            previous_position = position  # Cập nhật vị trí trước đó

    def run_algorithm(self, algorithm_name):
        if algorithm_name == "BFS":
            start, goal = find_start_goal(self.grid)
            path, self.steps, self.total_weight = bfs(start, goal, self.grid, self.stone_weights)
            self.animate_path(path)

    def handle_click(self, pos):
        # Xử lý sự kiện nhấn nút
        for name, rect in self.buttons.items():
            if rect.collidepoint(pos):
                self.run_algorithm(name)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)

            # Vẽ lưới, các nút, và hiển thị thông tin
            self.screen.fill((0, 0, 0))
            self.draw_grid()
            self.draw_buttons()
            self.draw_statistics()  # Hiển thị số bước và tổng trọng lượng đã đẩy
            pygame.display.flip()

        pygame.quit()
