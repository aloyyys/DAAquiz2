import pygame
import random
import os

# Constants
WIDTH = 800
HEIGHT = 600
CELL_SIZE = 20
DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]
DIRECTION_KEYS = {
    pygame.K_w: (-1, 0),  # Up
    pygame.K_s: (1, 0),   # Down
    pygame.K_a: (0, -1),  # Left
    pygame.K_d: (0, 1)    # Right
}

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

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
    cells = [(y, x) for y in range(height) for x in range(width)]
    random.shuffle(cells)
    for cell in cells:
        if maze[cell[0]][cell[1]] == 0:
            return cell
    return None  # No accessible cell found

def draw_maze(screen, maze, player_pos, goal_pos):
    height, width = len(maze), len(maze[0])
    for y in range(height):
        for x in range(width):
            color = WHITE if maze[y][x] == 0 else BLACK
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            if (y, x) == player_pos:
                pygame.draw.rect(screen, GREEN, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif (y, x) == goal_pos:
                pygame.draw.rect(screen, RED, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def main():
    pygame.init()
    width = WIDTH // CELL_SIZE
    height = HEIGHT // CELL_SIZE
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Maze Game")

    maze = create_maze(width, height)
    player_pos = (0, 0)
    goal_pos = find_accessible_goal(maze)

    if goal_pos is None:
        print("Error: Unable to find an accessible goal position.")
        return

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in DIRECTION_KEYS:
                    dy, dx = DIRECTION_KEYS[event.key]
                    new_y = player_pos[0] + dy
                    new_x = player_pos[1] + dx
                    if 0 <= new_y < height and 0 <= new_x < width and maze[new_y][new_x] == 0:
                        player_pos = (new_y, new_x)
                    if player_pos == goal_pos:
                        print("Congratulations! You've reached the goal!")
                        running = False

        screen.fill(BLACK)
        draw_maze(screen, maze, player_pos, goal_pos)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
