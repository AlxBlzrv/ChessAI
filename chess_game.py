import tkinter as tk
from PIL import Image, ImageTk
import chess
import chess.engine

class ChessBoard:
    def __init__(self, master):
        # Initialize the chessboard with a window title and canvas
        self.master = master
        self.master.title("Chess Board")
        self.canvas = tk.Canvas(master, width=480, height=480)
        self.canvas.pack()

        # Load images for the chess pieces from the specified directory
        self.images = {
            'wp': ImageTk.PhotoImage(Image.open("D:\\Dell\\repos\\chess\\pieces\\wp.png").convert("RGBA")),
            'wn': ImageTk.PhotoImage(Image.open("D:\\Dell\\repos\\chess\\pieces\\wn.png").convert("RGBA")),
            'wb': ImageTk.PhotoImage(Image.open("D:\\Dell\\repos\\chess\\pieces\\wb.png").convert("RGBA")),
            'wr': ImageTk.PhotoImage(Image.open("D:\\Dell\\repos\\chess\\pieces\\wr.png").convert("RGBA")),
            'wq': ImageTk.PhotoImage(Image.open("D:\\Dell\\repos\\chess\\pieces\\wq.png").convert("RGBA")),
            'wk': ImageTk.PhotoImage(Image.open("D:\\Dell\\repos\\chess\\pieces\\wk.png").convert("RGBA")),
            'bp': ImageTk.PhotoImage(Image.open("D:\\Dell\\repos\\chess\\pieces\\bp.png").convert("RGBA")),
            'bn': ImageTk.PhotoImage(Image.open("D:\\Dell\\repos\\chess\\pieces\\bn.png").convert("RGBA")),
            'bb': ImageTk.PhotoImage(Image.open("D:\\Dell\\repos\\chess\\pieces\\bb.png").convert("RGBA")),
            'br': ImageTk.PhotoImage(Image.open("D:\\Dell\\repos\\chess\\pieces\\br.png").convert("RGBA")),
            'bq': ImageTk.PhotoImage(Image.open("D:\\Dell\\repos\\chess\\pieces\\bq.png").convert("RGBA")),
            'bk': ImageTk.PhotoImage(Image.open("D:\\Dell\\repos\\chess\\pieces\\bk.png").convert("RGBA")),
        }

        # Create a new chess board (using python-chess library)
        self.board = chess.Board()
        self.draw_board()

        # Bind mouse events for click, drag, and release
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        self.selected_piece = None  # Track selected piece
        self.selected_coords = None  # Track piece coordinates
        self.ai_turn = False  # Flag to manage AI's turn

    def draw_board(self):
        # Draw the chessboard and pieces on the canvas
        colors = ["#DDB88C", "#A66D4D"]  # Light and dark square colors
        self.canvas.delete("all")  # Clear canvas
        for r in range(8):
            for c in range(8):
                x1, y1 = c * 60, (7 - r) * 60  # Calculate top-left corner of each square
                x2, y2 = x1 + 60, y1 + 60  # Bottom-right corner
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=colors[(r + c) % 2])  # Draw square
                piece = self.board.piece_at(r * 8 + c)  # Get piece at current square
                if piece:
                    piece_name = piece.symbol().lower()  # Get piece symbol (e.g., 'p', 'r', etc.)
                    color = 'w' if piece.color == chess.WHITE else 'b'  # Determine piece color (white/black)
                    self.canvas.create_image(x1 + 30, y1 + 30, image=self.images[f"{color}{piece_name}"])  # Place piece image

    def on_click(self, event):
        # Handle when a piece is clicked
        x, y = event.x // 60, (480 - event.y) // 60  # Get the clicked square coordinates
        if self.board.piece_at(y * 8 + x) and self.board.turn == chess.WHITE:  # Check if there's a piece and it's white's turn
            self.selected_piece = (x, y)  # Select piece

    def on_drag(self, event):
        # Handle dragging of a piece
        if self.selected_piece:
            self.canvas.coords(self.selected_piece, event.x, event.y)  # Update piece's position

    def on_release(self, event):
        # Handle releasing the piece (dropping it on a square)
        if self.selected_piece:
            x, y = event.x // 60, (480 - event.y) // 60  # Get the square coordinates where piece is released
            if 0 <= x < 8 and 0 <= y < 8:  # Ensure the drop is within bounds
                move = chess.Move.from_uci(f"{chess.square_name(self.selected_piece[0] + self.selected_piece[1] * 8)}{chess.square_name(x + y * 8)}")  # Create a move
                if move in self.board.legal_moves:  # Check if the move is legal
                    self.board.push(move)  # Make the move on the board
                    self.draw_board()  # Redraw the board
                    self.ai_turn = True  # Set AI's turn
                    self.ai_move()  # Trigger AI's move

    def ai_move(self):
        # Let the AI make its move
        if self.ai_turn:
            if self.board.is_game_over():
                return  # Stop if the game is over
            with chess.engine.SimpleEngine.popen_uci("D:\\Dell\\repos\\chess\\stockfish\\stockfish-windows-x86-64-sse41-popcnt.exe") as engine:
                result = engine.play(self.board, chess.engine.Limit(time=2.0))  # AI makes a move with a 2-second time limit
                self.board.push(result.move)  # Push AI's move onto the board
                self.draw_board()  # Redraw board
                self.ai_turn = False  # Reset AI's turn flag

if __name__ == "__main__":
    root = tk.Tk()  # Create a Tkinter window
    chess_board = ChessBoard(root)  # Create a ChessBoard instance
    root.mainloop()  # Start the Tkinter main loop
