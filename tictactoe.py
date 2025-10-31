from tkinter import *
import random
import winsound

# === LOGIQUE DU JEU ===

def next_turn(row, column):
    global player
    if buttons[row][column]["text"] == '' and check_winner() is False:
        buttons[row][column]["text"] = player
        winsound.MessageBeep()

        if check_winner() is False:
            player = players[1] if player == players[0] else players[0]
            label.config(text=(player + " turn"))

            # ✅ Si IA activée et c’est à l’IA de jouer
            if player == "O" and mode_ai.get():
                window.after(400, ai_move)
        elif check_winner() is True:
            label.config(text=(player + " wins!"))
        elif check_winner() == "Tie":
            label.config(text="Tie!")


def check_winner():
    # Lignes
    for r in range(3):
        if buttons[r][0]["text"] == buttons[r][1]["text"] == buttons[r][2]["text"] != '':
            color_win([(r, 0), (r, 1), (r, 2)])
            return True
    # Colonnes
    for c in range(3):
        if buttons[0][c]["text"] == buttons[1][c]["text"] == buttons[2][c]["text"] != '':
            color_win([(0, c), (1, c), (2, c)])
            return True
    # Diagonales
    if buttons[0][0]["text"] == buttons[1][1]["text"] == buttons[2][2]["text"] != '':
        color_win([(0, 0), (1, 1), (2, 2)])
        return True
    if buttons[0][2]["text"] == buttons[1][1]["text"] == buttons[2][0]["text"] != '':
        color_win([(0, 2), (1, 1), (2, 0)])
        return True
    # Égalité
    if all(buttons[r][c]["text"] != "" for r in range(3) for c in range(3)):
        for r in range(3):
            for c in range(3):
                buttons[r][c].config(bg="#FFD369")
        return "Tie"
    return False


def color_win(coords):
    for (r, c) in coords:
        buttons[r][c].config(bg="#32E0C4")


def new_game():
    global player
    player = random.choice(players)
    label.config(text=player + " turn")
    for r in range(3):
        for c in range(3):
            buttons[r][c].config(text="", bg="#222831", fg="#EEEEEE")
    if player == "O" and mode_ai.get():
        window.after(400, ai_move)


# === IA MINIMAX ===

def ai_move():
    """IA imbattable avec minimax"""
    best_score = -float("inf")
    best_move = None

    for r in range(3):
        for c in range(3):
            if buttons[r][c]["text"] == "":
                buttons[r][c]["text"] = "O"
                score = minimax(False)
                buttons[r][c]["text"] = ""
                if score > best_score:
                    best_score = score
                    best_move = (r, c)

    if best_move:
        next_turn(best_move[0], best_move[1])


def minimax(is_maximizing):
    result = evaluate()
    if result is not None:
        return result

    if is_maximizing:
        best_score = -float("inf")
        for r in range(3):
            for c in range(3):
                if buttons[r][c]["text"] == "":
                    buttons[r][c]["text"] = "O"
                    score = minimax(False)
                    buttons[r][c]["text"] = ""
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for r in range(3):
            for c in range(3):
                if buttons[r][c]["text"] == "":
                    buttons[r][c]["text"] = "X"
                    score = minimax(True)
                    buttons[r][c]["text"] = ""
                    best_score = min(score, best_score)
        return best_score


def evaluate():
    # Victoires O
    for r in range(3):
        if buttons[r][0]["text"] == buttons[r][1]["text"] == buttons[r][2]["text"] == "O":
            return 1
    for c in range(3):
        if buttons[0][c]["text"] == buttons[1][c]["text"] == buttons[2][c]["text"] == "O":
            return 1
    if buttons[0][0]["text"] == buttons[1][1]["text"] == buttons[2][2]["text"] == "O":
        return 1
    if buttons[0][2]["text"] == buttons[1][1]["text"] == buttons[2][0]["text"] == "O":
        return 1

    # Victoires X
    for r in range(3):
        if buttons[r][0]["text"] == buttons[r][1]["text"] == buttons[r][2]["text"] == "X":
            return -1
    for c in range(3):
        if buttons[0][c]["text"] == buttons[1][c]["text"] == buttons[2][c]["text"] == "X":
            return -1
    if buttons[0][0]["text"] == buttons[1][1]["text"] == buttons[2][2]["text"] == "X":
        return -1
    if buttons[0][2]["text"] == buttons[1][1]["text"] == buttons[2][0]["text"] == "X":
        return -1

    # Égalité
    if all(buttons[r][c]["text"] != "" for r in range(3) for c in range(3)):
        return 0
    return None


# === INTERFACE ===

window = Tk()
window.title("Tic Tac Toe Deluxe ✨")
window.configure(bg="#1B1B1B")

players = ["X", "O"]
player = random.choice(players)

label = Label(text=player + " turn", font=('consolas', 28),
              bg="#1B1B1B", fg="#FFD369")
label.pack(side="top", pady=15)

mode_ai = BooleanVar()
mode_ai.set(False)
Checkbutton(window, text="Play vs AI 🤖", font=('consolas', 14),
            variable=mode_ai, onvalue=True, offvalue=False,
            bg="#1B1B1B", fg="#EEEEEE", selectcolor="#393E46",
            activebackground="#1B1B1B").pack(pady=5)

reset_button = Button(text="New Game", font=('consolas', 16),
                      bg="#FFD369", fg="#1B1B1B",
                      activebackground="#FFB627",
                      command=new_game)
reset_button.pack(side="top", pady=10)

frame = Frame(window, bg="#1B1B1B")
frame.pack()

buttons = [[None for _ in range(3)] for _ in range(3)]

for row in range(3):
    for column in range(3):
        b = Button(frame, text="", font=('consolas', 42), width=5, height=2,
                   bg="#222831", fg="#EEEEEE",
                   activebackground="#393E46", activeforeground="#FFD369",
                   command=lambda row=row, column=column: next_turn(row, column))
        b.grid(row=row, column=column, padx=5, pady=5)
        b.bind("<Enter>", lambda e, btn=b: btn.config(bg="#393E46"))
        b.bind("<Leave>", lambda e, btn=b: btn.config(bg="#222831"))
        buttons[row][column] = b

window.mainloop()
