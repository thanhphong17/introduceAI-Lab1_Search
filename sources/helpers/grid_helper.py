# src/helpers/grid_helper.py

def find_stone_positions(grid):
    stone_positions = []
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == '$':
                stone_positions.append((i, j))
    return stone_positions

def map_weights_to_stones(stone_positions, weights):
    stone_weights = {}
    for idx, pos in enumerate(stone_positions):
        stone_weights[pos] = weights[idx] if idx < len(weights) else 1
    return stone_weights


# src/helpers/grid_helper.py

def find_start_goal(grid):
    start = None
    goal = None
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == '@':
                start = (i, j)
            elif cell == '.':
                goal = (i, j)
    return start, goal
# src/helpers/grid_helper.py

def get_neighbors(position):
    """
    Trả về danh sách các ô kề với vị trí hiện tại.
    Các ô kề được tính là trên, dưới, trái, phải.
    """
    x, y = position
    return [
        (x - 1, y),  # Ô trên
        (x + 1, y),  # Ô dưới
        (x, y - 1),  # Ô bên trái
        (x, y + 1)   # Ô bên phải
    ]

def is_valid_move(grid, position):
    """
    Kiểm tra xem vị trí có hợp lệ để di chuyển hay không.
    Điều kiện hợp lệ là vị trí trong phạm vi của lưới và không phải là tường ('#').
    """
    x, y = position
    rows = len(grid)
    cols = len(grid[0])

    # Kiểm tra xem vị trí có nằm trong phạm vi của lưới không
    if 0 <= x < rows and 0 <= y < cols:
        # Kiểm tra ô không phải là tường
        return grid[x][y] != '#'
    return False


def reconstruct_path(parent, start, goal):
    """
    Tái tạo đường đi từ điểm bắt đầu (start) đến điểm đích (goal)
    bằng cách đi ngược từ goal về start qua các nút cha trong parent.

    Args:
        parent (dict): Từ điển lưu cha của mỗi vị trí trên đường đi.
        start (tuple): Vị trí bắt đầu.
        goal (tuple): Vị trí đích.

    Returns:
        list: Danh sách các bước di chuyển từ start đến goal.
    """
    path = []
    current = goal

    # Duyệt ngược từ goal về start
    while current != start:
        path.append(current)
        current = parent[current]

        # Nếu không tìm thấy đường đi, thoát và trả về đường đi trống
        if current is None:
            return []

    # Thêm vị trí bắt đầu và đảo ngược đường đi để có thứ tự từ start đến goal
    path.append(start)
    path.reverse()
    return path
