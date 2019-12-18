import pygame
pygame.font.init()


class Grid:
    # s_board = [
    #     [3,0,6,5,0,8,4,0,0],
    #     [5,2,0,0,0,0,0,0,0],
    #     [0,8,7,0,0,0,0,3,1],
    #     [0,0,3,0,1,0,0,8,0],
    #     [9,0,0,8,6,3,0,0,5],
    #     [0,5,0,0,9,0,6,0,0],
    #     [1,3,0,0,0,0,2,5,0],
    #     [0,0,0,0,0,0,0,7,4],
    #     [0,0,5,2,0,6,3,0,0]
    # ]

    s_board = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]

    def __init__(self, rows, cols, width, height, win):
        self.rows = rows
        self.cols = cols
        self.box = [[Box(self.s_board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.grid = None
        self.grid_update()
        self.choose = None
        self.win = win

    def grid_update(self):
        self.grid = [[self.box[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def allocate(self, val):
        row, col = self.choose
        if self.box[row][col].value == 0:
            self.box[row][col].set(val)
            self.grid_update()

            if valid(self.grid, val, (row,col)) and self.solve():
                return True
            else:
                self.box[row][col].set(0)
                self.box[row][col].set_temp(0)
                self.grid_update()
                return False

    def layout(self, val):
        row, col = self.choose
        self.box[row][col].set_temp(val)

    def draw(self):
        block = self.width / 9
        for i in range(self.rows+1):
            if i % 3 == 0 and i != 0:
                thickness = 4
            else:
                thickness = 1
            pygame.draw.line(self.win, (0,0,0), (0, i*block), (self.width, i*block), thickness)
            pygame.draw.line(self.win, (0,0,0), (i*block, 0), (i*block, self.height), thickness)

        for i in range(self.rows):
            for j in range(self.cols):
                self.box[i][j].draw(self.win)

    def select(self, row, col):
        for i in range(self.rows):
            for j in range(self.cols):
                self.box[i][j].choose = False

        self.box[row][col].choose = True
        self.choose = (row, col)

    def clear(self):
        row, col = self.choose
        if self.box[row][col].value == 0:
            self.box[row][col].set_temp(0)

    def click(self, pos):
        if pos[0] < self.width and pos[1] < self.height:
            block = self.width / 9
            x = pos[0] // block
            y = pos[1] // block
            return (int(y),int(x))
        else:
            return None

    def complete(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.box[i][j].value == 0:
                    return False
        return True

    def solve(self):
        find = find_empty_block(self.grid)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if valid(self.grid, i, (row, col)):
                self.grid[row][col] = i

                if self.solve():
                    return True

                self.grid[row][col] = 0

        return False

    def solve_game(self):
        find = find_empty_block(self.grid)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if valid(self.grid, i, (row, col)):
                self.grid[row][col] = i
                self.box[row][col].set(i)
                self.box[row][col].draw_change(self.win)
                self.grid_update()
                pygame.display.update()
                pygame.time.delay(100)

                if self.solve_game():
                    return True

                self.grid[row][col] = 0
                self.box[row][col].set(0)
                self.grid_update()
                self.box[row][col].draw_change(self.win)
                pygame.display.update()
                pygame.time.delay(100)

        return False


class Box:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.choose = False

    def draw(self, win):
        font = pygame.font.SysFont("comicsansms", 25, True)

        block = self.width / 9
        x = self.col * block
        y = self.row * block

        if self.temp != 0 and self.value == 0:
            text = font.render(str(self.temp), 1, (255, 0, 0))
            win.blit(text, (x+(block//2-text.get_width()/2), y+(block//2-text.get_width()) ))
        elif not(self.value == 0):
            text = font.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x+(block/2-text.get_width()/2), y+(block/2-text.get_height()/2)))

        if self.choose:
            pygame.draw.rect(win, (0,0,0), (x,y, block ,block), 3)

    def draw_change(self, win):
        font = pygame.font.SysFont("comicsansms", 25, True)

        block = self.width / 9
        x = self.col * block
        y = self.row * block

        pygame.draw.rect(win, (255, 255, 255), (x, y, block, block), 0)

        text = font.render(str(self.value), 1, (0, 0, 0))
        win.blit(text, (x + (block/2-text.get_width()/2), y + (block/2-text.get_height()/2)))
        pygame.draw.rect(win, (0, 0, 0), (x, y, block, block), 3)

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val


def find_empty_block(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 0:
                return (i,j)

    return None


def valid(grid, num, pos):
    for i in range(len(grid[0])):
        if grid[pos[0]][i] == num and pos[1] != i:
            return False

    for i in range(len(grid)):
        if grid[i][pos[1]] == num and pos[0] != i:
            return False

    b_x = pos[1] // 3
    b_y = pos[0] // 3

    for i in range(b_y*3, b_y*3 + 3):
        for j in range(b_x * 3, b_x*3 + 3):
            if grid[i][j] == num and (i,j) != pos:
                return False

    return True


def draw_window(win, s_board, wrong):
    win.fill((255,255,255))

    font = pygame.font.SysFont("comicsans", 40)

    text = font.render("X " * wrong, 1, (255, 0, 0))
    win.blit(text, (20, 420))

    s_board.draw()

def game():
    win = pygame.display.set_mode((400,450))
    pygame.display.set_caption("Sudoku")
    s_board = Grid(9, 9, 400, 400, win)
    key = None
    run = True
    wrong = 0

    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_q:
                    run = False
                if event.key == pygame.K_DELETE:
                    s_board.clear()
                    key = None

                if event.key == pygame.K_SPACE:
                    if s_board.solve_game():
                        pygame.time.delay(3000)
                        display_surface = pygame.display.set_mode((500, 250))
                        font = pygame.font.SysFont("comicsans", 40)
                        text = font.render("Thank You For Playing !", True, (0,0,0))
                        textRect = text.get_rect()
                        display_surface.fill((255,255,255))
                        display_surface.blit(text, textRect)
                        pygame.display.update()
                        pygame.time.delay(3000)
                        run=False


                if event.key == pygame.K_RETURN:
                    i, j = s_board.choose
                    if s_board.box[i][j].temp != 0:
                        if s_board.allocate(s_board.box[i][j].temp):
                            print("Success")
                            if find_empty_block(s_board.grid) == None:
                                display_surface = pygame.display.set_mode((500, 250))
                                font = pygame.font.SysFont("comicsans", 40)
                                text = font.render("Congratulations !! You Solved It !!", True, (0,0,0))
                                textRect = text.get_rect()
                                display_surface.fill((255,255,255))
                                display_surface.blit(text, textRect)
                                pygame.display.update()
                                pygame.time.delay(3000)
                                run=False
                        else:
                            print("Wrong")
                            wrong += 1
                            if wrong == 3:
                                display_surface = pygame.display.set_mode((500, 250))
                                font = pygame.font.SysFont("comicsans", 40)
                                text = font.render("OH.. Hard Luck ! Try Again !", True, (0,0,0))
                                textRect = text.get_rect()
                                display_surface.fill((255,255,255))
                                display_surface.blit(text, textRect)
                                pygame.display.update()
                                pygame.time.delay(3000)
                                run=False
                        key = None

                        if s_board.complete():
                            print("Game over")

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                selected = s_board.click(pos)
                if selected:
                    s_board.select(selected[0], selected[1])
                    key = None

        if s_board.choose and key != None:
            s_board.layout(key)

        draw_window(win, s_board, wrong)
        pygame.display.update()

g = input(" Enter 'P' to play !!\n")
while g.lower() != "p":
    g = input("Press 'P' to play !!\n")

game()
pygame.quit()
