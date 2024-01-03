import pygame

def is_zeros(my_array, n):
    for i in range(n):
        if my_array[i] != 0:
            return 0
    return 1

def arr_2d(m, n):
    my_array = [[0 for i in range(n)] for j in range(m)]
    return my_array

def valid_pos(self, i, map):
    x = self.x + self.body[i][0]
    y = self.y + self.body[i][1]
    if x >= 0 and x <= map.num_cols:
        if y >= 0 and y <= map.num_rows:
            return 1
    else:
        return 0
    
class Target:
    def __init__(self):
        self.x = 5
        self.y = 1
        # Define rest of block in 2D array relative to lead block
        self.body = arr_2d(3,2)
        self.type = "square"
        self.angle = 0
        if self.type == "square":
            self.type_int = 1
            self.body[0][0] = 1
            self.body[0][1] = 0
            self.body[1][0] = 1
            self.body[1][1] = -1
            self.body[2][0] = 0
            self.body[2][1] = -1
    
    def update_map_int(self, map, n):
        map.arr[self.y][self.x] = n
        for i in range(3):
            if valid_pos(self, i, map) == 1:
                map.arr[self.y + self.body[i][1]][self.x + self.body[i][0]] = n

    def update_map(self, map):
        self.update_map_int(map, self.type_int)

    def next_blocks(self, map, dir):
        match dir:
            case "a":
                next_x = self.x - 1
                next_y = self.y
            case "d":
                next_x = self.x + 1
                next_y = self.y
            case "s":
                next_x = self.x
                next_y = self.y + 1
                
                
        if map.arr[next_y][next_x] != 0:
            return 0
        for i in range(3):
            if map.arr[next_y + self.body[i][1]][next_x + self.body[i][0]] != 0:
                return 0
        return 1
        

    def move_down(self, map):
        
        self.update_map_int(map, 0)
        if self.next_blocks(map, "s") == 1:
            self.update_map_int(map, 0)
            self.y += 1
        else:
            self.update_map(map)

    def move_left(self, map):
        self.update_map_int(map, 0)
        if self.x > 0 and self.next_blocks(map, "a") == 1:
            self.x -= 1
        else:
            self.update_map(map)

    def move_right(self, map):
        self.update_map_int(map, 0)
        if self.x < map.num_cols - 2 and self.next_blocks(map, "d") == 1:
            self.update_map_int(map, 0)
            self.x += 1
        else:
            self.update_map(map)
    def check_finish(self, map):
        self.update_map_int(map, 0)
        if self.y == map.num_rows - 1:
            return 1
        elif map.arr[self.y + 1][self.x] != 0:
            return 1
        for i in range(3):
            if self.y + self.body[i][1] == map.num_rows - 1:
                return 1
            elif map.arr[self.y + self.body[i][1] + 1][self.x + self.body[i][0]] != 0:
                return 1
        return 0
    def reset(self):
        self.x = 5
        self.y = 1

class Map:
    def __init__(self):
        self.num_cols = 10
        self.num_rows = 20
        self.arr = arr_2d(self.num_rows, self.num_cols)
        self.arr[6][0] = 2
        self.arr[6][1] = 2
        self.arr[6][2] = 2
        self.arr[6][3] = 2
        self.arr[6][4] = 2
        self.arr[6][7] = 2
        self.arr[6][8] = 2
        self.arr[6][9] = 2
        self.arr[7][0] = 2
        self.arr[7][1] = 2
        self.arr[7][2] = 2
        self.arr[7][3] = 2
        self.arr[7][4] = 2
        self.arr[8][5] = 3
        self.arr[8][6] = 3
        self.arr[7][7] = 2
        self.arr[7][8] = 2
        self.arr[7][9] = 2
        self.arr[19][0] = 3
        self.arr[19][5] = 2
        self.to_be_removed = [0 for i in range(self.num_rows)]

    def draw_blocks(self, screen):
        block_width = screen.get_width()/10
        red = (255,0,0)
        green = (0,255,0)
        blue = (0,0,255)
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                if self.arr[i][j] == 1:
                    pygame.draw.rect(screen, red, pygame.Rect(j*block_width, i*block_width, block_width, block_width))
                elif self.arr[i][j] == 2:
                    pygame.draw.rect(screen, green, pygame.Rect(j*block_width, i*block_width, block_width, block_width))
                elif self.arr[i][j] == 3:
                    pygame.draw.rect(screen, blue, pygame.Rect(j*block_width, i*block_width, block_width, block_width))

    def check_rows(self):
        
        self.to_be_removed = [1 for i in range(self.num_rows)]
        
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                if self.arr[i][j] == 0:
                    self.to_be_removed[i] = 0
                    break
        if is_zeros(map.to_be_removed, map.num_rows):
            return 0
        else:
            return 1
    
    def remove_rows(self):
        for i in range(self.num_rows):
            if self.to_be_removed[i] == 1:
                for j in range(self.num_cols):
                    self.arr[i][j] = 0
        
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 1000
TIME_PER_FRAME = 1000
time_previous_tick = 0
clock_slow = pygame.time.Clock()
clock_fast = pygame.time.Clock()
score = 0
print(score)

map = Map()
target = Target()
# Initializing Pygame
pygame.init()
 
# Initializing surface
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
map.draw_blocks(screen)


run = True
while run:

    # Fast commands
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            # checking if key "A" was pressed
            if event.key == pygame.K_a:
                target.move_left(map)
            if event.key == pygame.K_d:
                target.move_right(map)

    # Slow commands
    
    time_since_slow_tick = pygame.time.get_ticks() - time_previous_tick
    if time_since_slow_tick >= TIME_PER_FRAME or time_since_slow_tick == 0:
        time_previous_tick = pygame.time.get_ticks()
        if target.check_finish(map) == 1:
            target.update_map(map)
            target.reset()
            score += 1
            print(score)
            if map.check_rows():
                map.remove_rows()

        if target.y < map.num_rows - 1:  
            target.move_down(map)

    screen.fill((0,0,0))
    target.update_map(map)
    map.draw_blocks(screen)
    pygame.display.update()
    clock_fast.tick(60)
    

pygame.quit()