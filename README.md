# Falling-stars
Setting up the game:
    Step 1: Install Visual Studio code
    Step 2: Download Python 3.10.5 from https://www.python.org/downloads/macos/ (for Window https://www.python.org/downloads/windows/ )
    Step 3: Go to VS code extension, install the Python extension developed by Microsoft.
    Step 4: Open the FallingStars folder in VS code
    Step 5: Open up the terminal, then type "pip install pygame==2.1.2"
    Step 6: Open up falling_star.py file, then run the python file to start playing the game.

Game descriptions:
 - A player controlling a slime, and the player goal is to collect as many blue star as possible. The score is increase by one for each blue star collected.
 - The player also needs to dodge the spinning yellow star. If not, the player will lost 1 health. The player have 5 health.
 - When player's health reach zero, the game will be over and the game will close automatically.
 - For every 5 scores gained, the level increases 1, there are 3 levels total. And the game gets harder every time the level increase.
 - The game will continue to run when the player exit the game or the player's health is zero.
 - To control the character use left arrow key to move left, right arrow key to move right, up arrow key to jump, and hit spacebar to pause the game.