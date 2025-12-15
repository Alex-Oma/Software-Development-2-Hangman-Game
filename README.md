# Software-Development-2-Hangman-Game
This repo is for the mobile Hangman game which is capable of running on mobile phones and tablets

# Project Hangman:

Project Hangman is a mobile application that brings the classic word-guessing game, Hangman, to your fingertips. Designed for both phones and tablets, this app offers an engaging and interactive experience for users of all ages.

# Activity 1 – Requirements and Creative Session

I've decided to re-arrange the tasks stated in the assignment brief for the Activity 1 in a more logical order to make it easier to work on them.

## Task 1 – Review all available projects before deciding which to develop

Project: Hangman
Description: Multiple players can engage in a simple, GUI-based game of Hangman.

Project: Hide and Seek 
Description: Multiple players can hide items (or their avatar) in a scene while another player will try to find them (seek).

Project: Chat App
Description: Multiple users can send simple, text messages to each other.

I've reviewed all 3 available projects to chose from and having carried out some research, I've decided to go with the Hangman game project.
I felt that the Hangman game would be a good fit for my project as it combines word guessing with a simple yet engaging gameplay mechanic.

## Task 2 – Primary Target Audience

During the research, I've decided that my Hangman game targets **school kids aged 7–15**, mainly small kids who are just learning to read and spell and are learning vocabulary, as well as teenagers who enjoy word games and puzzles.
They prefer something quick, clean, and rewarding that helps improve vocabulary and overall erudition while relaxing.
This choice was made because this demographic is likely to appreciate the cognitive challenge of hangman while also valuing a polished user experience that fits into their education.

## Task 4 – User Profiles

I've created two user profiles representing my primary target audience:

### 👩‍💼 Olivia (9)
- Primary school student
- Plays hangman games to improve spelling and vocabulary.
- **Wants:** simple, fun puzzles with visual appeal.
- **Needs:** Intuitive interface, hints for difficult words.
- **Frustrations:** Overly complex rules or cluttered screens.

### 👨‍💻 Nathan (13)
- Secondary school student
- Enjoys word games during breaks.
- **Wants:** Challenging words and competitive scoring.
- **Needs:** Smooth gameplay and clear feedback.
- **Frustrations:** Laggy performance or lack of variety in words.

## Task 5 - High level user requirements

### High level user requirements

Based on my target audience and user profiles, I've developed the following preliminary high-level user requirements for my **Hangman game**.
Depending on available time, some of these may be deprioritised to ensure I am capable of meeting the assignment deadline. The strict timeline means I must first focus on the **core gameplay features**, polish those, and only then add additional features.
I’ve therefore identified the **core (MVP)** features and **nice-to-have (Phase 2)** features.

---

## MVP Features (Must Have)

1. **Main Menu**  
   The game must have a main menu with options to start a new game, view scores, and access settings.  

2. **Game Win Screen**  
   Displayed when the player successfully guesses the full word before running out of attempts.  

3. **Game Over Screen**  
   Displayed when the player runs out of allowed incorrect guesses.  

4. **New Game Functionality**  
   Player must be able to start a new Hangman game at any time.  

5. **Random Word Selection**  
   Each new Hangman round uses a random word from a wide range of topics (e.g., animals, countries, movies).  

6. **Scoring System**  
   Players earn points for correctly guessing letters or completing a word.  

7. **Heads-Up Display (HUD)**  
   The HUD should display current score, word progress (revealed/hidden letters), remaining attempts, and guessed letters.  

8. **Word Display**  
   The word must be shown as a series of blanks (“_”) that get filled as the player guesses correctly.  

9. **Letter Input System**  
   Player must be able to input a letter guess through keyboard or on-screen letter buttons.  

10. **Feedback on Guesses**  
   The game must give immediate feedback for each guessed letter (correct or incorrect).  

11. **Hint Feature**  
   Player can use a limited number of hints to reveal a letter, but each hint deducts points.  

12. **Full Word Guess Option**  
   Player can attempt to guess the entire word at once. An incorrect full-word guess applies a large penalty or counts as multiple missed guesses.  

13. **User Accounts and Login**  
   Players must be able to create an account and log in so that scores and progress can be saved.  

14. **Intuitive User Interface**  
   The game must have a clear and easy-to-navigate interface for menus, gameplay, and viewing stats.  

15. **Simple Scoring System**  
   Points awarded for correct guesses, penalties for incorrect guesses and hints.  

16. **Dynamic Word Generation**  
   The game should draw words dynamically from a curated dictionary or API to ensure variety.  

---

## Nice-to-Have Features (Phase 2)

1. **Difficulty Levels**  
   Player can select from *Easy*, *Medium*, or *Hard* modes, which change word length, allowed attempts, or topic difficulty.  
   **(Note: Completed in Phase 1)**  

2. **Advanced Scoring Logic**  
   Bonus points for streaks (e.g., multiple correct guesses in a row) or for finishing with remaining attempts.  

3. **Accessibility Features**  
   High-contrast color schemes, large font options, and full keyboard navigation.  

4. **Leaderboard**  
   Display the top 10 players along with their scores and completion times.  

5. **Game Timer**  
   Timer to measure how long the player takes to finish each word.  

6. **Timer Toggle Option**  
   Player can choose to enable or disable the game timer.  

7. **Responsive Design**  
   The game should adapt seamlessly to different screen sizes and devices (desktop, tablet, mobile).  

8. **Progress Saving**  
   Player’s progress and scores should be saved locally or online to allow them to resume unfinished games.  
   **(Note: Completed in Phase 1)**  

---

## Hardware Requirements

Players of the Hangman game will need a device capable of running a web browser—such as a desktop computer, laptop, tablet, or smartphone.  

The device should have at least **2GB RAM** and a **modern processor** for smooth gameplay. No dedicated GPU is required, as the game is not graphically intensive.

---

## Operating System Requirements

The Hangman game is meant to be **mobile-ready** as per the requirements and compatible with operating systems such as:  
- **iOS**  
- **Android**

---

## Key Application Functions

| Functionality              | Description                                                                                                                                 |
|----------------------------|---------------------------------------------------------------------------------------------------------------------------------------------|
| **User Authentication**    | Players can create accounts and log in to save scores and progress.                                                                         |
| **Game Interface**         | Intuitive UI for navigating menus, starting games, and viewing scores.                                                                      |


### AI in the game

In my game, I am not planning to use AI features as part of the core gameplay experience.
The only kind of 'AI' feature I am going to use is using an algorithm to generate crossword for a new game started by a user using random words from the vocabulary of clues.
For this I am going to use a predefined list of words and clues, and the algorithm would randomly select words from this list to create unique crossword puzzles for each game session played by a user.
So, this is going to be a basic implementation and does not involve advanced AI techniques.

---

## Task 3 - Create an overall specification 

Create an overall specification based on user and system requirements (including HCI, game/application-rules and the 
game/application-mechanics (e.g. what are the rules for the game, how will the game be controlled, how will 
any non-player characters interact, etc.) 

The following list of functional requirements has been produced to cover the high-level user requirements from task 5 above.
It has to be mentioned the list also has the acceptance criteria for each functional requirement to ensure that the requirement is testable and verifiable.

| Functional requirement             | Type | Specification                                                                                                                                                                                          | Acceptance Criteria                                                                                                                                                                                                                                                                                                                            |
|------------------------------------|------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Main menu when app starts          | UI   | The main menu is displayed with options to play a new game or check rules of the game how to play it.                                                                                                  | When the app starts, main menu is displayed with "Play" and "How to play" options visible and clickable.                                                                                                                                                                                                                                       |

---

## Task 6 – Non-Functional Specifications

It is important to consider non-functional specifications as part of the overall specification for the crossword game.
We've identified the following non-functional specifications to be important for our game:

| Category            | Specification                                           |
|---------------------|---------------------------------------------------------|
| **Aesthetic**       | Clean grid layout, minimal colours, modern typography.  |
| **Usability**       | Simple controls and clear instructions.                 |
| **Responsiveness**  | Works perfectly on desktop, tablet, and mobile.         |
| **Feedback**        | Real-time indicators: green for correct, red for wrong. |
| **Performance**     | Loads under 3 seconds, no noticeable lag.               |
| **Reliability**     | Auto-saves progress locally in memory.                  |
| **Maintainability** | Code modular and well-commented for easy updates.       |

---

## Task 9 - Identify and rank potential risks to the project’s success 

During the brainstorming session, we identified the following potential risks to the project's success along with their mitigation strategies:

| Category                                      | Description                                                                                                                                        | Mitigtion Strategy                                                                                                                                            |
|-----------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Lack of Coding Knowledge                      | Some people in this project may have different coding experience                                                                                   | Pair programming, online tutorials, books from LRC, team knowledge sharing and helping each other when someone is stuck.                                      |
| Scope creep                                   | The project may become too big to handle for the three of us if we keep adding more and more features to the scope.                                | The scope should be frozen to MVP features only to ensure it can be delievered by the deadline.                                                               |


---

## Task 10 - Software development strategy 

### Comparison of the three strategies


---


# Activity 3 – Coding

## Code Repository

The code for this project is hosted on GitHub at:
https://github.com/Alex-Oma/Software-Development-2-Hangman-Game

## Git Branching Strategy

I've decied to go with the following branch strategy on GitHub:
- `main` branch: Stable production-ready code.
- `new_stuff` branch: Development branch for new features and experiments.
- Feature branches: Created from `new_stuff` for specific features or bug fixes, then merged back into `new_stuff` after review and testing.
- Merging `new_stuff` into `main` only after thorough testing and validation to ensure stability.
- Regular commits and pull requests to maintain code quality.


## Developer notes — Backend (FastAPI) + PWA skeleton
To start with, I've created a simple FastAPI backend with a minimal PWA front-end skeleton. 

Running the backend on Windows:

1. Create a virtual environment:

   python -m venv .venv
   .venv\Scripts\activate

2. Install dependencies:

   python -m pip install -r requirements.txt

3. Run the app locally with uvicorn:

   python -m uvicorn backend.app.main:app --reload --port 8000

4. Open the PWA in the browser:

   http://127.0.0.1:8000/index.html

PowerShell helper: `run_local.ps1` is provided which runs uvicorn for convenience.

Unit tests can be run with:
python -m pytest -q





# Activity 4 – Testing

## Testing Strategy

For frontend testing, I've adopted a combination of manual and automated testing strategies to ensure comprehensive coverage of the application's functionality and user experience.
For manual testing, I've focused on exploratory testing to identify any usability issues or unexpected behaviors that automated tests might miss.
This involves navigating through the application, interacting with various UI elements, and verifying that the application behaves as expected.
For automated testing, I am going to implement unit tests for individual components using a testing framework Jest.
These tests focus on verifying the functionality of specific components, ensuring that they render correctly and handle user interactions as intended.
Additionally, I will try setting up end-to-end (E2E) tests using a tool called Cypress to simulate real user scenarios and validate the overall workflow of the application from start to finish.
This includes testing critical paths such as user login, gameplay interactions, and score tracking.

For the backend testing, I've utilized pytest to create unit tests for the FastAPI endpoints.

This way, I can ensure that both the frontend and backend components of the application are thoroughly tested, providing confidence in the application's reliability and user experience.

## Frontend Testing

### Manual Testing Plan and Test Cases with Results

Provided below is the manual testing plan and test cases for the frontend of the Hangman game and their results:

| Test Case ID | Test Description                                                                                          | Expected result                                                                                                                                                                                                                                                                                                                                                                   | Actual result                                                                                                                                                                                                                                                                                                                     | Evidence               | Passed? |
|------------|-----------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------|---------|
| TC001      | Theme button to switch from light theme to dark theme.                                                    | When the button is clicked, the page is  expected to switch from light theme to dark theme.                                                                                                                                                                                                                                                                                       | When the button is clicked, the page switches from light theme to dark theme.                                                                                                                                                                                                                                                     | 1.png                  | Yes     |
| TC002      | Theme button to switch from dark theme to light theme.                                                    | When the button is clicked, the page is expected to switch from dark theme to light theme.                                                                                                                                                                                                                                                                                        | When the button is clicked, the page switches from dark theme to light theme.                                                                                                                                                                                                                                                     | 2.png                  | Yes     | 
| TC003      | Attempt to click “Create Account” with empty fields.                                                      | When attempted, a message should appear underneath the Username field and the message should say “Please fill in this field”.                                                                                                                                                                                                                                                     | When attempted, a message appears underneath the Username field and the message says “Please fill in this field”.                                                                                                                                                                                                                 | 3.png                  | Yes     |
| TC004      | Navigating to home page by clicking “Home” button.                                                        | When the “Home” button is clicked, the app should navigate to the home page and display the home page to the user.                                                                                                                                                                                                                                                                | When the “Home” button is clicked, the app navigates to the home page and displays the home page to the user.                                                                                                                                                                                                                     | 4.png                  | Yes     |
| TC005      | Navigating back to home page from Registration page by clicking “Cancel” button.                          | When the “Cancel” button is clicked. The app should navigate back to the home page from the registration page.                                                                                                                                                                                                                                                                    | When the “Cancel” button is clicked. The app navigates back to the home page from the registration page.                                                                                                                                                                                                                          | 4.png, 5.png           | Yes     |
| TC006      | Attempt to create account with invalid email format.                                                      | The user fills in the details but enters email in invalid format and the user should get an error message saying “Please include an ‘@’ in the email address.”.                                                                                                                                                                                                                   | The user fills in the details but enters email in invalid format and the user gets an error message saying “Please include an ‘@’ in the email address.”.                                                                                                                                                                         | 6.png                  | Yes     |
| TC007      | Creating account with valid credentials                                                                   | When the user enters all the valid credentials, it is expected that they will be transferred onto the game description page.                                                                                                                                                                                                                                                      | When the user enters all the valid credentials, they are transferred onto the game description page.                                                                                                                                                                                                                              | 7.png                  | Yes     |
| TC008      | Attempt to create account with already existing username                                                  | When the user enters the credentials of an already existing account, they are supposed to get the error message “Username already exists”                                                                                                                                                                                                                                         | When the user enters the credentials of an already existing account, they get the error message “Username already exists”.                                                                                                                                                                                                        | 9.png                  | Yes     |
| TC009      | Attempt to enter not matching passwords when creating new account                                         | When the user enters passwords that do not match when entering credentials of an already existing account, they are supposed to get the error message “Password and confirmation do not match”.                                                                                                                                                                                   | When the user enters passwords that do not match when entering credentials of an already existing account, they get the error message “Password and confirmation do not match”.                                                                                                                                                   | 10.png                 | Yes     |
| TC010      | Login page when the user enters their username and password                                               | When the user enters their correct username and password, they should be signed in successfully and transferred to the game page.                                                                                                                                                                                                                                                 | When the user enters their correct username and password, they are signed in successfully and are transferred to the game page.                                                                                                                                                                                                   | 16.png                 | Yes     |
| TC011      | User enters one wrong password                                                                            | When the user enters the wrong password, they should get an error “Invalid credentials”.                                                                                                                                                                                                                                                                                          | When the user enters the wrong password, they get an error “Invalid credentials”.                                                                                                                                                                                                                                                 | 11.png                 | Yes     |
| TC012      | User enters the wrong username.                                                                           | When the user enters the wrong username, they should get an error “Invalid credentials”.                                                                                                                                                                                                                                                                                          | When the user enters the wrong username, they get an error “Invalid credentials”.                                                                                                                                                                                                                                                 | 12.png                 | Yes     |
| TC013      | User enters both incorrect credentials.                                                                   | When the user enters the wrong username and password, they should get an error “Invalid credentials”.                                                                                                                                                                                                                                                                             | When the user enters the wrong username and password, they get an error “Invalid credentials”.                                                                                                                                                                                                                                    | 13.png                 | Yes     |
| TC014      | Theme button to switch from light theme to dark theme.                                                    | When the button is clicked, the page is  expected to switch from light theme to dark theme.                                                                                                                                                                                                                                                                                       | When the button is clicked, the page switches from light theme to dark theme.                                                                                                                                                                                                                                                     | 14.png                 | Yes     |
| TC015      | Theme button to switch from dark theme to light theme.                                                    | When the button is clicked, the page is expected to switch from dark theme to light theme.                                                                                                                                                                                                                                                                                        | When the button is clicked, the page switches from dark theme to light theme.                                                                                                                                                                                                                                                     | 15.png                 | Yes     |
| TC016      | Navigating to home page by clicking “Home” button.                                                        | When the “Home” button is clicked, the app should navigate to the home page and display the home page to the user.                                                                                                                                                                                                                                                                | When the “Home” button is clicked, the app navigates to the home page and displays the home page to the user.                                                                                                                                                                                                                     | 4.png                  | Yes     |
| TC017      | Attempt to click “Create Account”.                                                                        | When attempted, the user should be transferred to the Registration page.                                                                                                                                                                                                                                                                                                          | When attempted, the user is transferred to the Registration page.                                                                                                                                                                                                                                                                 | 17.png                 | Yes     |
| TC018      | Clicking “Resume Game” when signed in.                                                                    | The user is signed in at the moment and when the user clicks the “Resume Game” button, they should be transferred to the game screen.                                                                                                                                                                                                                                             | The user is signed in at the moment and when the user clicks the “Resume Game” button, they are transferred to the game screen.                                                                                                                                                                                                   | 16.png                 | Yes     |
| TC019      | Theme button to switch from light theme to dark theme.                                                    | When the button is clicked, the page is  expected to switch from light theme to dark theme.                                                                                                                                                                                                                                                                                       | When the button is clicked, the page switches from light theme to dark theme.                                                                                                                                                                                                                                                     | 18.png                 | Yes     |
| TC020      | Theme button to switch from dark theme to light theme.                                                    | When the button is clicked, the page is expected to switch from dark theme to light theme.                                                                                                                                                                                                                                                                                        | When the button is clicked, the page switches from dark theme to light theme.                                                                                                                                                                                                                                                     | 19.png                 | Yes     |
| TC021      | Clicking “Sign out” button.                                                                               | Upon clicking “Sign out”, the screen should remain the same, but the options should change from “Resume Game” and “Sign out” to “Sign in” and “Create account” to show that the user has been signed out.                                                                                                                                                                         | Upon clicking “Sign out”, the screen remains the same, but the options change from “Resume Game” and “Sign out” to “Sign in” and “Create account” to show that the user has been signed out.                                                                                                                                      | 20.png                 | Yes     |
| TC022      | Clicking “Sign in” button on index page                                                                   | Upon clicking the “Sign in” button, the user should be transferred to the login page.                                                                                                                                                                                                                                                                                             | Upon clicking the “Sign in” button, the user is transferred to the login page.                                                                                                                                                                                                                                                    | 21.png                 | Yes     |
| TC023      | Clicking “Create account” button on index page                                                            | Upon clicking the “Sign in” button, the user should be transferred to the registration page.                                                                                                                                                                                                                                                                                      | Upon clicking the “Sign in” button, the user is transferred to the registration page.                                                                                                                                                                                                                                             | 17.png                 | Yes     |
| TC024      | game.html page is loaded and game layout is being rendered when user logs into the game.                  | When user logs in to the  game, the game.html page is supposed to be loaded and game layout is supposed to be rendered.                                                                                                                                                                                                                                                           | When user logs in to the game, the game.html page is loaded and game layout is being rendered.                                                                                                                                                                                                                                    | 16.png                 | Yes     |
| TC025      | Theme button to switch from light theme to dark theme.                                                    | When the button is clicked, the page is  expected to switch from light theme to dark theme.                                                                                                                                                                                                                                                                                       | When the button is clicked, the page switches from light theme to dark theme.                                                                                                                                                                                                                                                     | 22.png                 | Yes     |
| TC026      | Theme button to switch from dark theme to light theme.                                                    | When the button is clicked, the page is expected to switch from dark theme to light theme.                                                                                                                                                                                                                                                                                        | When the button is clicked, the page switches from dark theme to light theme.                                                                                                                                                                                                                                                     | 23.png                 | Yes     |
| TC027      | Clicking “Sign out” option to transfer back to index.html page from game.html page.                       | When the user clicks on the “Sign out” button, they should be transferred to the index.html page.                                                                                                                                                                                                                                                                                 | When the user clicks on the “Sign out” button, they are transferred to the index.html page.                                                                                                                                                                                                                                       | 24.png                 | Yes     |
| TC028      | Clicking “Start New Game”                                                                                 | When the user clicks “Start New Game”, they are supposed to get a dropdown menu of game difficulty options.                                                                                                                                                                                                                                                                       | When the user clicks “Start New Game”, they get a dropdown menu of game difficulty options.                                                                                                                                                                                                                                       | 25.png                 | Yes     |
| TC029      | Clicking “Cancel” button in the bottom right corner of the game difficulty menu.                          | When the user clicks the “Cancel” button, the game difficulty menu is supposed to close and the user is supposed to see the game screen again.                                                                                                                                                                                                                                    | When the user clicks the “Cancel” button, the game difficulty menu closes and the user sees the game screen again.                                                                                                                                                                                                                | 26.png, 16.png         | Yes     |
| TC030      | Testing that game starts based on the difficulty the user has chosen                                      | The user selects “Medium” game difficulty in the game difficulty menu options. After the user selects the game difficulty, the game is supposed to start where the user should be able to see the letters, the empty spaces for the letters to be filled into, the buttons “Use Hint” and “Guess Word” and should be able to see the labels “Score”, “Attempts left” and “Hints”. | The user selects “Medium” game difficulty in the game difficulty menu options. After the user selects the game difficulty, the game starts where the user sees the letters, the empty spaces for the letters to be filled into, the buttons “Use Hint” and “Guess Word” and sees the labels “Score”, “Attempts left” and “Hints”. | 27.png                 | Yes     |
| TC031      | Clicking “Start New Game” when current game is in progress.                                               | When the user clicks “Start New Game” while the current game is in progress, they should get a message with a question “Start a new game?” and a message “You haven't finished the current game. Would you like to cancel it and start a new one?” and have a yes and a no option                                                                                                 | When the user clicks “Start New Game” while the current game is in progress, they get a message with a question “Start a new game?” and a message “You haven't finished the current game. Would you like to cancel it and start a new one?” and have a yes and a no option                                                        | 28.png                 | Yes     |
| TC032      | Clicking “No” to return to the current game.                                                              | When the user clicks “No”, they should be able to continue with the current game.                                                                                                                                                                                                                                                                                                 | When the user clicks “No”, they are able to continue with the current game.                                                                                                                                                                                                                                                       | 29.png, 30.png         | Yes     |
| TC033      | Clicking “Yes” to start new game                                                                          | When the user clicks “Yes” to start new game, they should get a drop down menu of the game difficulty options and after selecting they should be able to start a new game.                                                                                                                                                                                                        | When the user clicks “Yes” to start new game, they get a drop down menu of the game difficulty options and after selecting they are able to start a new game.                                                                                                                                                                     | 31.png, 32.png, 33.png | Yes     |
| TC034      | The user guess the word correctly and get a congratulations message.                                      | When the user guesses the word correctly, they are supposed to get this message "You Won! Congratulations — you won!"                                                                                                                                                                                                                                                             | When the user guesses the word correctly, they are get this message "You Won! Congratulations — you won!"                                                                                                                                                                                                                         | 34.png                 | Yes     |
| TC035      | The user does not guess the word and loses and gets a game lost message                                   | The user fails to guess the word and they lose the game and they should get this message “Game Over Game over — you lost. Hint: hint, topic: topic”                                                                                                                                                                                                                               | The user fails to guess the word and they lose the game and they get this message “Game Over Game over — you lost. Hint:  topic: ”.                                                                                                                                                                                               | 35.png, 36.png         | Yes     |
| TC036      | User getting the option to resume game when signing back in                                               | When the user signs back in, they should get a message saying “Resume previous game? You have an unfinished game. Would you like to resume it? ” and that gives them a choice to resume the current game or no.                                                                                                                                                                   | When the user signs back in, they get a message saying “Resume previous game? You have an unfinished game. Would you like to resume it? ” and that gives them a choice to resume the current game or no.                                                                                                                          | 37.png, 38.png, 39.png | Yes     |
| TC037      | User clicks “Cancel” to not resume current game.                                                          | When the user clicks “Cancel”, the current game does not resume and they should be able to start a new game.                                                                                                                                                                                                                                                                      | When the user clicks “Cancel”, the current game does not resume and they are able to start a new game.                                                                                                                                                                                                                            | 40.png, 41.png         | Yes     |
| TC038      | User clicks “Resume” to resume the current game.                                                          | When the user clicks “Resume”, they should be able to continue with the current game.                                                                                                                                                                                                                                                                                             | When the user clicks “Resume”, they are able to continue with the current game.                                                                                                                                                                                                                                                   | 42.png, 43.png         | Yes     |
| TC039      | Testing to ensure that the already guessed letters are not clickable.                                     | When the user has attempted to guess any letters, they should become unclickable.                                                                                                                                                                                                                                                                                                 | When the user has attempted to guess any letters, they become unclickable.                                                                                                                                                                                                                                                        | 44.png                 | Yes     | 
| TC040      | Testing to ensure that letter placeholders are rendered correctly when the user starts a new game.        | When the user starts a new game, the letter placeholders should be rendered correctly neatly in one line.                                                                                                                                                                                                                                                                         | When the user starts a new game, the letter placeholders are rendered correctly neatly in one line.                                                                                                                                                                                                                               | 45.png                 | Yes     |
| TC041      | Testing to ensure that when new game is started, the alphabet is rendered correctly in the correct order. | When the user starts a new game,the alphabet should be rendered correctly in the correct order.                                                                                                                                                                                                                                                                                   | When the user starts a new game,the alphabet is rendered correctly in the correct order.                                                                                                                                                                                                                                          | 46.png                 | Yes     |
| TC042      | Testing to ensure that when wrong guess is made, the number of attempts left decreases by one each time.  | When the user makes a wrong guess, the number of attempts left should decrease by 1 each time.                                                                                                                                                                                                                                                                                    | When the user makes a wrong guess, the number of attempts left decreases by 1 each time.                                                                                                                                                                                                                                          | 47.png, 48.png         | yes     |
| TC043      | Testing to ensure that 10 points is earned after correct guess  is made                                   | When the user makes a correct guess, they should earn 10 points for each correct guess.                                                                                                                                                                                                                                                                                           | When the user makes a correct guess, they earn 10 points for each correct guess.                                                                                                                                                                                                                                                  | 49.png                 | Yes     |
| TC044      | Testing to ensure that when new game s started, Clue and Topic panel are rendered correctly.              | When the user starts a new game, the clue and topic panel should be rendered correctly under the letter placeholders.                                                                                                                                                                                                                                                             | When the user starts a new game, the clue and topic panel are rendered correctly under the letter placeholders.                                                                                                                                                                                                                   | 50.png                 | Yes     |


### Automated Testing Plan and Test Cases

Provided below is the automated testing plan and test cases for the frontend of the Hangman game:

| Test Case ID | Test Description                        | Steps to Reproduce                                                                 | Expected Result                                               | Actual Result | Pass/Fail |
|--------------|-----------------------------------------|-----------------------------------------------------------------------------------|---------------------------------------------------------------|---------------|-----------|
| ATC001       | Verify main menu component renders      | 1. Render MainMenu component<br>2. Check for presence of "Play" and "How to play" buttons | | Both buttons are present in the DOM | Buttons render correctly |       |
| ATC002       | Test letter input functionality         | 1. Render Game component<br>2. Simulate letter input<br>3. Check if letter appears in word display | | Letter appears in the word display | Letter input works correctly |       |
| ATC003       | Test hint functionality                 | | 1. Render Game component<br>2. Simulate clicking "Hint" button<br>3. Check if a letter is revealed and score decreases | | Letter is revealed and score updates | | Hint functionality works correctly |       |


## Backend Testing

### Unit Testing Plan and Test Cases

Provided below is the unit testing plan and test cases for the backend of the Hangman game:

| Test Case ID | Test Description                        | Steps to Reproduce                                                                 | Expected Result                                               | Actual Result | Pass/Fail |
|--------------|-----------------------------------------|-----------------------------------------------------------------------------------|---------------------------------------------------------------|---------------|-----------|
| BTC001       | Test user registration endpoint         | 1. Send POST request to /register with valid user data<br>2. Check response status and body | | Response status is 201 and user data is returned | User registration works correctly |       |
| BTC002       | Test user login endpoint                | 1. Send POST request to /login with valid credentials<br> 2. Check response status and body | | Response status is 200 and token is returned | User login works correctly |       |       |
| BTC003       | Test start new game endpoint            | 1. Send POST request to /start_game with valid user token<br>2. Check response status and body | | Response status is 200 and game data is returned | Start new game works correctly |       |
| BTC004       | Test submit guess endpoint              | 1. Send POST request to /submit_guess with valid game ID and letter<br>2. Check response status and body | | Response status is 200 and updated game state is returned | Submit guess works correctly |       |
| BTC005       | Test get game state endpoint            | 1. Send GET request to /game_state with valid game ID<br>2. Check response status and body | | Response status is 200 and current game state is returned | Get game state works correctly |       |
| BTC006       | Test scoring system                     | 1. Simulate correct and incorrect guesses<br>2. Check if score updates correctly | | Score updates as expected after each guess | Scoring system works correctly |       |
| BTC007       | Test hint functionality                 | 1. Send POST request to /use_hint with valid game ID<br>2. Check response status and body | | Response status is 200 and a letter is revealed with score deduction | Hint functionality works correctly |       |
| BTC008       | Test full word guess functionality      | 1. Send POST request to /guess_word with valid game ID and word<br>2. Check response status and body | | Response status is 200 and game state updates accordingly | Full word guess works correctly |       |
| BTC009       | Test user authentication middleware     | 1. Send requests with and without valid tokens<br>2. Check if access is granted or denied appropriately | | Requests with valid tokens are granted access; invalid tokens are denied | Authentication middleware works correctly |       |
| BTC010       | Test error handling                     | 1. Send invalid requests to various endpoints<br>2. Check if appropriate error responses are returned | | Appropriate error messages and status codes are returned for invalid requests | Error handling works correctly |       |
| BTC011       | Test data persistence                   | 1. Create a new user and start a game<br>2. Restart the server and retrieve user/game data<br>3. Check if data persists correctly | | User and game data persist correctly after server restart | Data persistence works correctly |       |
| BTC012       | Test performance under load             | 1. Simulate multiple concurrent requests to key endpoints<br>2. Measure response times and server stability | | Server handles load without significant performance degradation | Performance under load is acceptable |       |


## Test Results

### Frontend Test Results


CSS layout smoke test: Pass

Very first basic smoke test to ensure that the CSS layout is loading correctly without any major issues.

Light mode screenshot:
[<img alt="image" src="img/testing/frontend/initial_ui_layout_test_light.png" />](img/testing/frontend/initial_ui_layout_test_light.png)

Dark mode screenshot:
[<img alt="image" src="img/testing/frontend/initial_ui_layout_test_dark.png" />](img/testing/frontend/initial_ui_layout_test_dark.png)