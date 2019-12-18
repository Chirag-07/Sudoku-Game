def empty_loc(grid,empty):
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                empty[0]=i
                empty[1]=j
                return True
    return False

def not_in_box(grid,row,col,num):
    for i in range(3):
        for j in range(3):
            if grid[i+row][j+col] == num:
                return False
    return True

def not_in_col(grid,col,num):
    for i in range(9):
        if grid[i][col] == num:
            return False
    return True

def not_in_row(grid, row, num):
    for i in range(9):
        if grid[row][i] == num:
            return False
    return True

def sudoku(grid):
    empty = [-1,-1]

    if not empty_loc(grid,empty):
        return True

    row=empty[0]
    col=empty[1]

    for i in range(1,10):
        if not_in_row(grid,row,i) and not_in_col(grid,col,i) and not_in_box(grid,row-row%3, col-col%3, i):

            grid[row][col]=i

            if sudoku(grid):
                return True

            grid[row][col]=0

    return False

if __name__ == '__main__':
    # grid=[[3,0,6,5,0,8,4,0,0],
    #       [5,2,0,0,0,0,0,0,0],
    #       [0,8,7,0,0,0,0,3,1],
    #       [0,0,3,0,1,0,0,8,0],
    #       [9,0,0,8,6,3,0,0,5],
    #       [0,5,0,0,9,0,6,0,0],
    #       [1,3,0,0,0,0,2,5,0],
    #       [0,0,0,0,0,0,0,7,4],
    #       [0,0,5,2,0,6,3,0,0]]
    grid = [
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

    if not sudoku(grid):
        print("Solution does not exist")
    else:
        for i in range(9):
            print("[",end='')
            for j in range(9):
                print("{}".format(grid[i][j]), end=", ")
            print("]",end='')
            print()
