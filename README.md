# CardGamesOnMotorcycles-pygame

Working on making a trading/collectible card game. Currently writing the UI so that 
there is an actual interface in which to interact with the game while creating game
mechanics. I want to refactor the code into a sort of MVC architecture, which will make
it much easier to expand in the future.

# Setup
Just download the source code, and run in a python environment with pygame installed. 
This was written in pygame 1.9.3.

# Controls
Currently the controls are cryptic. Running the game will present you an 
empty field and some cards in your starting hand. There is also a turn counter and
some text indicating the current phase. There are three phases during a turn:
the Draw Phase, Main Phase, and End Phase. Drawing a card is only allowed in 
the Draw Phase, so that is the only time that button will work. Similarly, 
you can only play cards from your hand during the Main Phase. To play a card from 
your hand, simply click it during the Main Phase. Nothing happens during the end phase,
but clicking next phase will advance to the next turn. Currently there is only one
player so this does effectively nothing except let you repeat those actions. View Deck
is self explanatory, and can be clicked during all phases. Pressing ESC will bring up
a menu which will let you start a new game or exit the game.
