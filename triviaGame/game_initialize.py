import tkinter as tk
from tkinter import messagebox
import psycopg2
import bcrypt

#from main import player_score

conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="admin",
    host="localhost",
    port="5560"
)
cur = conn.cursor()

#def initialize() -> any:
    # """
    # Initialize the game by showing the login/register window and returning the result to the main program.
    # This function should return the current_player_id after successful login/registration.
    # """
    # login_success = [False]
    # current_player_id = [None]  # Mutable object to store the player ID
    #
    # login_window = tk.Toplevel()
    # login_window.title("Trivia Game - Login/Register")
    #
    # tk.Button(login_window, text="Register",
    #           command=lambda: open_register(login_window, login_success, current_player_id)).pack()
    # tk.Button(login_window, text="Login",
    #           command=lambda: open_login(login_window, login_success, current_player_id)).pack()
    # tk.Button(login_window, text="Exit Game",
    #           command=lambda: exit_game(login_window, login_success, current_player_id)).pack()
    #
    # login_window.wait_window()
    #
    # if login_success[0]:
    #     return current_player_id[0]  # Return the player's ID
    # return [None]

def exit_game(window, login_success: bool, current_player_id: any) -> int:
    print("Exit game button clicked!")
    if window is not None:  # Close the login window if open
        window.destroy()

    login_success[0] = True
    current_player_id[0] = 999999  # Modify the value inside the list (mutable)
    return current_player_id[0]  #


def open_register(window, login_success, current_player_id):
    """
    The function shows the register form and gets the fields inside it using tkinter window.
    """
    # login_success = [False]
    # current_player_id = [None]  # M
    register_window = tk.Toplevel()
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
        else:
            player_id = register_player(username, password, email, float(age))
            if player_id:
                login_success[0] = True  # Set success to True
                current_player_id[0] = player_id  # Set the player ID
                register_window.destroy()
                # window.quit()  # Quit mainloop to return the result
                # return(login_success, current_player_id)

    tk.Button(register_window, text="Register", command=submit_register).pack()
    register_window.wait_window()


def open_login(window, login_success, current_player_id):
    """
    The function shows the login window (form) and accepts the fields in it using tkinter form.
    """
    login_window = tk.Toplevel(window)
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
        else:
            player_id = login_player(username, password)
            if player_id:
                login_success[0] = True  # Set success to True
                current_player_id[0] = player_id  # Set the player ID
                login_window.destroy()
                #window.quit()  # Quit mainloop to return the result

    tk.Button(login_window, text="Login", command=submit_login).pack()
    login_window.wait_window()

def register_player(username: str, password: str, email: str, age: float) -> int:
    """
    The function registers a new user, hashes the password, and saves it.
    Returns the new player's ID if successful.
    """
    hashed_password = hash_password(password)
    try:
        cur.execute(
            """
            INSERT INTO players (username, password, email, age, last_login, score)
            VALUES (%s, %s, %s, %s, NOW(), 0) RETURNING player_id
            """,
            (username, hashed_password.decode(), email, age)
        )
        player_id = cur.fetchone()[0]
        conn.commit()
        messagebox.showinfo("Success", f"Player {username} registered successfully!")
        return player_id  # Return the new player's ID
    except psycopg2.Error as e:
        conn.rollback()
        messagebox.showerror("Error", f"Could not register: {e}")
        return None

def login_player(username: str, password: str) -> int:
    """
    The function logs in a user, checks the hashed password, and verifies the credentials.
    Returns the player's ID if successful.
    """
    #global current_player_id, player_score
    cur.execute("SELECT player_id, password  FROM players WHERE username = %s", (username,))
    result = cur.fetchone()

    if result:
        player_id, stored_password = result
        if bcrypt.checkpw(password.encode(), stored_password.encode()):
            # Update the last_login field to NOW on successful login
            cur.execute("UPDATE players SET last_login = NOW() WHERE player_id = %s", (player_id,))
            conn.commit()

            messagebox.showinfo("Login", f"Welcome, {username}!")
            return player_id

        else:
            messagebox.showerror("Login Failed", "Incorrect password.")
            return None
    else:
        messagebox.showerror("Login Failed", "Username not found.")
        return None


def hash_password(password: str) -> bytes:
    """
    Hash the password using bcrypt.
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def check_password(hashed_password: str, user_password: str) -> bool:
    """
    Verify if the hashed password matches the user password.
    """
    return bcrypt.checkpw(user_password.encode(), hashed_password.encode())





