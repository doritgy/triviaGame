import tkinter as tk

# Create the Tkinter root window
root = tk.Tk()
root.title("Test Exit Game")

def exit_game():
    """
    Exit the game by stopping the Tkinter main loop and closing the window safely.
    """
    print("Exit game button clicked!")  # Debug print
    root.quit()  # Stop the Tkinter main loop
    root.destroy()  # Safely destroy the root window and exit

# Add buttons
tk.Button(root, text="Exit Game", command=exit_game).pack()

# Start Tkinter event loop
root.mainloop()