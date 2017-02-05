##python driver.py bfs 1,2,5,3,4,0,6,7,8 ## test case

### Class state, starting with BFS
import numpy as np
class State():
    """Solve a 3x3 puzzle.
    Input: list of nine numbers in a string
    Output: Path taken to reach goal, time taken to reach goal, steps taken to reach goal"""
    def __init__(self,board):
        self.board = self.board_box(board) ### fetch a 3x3 matrix that represents that board
        self.queue = [] ##new queue for every move
        self.finished_board = np.array([[0,1,2],
                                       [3,4,5],
                                       [6,7,8]]) ### finished board
        self.visited_states=[] ### store  visited states here
        self.number_of_moves = 0 ##number of moves taken
        ### add the initial board as a visited state
        self.visited_states.append(self.board.flatten())
        min_idx = np.where(self.board == 0) ## find the starting indexes on the board
        row_num = min_idx[0][0]
        col_num = min_idx[1][0]
        self.curr_row = row_num
        self.curr_col = col_num
        self.path_taken = []
    def board_box(self,game_numbers):
        """Create a board from a list of nine numbers."""
        f = np.zeros((3,3))
        row_num = 0
        col_num = 0
        for idx, number in enumerate(game_numbers):
            if col_num ==2:
                f[row_num,col_num]=number
                col_num=0
                row_num+=1
            else:
                f[row_num,col_num]=number
                col_num+=1
        return f
    def enqueue(self,item):
        """Insert an item and the move into the queue (a tuple)."""
        self.queue.insert(0,item)
    def dequeue(self):
        """Take out item from the queue once a move has been completed."""
        self.number_of_moves +=1 ## another move
        move = self.queue.pop() ## get the last item out of the queue
        print(move,' move to take')
        number_of_move_taken, move_taken = move[0],move[1] ## break into the text and the number
        pointer_of_potential_move = np.where(self.board == number_of_move_taken)
        current_pointer = np.where(self.board == 0) ## find the index of where the zero is on the board
        ## compare the pointer of the potential move and where the current zero is to ensure it is a legal move
        potential_move_row = pointer_of_potential_move [0][0]
        potential_move_col = pointer_of_potential_move [1][0]
        current_pointer_row = current_pointer[0][0]
        current_pointer_col = current_pointer[1][0]
        ### make sure that the proposed move is legal
        if (potential_move_row +1 or potential_move_row -1 ) == current_pointer_row:
             if potential_move_col==current_pointer_col:
                self.board_swap(move_taken,'actual')
                self.curr_row  = current_pointer[0][0] ## change the pointer after completing the move
                self.curr_col = current_pointer[1][0]
                self.path_taken.insert(0,move) ## keep track of the moves taken
        elif (potential_move_col +1 or potential_move_col -1 ) == current_pointer_col:
            if potential_move_row==current_pointer_row:
                self.board_swap(move_taken,'actual')
                self.curr_row  = current_pointer[0][0] ## change the pointer after completing the move
                self.curr_col = current_pointer[1][0]
                self.path_taken.insert(0,move) ## keep track of the moves taken
        else:
            self.curr_row  = current_pointer[0][0] ## to the zero position
            self.curr_col = current_pointer[1][0]

    def size(self):
        return len(self.queue)
    def move(self): # Move once
        """Move the pieces on the board in the UDLR sequence (up down left right)."""
        current_pointer = np.where(self.board == 0) ## make sure we have the correct pointer
        self.curr_row  = current_pointer[0][0] ## to the zero position
        self.curr_col = current_pointer[1][0]

        try:
            if self.curr_row-1 <0:
                raise Exception
            print(self.board,' BOARD before up ')
            up = self.board[self.curr_row-1,self.curr_col] ## Up
            if self.arreq_in_list(self.board_swap('up','test').flatten(),self.visited_states)==False: ### do not allow the algo to visit states again
                self.enqueue((up,'up'))
            else:
                print('up broke')
        except :
            print('up broke')
        try:
            if self.curr_row+1>2: ## going beyond our board
                raise Exception
            down = self.board[self.curr_row+1,self.curr_col]
            test_down_swap = self.board_swap('down','test').flatten()
            if self.arreq_in_list(test_down_swap,self.visited_states)==False: ### do not allow the algo to visit states again
                self.enqueue((down,'down'))
            else:
                print('down broke')
        except:
            print('down broke - try')
        try:
            if self.curr_col-1 <0:
                raise Exception
            left = self.board[self.curr_row,self.curr_col-1]
            #print(self.board_swap('left','test') , 'testing left')
            if self.arreq_in_list(self.board_swap('left','test').flatten(),self.visited_states)==False: ### do not allow the algo to visit states again
                self.enqueue((left,'left'))
            else:
                print('left broke')
        except:
            pass
        try:
            if self.curr_col+1>2:
                raise Exception
            right = self.board[self.curr_row,self.curr_col+1]
            if self.arreq_in_list(self.board_swap('right','test').flatten(),self.visited_states)==False: ### do not allow the algo to visit states again
                self.enqueue((right,'right'))
            else:
                print('right broke')
        except:
            pass
    def board_swap(self,s_type,test_or_actual):
        """test_or_actual is the swap type.
        Test: means that the board will not be permantely changed.
        Actual: means that the board WILL be changed. The moves taken here will be recorded in self.visited_states
        s_type: is the direction of the swap. options are up, down,left,right.
        returns either a test board or actual board with the desired swap."""
        self.test_board = self.board.copy()
        if test_or_actual =='actual': ### permantely change the board
            if s_type == 'up':
                self.board[self.curr_row,self.curr_col] ,self.board[self.curr_row-1,self.curr_col] = \
                self.board[self.curr_row-1,self.curr_col], self.board[self.curr_row,self.curr_col]
                self.visited_states.append(self.board.flatten())
            elif s_type == 'down':
                self.board[self.curr_row,self.curr_col] ,self.board[self.curr_row+1,self.curr_col]  = \
                self.board[self.curr_row+1,self.curr_col] , self.board[self.curr_row,self.curr_col]
                self.visited_states.append(self.board.flatten())
            elif s_type =='left':
                self.board[self.curr_row,self.curr_col] ,self.board[self.curr_row,self.curr_col-1]   = \
                self.board[self.curr_row,self.curr_col-1]  , self.board[self.curr_row,self.curr_col]
                self.visited_states.append(self.board.flatten())
            elif s_type =='right':
                self.board[self.curr_row,self.curr_col] ,self.board[self.curr_row,self.curr_col+1]  = \
                self.board[self.curr_row,self.curr_col+1], self.board[self.curr_row,self.curr_col]
                self.visited_states.append(self.board.flatten())
        elif test_or_actual =='test': ## don't change the board
            if s_type == 'up':
                self.test_board[self.curr_row,self.curr_col] ,self.test_board[self.curr_row-1,self.curr_col] = \
                self.test_board[self.curr_row-1,self.curr_col], self.test_board[self.curr_row,self.curr_col]
                return self.test_board
            elif s_type == 'down':
                self.test_board[self.curr_row,self.curr_col] ,self.test_board[self.curr_row+1,self.curr_col]  = \
                self.test_board[self.curr_row+1,self.curr_col] , self.test_board[self.curr_row,self.curr_col]
                return self.test_board
            elif s_type =='left':
                self.test_board[self.curr_row,self.curr_col] ,self.test_board[self.curr_row,self.curr_col-1]   = \
                self.test_board[self.curr_row,self.curr_col-1]  , self.test_board[self.curr_row,self.curr_col]
                return self.test_board
            elif s_type =='right':
                self.test_board[self.curr_row,self.curr_col] ,self.test_board[self.curr_row,self.curr_col+1]  = \
                self.test_board[self.curr_row,self.curr_col+1], self.test_board[self.curr_row,self.curr_col]
                return self.test_board
    def arreq_in_list(self, myarr, list_arrays):
            #http://stackoverflow.com/questions/23979146/check-if-numpy-array-is-in-list-of-numpy-arrays#23979509
            """test if myarr is in list_arrays. Return True is it is. Otherwise, return False"""
            return next((True for elem in list_arrays if np.array_equal(elem, myarr)), False)
    def solve(self):
        """solve the board"""
        while np.array_equal(self.board.flatten(),self.finished_board.flatten())==False:
            print(self.board,'board before move')
            self.move()
            self.dequeue()
            print(self.queue,'queue')
            print(self.board,'board after move')
            print(self.curr_col,'current col')
            print(self.curr_row,'curr row')

        print('YOU SOLVED IT!')
        print("It took {} moves to solve".format(self.number_of_moves ))
        print("The path taken was {}".format(self.path_taken))
        return(self.board, ' You found a board!')

if __name__ =='__main__':
    # t = [1,2,5,3,4,0,6,7,8]
    # s = State(t)
    # s.solve()
    # x = [3,1,2,0,4,5,6,7,8]
    # p = State(x)
    # p.solve()
    z = [1,3,2,4,6,5,7,8,0]
    e = State(z)
    e.solve()
