from game_mechanics import *

turn_counter = 0

board = clear_board()

player_first = False

cont = True

def check_player(board, turn_counter, player_first, cont):
	if turn_counter > 5:
		win, draw = check_for_win(board)

		if win:
			print('You win!')
			if player_first:
				player_first = False
			else:
				player_first = True

			answer = input('Would you like to continue? ([y]es, [n]o): ')
			if answer[0].lower() == 'n':
				cont = False

			turn_counter = 0
			board = clear_board()

		if draw:
			print('Draw!')
			if player_first:
				player_first = False
			else:
				player_first = True

			answer = input('Would you like to continue? ([y]es, [n]o): ')
			if answer[0].lower() == 'n':
				cont = False

			turn_counter = 0
			board = clear_board()

	return board, cont

def check_ai(board, turn_counter, player_first, cont):
	if turn_counter > 5:
		win, draw = check_for_win(board)

		if win:
			print('You lose :(')
			if player_first:
				player_first = False
			else:
				player_first = True

			answer = input('Would you like to continue? ([y]es, [n]o): ')
			if answer[0].lower() == 'n':
				cont = False

			turn_counter = 0
			board = clear_board()

		if draw:
			print('Draw!')
			if player_first:
				player_first = False
			else:
				player_first = True

			answer = input('Would you like to continue? ([y]es, [n]o): ')
			if answer[0].lower() == 'n':
				cont = False

			turn_counter = 0
			board = clear_board()

	return board, cont

while cont:
	if player_first:
		display_board(board)
		display_visual_aid()
		
		move = input('Make your move (0-8): ')
		board = player_move(board, int(move))
		print(f'\n\n')
		turn_counter += 1

		board, cont = check_player(board, turn_counter, player_first, cont)
		
		board = ai_move(board)
		print(f'\n\n')
		turn_counter += 1

		board, cont = check_ai(board, turn_counter, player_first, cont)

	else:
		board = ai_move(board)
		print(f'\n\n')
		turn_counter += 1

		board, cont = check_ai(board, turn_counter, player_first, cont)

		display_visual_aid()
		move = input('Make your move (0-8): ')
		board = player_move(board, int(move))
		print(f'\n\n')
		turn_counter += 1

		board, cont = check_player(board, turn_counter, player_first, cont)

