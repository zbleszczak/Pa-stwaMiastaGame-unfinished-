import tkinter as tk
import random
import string
import wikipedia

def setup_game():
    return {
        'Animals',
        'Fruits',
        'Countries',
        'Cities',
        'River'
    }


class WordGuessingGameGUI:
    def __init__(self, master):
        self.master = master
        self.selected_categories = []
        self.players = []
        self.wiki_cache = WikipediaCache()
        self.setup_ui()
        self.num_rounds = 1  # Default number of rounds
        self.current_round = 1  # Initialize current round
        self.total_rounds = 1  # Initialize total rounds to default
    def show_scores(self):
        # Create a new window for displaying scores
        self.score_window = tk.Toplevel(self.master)
        self.score_window.title("Game Scores")
        self.score_window.geometry("300x200")

        # Display player scores
        for player in self.players:
            score = self.points.get(player, 0)
            score_label = tk.Label(self.score_window, text=f"{player}: {score} points", font=("Arial", 14))
            score_label.pack()

        if self.current_round < self.total_rounds:
            next_round_button = tk.Button(self.score_window, text="Next Round", command=self.next_round)
            next_round_button.pack(pady=10)
        else:
            new_game_button = tk.Button(self.score_window, text="Start New Game", command=self.start_new_game)
            new_game_button.pack(pady=10)

    def next_round(self):
        self.current_round += 1
        self.reset_for_new_round()
        self.score_window.destroy()

    def start_new_game(self):
        self.reset_game()
        self.score_window.destroy()


    def reset_game(self):
        # Reset game state
        self.selected_categories = []
        self.players = []
        self.points = {player: 0 for player in self.players}  # Reset points
        # Close score window and reset input forms, etc.
        self.score_window.destroy()

    def reset_for_new_round(self):
        # Close the existing game window if it's open
        if hasattr(self, 'game_window') and self.game_window.winfo_exists():
            self.game_window.destroy()

        # Create a new game window
        self.game_window = tk.Toplevel(self.master)
        self.game_window.title("Game On!")
        self.game_window.geometry("600x600")

        # Recreate the info label in the new game window
        self.info_label = tk.Label(self.game_window, text=f"Player: {self.player_name}\nPoints: {self.points}", font=("Arial", 16))
        self.info_label.pack()

        # Generate a new random letter for the new round
        self.random_letter = random.choice(string.ascii_uppercase)
        self.letter_label = tk.Label(self.game_window, text=f"Letter: '{self.random_letter}'", font=("Arial", 16))
        self.letter_label.pack()

        # Reset the timer and other round-specific attributes
        self.time_left = 60
        self.timer_label = tk.Label(self.game_window, text=f"Time left: {self.time_left} seconds", font=("Arial", 16))
        self.timer_label.pack()
        self.update_timer()  # Start the timer for the new round

        # Create new entry fields for each category
        self.category_inputs = {}
        for category in self.selected_categories:
            label = tk.Label(self.game_window, text=f"{category}:", font=("Arial", 14))
            label.pack()
            entry = tk.Entry(self.game_window, font=("Arial", 14))
            entry.pack()
            self.category_inputs[category] = entry

        # Re-enable the submit button for the new round
        self.submit_guesses_button = tk.Button(self.game_window, text="Submit Guesses")
        self.submit_guesses_button.pack()

    def next_round(self):
        self.current_round += 1  # Move to the next round
        self.reset_for_new_round()
        self.score_window.destroy()  # Close the score window

    def set_rounds(self):
        try:
            self.num_rounds = int(self.rounds_entry.get())  # Set based on user input
            self.total_rounds = self.num_rounds  # Update total rounds
            print(f"Number of rounds set to: {self.num_rounds}")
        except ValueError:
            print("Invalid number of rounds. Please enter a valid number.")
    def setup_ui(self):
        # Form 1: Category selection
        self.form1 = tk.Frame(self.master)
        self.form1.pack(padx=10, pady=10, fill='both', expand=True)

        self.category_buttons = {}
        row, col = 0, 0
        for category in setup_game():
            btn = tk.Button(self.form1, text=category, bg='white', width=10, height=5, command=lambda cat=category: self.toggle_category(cat))
            btn.grid(row=row, column=col, padx=5, pady=5)
            self.category_buttons[category] = btn
            col += 1
            if col >= 3:  # Adjust number of columns as needed
                row += 1
                col = 0

        # Form 2: Gameplay and Player Management
        self.form2 = tk.Frame(self.master)
        self.form2.pack(padx=10, pady=10, fill='both', expand=True)

        # Add Rounds selection to form2
        self.rounds_label = tk.Label(self.form2, text="Number of Rounds:")
        self.rounds_label.pack()
        self.rounds_entry = tk.Entry(self.form2, width=5)
        self.rounds_entry.pack()
        self.rounds_entry.insert(0, "1")  # Default to 1 round

        # Button to set number of rounds
        self.set_rounds_button = tk.Button(self.form2, text="Set Rounds", command=self.set_rounds)
        self.set_rounds_button.pack(pady=5)

        self.chosen_categories_label = tk.Label(self.form2, text="Chosen Categories: ")
        self.chosen_categories_label.pack()

        self.play_game_button = tk.Button(self.form2, text="Play the Game", command=self.play_game)
        self.play_game_button.pack(pady=5)

        self.invite_players_button = tk.Button(self.form2, text="Invite Players", command=self.invite_players)
        self.invite_players_button.pack(pady=5)

        self.current_players_label = tk.Label(self.form2, text="Current Players: None")
        self.current_players_label.pack()
    def toggle_category(self, category):
        if category in self.selected_categories:
            self.selected_categories.remove(category)
            self.category_buttons[category].config(bg='white')
        elif len(self.selected_categories) < 5:
            self.selected_categories.append(category)
            self.category_buttons[category].config(bg='gray')
        self.update_chosen_categories_label()

    def update_chosen_categories_label(self):
        chosen_categories_text = "Chosen Categories: " + ", ".join(self.selected_categories)
        self.chosen_categories_label.config(text=chosen_categories_text)

    def play_game(self):
        # Open a new window for the game
        self.game_window = tk.Toplevel(self.master)
        self.game_window.title("Game On!")
        self.game_window.geometry("600x600")  # Adjust size as needed

        # Example player info and points
        self.player_name = "Nickname"  # Replace with actual player name logic
        self.points = 0  # Replace with actual points logic

        # Display Points and Player Nickname
        self.info_label = tk.Label(self.game_window, text=f"Player: {self.player_name}\nPoints: {self.points}", font=("Arial", 16))
        self.info_label.pack()

        # Choose a random letter
        self.random_letter = random.choice(string.ascii_uppercase)

        # Display the chosen letter
        self.letter_label = tk.Label(self.game_window, text=f"Letter: '{self.random_letter}'", font=("Arial", 16))
        self.letter_label.pack()

        self.time_left = 60
        self.timer_label = tk.Label(self.game_window, text=f"Time left: {self.time_left} seconds", font=("Arial", 16))
        self.timer_label.pack()
        self.update_timer()

        # Create input fields for each chosen category
        self.category_inputs = {}
        for category in self.selected_categories:
            label = tk.Label(self.game_window, text=f"{category}:", font=("Arial", 14))
            label.pack()

            entry = tk.Entry(self.game_window, font=("Arial", 14))
            entry.pack()
            self.category_inputs[category] = entry

        # Submit button for the guesses
        self.submit_guesses_button = tk.Button(self.game_window, text="Submit Guesses")
        self.submit_guesses_button.pack()

    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"Time left: {self.time_left} seconds")
            self.game_window.after(100, self.update_timer)
        else:
            # Timer has run out
            self.submit_guesses()  # Automatically submit guesses
            self.game_window.destroy()  # Close the game window
            self.show_scores()  # Show the scores

    def calculate_points(self, player_guesses):
        round_points = 0  # Initialize points for this round

        for category, guess in player_guesses.items():
            # Check if guess is valid using WikipediaCache
            if not guess or not guess.startswith(self.random_letter) or not self.wiki_cache.check_word(guess):
                print(f"Invalid guess '{guess}' for {category}.")
                continue  # Skip adding points for invalid guesses

            # Scoring logic
            if list(player_guesses.values()).count(guess) > 1:
                round_points += 5  # Add points for duplicate word
            else:
                round_points += 10  # Add points for unique word

        # Add the points earned this round to the player's total points
        self.points += round_points
        print(f"Points this round: {round_points}, Total Points: {self.points}")

        # Update the info label only if the game window and label exist
        if hasattr(self, 'game_window') and self.game_window.winfo_exists() and hasattr(self, 'info_label'):
            self.info_label.config(text=f"Player: {self.player_name}\nPoints: {self.points}")

    def submit_guesses(self):
        # Collect guesses from input forms
        player_guesses = {category: self.category_inputs[category].get().strip().upper() for category in
                          self.selected_categories}

        # Pass these guesses to calculate_points for validation and scoring
        self.calculate_points(player_guesses)

        # Disable the submit button to prevent multiple submissions
        self.submit_guesses_button.config(state='disabled')

    def invite_players(self):
        # For demonstration, let's simulate adding a player
        new_player = f"Player {len(self.players) + 1}"
        self.players.append(new_player)
        self.update_current_players_label()
        print("Inviting players...")

    def update_current_players_label(self):
        players_text = "Current Players: " + ", ".join(self.players) if self.players else "Current Players: None"
        self.current_players_label.config(text=players_text)

class WikipediaCache:
    def __init__(self):
        self.cache = {}
    wikipedia.set_lang("pl")
    def check_word(self, word):
        word_lower = word.lower()
        if word_lower in self.cache:
            return self.cache[word_lower]

        try:
            wikipedia.summary(word, sentences=1)
            self.cache[word_lower] = True
            return True
        except (wikipedia.exceptions.DisambiguationError, wikipedia.exceptions.PageError):
            self.cache[word_lower] = False
            return False

# Main Window
root = tk.Tk()
root.title("Word Guessing Game")
root.geometry("800x600")  # Set the size of the window

app = WordGuessingGameGUI(root)

root.mainloop()