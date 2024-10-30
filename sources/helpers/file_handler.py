# src/helpers/file_handler.py
def load_maze(file_path):
    with open(file_path, 'r') as f:
        weights = list(map(int, f.readline().strip().split()))
        grid = [list(line.rstrip()) for line in f if line.strip()]
    return grid, weights
