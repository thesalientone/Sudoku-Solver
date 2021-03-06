import csv
from collections import defaultdict
import datetime

#Class to maintain board structure


class Board():

    #Create board based on size
    #Note easy from https://www.puzzles.ca/sudoku_puzzles/sudoku_easy_481.html
    #Note hard from https://stackoverflow.com/questions/10630442/assigning-a-value-to-list-by-index-out-of-range
    #Some notes borrowed from https://stackoverflow.com/questions/1697334/algorithm-for-solving-sudoku



    def __init__(self, size):
        print("Board Created")

        self.size = size
        board_size = size
        self.sectors = Grid(size, Sector, self)
        self.output_file = f"output/{datetime.date.today()}-{self.size}.csv"
        self.filled_cells = 0



    def print_grid_tabulation(self):
        for i in self.sectors.index:
            for d in i:
                d.print_index()
                for c in d.cells:
                    print("                 ", end="")
                    c.print_index()
                    print(c.value)
    def print_cell_locations(self):

        for s in self.sectors:
            for c in s.cells:
                c.print_location()


    def initialize_sample_game(self, game_csv):

        i = 0
        j = 0

        with open(game_csv) as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                j = 0
                for value in row:

                    c = self.absolute_cell_reference(i, j)
                    if value != '':
                        c.value = int(value)
                    j +=1
                    pass
                i+=1

            csvfile.close()



        #self.check_rows()

    def table_cells(self):

        output = defaultdict(SparseList)

        for c in self.all_cells():
            output[c.abs_row][c.abs_col] = c.value

        return output


    def write_board(self, output_csv):



        i = 0
        j = 0
        table_cells = self.table_cells()
        with open(output_csv, "w+") as csvfile:
            csv_writer = csv.writer(csvfile)
            for row in table_cells.values():

                csv_writer.writerow(row)

            csvfile.close()


    def count_filled_cells(self):

        i = 0

        for c in self.all_cells():
            if c.base_set == set([]):
                i += 1
        return i

    def execute_game(self):

        filled_cells = self.count_filled_cells()
        goal_cells = (self.size ** 2) ** 2
        counter = 0
        while filled_cells != goal_cells:

            self.filled_cells = filled_cells
            print(f"Filled {filled_cells}/{goal_cells} cells")
            print(f"Beginning Iteration : {counter}")

            self.execute_constraints()
            self.execute_conclusions()
            filled_cells = self.count_filled_cells()

            if self.filled_cells == filled_cells:
                self.print_cell_locations()
                print("The process is failing")

            counter += 1

        print(f"Filled {filled_cells}/{goal_cells} cells")
        print(f"Simulation Complete")

        self.write_board(self.output_file)


    def values_in_col(self, col, **kwargs):

        output = set([])

        if 'counts' in kwargs:
            output = {}
            look_up = {}
            for s in self.sectors:
                for c in s.cells:
                    if c.abs_col == col:
                        self.update_output_look_up(c, output, look_up)
            return output, look_up

        for s in self.sectors:
            for c in s.cells:
                if c.abs_col == col:
                    output.add(c.value)

        return output

    def update_output_look_up(self, c, output, look_up):
        for n in c.base_set:
            if n in output.keys():
                output[n] += 1
                look_up[n].append((c.abs_row, c.abs_col))
            else:
                output[n] = 1
                look_up[n] = [(c.abs_row, c.abs_col)]


    def values_in_row(self, row, **kwargs):

        output = set([])

        if 'counts' in kwargs:
            output = {}
            look_up = {}
            for s in self.sectors:
                for c in s.cells:
                    if c.abs_row == row:
                        self.update_output_look_up(c, output, look_up)
            return output, look_up

        for s in self.sectors:
            for c in s.cells:
                if c.abs_row == row:
                    output.add(c.value)

        return output

    def values_in_sector(self, sector, **kwargs):
        output = set([])
        i = sector[0]
        j = sector[1]

        if 'counts' in kwargs:
            output = {}
            look_up = {}

        for c in self.sectors.index[i][j].cells:

            if 'counts' in kwargs:
                self.update_output_look_up(c, output, look_up)

            else:
                output.add(c.value)
        if 'counts' in kwargs:
            return output, look_up
        return output


    def check_rows(self):

        for i in range(self.size ** 2):
            print(f"Values in Row {i} : ", self.values_in_row(i))
            print(f"Values in Column {i} : ", self.values_in_col(i))

        for i in range(self.size):
            for j in range(self.size):
               print(f"Values in Sector {i},{j} :", self.values_in_sector((i,j)))



    def absolute_cell_reference(self, abs_row, abs_col):

        i = abs_row // 3
        j = abs_col // 3
        k = (abs_row % 3)
        l = (abs_col % 3)

        return self.sectors.index[i][j].cells.index[k][l]

    def all_cells(self):
        for s in self.sectors:
            for c in s.cells:
                yield c

    def vertical_constraint(self,col):
        #print("Starting Vertical Constraint")
        values_in_col = set(self.values_in_col(col))
        [c.base_set.difference_update(values_in_col) for c in self.all_cells() if c.abs_col == col]



    def horizontal_constraint(self,row):

        #print("Starting Horizontal Constraint")
        values_in_row = set(self.values_in_row(row))

        [c.base_set.difference_update(values_in_row) for c in self.all_cells() if c.abs_row == row]

        pass

    def sector_constraint(self, index):
        #print("Starting Sector Constraint")
        values_in_sector = set(self.values_in_sector(index))
        i = index[0]
        j = index[1]

        [c.base_set.difference_update(values_in_sector) for c in self.all_cells() if c.parent is self.sectors.index[i][j]]


    def sector_conclusion(self, index):

        #print(f"Starting Sector Conclusion : {index}")
        base_values_in_sector, look_up_values = self.values_in_sector(index, counts=True)


        i = index[0]
        j = index[1]

        for k, v in base_values_in_sector.items():
            if v == 1:

                self.find_conclusion(k, look_up_values)

    def find_conclusion(self, number, look_up_values):
        #print(f"CONCLUSION FOUND Value = {number}")
        cell_coordinates = look_up_values[number]  # Note lookup values contains a list of points [(x,y)]
        cell_x = cell_coordinates[0][0]
        cell_y = cell_coordinates[0][1]
        c = self.absolute_cell_reference(cell_x, cell_y)
        #c.print_location()
        # Code to assign value
        c.value = number


    def col_conclusion(self, col):
        #print(f"Starting Column Conclusion : {col}")
        base_values_in_col, look_up_values = self.values_in_col(col, counts=True)

        for k,v in base_values_in_col.items():
            if v == 1:
                self.find_conclusion(k, look_up_values)

    def row_conclusion(self, row):
        #print(f"Starting Row Conclusion : {row}")
        base_values_in_row, look_up_values = self.values_in_row(row, counts=True)

        for k,v in base_values_in_row.items():
            if v == 1:
                self.find_conclusion(k, look_up_values)




    def execute_constraints(self):

        #Row and column base set exclusion
        for i in range(self.size ** 2):
            self.vertical_constraint(i)
            self.horizontal_constraint(i)


        #Sector base set exclusion
        for i in range(self.size):
            for j in range(self.size):
                self.sector_constraint((i,j))



    def execute_conclusions(self):
        #Sector conclusion
        for i in range(self.size):
            for j in range(self.size):
                self.sector_conclusion((i, j))

        for i in range(self.size ** 2):
            self.col_conclusion(i)

        for i in range(self.size ** 2):
            self.row_conclusion(i)


        #self.print_cell_locations()
        #print("constraints done")

class Grid():


    def __init__(self, size, type, parent):

        self.size = size
        self.create(size,type, parent)


    def __iter__(self):
        self.__i = 0  # Row index for iterator
        self.__j = 0  # Column index for iterator
        return self

    def __next__(self):
        if self.__i == self.size:
            raise StopIteration
        elif self.__j == self.size - 1:
            output = self.index[self.__i][self.__j]
            self.__j = 0
            self.__i += 1
            return output
        else:
            output = self.index[self.__i][self.__j]
            self.__j += 1
            return output


    def create(self, size, type, parent):
        self.index = []
        for i in range(size):
            self.index.append([type((i,j),size, parent) for j in range(size)])


class Frame():

    def __init__(self, index,size, parent_obj):
        self.parent = parent_obj
        self.row = index[0]
        self.col = index[1]
        self.index = index
        self.size = size #This is board size. Board and sectors should be the same size.


    def print_index(self):
        class_text = self.__class__
        print(f"{class_text} object with index: ({self.index})")


class Sector(Frame):

    def __init__(self, index, size, parent_obj):
        super(Sector, self).__init__(index, size, parent_obj)
        self.cells = Grid(self.size, Cell, self)





class Cell(Frame):


    def __init__(self, index, size,sector, **kwargs):
        super(Cell, self).__init__(index, size, sector)

        self.abs_row = 3 * sector.row + index[0]
        self.abs_col = 3 * sector.col + index[1]
        self.base_set = set(range(1,(size ** 2)+1))
        self.value = None



    def __setattr__(self, key, value):
        if key == 'value':
            self.__dict__[key] = value
            if value != None:
                self.base_set.clear()
                self.parent.parent.vertical_constraint(self.abs_col)
                self.parent.parent.horizontal_constraint(self.abs_row)
                self.parent.parent.sector_constraint(self.parent.index)



        else:
            self.__dict__[key] = value




    def print_location(self):

        print(f"{self.abs_row},{self.abs_col} At Sector {self.parent.index} Cell {self.index} Value {self.value} Base Set {self.base_set}")


class SparseList(list):
    #https://stackoverflow.com/questions/10630442/assigning-a-value-to-list-by-index-out-of-range
    def __setitem__(self, index, value):
        """Overrides list's __setitem__ to extend the list
           if the accessed index is out of bounds."""
        sparsity = index - len(self) + 1
        self.extend([None] * sparsity)
        list.__setitem__(self, index, value)







