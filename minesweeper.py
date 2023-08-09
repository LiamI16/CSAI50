import itertools
import random

class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        if len(self.cells) == self.count:
            return self.cells
        return set()

    def known_safes(self):
        if self.count == 0:
            return self.cells
        return set()

    def mark_mine(self, cell):
        if(cell in self.cells):
            self.cells.remove(cell)
            self.count-=1

    def mark_safe(self, cell):
        if(cell in self.cells):
            self.cells.remove(cell)
                
class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        #Hidden Cells
        self.hidden = set()
        for i in range(height):
            for j in range(width):
                self.hidden.add((i, j))

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        self.safes.add(cell)

        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        self.moves_made.add(cell)
        self.mark_safe(cell)
        cells = set()
        for i in range(-1, 2):
            for j in range(-1, 2):
                if cell[0]+i >= 0 and cell[0]+i < self.height and cell[1]+j >= 0 and cell[1]+j < self.width:
                    cells.add((cell[0]+i, cell[1]+j))
        
        cells = cells.difference(self.safes)
        set_total = len(cells.union(self.mines))
        len_total = len(cells) + len(self.mines)
        if set_total != len_total:
            cells = cells.difference(self.mines)
            count -= len_total - set_total

        self.knowledge.append(Sentence(cells, count))

        for i in self.knowledge:
            for sentence in self.knowledge:
                while sentence.known_safes() != set():
                    self.mark_safe(list(sentence.known_safes())[0])
                
                while sentence.known_mines() != set():
                    self.mark_mine(list(sentence.known_mines())[0])

        self.knowledge = [sentences for sentences in self.knowledge if len(sentences.cells) != 0]

        for i in self.knowledge:
            print(i)
        print("\n\n")
        
    def make_safe_move(self):
        moves = self.safes.difference(self.moves_made)
        if len(moves) != 0:
            safe_move = list(moves)[0]
            return safe_move


    def make_random_move(self):
        return random.choice(list(self.hidden.difference(self.moves_made.union(self.mines))))

