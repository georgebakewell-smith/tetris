import pygame
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
    def update_map(self, map):
        map.arr[self.y][self.x] = self.type_int
        for i in range(3):
            if valid_pos(self, i, map) == 1:
                map.arr[self.y + self.body[i][1]][self.x + self.body[i][0]] = self.type_int
                            

class Map:
    def __init__(self):
        self.num_cols = 10
        self.num_rows = 20
        self.arr = arr_2d(self.num_rows, self.num_cols)

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


        pygame.display.update()
        
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 1000

map = Map()
target = Target()
# Initializing Pygame
pygame.init()
 
# Initializing surface
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
map.draw_blocks(screen)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            # checking if key "A" was pressed
            if event.key == pygame.K_a:
                target.update_map(map)
    map.draw_blocks(screen)
    pygame.display.update()

pygame.quit()

array = arr_2d(3,2)