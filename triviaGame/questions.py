import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import psycopg2
from select import select

# You will need to pass cur, conn, current_player_id from the main application
current_question = None
ques_win = None
#player_score = 0

def show_question(cur, conn, current_player_id: any, player_score):
    global current_question, ques_win
    if ques_win is None or not ques_win.winfo_exists():
        ques_win = tk.Toplevel()
        ques_win.title("Trivia Game")

        # Set a protocol handler for when the user closes the window with "X"
        ques_win.protocol("WM_DELETE_WINDOW", on_close_question_window)

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

        ques_win.radio_s = tk.Radiobutton(ques_win, text="", variable=ques_win.selected_answer, value="s")
        ques_win.radio_s.pack()

        tk.Button(ques_win, text="Submit Answer", command=lambda: submit_answer(cur, conn, current_player_id, player_score, ques_win.selected_answer.get())).pack()

    # Fetch the next question
    fetch_new_question(cur, current_player_id, player_score)



def on_close_question_window():
    """ Handle the event when the user closes the question window with 'X'. """
    global ques_win
    ques_win.destroy()
    ques_win = None  # Reset ques_


def fetch_new_question(cur, current_player_id: int, player_score):
    global current_question, ques_win
    cur.execute("SELECT * FROM questions ORDER BY RANDOM() LIMIT 1")
    current_question = cur.fetchone()

    if not current_question:
        messagebox.showinfo("No Questions", "No questions available.")
        if ques_win:
            ques_win.destroy()
            ques_win = None
        return

    question_id, question_text, answer_a, answer_b, answer_c, answer_d, correct_answer = current_question
    #print(f"Question: {question_text}, A: {answer_a}, B: {answer_b}, C: {answer_c}, D: {answer_d}")
    cur.execute(
        "SELECT p.question_id FROM player_answers p WHERE p.question_id = %s AND p.player_id = %s",
        (question_id, current_player_id[0])
    )
    saved_question = cur.fetchone()

    if saved_question:
        messagebox.showinfo("Info", "You have already answered this question. Fetching a new one.")
        fetch_new_question(cur, current_player_id, player_score)  # Recursively fetch a new question if already answered
    else:
        if ques_win:
            ques_win.question_label.config(text=question_text)
            ques_win.radio_a.config(text=f"a) {answer_a}")
            ques_win.radio_b.config(text=f"b) {answer_b}")
            ques_win.radio_c.config(text=f"c) {answer_c}")
            ques_win.radio_d.config(text=f"d) {answer_d}")
            ques_win.radio_s.config(text=f"s) 'personal_statistics'")


def submit_answer(cur, conn, current_player_id: int,player_score, selected_answer: str):
    global current_question, ques_win

    if current_player_id is None or current_question is None:
        messagebox.showerror("Error", "You need to login and answer a question first.")
        return
    if selected_answer == "s":
        personal_statistics(cur, conn, current_player_id)
        return
    question_id = current_question[0]
    correct_answer = current_question[6]
    is_correct = selected_answer == correct_answer

    cur.execute(
        "INSERT INTO player_answers (player_id, question_id, selected_answer, is_correct, login_time) VALUES (%s, %s, %s, %s, %s)",
        (current_player_id[0], question_id, selected_answer, is_correct, datetime.now())
    )
    conn.commit()

    if is_correct:
        player_score[0] += 1
        cur.execute("UPDATE players SET score = %s WHERE player_id = %s", (player_score[0], current_player_id[0]))
        conn.commit()
        messagebox.showinfo("Correct!", f"Your answer is correct. Your new score is now {player_score[0]}.")
    else:
        messagebox.showinfo("Wrong!", f"Wrong answer! The correct answer was '{correct_answer}'. Your score remains {player_score[0]}.")

    cur.execute("SELECT COUNT(*) FROM player_answers WHERE player_id = %s", (current_player_id[0],))
    num_of_questions = cur.fetchone()[0]

    if num_of_questions % 3 == 0:
        messagebox.showinfo("Game over", f"You answered 20 questions. Your score is now {player_score}.")
        # cur.execute("UPDATE players SET score = %s WHERE player_id = %s", (0, current_player_id[0]))
        # conn.commit()
        cur.execute("SELECT last_login FROM players WHERE player_id = %s", (current_player_id[0],))
        last_login = cur.fetchone()[0]
        achieved_in = datetime.now() - last_login

        # Insert or update high score
        update_high_scores(cur, conn, current_player_id[0], player_score[0], achieved_in)

        messagebox.showinfo("Game over", f"You answered 20 questions. Your score is now {player_score[0]}.")
        ques_win.destroy()
        # ques_win = None
        return
    else:
        fetch_new_question(cur, current_player_id, player_score)

def update_high_scores(cur, conn, player_id: int, score: int, achieved_in):
    cur.execute(
        "INSERT INTO high_scores (player_id, score, achieved_in) VALUES (%s, %s, %s) RETURNING score_id",
        (player_id, score, achieved_in)
    )
    conn.commit()
    new_score_id = cur.fetchone()[0]

    # Check if there are more than 5 scores
    cur.execute("SELECT score_id FROM high_scores ORDER BY score DESC, achieved_in LIMIT 5")
    top_five_ids = [row[0] for row in cur.fetchall()]

    # If the new score_id is not in the top five, delete it
    if new_score_id not in top_five_ids:
        cur.execute("DELETE FROM high_scores WHERE score_id = %s", (new_score_id,))
        conn.commit()

    # Remove any extra scores beyond the top 5
    cur.execute("DELETE FROM high_scores WHERE score_id NOT IN %s", (tuple(top_five_ids),))
    conn.commit()

def personal_statistics(cur, conn, current_player_id:int):
    import tkinter as tk
    from tkinter import ttk
    cur.execute("select count(*) from player_answers p where p.player_id = %s", current_player_id)
    num_of_questions = cur.fetchone()[0]
    cur.execute("select count(*) from player_answers p where p.player_id = %s and is_correct", current_player_id)
    num_of_correct_answers = cur.fetchone()[0]
    num_of_last_questions = num_of_questions % 20
    num_of_full_games = num_of_questions / 20
    if num_of_last_questions == 0:
        exp = "You played only full games"

    root = tk.Tk()
    root.title("Player Statistics")
    root.geometry("300x250")

    def on_closing():
        root.destroy()  # Close the window
        root.quit()  # Quit the Tkinter main loop to return to the calling function

    root.protocol("WM_DELETE_WINDOW", on_closing)
    # Create a frame for layout
    frame = ttk.Frame(root)
    frame.pack(pady=20, padx=20)

    # Labels and values displayed in rows
    stats = [
        ("Player ID", current_player_id),
        ("Number of Full Games", num_of_full_games),
        ("Number of Questions", num_of_questions),
        ("Number of Last Questions", num_of_last_questions),
        ("Number of Correct Answers", num_of_correct_answers)
    ]

    # Loop through the stats to display each in a row
    for i, (label_text, value) in enumerate(stats):
        label = ttk.Label(frame, text=f"{label_text}:")
        label.grid(row=i, column=0, sticky="W", padx=5, pady=5)
        value_label = ttk.Label(frame, text=str(value))
        value_label.grid(row=i, column=1, padx=5, pady=5)

    # Run the application
    root.mainloop()




