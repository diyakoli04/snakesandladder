import random
import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk  # Correct import for resizing images

# Snakes and Ladders positions
snakes = {98: 79, 94: 75, 93: 73, 87: 36, 62: 19, 64: 60, 54: 34, 17: 7}
ladders = {4: 15, 9: 31, 28: 84, 1: 38, 21: 42, 51: 67, 80: 99, 72: 91}

# Player Positions
positions = {"Red": 1, "Blue": 1}
current_turn = "Red"  # Track whose turn it is

# Game Setup
root = tk.Tk()
root.title("Snakes and Ladders")

# Load Board Image
original_board = Image.open(r"board.jpg")
resized_board = original_board.resize((500, 500))  # Adjust size as needed
board_img = ImageTk.PhotoImage(resized_board)

# Create Canvas and Set Board Image
canvas = tk.Canvas(root, width=500, height=500)
canvas.pack()
canvas.create_image(0, 0, anchor=tk.NW, image=board_img)

# Load Dice Images
dice_images = {
    1: ImageTk.PhotoImage(Image.open("dice_1.jpeg")),
    2: ImageTk.PhotoImage(Image.open("dice_2.jpeg")),
    3: ImageTk.PhotoImage(Image.open("dice_3.jpeg")),
    4: ImageTk.PhotoImage(Image.open("dice_4.jpeg")),
    5: ImageTk.PhotoImage(Image.open("dice_5.jpeg")),
    6: ImageTk.PhotoImage(Image.open("dice_6.jpeg")),
}

# Player Turn Display
turn_label = tk.Label(root, text="Red's Turn", font=("Arial", 14))
turn_label.pack()

# Dice Image Display
dice_label = tk.Label(root)
dice_label.pack()
dice_label.config(image=dice_images[1])

# Move Player Function
def move_player(player):
    global positions, current_turn

    if player != current_turn:
        return  # Prevent playing out of turn

    roll = random.randint(1, 6)
    dice_label.config(image=dice_images[roll])  # Update dice image

    new_pos = positions[player] + roll
    if new_pos <= 100:
        # Snakes or ladders check
        new_pos = snakes.get(new_pos, new_pos)
        new_pos = ladders.get(new_pos, new_pos)
        positions[player] = new_pos

    draw_players()
    root.update()

    # Check win
    if positions[player] == 100:
        win_screen(player)
        return

    # Change Turn
    current_turn = "Red" if player == "Blue" else "Blue"
    turn_label.config(text=f"{current_turn}'s Turn")
    update_buttons()

# Update Button States Based on Turn
def update_buttons():
    if current_turn == "Red":
        btn_red.config(state="normal")
        btn_blue.config(state="disabled")
    else:
        btn_red.config(state="disabled")
        btn_blue.config(state="normal")

# Draw Player Markers
player_markers = {}

def draw_players():
    for marker in player_markers.values():
        canvas.delete(marker)

    cell_size = 50
    board_size = 10

    for player, pos in positions.items():
        row = 9 - ((pos - 1) // board_size)
        col = (pos - 1) % board_size

        # Zigzag pattern adjustment
        if (9 - row) % 2 == 1:
            col = board_size - 1 - col

        x = col * cell_size + cell_size // 2
        y = row * cell_size + cell_size // 2

        color = "red" if player == "Red" else "blue"

        player_markers[player] = canvas.create_oval(
            x - 5, y - 5, x + 5, y + 5, fill=color
        )

# Win Screen
def win_screen(player):
    root.destroy()
    win_root = tk.Tk()
    win_root.configure(bg="red" if player == "Red" else "blue")
    win_root.geometry("400x400")
    label = tk.Label(win_root, text=f"{player} Won!", font=("Arial", 24, "bold"), fg="white", bg=win_root["bg"])
    label.pack(expand=True)
    win_root.mainloop()

# Buttons
btn_red = tk.Button(root, text="Red Rolls", command=lambda: move_player("Red"), bg="red", fg="white", font=("Arial", 12))
btn_red.pack(side="left", padx=20)

btn_blue = tk.Button(root, text="Blue Rolls", command=lambda: move_player("Blue"), bg="blue", fg="white", font=("Arial", 12))
btn_blue.pack(side="right", padx=20)

# Initial setup
draw_players()
update_buttons()

# Start the game
root.mainloop()

