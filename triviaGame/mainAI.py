
import tkinter as tk
from tkinter import messagebox
import psycopg2
import bcrypt

conn = psycopg2.connect(
    dbname="postgres",  # my database name
    user="postgres",  # user PostgreSQL username
    password="admin",  # user PostgreSQL password
    host="localhost",  # host name
    port="5560"
)
cur = conn.cursor()

# Global variables
current_player_id = None
current_question = None
player_score = 0  # the score of the current player


def hash_password(password:str) ->bytes:
    """
    The function gets as parameter a password given by the user

    :return: hashed password by the "gensalt()" function using salt algorithm
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())



def check_password(hashed_password:str, user_password:str) -> bool:
    """
    The function gets the user password from the Data Base and the hashed
    password given by the login of the user
    :param hashed_password:
    :param user_password:
    :return:
    """
    ##return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password)
    return  bcrypt.checkpw(user_password.encode(), hashed_password.encode())


def register_player(username:str, password:str, email:str, age:float):
    """
    The function registers a new user, and lets the user know if he registered
    successfully or not
    The function in addition hashes the password and saves it hashed
    If the function did not succeed it rolls back the tables of the player
    so that no partial items of the player are saved, and the data base maintais
    it's integrity
    :param username:
    :param password:
    :param email:
    :param age:
    :return: No value returned
    """
    hashed_password = hash_password(password)
    try:
        cur.execute(
            "INSERT INTO players (username, password, email, age, score) VALUES (%s, %s, %s, %s, 0)",
            (username,hashed_password.decode(), email, age)
        )
        conn.commit()
        messagebox.showinfo("Success", f"Player {username} registered successfully!")
    except psycopg2.Error as e:
        conn.rollback()
        messagebox.showerror("Error", f"Could not register: {e}")



def login_player(username:str, password:str):
    """
    The function gets username and password, checks the hashed password
    checks it together with the username, and if it was successful
    shows the first random question
    return: No returned value
    """
    global current_player_id, player_score
    cur.execute("SELECT player_id, password, score FROM players WHERE username = %s", (username,))
    result = cur.fetchone()

    if result:
        player_id, stored_password, score = result
        hashed_password = stored_password
        if check_password(hashed_password, password):
            current_player_id = player_id
            player_score = score
            messagebox.showinfo("Login", f"Welcome, {username}! Your current score is {player_score}.")
            show_question()
        else:
            messagebox.showerror("Login Failed", "Incorrect password.")
    else:
        messagebox.showerror("Login Failed", "Username not found.")


def show_question():
    """
    The function shows the random question on the form, and shows the
    radio buttons for the user to choose one
    :return: No value is returned
    """

    global current_question
    global current_player_id
    while True:
        cur.execute("SELECT * FROM questions ORDER BY RANDOM() LIMIT 1")
        current_question = cur.fetchone()
        if not current_question:
            messagebox.showinfo("No Questions", "No questions available.")
            return
        print("current_question", current_question)
        question_id, question_text, answer_a, answer_b, answer_c, answer_d, correct_answer = current_question
        saved_question = cur.execute("SELECT p.question_id FROM player_answers p where p.question_id = %s\
                                     and p.player_id = %s"
                                     , (question_id, current_player_id))
        print("saved_question", saved_question)

        if saved_question:
            continue
        else:
            break
    # Insert the question and answers into the question form with radio buttons
    question_label.config(text=question_text)
    radio_a.config(text=f"a) {answer_a}", value="a")
    radio_b.config(text=f"b) {answer_b}", value="b")
    radio_c.config(text=f"c) {answer_c}", value="c")
    radio_d.config(text=f"d) {answer_d}", value="d")


def submit_answer(selected_answer:list):
    """
    The function checks the answer chosen by the user, and also
    adds 1 to the score of the player if the answer is correct
    The function also lets the user know if the answer is correct
    and what the new score is
    :param selected_answer from the radio button:
    :return: No value is returned
    """
    global player_score
    if current_player_id is None or current_question is None:
        messagebox.showerror("Error", "You need to login and answer a question first.")
        return

    question_id = current_question[0]
    correct_answer = current_question[6]
    is_correct:bool = selected_answer == correct_answer

    # Store the answer in the database
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
        messagebox.showinfo("Wrong!",
                            f"Wrong answer! The correct answer was '{correct_answer}'. Your score remains {player_score}.")
    cur.execute(
    "SELECT COUNT(*) FROM player_answers WHERE player_id = %s",
    (current_player_id,)
    )
    num_of_questions = cur.fetchone()[0]
    if num_of_questions:
        if num_of_questions >= 15:
            messagebox.showinfo("Game over", f"you answered 20 questions Your score is now {player_score}.")
            return
        else:
            show_question()
    else:
        show_question()

def open_register():
    """
    The function only shows the register form and gets the fields inside it
    using tkinter window
    :return: No returned value
    """
    register_window = tk.Toplevel(root)
    register_window.title("Register")

    tk.Label(register_window, text="Username:").pack()
    username_entry = tk.Entry(register_window)
    username_entry.pack()

    tk.Label(register_window, text="Password:").pack()
    password_entry = tk.Entry(register_window, show='*')
    password_entry.pack()

    tk.Label(register_window, text="Email:").pack()
    email_entry = tk.Entry(register_window)
    email_entry.pack()

    tk.Label(register_window, text="Age:").pack()
    age_entry = tk.Entry(register_window)
    age_entry.pack()

    def submit_register():
        username = username_entry.get()
        password = password_entry.get()
        email = email_entry.get()
        age = age_entry.get()

        if not username or not password or not email or not age:
            messagebox.showerror("Error", "All fields are required!")
            return

        register_player(username, password, email, float(age))
        register_window.destroy()

    tk.Button(register_window, text="Register", command=submit_register).pack()


# Function to open login form
def open_login():
    """
    The function shows the login window (form) and
    accepts the fields in it
    The function uses tkinter form
    :return: No value returned
    """
    login_window = tk.Toplevel(root)
    login_window.title("Login")

    tk.Label(login_window, text="Username:").pack()
    username_entry = tk.Entry(login_window)
    username_entry.pack()

    tk.Label(login_window, text="Password:").pack()
    password_entry = tk.Entry(login_window, show='*')
    password_entry.pack()

    def submit_login():
        username = username_entry.get()
        password = password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Both fields are required!")
            return

        login_player(username, password)
        login_window.destroy()

    tk.Button(login_window, text="Login", command=submit_login).pack()


# Create main window
root = tk.Tk()
root.title("Trivia Game")

# Create login and register buttons
tk.Button(root, text="Register", command=open_register).pack()
tk.Button(root, text="Login", command=open_login).pack()

# Trivia question UI
question_label = tk.Label(root, text="Please log in to start the game.")
question_label.pack()

selected_answer = tk.StringVar(value="a")

radio_a = tk.Radiobutton(root, text="", variable=selected_answer, value="a")
radio_a.pack()

radio_b = tk.Radiobutton(root, text="", variable=selected_answer, value="b")
radio_b.pack()

radio_c = tk.Radiobutton(root, text="", variable=selected_answer, value="c")
radio_c.pack()

radio_d = tk.Radiobutton(root, text="", variable=selected_answer, value="d")
radio_d.pack()

tk.Button(root, text="Submit Answer", command=lambda: submit_answer(selected_answer.get())).pack()

# Run the main loop
root.mainloop()

# Close PostgreSQL connection when the GUI exits
cur.close()
conn.close()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
   main()


