import tkinter as tk
import random
from tkinter import messagebox
import psycopg2
from datetime import datetime
from pymongo import MongoClient
import game_initialize
import statistics
import questions
import psycopg2.extras
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="admin",
    host="localhost",
    port="5560"
)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

client = MongoClient(host="localhost", port=27022, username="root", password="rootpassword")
trivia_game = client["trivia_game"]
collection = trivia_game['questions_collection']


# Global variables
current_player_id = None
current_question = None
player_score = 0
login_success = False

def main():
    global root, current_player_id, player_score, login_success
    root = tk.Tk()  # Create the root window once
    root.title("Trivia Game")
    login_success = [False]
    current_player_id = [None]  # Mutable object to store the player ID

    tk.Button(root, text="Register", command=lambda: open_register_login('register')).pack()
    tk.Button(root, text="Login", command=lambda: open_register_login('login')).pack()
    tk.Button(root, text="Statistics", command=open_statistics_menu).pack()  # Opens the statistics window
    tk.Button(root, text="Exit Game", command=exit_game).pack()

    root.mainloop()


def open_register_login(action:str):
    """
    This function opens either the login or register window.
    It waits for the result and processes it in `main.py`.
    """
    global current_player_id, login_success, player_score
    if action == 'register':
        game_initialize.open_register(root, login_success, current_player_id)
    elif action == 'login':
        game_initialize.open_login(root, login_success, current_player_id)

    # Wait for the login/register window to complete and check result
    if login_success and current_player_id is not None:
        cur.execute("SELECT COUNT(*) FROM player_answers WHERE player_id = %s", (current_player_id[0],))
        num_of_questions = cur.fetchone()[0]

        # If the number of questions is a multiple of 20, start a new game
        if num_of_questions % 20 == 0:
            player_score = [0]
            messagebox.showinfo("New Game", f"Hi Player, You just started a new game with a score of 0.")
            cur.execute("UPDATE players SET score = %s WHERE player_id = %s", (0, current_player_id[0]))
            conn.commit()
            transfer_random_questions()
        else:
            # If number of questions is not a multiple of 20, prompt to start a new game or continue
            start_new_game = messagebox.askyesno("Game in Progress",
                                                 "Do you want to start a new game? Your current progress will be reset.")

            if start_new_game:
                player_score = [0]
                cur.execute("UPDATE players SET score = %s WHERE player_id = %s", (0, current_player_id[0]))

                # Calculate how many answers to delete to make questions answered % 20 == 0
                excess_answers = num_of_questions % 20
                cur.execute("""
                        WITH deletable AS (
                            SELECT question_id
                            FROM player_answers
                            WHERE player_id = %s
                            ORDER BY question_id DESC
                            LIMIT %s
                        )
                        DELETE FROM player_answers
                        WHERE question_id IN (SELECT question_id FROM deletable);
                    """, (current_player_id[0], excess_answers))

                conn.commit()
                transfer_random_questions()
                messagebox.showinfo("New Game", "Your game has been reset. Starting with a score of 0.")

            else:
                # Continue with the existing game and score
                cur.execute("SELECT find_score(%s);", (current_player_id[0],))
                player_score = [cur.fetchone()[0]]

        # Show the next question
        questions.show_question(cur, conn, current_player_id, player_score)
    else:
        messagebox.showerror("Error", "Failed to login or register.")


def transfer_random_questions():
    """
    This program transfers questions from nomgo to postgresql, questions table
    """
    total_questions = collection.count_documents({})
    if total_questions > 100:
        # Select 100 random questions from MongoDB
        random_indexes = random.sample(range(total_questions), 100)
        questions = collection.find().skip(random_indexes[0]).limit(100)
    else:
        questions = collection.find()
    # Insert each question into the PostgreSQL `questions` table
    for question in questions:
        question_text = question['question_text']
        answer_a = question['answers']['a']
        answer_b = question['answers']['b']
        answer_c = question['answers']['c']
        answer_d = question['answers']['d']
        correct_answer = question['correct_answer']

        cur.execute("""
                INSERT INTO questions (question_text, answer_a, answer_b, answer_c, answer_d, correct_answer)
                VALUES (%s, %s, %s, %s, %s, %s);
            """, (question_text, answer_a, answer_b, answer_c, answer_d, correct_answer))

    # Commit the transaction to save changes to PostgreSQL
    conn.commit()
    print("Transferred 100 random questions from MongoDB to PostgreSQL.")
    return


def open_statistics_menu():
    """
    This program calls the games statistics, with 5 sorts of statistics
    """
    statistics.open_statistics_window(conn, cur)

def exit_game():
    print("Exit game button clicked!")
    root.quit()
    cur.close()
    conn.close()

def fetch_questions():
    """
    This program fetches questions from the opentdb.com, with API, where many questions are found
    and copies the questions to the Mongo DB
    The  API  URL used in the  code, https: // opentdb.com / api.php,
    refers  to the Open Trivia Database(OpenTDB), which is a public, free
    trivia question database API .
    """
    import json
    import requests
    from pymongo import MongoClient

    # MongoDB connection
    client = MongoClient(host="localhost", port=27022, username="root", password="rootpassword")

    # Fetch questions from Open Trivia Database API
    url = "https://opentdb.com/api.php?amount=250&type=multiple"

    response = requests.get(url)
    questions = response.json()["results"]
    db = client['trivia_game']
    questions_collection = db['questions_new']

    # Prepare data in JSON format for MongoDB
    questions_data = []
    for q in questions:
        question_doc = {
            "question_text": q['question'],
            "answers": {
                "a": q['incorrect_answers'][0],
                "b": q['incorrect_answers'][1],
                "c": q['incorrect_answers'][2],
                "d": q['correct_answer']  # assuming the correct answer is always last
            },
            "correct_answer": "d"  # label the correct option as "d"
        }
        questions_data.append(question_doc)

    # Save to a JSON file
    with open('trivia_questions.json', 'w') as jsonfile:
        json.dump(questions_data, jsonfile, indent=4)

    # Insert data into MongoDB
    questions_collection.insert_many(questions_data)

    print("Questions successfully added to MongoDB and saved to trivia_questions.json")

    # Fetch all questions from the "questions_new" collection
    questions = list(questions_collection.find())

    # Iterate through each question to randomize answers and update the correct answer
    for question in questions:
        answers = question['answers']
        correct_answer_key = "d"  # Initially, the correct answer is always "d"

        # Create a list of answer items and shuffle it, so that not always the answer is "d"
        answer_items = list(answers.items())
        random.shuffle(answer_items)

        # Reassign the shuffled answers to the answers dictionary with new keys a, b, c, d
        new_answers = {}
        new_correct_answer_key = None

        for idx, (key, value) in enumerate(answer_items):
            new_key = chr(ord('a') + idx)  # Generate keys "a", "b", "c", "d"
            new_answers[new_key] = value
            if key == correct_answer_key:  # Check if this is the correct answer
                new_correct_answer_key = new_key

        # Update the question in MongoDB
        questions_collection.update_one(
            {"_id": question["_id"]},
            {
                "$set": {
                    "answers": new_answers,
                    "correct_answer": new_correct_answer_key
                }
            }
        )

    print("Updated all questions with randomized answers and correct answer positions.")
    source_collection = db["questions_new"]
    destination_collection = db["questions_collection"]

    # Fetch all documents from the source collection
    questions = list(source_collection.find())

    # Insert each document into the destination collection
    if questions:
        destination_collection.insert_many(questions)
        print(f"Successfully transferred {len(questions)} questions from 'questions_new' to 'questions_collection'.")
    else:
        print("No documents found in 'questions_new' to transfer.")

    source_collection.delete_many({})

    print("Transfer complete.")

if __name__ == "__main__":
    main()

    ###################################
    #In order to fetch quesions to mongoDB from the web site in have to run here
    # in the "if __name__" fetch_questions function
    ######################################
