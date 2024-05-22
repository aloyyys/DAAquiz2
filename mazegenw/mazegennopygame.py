import random
import os

DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]
DIRECTION_KEYS = {
    "w": (-1, 0),  # Up
    "s": (1, 0),   # Down
    "a": (0, -1),  # Left
    "d": (0, 1)    # Right
}

def create_maze(width, height):
    maze = [[1 for _ in range(width)] for _ in range(height)]
    visited = [[False for _ in range(width)] for _ in range(height)]

    def is_valid(x, y):
        return 0 <= x < width and 0 <= y < height

    def dfs(x, y):
        visited[y][x] = True
        maze[y][x] = 0

        directions = random.sample(DIRECTIONS, len(DIRECTIONS))
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny) and not visited[ny][nx]:
                if is_valid(nx + dx, ny + dy) and not visited[ny + dy][nx + dx]:
                    maze[ny][nx] = 0
                    dfs(nx + dx, ny + dy)

    dfs(0, 0)
    return maze

def find_accessible_goal(maze):
    height, width = len(maze), len(maze[0])
    # Shuffle the cells to find an open cell for the goal
    cells = [(y, x) for y in range(height) for x in range(width)]
    random.shuffle(cells)
    for cell in cells:
        if maze[cell[0]][cell[1]] == 0:
            return cell
    return None  # No accessible cell found

def print_maze(maze, player_pos, goal_pos):
    os.system('cls' if os.name == 'nt' else 'clear')
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if (y, x) == player_pos:
                print("P", end="")
            elif (y, x) == goal_pos:
                print("x", end="")
            elif cell == 0:
                print(" ", end="")
            else:
                print("#", end="")
        print()
    print()

def main():
    width = int(input("Enter the width of the maze: "))
    height = int(input("Enter the height of the maze: "))
    maze = create_maze(width, height)
    player_pos = (0, 0)
    goal_pos = find_accessible_goal(maze)

    if goal_pos is None:
        print("Error: Unable to find an accessible goal position.")
        return

    while True:
        print_maze(maze, player_pos, goal_pos)
        move = input("Move (w/a/s/d) or type 'exit' to quit: ").lower()
        if move == "exit":
            print("Exiting the game. Goodbye!")
            break
        if move in DIRECTION_KEYS:
            dy, dx = DIRECTION_KEYS[move]
            new_y = player_pos[0] + dy
            new_x = player_pos[1] + dx
            if 0 <= new_y < height and 0 <= new_x < width and maze[new_y][new_x] == 0:
                player_pos = (new_y, new_x)
            if player_pos == goal_pos:
                print_maze(maze, player_pos, goal_pos)
                print("Congratulations! You've reached the goal!")
                break

if __name__ == "__main__":
    main()
