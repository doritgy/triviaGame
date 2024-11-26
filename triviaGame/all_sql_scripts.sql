CREATE TABLE questions (
    question_id SERIAL PRIMARY KEY,
    question_text TEXT NOT NULL,
    answer_a TEXT NOT NULL,
    answer_b TEXT NOT NULL,
    answer_c TEXT NOT NULL,
    answer_d TEXT NOT NULL,
    correct_answer CHAR(1) CHECK (correct_answer IN ('a', 'b', 'c', 'd')) NOT NULL

 CREATE TABLE players (
    player_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password text NOT NULL, -- should store hashed passwords in a real scenario
    email VARCHAR(100) UNIQUE NOT NULL,
    age float NOT NULL,
    last_login timestamp default current timestamp
    score int default 0
);

CREATE TABLE player_answers (
    player_id INTEGER REFERENCES players(player_id) ON DELETE CASCADE,
    question_id INTEGER REFERENCES questions(question_id) ON DELETE CASCADE,
    PRIMARY KEY (player_id, question_id)
    selected_answer CHAR(1) CHECK (selected_answer IN ('a', 'b', 'c', 'd')) NOT NULL,
    is_correct BOOLEAN NOT NULL,
);

CREATE TABLE high_scores (
    score_id INTEGER PRIMARY KEY CHECK (score_id >= 1 AND score_id <= 20), -- representing scores from 1 to 20
    player_id INTEGER REFERENCES players(player_id) ON DELETE CASCADE,
    achieved_in float default 0
);

INSERT INTO questions (question_text, answer_a, answer_b, answer_c, answer_d, correct_answer)
VALUES
  ('What is the capital of France?', 'Berlin', 'London', 'Paris', 'Rome', 'c'),
  ('Which planet is known as the Red Planet?', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'b'),
  ('Who wrote "Romeo and Juliet"?', 'Mark Twain', 'Jane Austen', 'William Shakespeare', 'Charles Dickens', 'c'),
  ('What is the largest ocean on Earth?', 'Indian Ocean', 'Atlantic Ocean', 'Pacific Ocean', 'Southern Ocean', 'c'),
  ('What is the chemical symbol for water?', 'H2O', 'CO2', 'NaCl', 'O2', 'a'),
  ('What is the capital of Germany?', 'Berlin', 'Paris', 'Rome', 'London', 'a'),
  ('Which element is represented by the symbol O?', 'Osmium', 'Oxygen', 'Oganesson', 'Ozone', 'b'),
  ('Who painted the Mona Lisa?', 'Vincent Van Gogh', 'Pablo Picasso', 'Leonardo da Vinci', 'Claude Monet', 'c'),
  ('What is the largest mammal in the world?', 'Elephant', 'Blue Whale', 'Giraffe', 'Hippo', 'b'),
  ('What is the hardest natural substance on Earth?', 'Diamond', 'Iron', 'Quartz', 'Gold', 'a'),
  ('Which planet is closest to the sun?', 'Venus', 'Mars', 'Mercury', 'Jupiter', 'c'),
  ('What is the capital of Japan?', 'Kyoto', 'Tokyo', 'Osaka', 'Hiroshima', 'b'),
  ('Who discovered penicillin?', 'Marie Curie', 'Alexander Fleming', 'Louis Pasteur', 'Isaac Newton', 'b'),
  ('What is the square root of 64?', '6', '7', '8', '9', 'c'),
  ('Who was the first man to step on the moon?', 'Buzz Aldrin', 'Yuri Gagarin', 'Neil Armstrong', 'John Glenn', 'c'),
  ('Which is the largest continent?', 'Africa', 'Asia', 'Europe', 'South America', 'b'),
  ('What is the largest desert in the world?', 'Sahara', 'Gobi', 'Antarctic Desert', 'Arabian Desert', 'c'),
  ('What language has the most native speakers?', 'Spanish', 'English', 'Mandarin', 'Hindi', 'c'),
  ('Which country invented tea?', 'India', 'Japan', 'China', 'England', 'c'),
  ('How many colors are in a rainbow?', '5', '6', '7', '8', 'c'),
  ('What is the national flower of Japan?', 'Cherry Blossom', 'Rose', 'Lotus', 'Lily', 'a'),
  ('Who invented the telephone?', 'Alexander Graham Bell', 'Thomas Edison', 'Nikola Tesla', 'Guglielmo Marconi', 'a'),
  ('What is the largest bone in the human body?', 'Femur', 'Tibia', 'Skull', 'Humerus', 'a'),
  ('Who directed the movie "Titanic"?', 'Steven Spielberg', 'James Cameron', 'Christopher Nolan', 'Martin Scorsese', 'b'),
  ('How many planets are in our solar system?', '7', '8', '9', '10', 'b'),
  ('Which ocean is the largest?', 'Indian', 'Pacific', 'Atlantic', 'Arctic', 'b'),
  ('What is the most spoken language in Brazil?', 'Portuguese', 'Spanish', 'French', 'English', 'a'),
  ('Who invented the light bulb?', 'Nikola Tesla', 'Alexander Graham Bell', 'Thomas Edison', 'Benjamin Franklin', 'c'),
  ('What is the chemical symbol for gold?', 'Au', 'Ag', 'Pb', 'Fe', 'a'),
  ('What country has the most islands?', 'Australia', 'Indonesia', 'Philippines', 'Sweden', 'd'),
  ('What is the tallest mountain in the world?', 'K2', 'Mount Kilimanjaro', 'Mount Everest', 'Mount Fuji', 'c'),
  ('Which animal is known as the "King of the Jungle"?', 'Elephant', 'Tiger', 'Lion', 'Gorilla', 'c'),
  ('What is the most abundant gas in Earth’s atmosphere?', 'Oxygen', 'Carbon Dioxide', 'Nitrogen', 'Helium', 'c'),
  ('How many teeth does an adult human have?', '28', '30', '32', '34', 'c'),
  ('Who wrote "The Odyssey"?', 'Homer', 'Shakespeare', 'Plato', 'Socrates', 'a'),
  ('What year did the Titanic sink?', '1911', '1912', '1913', '1914', 'b'),
  ('Which country is home to the kangaroo?', 'South Africa', 'Australia', 'New Zealand', 'Canada', 'b'),
  ('How many bones are in the human body?', '204', '206', '208', '210', 'b'),
  ('What is the hottest planet in our solar system?', 'Mercury', 'Venus', 'Mars', 'Earth', 'b'),
  ('What is the currency of Japan?', 'Dollar', 'Euro', 'Yen', 'Won', 'c'),
  ('Who is the author of "Harry Potter"?', 'J.R.R. Tolkien', 'George R.R. Martin', 'J.K. Rowling', 'Suzanne Collins', 'c'),
  ('What is the fastest land animal?', 'Cheetah', 'Lion', 'Horse', 'Leopard', 'a'),
  ('What is the most popular sport in the world?', 'Basketball', 'Cricket', 'Soccer', 'Tennis', 'c'),
  ('What year did World War II end?', '1944', '1945', '1946', '1947', 'b'),
  ('What country has the most natural lakes?', 'USA', 'Russia', 'Canada', 'Brazil', 'c'),
  ('Who developed the theory of relativity?', 'Newton', 'Einstein', 'Bohr', 'Tesla', 'b'),
  ('What is the name of the longest river in the world?', 'Amazon', 'Nile', 'Yangtze', 'Mississippi', 'b'),
  ('How many continents are there?', '5', '6', '7', '8', 'c'),
  ('Which famous scientist introduced the idea of natural selection?', 'Darwin', 'Einstein', 'Newton', 'Galileo', 'a'),
  ('What is the speed of light?', '300,000 km/s', '150,000 km/s', '250,000 km/s', '400,000 km/s', 'a'),
  ('Which planet has the most moons?', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'c'),
  ('What element does "H" represent on the periodic table?', 'Helium', 'Hydrogen', 'Hafnium', 'Holmium', 'b'),
  ('What is the national language of Canada?', 'English', 'French', 'Both', 'Neither', 'c'),
  ('What is the most abundant element in the universe?', 'Oxygen', 'Carbon', 'Hydrogen', 'Helium', 'c'),
  ('Who was the first President of the United States?', 'Abraham Lincoln', 'George Washington', 'Thomas Jefferson', 'John Adams', 'b');

CREATE TABLE high_scores (
    score_id SERIAL PRIMARY KEY,
    player_id INT REFERENCES players(player_id) ON DELETE CASCADE,
    score INT NOT NULL,
    achieved_in INTERVAL NOT NULL
);

CREATE OR REPLACE FUNCTION find_score(_current_player_id INTEGER)
RETURNS INTEGER
LANGUAGE plpgsql AS
$$
DECLARE
    player_score INTEGER;  -- Variable to hold the score
BEGIN
    -- Store the score in the variable
    SELECT p.score INTO player_score
    FROM players p
    WHERE p.player_id = _current_player_id;

    -- Return the stored score
    RETURN player_score;
END;
$$;


