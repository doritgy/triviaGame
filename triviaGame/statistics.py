import tkinter as tk
from tkinter import messagebox, scrolledtext

# Function to open the statistics window
def open_statistics_window(conn, cur):
    # Create a new window for statistics
    stat_window = tk.Toplevel()
    stat_window.title("Statistics Menu")

    # Display result area
    result_text = scrolledtext.ScrolledText(stat_window, width=80, height=20)
    result_text.pack()

    def show_result(title, text):
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"{title}\n{'=' * len(title)}\n{text}")

    def total_users():
        cur.execute("SELECT COUNT(DISTINCT player_id) FROM player_answers;")
        total = cur.fetchone()[0]
        show_result("Total Users Who Played", f"Total users who played: {total}")

    def question_most_least_correct():
        cur.execute("""
            SELECT MAX(correct_count) FROM (
                SELECT question_id, COUNT(player_id) AS correct_count
                FROM player_answers
                WHERE is_correct = TRUE
                GROUP BY question_id
            ) AS correct_counts;
        """)
        max_correct_count = cur.fetchone()[0]

        cur.execute("""
            SELECT MIN(correct_count) FROM (
                SELECT question_id, COUNT(player_id) AS correct_count
                FROM player_answers
                WHERE is_correct = TRUE
                GROUP BY question_id
            ) AS correct_counts;
        """)
        min_correct_count = cur.fetchone()[0]

        cur.execute("""
            SELECT questions.question_text, questions.correct_answer, COUNT(player_answers.player_id) AS correct_count
            FROM player_answers
            JOIN questions ON player_answers.question_id = questions.question_id
            WHERE player_answers.is_correct = TRUE
            GROUP BY questions.question_id, questions.question_text, questions.correct_answer
            HAVING COUNT(player_answers.player_id) = %s;
        """, (max_correct_count,))
        most_correct = cur.fetchall()

        cur.execute("""
            SELECT questions.question_text, questions.correct_answer, COUNT(player_answers.player_id) AS correct_count
            FROM player_answers
            JOIN questions ON player_answers.question_id = questions.question_id
            WHERE player_answers.is_correct = TRUE
            GROUP BY questions.question_id, questions.question_text, questions.correct_answer
            HAVING COUNT(player_answers.player_id) = %s;
        """, (min_correct_count,))
        least_correct = cur.fetchall()

        result = ""
        if most_correct:
            result += "Questions Answered Correctly by the Most Players:\n"
            for question_text, correct_answer, correct_count in most_correct:
                result += f"Question: {question_text}\nCorrect Answer: {correct_answer}\nCorrect Count: {correct_count}\n\n"

        if least_correct:
            result += "Questions Answered Correctly by the Fewest Players:\n"
            for question_text, correct_answer, correct_count in least_correct:
                result += f"Question: {question_text}\nCorrect Answer: {correct_answer}\nCorrect Count: {correct_count}\n\n"

        show_result("Most and Least Correctly Answered Questions", result)

    def players_by_correct_answers():
        cur.execute("""
            SELECT players.player_id, players.username, COUNT(player_answers.is_correct) AS correct_count
            FROM players
            JOIN player_answers ON players.player_id = player_answers.player_id
            WHERE player_answers.is_correct = TRUE
            GROUP BY players.player_id, players.username
            ORDER BY correct_count DESC;
        """)
        players = cur.fetchall()
        result = "Players in Descending Order of Correct Answers:\n"
        for player in players:
            result += f"Player ID: {player[0]}, Username: {player[1]}, Correct Answers: {player[2]}\n"
        show_result("Players by Correct Answers", result)

    def question_statistics():
        cur.execute("""
            SELECT questions.question_text,
                COUNT(player_answers.player_id) AS total_answers,
                SUM(CASE WHEN player_answers.is_correct = TRUE THEN 1 ELSE 0 END) AS correct_answers,
                SUM(CASE WHEN player_answers.is_correct = FALSE THEN 1 ELSE 0 END) AS incorrect_answers
            FROM questions
            LEFT JOIN player_answers ON questions.question_id = player_answers.question_id
            GROUP BY questions.question_text;
        """)
        stats = cur.fetchall()
        result = "Question Statistics:\n"
        for question_text, total_answers, correct_answers, incorrect_answers in stats:
            result += f"Question: {question_text}\nTotal Answers: {total_answers}, Correct: {correct_answers}, Incorrect: {incorrect_answers}\n\n"
        show_result("Statistics for Each Question", result)

    # Buttons for each statistic
    tk.Button(stat_window, text="Total Users", command=total_users).pack(fill=tk.X)
    tk.Button(stat_window, text="Most/Least Correctly Answered Questions", command=question_most_least_correct).pack(fill=tk.X)
    tk.Button(stat_window, text="Players by Correct Answers", command=players_by_correct_answers).pack(fill=tk.X)
    tk.Button(stat_window, text="Question Statistics", command=question_statistics).pack(fill=tk.X)
    tk.Button(stat_window, text="Close Statistics", command=stat_window.destroy).pack(fill=tk.X)  # Closes the statistics window

    # Start the Toplevel event loop (new window)
    stat_window.mainloop()
