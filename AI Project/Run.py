import tkinter as tk
from PIL import Image, ImageTk

class AbstractPiece(tk.Label):
    """docstring for Piece"""
    def __init__(self, root, row, column, *args, **kwargs):
        tk.Label.__init__(self, root, *args, **kwargs)
        self.current_piece=""
        self.row=row
        self.column=column
        self.color = 0
        self.defaultbg=""
        self.selected = False
        self.used = False

class ChessApp(tk.Frame):
    Black_Pawn_Image =Image.open("iloveimg-resized/bp2.png")
    Black_Horse_Image = Image.open("iloveimg-resized/bn2.png")
    Black_Knight_Image =Image.open("iloveimg-resized/bb2.png")
    Black_Tower_Image = Image.open("iloveimg-resized/br2.png")
    Black_King_Image =Image.open("iloveimg-resized/bk2.png")
    Black_Queen_Image = Image.open("iloveimg-resized/bq2.png")
    Gold_Pawn_Image =Image.open("iloveimg-resized/wp2.png")
    Gold_Horse_Image = Image.open("iloveimg-resized/wn2.png")
    Gold_Knight_Image =Image.open("iloveimg-resized/wb2.png")
    Gold_Tower_Image = Image.open("iloveimg-resized/wr2.png")
    Gold_King_Image =Image.open("iloveimg-resized/wk2.png")
    Gold_Queen_Image = Image.open("iloveimg-resized/wq2.png")

    def __init__(self, chess_window):
        super().__init__(chess_window)
        chess_window.title("Chess Game For AI Project      PvP")
        self.place(width=800, height=800)
        chess_window.geometry("800x800")
        self.selected_square=False
        self.selected_square_tuple=0
        self.selected_square_moves=0
        self.selected_piece=""
        self.color_turn=2
        self.check=False
        self.PhotoPixel=tk.PhotoImage(width=1, height=1)
        self.BlackPiecesPhotos={"Pawn":   ImageTk.PhotoImage(ChessApp.Black_Pawn_Image),
        "Horse": ImageTk.PhotoImage(ChessApp.Black_Horse_Image),
        "Knight":  ImageTk.PhotoImage(ChessApp.Black_Knight_Image),
        "Tower":  ImageTk.PhotoImage(ChessApp.Black_Tower_Image),
        "King":   ImageTk.PhotoImage(ChessApp.Black_King_Image),
        "Queen":  ImageTk.PhotoImage(ChessApp.Black_Queen_Image)}
        self.GoldPiecesPhotos={"Pawn":   ImageTk.PhotoImage(ChessApp.Gold_Pawn_Image),
        "Horse": ImageTk.PhotoImage(ChessApp.Gold_Horse_Image),
        "Knight":  ImageTk.PhotoImage(ChessApp.Gold_Knight_Image),
        "Tower":  ImageTk.PhotoImage(ChessApp.Gold_Tower_Image),
        "King":   ImageTk.PhotoImage(ChessApp.Gold_King_Image),
        "Queen":  ImageTk.PhotoImage(ChessApp.Gold_Queen_Image)}
        self.GoldPiecesAlive={"Pawn":   [(6, i) for i in range(8)],
        "Knight": [(7, 2), (7, 5)],
        "Tower":  [(7, 0), (7, 7)],
        "Horse":  [(7, 1), (7, 6)],
        "King":   [(7, 4)],
        "Queen":  [(7, 3)]}
        self.BlackPiecesAlive={"Pawn":   [(1, i) for i in range(8)],
        "Knight": [(0, 2), (0, 5)],
        "Tower":  [(0, 0), (0, 7)],
        "Horse":  [(0, 1), (0, 6)],
        "King":   [(0, 4)],
        "Queen":  [(0, 3)]}
        self.Board=[[AbstractPiece(self, y, x, image=self.PhotoPixel, width=99, height=87, compound="c") for x in range(8)] for y in range(8)]
        self.CreateBoard()
        self.CreatePieces()
        self.targetedbrown=self.CheckPlayerMoves(self.GoldPiecesAlive)
        self.targetedgray=self.CheckPlayerMoves(self.BlackPiecesAlive)

    def CreatePieces(self):
        def IterRender(PieceAliveDict, PieceAlivePhoto, color):
            for a, b in PieceAliveDict.items():
                if b:
                    for item in b:
                        # noinspection PyTypeChecker
                        self.RenderPiece(self.Board[item[0]][item[1]], PieceAlivePhoto[a], a, color)
        IterRender(self.BlackPiecesAlive, self.BlackPiecesPhotos, 1)
        IterRender(self.GoldPiecesAlive, self.GoldPiecesPhotos, 2)

    def CreateBoard(self):
        for i, row in enumerate(self.Board):
            for h, square in enumerate(row):
                if (i+1)%2!=0:
                    if (h+1)%2!=0:
                        square.defaulbg="silver"
                    elif (h+1)%2==0:
                        square.defaulbg="dimgray"
                elif (i+1)%2==0:
                    if (h+1)%2!=0:
                        square.defaulbg="dimgray"
                    elif (h+1)%2==0:
                        square.defaulbg="silver"
                square.configure(bg=square.defaulbg)
                square.bind('<Button-1>', lambda event, Square=square: self.PieceSelect(Square))
                square.grid(row=i, column=h)

    def UpdateBoard(self):
        for row in self.Board:
            for square in row:
                square.configure(bg=square.defaulbg, image=self.PhotoPixel)
                square.image=self.PhotoPixel
                square.current_piece=""
                square.color=0
                square.selected=False
                square.update()
        self.CreatePieces()
        self.after(0)

    def RenderPiece(self, Square, img, name, color):
        Square.configure(image=img)
        Square.image=img
        Square.current_piece=name
        Square.color= color
        Square.update()

    def EndTurn(self, Square):

        if self.color_turn==1:
            print(f"Black player just moved its {self.selected_piece} from {self.selected_square_tuple} to {(Square.row, Square.column)}")
            self.targetedgray=self.CheckPlayerMoves(self.BlackPiecesAlive)
            print(f"Black player Possible Moves: {sorted(self.targetedgray)}")
            for item in self.targetedgray:
                if item==self.GoldPiecesAlive["King"][0]:
                    self.check=True
                    print("CHECK")
            self.color_turn=2
        elif self.color_turn==2:
            print(f"Gold player just moved its {self.selected_piece} from {self.selected_square_tuple} to {(Square.row, Square.column)}")
            self.targetedbrown=self.CheckPlayerMoves(self.GoldPiecesAlive)
            print(f"Gold Player Possible Moves: {sorted(self.targetedbrown)}")
            for item in self.targetedbrown:
                if item==self.BlackPiecesAlive["King"][0]:
                    self.check=True
                    print("CHECK")
            self.color_turn=1
        print("---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
        self.selected_square=False
        self.selected_square_tuple=0
        self.selected_square_moves=0
        self.selected_piece=""

    def Checkmate(self):
        if self.check:
            if self.color_turn == 1:
                for king_move in self.PieceMove(
                        self.Board[self.GoldPiecesAlive["King"][0][0]][self.GoldPiecesAlive["King"][0][1]]):
                    if king_move not in self.targetedgray:
                        return False
                return True
            elif self.color_turn == 2:
                for king_move in self.PieceMove(
                        self.Board[self.BlackPiecesAlive["King"][0][0]][self.BlackPiecesAlive["King"][0][1]]):
                    if king_move not in self.targetedbrown:
                        return False
                return True
        return False

    # noinspection PyTypeChecker
    def ExecuteMove(self, Square):
        def MovePiece(Square, piecename, piecearr):
            if self.selected_piece==piecename:
                for item in piecearr:
                    if item[0]==self.selected_square_tuple[0] and item[1]==self.selected_square_tuple[1]:
                        holder = list(item)
                        piecearr.remove(item)
                        holder[0]=Square.row
                        holder[1]=Square.column
                        piecearr.append(tuple(holder))
        for item in self.selected_square_moves:
            if Square.row==item[0] and Square.column==item[1]:
                if Square.current_piece!="":
                    self.EatPiece(Square)
                if self.color_turn==1:
                    MovePiece(Square, self.selected_piece, self.BlackPiecesAlive[self.selected_piece])
                elif self.color_turn==2:
                    MovePiece(Square, self.selected_piece, self.GoldPiecesAlive[self.selected_piece])
        self.UpdateBoard()
        self.after(0)

    def PieceSelect(self, Square):
        if not Square.selected and not self.selected_square and Square.color==self.color_turn:
            Square.configure(bg="yellow")
            Square.selected=True
            self.selected_piece=Square.current_piece
            self.selected_square=True
            self.selected_square_tuple=(Square.row, Square.column)
            self.selected_square_moves=self.PieceMove(Square)
            try:
                for item in self.selected_square_moves:
                    self.Board[item[0]][item[1]].configure(bg="white")
                    self.Board[item[0]][item[1]].update()
            except IndexError:
                pass

        elif (not Square.selected and self.selected_square and Square.color==0)\
         or (not Square.selected and self.selected_square and Square.color!=self.color_turn):
            if self.CheckCalc(Square):
                self.ExecuteMove(Square)
                self.EndTurn(Square)
                Square.used = True
            else:
                print("You can't do that move, take care of your King")

        elif Square.selected and self.selected_square and Square.color==self.color_turn:
            print("Rethink!")
            Square.selected=False
            self.selected_square=False
            self.selected_square_moves=0
            self.selected_square_tuple=0
            self.selected_piece=""
            self.UpdateBoard()

    def EatPiece(self, Square):
        def eatsetup(piecearr):
            for item in piecearr:
                if item[0]==Square.row and item[1]==Square.column:
                    print(f"{'Gold' if Square.color==1 else 'Black'} Player\'s {self.selected_piece} ate {'Black' if Square.color==1 else 'Gold'} Player\'s {Square.current_piece}")
                    piecearr.remove(item)
        if Square.color==1:
            eatsetup(self.BlackPiecesAlive[Square.current_piece])
        elif Square.color==2:
            eatsetup(self.GoldPiecesAlive[Square.current_piece])

    def MinOfTwo(self, a, b):
        if a>b:
            return b
        else:
            return a

    def IterMove(self, a, b, movelist, Square):
        if a<0 or b<0:
            return False
        elif self.Board[a][b].current_piece!="" and self.Board[a][b].color==Square.color:
            return False
        elif self.Board[a][b].current_piece!="" and self.Board[a][b].color!=Square.color:
            movelist.append((a, b))
            return False
        else:
            movelist.append((a, b))
            return True

    def NormalMove(self, a, b, movelist, Square):
        if self.Board[a][b].current_piece=="" or self.Board[a][b].color!=Square.color:
            movelist.append((a, b))

    def EmptySpaceAdd(self, a, b, movelist):
        if self.Board[a][b].current_piece=="":
            movelist.append((a, b))

    def PossibleMove(self, a, b, movelist, Square):
        if self.Board[a][b].current_piece!="" and self.Board[a][b].color!=Square.color:
            movelist.append((a, b))

    def HorseMove(self, a, b, movelist, Square):
        if self.Board[a][b].current_piece=="" or self.Board[a][b].color!=Square.color:
            movelist.append((a, b))

    def CheckPlayerMoves(self, piecedict):
        movelist=[]
        for values in piecedict.values():
            for item in values:
                movelist+=self.PieceMove(self.Board[item[0]][item[1]])
        return list(set(movelist))

    def CheckMovesHelper(self, piecedict, piece, Square):
        movelist=[]
        class square(object):
            def __init__(self, Square):
                self.color=Square.color
                self.row=Square.row
                self.column=Square.column
                self.current_piece=super.current_piece
        for key, values in piecedict.items():
            for item in values:
                if item!=self.selected_square_tuple:
                    movelist+=self.PieceMove(self.Board[item[0]][item[1]])
                elif item==self.selected_square_tuple:
                    movelist+=self.PieceMove(square(Square))
        return list(set(movelist))

    def CheckCalc(self, Square):
        a = self.selected_piece
        b = self.selected_square_tuple
        x = Square
        if self.check:
            if self.color_turn==1:
                for item in self.CheckMovesHelper(self.GoldPiecesAlive, Square.current_piece, Square):
                    if self.selected_piece!="King":
                        if item==self.BlackPiecesAlive["King"][0]:
                           return False
                    else:
                        if item==(Square.row, Square.column):
                            return False
                return True
            elif self.color_turn==2:
                for item in self.CheckMovesHelper(self.BlackPiecesAlive, Square.current_piece, Square):
                    if self.selected_piece!="King":
                        if item==self.GoldPiecesAlive["King"][0]:
                           return False
                    else:
                        if item==(Square.row, Square.column):
                            return False
                return True
        else:
            return True

    def PieceMove(self, Square):
        movelist=[]
        if Square.current_piece=="Pawn":
            if Square.color==2:
                self.EmptySpaceAdd(Square.row-1, Square.column, movelist)
                if not Square.used and self.Board[Square.row-1][Square.column].current_piece=="":
                    self.EmptySpaceAdd(Square.row-2, Square.column, movelist)
                try:
                    self.PossibleMove(Square.row-1, Square.column-1, movelist, Square)
                    self.PossibleMove(Square.row-1, Square.column+1, movelist, Square)
                except IndexError:
                    pass
            elif Square.color==1:
                self.EmptySpaceAdd(Square.row+1, Square.column, movelist)
                if not Square.used and self.Board[Square.row+1][Square.column].current_piece=="":
                    self.EmptySpaceAdd(Square.row+2, Square.column, movelist)
                try:
                    self.PossibleMove(Square.row+1, Square.column-1, movelist, Square)
                    self.PossibleMove(Square.row+1, Square.column+1, movelist, Square)
                except IndexError:
                    pass
        elif Square.current_piece=="Horse":
            if Square.row+2<=7 and Square.column+1<=7:
                self.HorseMove(Square.row+2, Square.column+1, movelist, Square)
            if Square.row+2<=7 and Square.column-1>=0:
                self.HorseMove(Square.row+2, Square.column-1, movelist, Square)
            if Square.row-2>=0 and Square.column+1<=7:
                self.HorseMove(Square.row-2, Square.column+1, movelist, Square)
            if Square.row-2>=0 and Square.column-1>=0:
                self.HorseMove(Square.row-2, Square.column-1, movelist, Square)
            if Square.row-1>=0 and Square.column-2>=0:
                self.HorseMove(Square.row-1, Square.column-2, movelist, Square)
            if Square.row-1>=0 and Square.column+2<=7:
                self.HorseMove(Square.row-1, Square.column+2, movelist, Square)
            if Square.row+1<=7 and Square.column-2>=0:
                self.HorseMove(Square.row+1, Square.column-2, movelist, Square)
            if Square.row+1<=7 and Square.column+2<=7:
                self.HorseMove(Square.row+1, Square.column+2, movelist, Square)
        elif Square.current_piece=="Tower":
            for i in range(Square.row-1, -1, -1):
                if not self.IterMove(i, Square.column, movelist, Square):
                    break
            for i in range(Square.column-1, -1, -1):
                if not self.IterMove(Square.row, i, movelist, Square):
                    break
            for i in range(1, 8-Square.row):
                if not self.IterMove(Square.row+i, Square.column, movelist, Square):
                    break
            for i in range(1, 8-Square.column):
                if not self.IterMove(Square.row, Square.column+i, movelist, Square):
                    break
        elif Square.current_piece=="Knight":
            for i in range(1, self.MinOfTwo(Square.row, Square.column)+1):
                if not self.IterMove(Square.row-i, Square.column-i, movelist, Square):
                    break
            for i in range(1, self.MinOfTwo(Square.row, 7-Square.column)+1):
                if not self.IterMove(Square.row-i, Square.column+i, movelist, Square):
                    break
            for i in range(1, self.MinOfTwo(7-Square.row, Square.column)+1):
                if not self.IterMove(Square.row+i, Square.column-i, movelist, Square):
                    break
            for i in range(1, self.MinOfTwo(7-Square.row, 7-Square.column)+1):
                if not self.IterMove(Square.row+i, Square.column+i, movelist, Square):
                    break
        elif Square.current_piece=="King":
            try:
                if Square.row-1>=0:
                    self.NormalMove(Square.row-1, Square.column, movelist, Square)
                if Square.row+1<=7:
                    self.NormalMove(Square.row+1, Square.column, movelist, Square)
                if Square.column-1>=0:
                    self.NormalMove(Square.row, Square.column-1, movelist, Square)
                if Square.column+1<=7:
                    self.NormalMove(Square.row, Square.column+1, movelist, Square)
                if Square.row-1>=0 and Square.column-1>=0:
                    self.NormalMove(Square.row-1, Square.column-1, movelist, Square)
                if Square.row+1<=7 and Square.column-1>=0:
                    self.NormalMove(Square.row+1, Square.column-1, movelist, Square)
                if Square.row-1>=0 and Square.column+1<=7:
                    self.NormalMove(Square.row-1, Square.column+1, movelist, Square)
                if Square.row+1<=7 and Square.column+1<=7:
                    self.NormalMove(Square.row+1, Square.column+1, movelist, Square)
            except IndexError:
                pass
        elif Square.current_piece=="Queen":
            for i in range(Square.row-1, -1, -1):
                if not self.IterMove(i, Square.column, movelist, Square):
                    break
            for i in range(Square.column-1, -1, -1):
                if not self.IterMove(Square.row, i, movelist, Square):
                    break
            for i in range(1, 8-Square.row):
                if not self.IterMove(Square.row+i, Square.column, movelist, Square):
                    break
            for i in range(1, 8-Square.column):
                if not self.IterMove(Square.row, Square.column+i, movelist, Square):
                    break
            for i in range(1, self.MinOfTwo(Square.row, Square.column)+1):
                if not self.IterMove(Square.row-i, Square.column-i, movelist, Square):
                    break
            for i in range(1, self.MinOfTwo(Square.row, 7-Square.column)+1):
                if not self.IterMove(Square.row-i, Square.column+i, movelist, Square):
                    break
            for i in range(1, self.MinOfTwo(7-Square.row, Square.column)+1):
                if not self.IterMove(Square.row+i, Square.column-i, movelist, Square):
                    break
            for i in range(1, self.MinOfTwo(7-Square.row, 7-Square.column)+1):
                if not self.IterMove(Square.row+i, Square.column+i, movelist, Square):
                    break
        return movelist

def EndTurn(self, Square):
    if self.color_turn == 1:
        print(f"Black player just moved its {self.selected_piece} from {self.selected_square_tuple} to {(Square.row, Square.column)}")
        self.targetedgray = self.CheckPlayerMoves(self.BlackPiecesAlive)
        print(f"Black player Possible Moves: {sorted(self.targetedgray)}")
        checkmate = self.CheckmateCheck(self.BlackPiecesAlive, self.targetedgray)
        if checkmate:
            print("CHECKMATE! Gold player wins!")
            return
        for item in self.targetedgray:
            if item == self.GoldPiecesAlive["King"][0]:
                self.check = True
                print("CHECK")
        self.color_turn = 2
    elif self.color_turn == 2:
        print(f"Gold player just moved its {self.selected_piece} from {self.selected_square_tuple} to {(Square.row, Square.column)}")
        self.targetedbrown = self.CheckPlayerMoves(self.GoldPiecesAlive)
        print(f"Gold Player Possible Moves: {sorted(self.targetedbrown)}")
        checkmate = self.CheckmateCheck(self.GoldPiecesAlive, self.targetedbrown)
        if checkmate:
            print("CHECKMATE! Black player wins!")
            return
        for item in self.targetedbrown:
            if item == self.BlackPiecesAlive["King"][0]:
                self.check = True
                print("CHECK")
        self.color_turn = 1
    print("---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    self.selected_square = False
    self.selected_square_tuple = 0
    self.selected_square_moves = 0
    self.selected_piece = ""

def CheckmateCheck(self, piecedict, movelist):
    for key, values in piecedict.items():
        for item in values:
            for move in self.PieceMove(self.Board[item[0]][item[1]]):
                if move not in movelist:
                    return False
    return True


def main():
    aa = tk.Tk()
    cc = ChessApp(aa)
    cc.mainloop()

if __name__ == "__main__":
    main()
