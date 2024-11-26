import random
from pymongo import MongoClient

# MongoDB connection
client = MongoClient(host="localhost", port=27022, username="root", password="rootpassword")
trivia_game = client["trivia_game"]
collection = trivia_game['questions_collection']

questions = [
    {
        "question_text": "Which vitamin is produced when a person is exposed to sunlight?",
        "answers": {"a": "Vitamin A", "b": "Vitamin B", "c": "Vitamin C", "d": "Vitamin D"},
        "correct_answer": "d"
    },
    {
        "question_text": "What is the largest internal organ in the human body?",
        "answers": {"a": "Liver", "b": "Heart", "c": "Lung", "d": "Kidney"},
        "correct_answer": "a"
    },
    {
        "question_text": "Who was the first woman to win a Nobel Prize?",
        "answers": {"a": "Marie Curie", "b": "Rosalind Franklin", "c": "Ada Lovelace", "d": "Jane Goodall"},
        "correct_answer": "a"
    },
    {
        "question_text": "In which year did World War I begin?",
        "answers": {"a": "1912", "b": "1914", "c": "1916", "d": "1918"},
        "correct_answer": "b"
    },
    {
        "question_text": "What is the hottest continent on Earth?",
        "answers": {"a": "Africa", "b": "Australia", "c": "South America", "d": "Asia"},
        "correct_answer": "a"
    },
    {
        "question_text": "Who invented the World Wide Web?",
        "answers": {"a": "Bill Gates", "b": "Steve Jobs", "c": "Tim Berners-Lee", "d": "Elon Musk"},
        "correct_answer": "c"
    },
    {
        "question_text": "Which country hosted the first modern Olympics?",
        "answers": {"a": "France", "b": "USA", "c": "Greece", "d": "Italy"},
        "correct_answer": "c"
    },
    {
        "question_text": "What is the currency of Mexico?",
        "answers": {"a": "Peso", "b": "Dollar", "c": "Real", "d": "Euro"},
        "correct_answer": "a"
    },
    {
        "question_text": "What is the longest river in Asia?",
        "answers": {"a": "Yangtze", "b": "Yellow", "c": "Ganges", "d": "Mekong"},
        "correct_answer": "a"
    },
    {
        "question_text": "Which planet is the smallest in our solar system?",
        "answers": {"a": "Venus", "b": "Earth", "c": "Mars", "d": "Mercury"},
        "correct_answer": "d"
    },
    {
        "question_text": "In which country would you find the Leaning Tower of Pisa?",
        "answers": {"a": "France", "b": "Italy", "c": "Spain", "d": "Portugal"},
        "correct_answer": "b"
    },
    {
        "question_text": "What is the tallest animal in the world?",
        "answers": {"a": "Elephant", "b": "Giraffe", "c": "Whale", "d": "Ostrich"},
        "correct_answer": "b"
    },
    {
        "question_text": "Who is the author of 'The Hobbit'?",
        "answers": {"a": "C.S. Lewis", "b": "George Orwell", "c": "J.R.R. Tolkien", "d": "J.K. Rowling"},
        "correct_answer": "c"
    },
    {
        "question_text": "Which ocean is the Bermuda Triangle located in?",
        "answers": {"a": "Indian", "b": "Atlantic", "c": "Pacific", "d": "Arctic"},
        "correct_answer": "b"
    },
    {
        "question_text": "What is the most popular social media platform in the world?",
        "answers": {"a": "Facebook", "b": "Twitter", "c": "Instagram", "d": "TikTok"},
        "correct_answer": "a"
    },
    {
        "question_text": "Who discovered gravity?",
        "answers": {"a": "Albert Einstein", "b": "Galileo Galilei", "c": "Isaac Newton", "d": "Nikola Tesla"},
        "correct_answer": "c"
    },
    {
        "question_text": "Which fruit is the most consumed in the world?",
        "answers": {"a": "Apple", "b": "Banana", "c": "Orange", "d": "Grapes"},
        "correct_answer": "b"
    },
    {
        "question_text": "Who was the first person to reach the South Pole?",
        "answers": {"a": "Ernest Shackleton", "b": "Roald Amundsen", "c": "Robert Falcon Scott", "d": "Edmund Hillary"},
        "correct_answer": "b"
    },
    {
        "question_text": "In what year did the Titanic sink?",
        "answers": {"a": "1910", "b": "1912", "c": "1914", "d": "1916"},
        "correct_answer": "b"
    },
    {
        "question_text": "Which organ is responsible for pumping blood throughout the body?",
        "answers": {"a": "Brain", "b": "Liver", "c": "Heart", "d": "Lungs"},
        "correct_answer": "c"
    },
    {
        "question_text": "What is the capital city of Canada?",
        "answers": {"a": "Toronto", "b": "Ottawa", "c": "Vancouver", "d": "Montreal"},
        "correct_answer": "b"
    },
    {
        "question_text": "What is the hardest rock on Earth?",
        "answers": {"a": "Granite", "b": "Limestone", "c": "Diamond", "d": "Marble"},
        "correct_answer": "c"
    },
    {
        "question_text": "Who painted 'Starry Night'?",
        "answers": {"a": "Claude Monet", "b": "Vincent van Gogh", "c": "Pablo Picasso", "d": "Leonardo da Vinci"},
        "correct_answer": "b"
    },
    {
        "question_text": "In which city would you find Times Square?",
        "answers": {"a": "Chicago", "b": "New York", "c": "Los Angeles", "d": "Miami"},
        "correct_answer": "b"
    },
    {
        "question_text": "What is the main ingredient in traditional Japanese miso soup?",
        "answers": {"a": "Tofu", "b": "Seaweed", "c": "Soybean paste", "d": "Rice"},
        "correct_answer": "c"
    },
    {
        "question_text": "Which two elements make up water?",
        "answers": {"a": "Hydrogen and Oxygen", "b": "Carbon and Oxygen", "c": "Nitrogen and Oxygen", "d": "Carbon and Hydrogen"},
        "correct_answer": "a"
    },
    {
        "question_text": "What does the 'www' stand for in a website browser?",
        "answers": {"a": "World Web Wide", "b": "World Wide Web", "c": "Web Wide World", "d": "Wide Web World"},
        "correct_answer": "b"
    },
    {
        "question_text": "Which type of blood cell carries oxygen?",
        "answers": {"a": "Red", "b": "White", "c": "Platelets", "d": "Plasma"},
        "correct_answer": "a"
    },
    {
        "question_text": "What language has the second highest number of native speakers in the world?",
        "answers": {"a": "Spanish", "b": "Mandarin", "c": "Hindi", "d": "English"},
        "correct_answer": "a"
    },
    {
        "question_text": "What color are aircraft black boxes?",
        "answers": {"a": "Black", "b": "Orange", "c": "Red", "d": "Blue"},
        "correct_answer": "b"
    }
]
# Insert each question individually into the MongoDB collection
for question in questions:
   collection.insert_one(question)

print("Inserted questions into MongoDB one by one.")