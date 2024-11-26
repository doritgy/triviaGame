import tkinter as tk
from tkinter import messagebox
import psycopg2
import game_initialize

conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="admin",
    host="localhost",
    port="5560"
)
cur = conn.cursor()

# Global variables
current_player_id = None
current_question = None
player_score = 0
ques_win = None
root = None  # Define root globally to prevent multiple windows

def reset_game_state():
    """ Resets the game state for a new session. """
    global current_player_id, current_question, player_score, ques_win
    current_player_id = None
    current_question = None
    player_score = 0
    if ques_win is not None:
        ques_win.destroy()  # Close the question window if it's open
        ques_win = None

def main():
    global root, current_player_id
    root = tk.Tk()  # Create the root window once
    root.withdraw()  # Hide the root window until login is done

    # Start the game by logging in or registering
    login_or_register()

    root.mainloop()  # Start the Tkinter event loop (only once!)

    cur.close()
    conn.close()

def login_or_register():
    """Handles the login or registration process."""
    global current_player_id
    reset_game_state()  # Reset game state before a new login or registration

    current_player_id = game_initialize.initialize()
    if current_player_id:
        if current_player_id == 999999:
            root.quit()  # Exit the game if 999999 is returned
        else:
            if not root.winfo_viewable():  # Checks if the root window is already shown
                root.deiconify()  # Show the root window
            show_question(current_player_id)
    else:
        messagebox.showerror("Error", "Failed to login or register.")

def show_question(current_player_id: int):
    global current_question, ques_win
    if ques_win is None:  # Create a new window only if it doesn't exist
        ques_win = tk.Toplevel()
        ques_win.title("Trivia Game")

        # Create a label to show the question text
        ques_win.question_label = tk.Label(ques_win, text="")
        ques_win.question_label.pack()

        ques_win.selected_answer = tk.StringVar(value="a")

        ques_win.radio_a = tk.Radiobutton(ques_win, text="", variable=ques_win.selected_answer, value="a")
        ques_win.radio_a.pack()

        ques_win.radio_b = tk.Radiobutton(ques_win, text="", variable=ques_win.selected_answer, value="b")
        ques_win.radio_b.pack()

        ques_win.radio_c = tk.Radiobutton(ques_win, text="", variable=ques_win.selected_answer, value="c")
        ques_win.radio_c.pack()

        ques_win.radio_d = tk.Radiobutton(ques_win, text="", variable=ques_win.selected_answer, value="d")
        ques_win.radio_d.pack()

        tk.Button(ques_win, text="Submit Answer", command=lambda: submit_answer(ques_win.selected_answer.get())).pack()

    # Fetch the next question
    fetch_new_question(current_player_id)

def fetch_new_question(current_player_id: int):
    global current_question
    cur.execute("SELECT * FROM questions ORDER BY RANDOM() LIMIT 1")
    current_question = cur.fetchone()

    if not current_question:
        messagebox.showinfo("No Questions", "No questions available.")
        ques_win.destroy()
        return

    question_id, question_text, answer_a, answer_b, answer_c, answer_d, correct_answer = current_question

    cur.execute(
        "SELECT p.question_id FROM player_answers p WHERE p.question_id = %s AND p.player_id = %s",
        (question_id, current_player_id)
    )
    saved_question = cur.fetchone()

    if saved_question:
        messagebox.showinfo("Info", "You have already answered this question. Fetching a new one.")
        fetch_new_question(current_player_id)  # Recursively fetch a new question if already answered
    else:
        ques_win.question_label.config(text=question_text)
        ques_win.radio_a.config(text=f"a) {answer_a}")
        ques_win.radio_b.config(text=f"b) {answer_b}")
        ques_win.radio_c.config(text=f"c) {answer_c}")
        ques_win.radio_d.config(text=f"d) {answer_d}")

def submit_answer(selected_answer: str):
    global player_score, current_player_id, current_question

    if current_player_id is None or current_question is None:
        messagebox.showerror("Error", "You need to login and answer a question first.")
        return

    question_id = current_question[0]
    correct_answer = current_question[6]
    is_correct = selected_answer == correct_answer

    cur.execute(
        "INSERT INTO player_answers (player_id, question_id, selected_answer, is_correct) VALUES (%s, %s, %s, %s)",
        (current_player_id, question_id, selected_answer, is_correct)
    )
    conn.commit()

    if is_correct:
        player_score += 1
        cur.execute("UPDATE players SET score = %s WHERE player_id = %s", (player_score, current_player_id))
        conn.commit()
        messagebox.showinfo("Correct!", f"Your answer is correct. Your new score is now {player_score}.")
    else:
        messagebox.showinfo("Wrong!", f"Wrong answer! The correct answer was '{correct_answer}'. Your score remains {player_score}.")

    cur.execute("SELECT COUNT(*) FROM player_answers WHERE player_id = %s", (current_player_id,))
    num_of_questions = cur.fetchone()[0]

    if num_of_questions % 20 == 0:
        messagebox.showinfo("Game over", f"You answered 20 questions. Your score is now {player_score}.")
        cur.execute("UPDATE players SET score = %s WHERE player_id = %s", (0, current_player_id))
        conn.commit()
        ques_win.destroy()
        login_or_register()  # Reset game without closing the root window
    else:
        fetch_new_question(current_player_id)

if __name__ == "__main__":
    main()