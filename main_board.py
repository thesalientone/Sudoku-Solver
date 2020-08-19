from board import *

#c1 = Cell((1,1))


#s1 = Sector((2,2))


b = Board(3)

sample_game_file = "resources/sudoku_easy_481.csv"
b.initialize_sample_game(sample_game_file)

#b.print_grid_tabulation()
#b.print_cell_locations()

b.execute_game()
