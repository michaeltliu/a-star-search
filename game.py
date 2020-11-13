import pygame, sys, random, math
from queue import PriorityQueue

pygame.init()

WIDTH_PIX, HEIGHT_PIX = 640, 480
BLOCK_SIZE = 20

WIDTH = int(WIDTH_PIX / BLOCK_SIZE)
HEIGHT = int(HEIGHT_PIX / BLOCK_SIZE)

screen = pygame.display.set_mode((WIDTH_PIX, HEIGHT_PIX))
screen.fill([255,255,255])

def magnitude(tup):
    return math.sqrt(tup[0]**2 + tup[1]**2)

def on_grid(x, y):
    return x >= 0 and x < WIDTH and y >= 0 and y < HEIGHT

def generate_obstacles():
    n = WIDTH * HEIGHT
    l = []

    # Randomly fills ~35% of blocks with an obstacle
    for i in range(int(n)):
        # Leave TL and BR corners open for start and target
        if i == 0 or i == int(n) - 1:
            continue
        
        if random.random() < 0.35:
            l.append(i)
    
    return l

# Draw grid lines and obstacles
for i in range(WIDTH):
    pygame.draw.line(screen, (0,0,0), (i * BLOCK_SIZE, 0), (i * BLOCK_SIZE, HEIGHT_PIX))
for i in range(HEIGHT):
    pygame.draw.line(screen, (0,0,0), (0, i * BLOCK_SIZE), (WIDTH_PIX, i * BLOCK_SIZE))

obstacles = generate_obstacles()
for obs in obstacles:
    row = int(obs / WIDTH)
    col = obs % WIDTH
    screen.fill([0,0,0], pygame.Rect(col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

screen.fill([0,0,255], pygame.Rect(0, 0, BLOCK_SIZE, BLOCK_SIZE))
screen.fill([255,0,0], pygame.Rect(WIDTH_PIX - BLOCK_SIZE, HEIGHT_PIX - BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

pygame.display.update()

q = PriorityQueue()
q.put((0,0,0))
visited = set()
visited.add(0)

movement_directions = [(1,0), (1,1), (0,1), (-1,1), (-1,0), (-1,-1), (0,-1), (1,-1)]
running = True

# We are using a consistent heuristic (Euclidean distance) so we can omit a few steps from 
# the typical A* search.
while running and not q.empty():
    F, dist, loc = q.get()
    print(F, dist, loc)
    row = int(loc / WIDTH)
    col = loc % WIDTH

    screen.fill([0,0,255], pygame.Rect(col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
    pygame.display.update()
    pygame.time.delay(200)
    
    for dir in movement_directions:
        nrow = row + dir[1]
        ncol = col + dir[0]
        nloc = nrow * WIDTH + ncol

        if not on_grid(ncol, nrow):
            continue

        if nloc == WIDTH * HEIGHT - 1:
            running = False
            break
        
        if nloc not in visited and nloc not in obstacles:
            heuristic = magnitude((WIDTH - 1 - ncol, HEIGHT - 1 - nrow))
            f_val = dist + magnitude(dir) + heuristic
            q.put((f_val, dist + magnitude(dir), nloc))
            visited.add(nloc)

if running:
    print("No path to target")
else:
    print("Reached target")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
