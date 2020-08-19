

#Class to maintain board structure

class Board():

    #Create board based on size



    def __init__(self, size):
        print("Board Created")
        self.sector_array = []
        self.create(size)



    def create(self, size):
        self.size = size

        for i in range(size):
            self.sector_array.append([Sector((i,j)) for j in range(size)])

        #[self.sector_array.append([Sector((i,j)) for j in range(size) ] for i in range(size))]

        for s in self.sector_array:
            for d in s:
                d.print_index()



class Grid():
    pass



class Frame():

    def __init__(self, index):
        self.row = index[0]
        self.column = index[1]
        self.index = index
        print("made frame")

    def print_index(self):
        class_text = self.__class__
        print(f"{class_text} object with index: ({self.index})")


class Sector(Frame):

    pass





class Cell(Frame):
    pass




