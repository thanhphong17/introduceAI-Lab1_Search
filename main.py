# main.py
import pygame
from sources.helpers.grid_helper import *
from sources.gui.gui import *
from sources.helpers.file_handler import  *

if __name__ == "__main__":
    # Đọc dữ liệu từ file
    grid, weights = load_maze("./testcase/input-01.txt")

    # Tìm vị trí viên đá và ánh xạ trọng lượng
    stone_positions = find_stone_positions(grid)
    stone_weights = map_weights_to_stones(stone_positions, weights)

    # Khởi tạo và hiển thị GUI
    gui = MazeGUI(grid, stone_weights)
    gui.run()
