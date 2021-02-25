# sudoku desktop app 

from copy import deepcopy
import random
import tkinter as tk

class sudoku_board: 
	# creates a full sudoku board and a playing board with clues missing
	def __init__(self):
		self.board = self.full_board()
		# create playing board by randomly removing as many clues
		# as possible (up to 51) as long as there remains a unique solution
		# average of 45 clues
		self.playing_board = deepcopy(self.board)
		sample = random.sample(range(0, 81), 51)
		removed = []
		for i in sample:
			r, c = i//9, i%9
			removed.append((r,c,self.playing_board[r][c]))
			self.playing_board[r][c] = '.'

		while self.non_unique_solution(deepcopy(self.playing_board),self.board):
			r,c,s = removed.pop()
			self.playing_board[r][c] = s
		
	def avail_choices(self, board, i):
			r, c = i//9, i%9
			row = {n for n in board[r]}
			col = {board[n][c] for n in range(9)}
			block = {board[(r//3)*3+m][(c//3)*3+n]
				for m in range(3) 
				for n in range(3)}
			return set('123456789') - row - col - block - set('.')

	def full_board(self):
		board = [['.' for _ in range(9)] for _ in range(9)]
		def populate(i):
			if i == 81: return True
			r, c = i//9, i%9
			if board[r][c] == '.':
				for n in self.avail_choices(board, i):
					board[r][c] = n
					if populate(i+1):
						return True
					board[r][c] = '.'
			else:
				if populate(i+1):
					return True
			return False
		
		populate(0)
		return board
	
	def non_unique_solution(self, playing_board,board):
		def solve(i):
			if i == 81: 
				if playing_board == board: return False
				else: return True
			r, c = i//9, i%9
			if playing_board[r][c] == '.':
				for n in self.avail_choices(playing_board, i):
					playing_board[r][c] = n
					if solve(i+1):
						return True
					playing_board[r][c] = '.'
			else:
				if solve(i+1):
					return True
			return False
	
		return solve(0)
	
def initiate(): # populate new sudoku board
	global sb
	sb = sudoku_board()
	# destroy previous board
	for widget in brd_frm.winfo_children():
		widget.destroy()
	for i in range(3):
		for j in range(3):
			frame = tk.Frame(
				master=brd_frm,
				relief=tk.RAISED,
				borderwidth=.5
			)
			frame.grid(row=i, column=j, padx=5, pady=5)
			for k in range(3):
				for l in range(3):
					if sb.playing_board[3*i+k][3*j+l] == '.':
						entry = tk.Entry(
							master=frame,
							font=(None, 15),
							justify='center',
							width=2
						)
						entry.grid(row=k, column=l)
					else:
						label = tk.Label(master=frame, font=(None, 15), text=sb.board[3*i+k][3*j+l])
						label.grid(row=k, column=l, padx=10, pady=2)
	result["text"] = ""

def check_result(): # check if submission is correct
	global sb
	# get board consisting of entries
	board_to_check = deepcopy(sb.playing_board)
	for i in range(9):
		for j in range(9):
			widget = brd_frm.winfo_children()[i].winfo_children()[j]
			if widget.winfo_class() == 'Entry':
				s = widget.get().strip()
				board_to_check[3*(i//3)+(j//3)][3*(i%3)+(j%3)] = s
	# check if submission is correct
	if sb.board == board_to_check:
		result["text"] = "Congratulations, you solved the puzzle!"
	else:
		result["text"] = "Sorry that is incorrect"

window = tk.Tk()
window.title("Sudoku")

top_frm = tk.Frame(master=window)
bot_frm = tk.Frame(master=window)

new_board = tk.Button(master=top_frm, text="New Board", command=lambda: initiate())
new_board.pack()

submit = tk.Button(master=bot_frm, text="Submit", command=lambda: check_result())
result = tk.Label(master=bot_frm, text='',pady=10)
submit.grid(row=0)
result.grid(row=1)

brd_frm = tk.Frame(master=window)
sb = sudoku_board()
initiate()


top_frm.grid(row=0)	
brd_frm.grid(row=1)
bot_frm.grid(row=2)	
	
window.mainloop()