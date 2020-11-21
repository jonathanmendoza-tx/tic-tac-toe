import pandas as pd
import joblib
import copy
from sklearn.ensemble import RandomForestClassifier

model = joblib.load("./model/tictactoemaster.joblib")

board_columns = ['tl_x', 'tl_o', 'tm_x', 'tm_o', 'tr_x', 'tr_o', 'ml_x', 'ml_o', 
				'mm_x','mm_o', 'mr_x', 'mr_o', 'nl_x', 'nl_o', 'bm_x', 'bm_o', 
				'br_x', 'br_o']

def clear_board():
	board = [[' ',' ',' '], 
			[' ',' ',' '], 
			[' ',' ',' ']]

	return board

def display_board(board):
	for i in range(len(board)):
		print(f' {board[i][0]} | {board[i][1]} | {board[i][2]} ')
		if i < len(board)-1:
			print('-----------')

def display_visual_aid():
	print()
	for i in range(0, 9, 3):
		print(f' {i} | {i+1} | {i+2} ')
		if i < 6:
			print('-----------')

def update_map(board):
	move_dict = {0: board[0][0], 
			1: board[0][1], 
			2: board[0][2], 
			3: board[1][0], 
			4: board[1][1], 
			5: board[1][2], 
			6: board[2][0], 
			7: board[2][1],
			8: board[2][2]}
	
	current_places = []
	
	for key, val in move_dict.items():
		if val == 'x':
			current_places += [1,0]

		elif val == 'o':
			current_places += [0,1]
			
		else:
			current_places += [0,0]

	return pd.DataFrame([current_places], columns = board_columns)

def find_best_move(current_places, board):
	best_move = None
	best_prob = 0

	for i in range(len(board_columns)):
		if '_x' in board_columns[i]:
			available = ((current_places[board_columns[i]] == 0) & (current_places[board_columns[i][:-1]+'o'] == 0))[0]
			if available:
				test_placement = current_places.copy()
				test_placement[board_columns[i]] = 1

				test_prob = model.predict_proba(test_placement)
				
				x_move_to_win = make_move(copy.deepcopy(board), i//2, 'x')
				win, draw = check_for_win(x_move_to_win)
				
				if win or draw:
					best_move = i//2
					return best_move
				
				o_wins = test_prob[0][0]
				x_wins = test_prob[0][1]
				
				if o_wins < x_wins:
					if  x_wins > best_prob:
						best_prob = x_wins
						best_move = i//2
						
		else:
			available = ((current_places[board_columns[i]] == 0) & (current_places[board_columns[i][:-1]+'x'] == 0))[0]
			if available:
				test_placement = current_places.copy()
				test_placement[board_columns[i]] = 1

				test_prob = model.predict_proba(test_placement)
				
				o_move_to_win = make_move(copy.deepcopy(board), i//2, 'o')
				win, draw = check_for_win(o_move_to_win)
				
				if win or draw:
					best_move = i//2
					return best_move
				
				o_wins = test_prob[0][0]
				x_wins = test_prob[0][1]
				
				if o_wins > x_wins:
					if  o_wins > best_prob:
						best_prob = o_wins
						best_move = i//2

	return best_move

def make_move(board, move, sign):
	move_board = copy.deepcopy(board)
	move_map = {0: (0,0), 
				1: (0,1), 
				2: (0,2), 
				3: (1,0), 
				4: (1,1), 
				5: (1,2), 
				6: (2,0), 
				7: (2,1),
				8: (2,2)}
	
	i, j = move_map[move]
	
	if move_board[i][j] == ' ':
		move_board[i][j] = sign
		
	else:
		print(f'---Error: Illegal move---')
		
	return move_board

def check_for_win(board):
	win = False
	draw = False

	for i in range(len(board)):
			if board[i][0] == board[i][1] == board[i][2]:
				if board[i][0] != ' ':
					win = True
					return win, draw

			if board[0][i] == board[1][i] == board[2][i]:
				if board[0][i] != ' ':
					win = True
					return win, draw

			if i == 0:
				if board[i][i] == board[1][1] == board[2][2]:
					if board[i][i] != ' ':
						win = True
						return win, draw

			if i == 2:
				if board[0][i] == board[1][1] == board[i][0]:
					if board[0][i] != ' ':
						win = True
						return win, draw

	current_places = update_map(board) 
	if current_places.values.sum() == 9:
		draw = True

	return win, draw

def ai_move(board):
	current_places = update_map(board)
	best_move = find_best_move(current_places, board)
	board = make_move(board, best_move, 'x')
	print('===========')
	print('| AI Move |')
	print('===========\n')
	display_board(board)
	
	return board

def player_move(board, move):
	board = make_move(board, move, 'o')
	display_board(board)

	return board