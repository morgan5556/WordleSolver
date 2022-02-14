# WordleSolver

## About

This repository contains an algorithm that attempts to solve a round of the popular game [Wordle](https://www.nytimes.com/games/wordle/index.html). Currently, the algorithm takes an average of 3.91 guesses with a 98.6% success rate. The aim for this project is to get a 100% success rate.

## Menu

The program has 2 features:
- `WordleSolver`: this is where the program plays a single game of Wordle, the user must reply with `G` for a green square, `Y` for a yellow square and `B` for a blank square in a form such as `GYBBY`.
- `Simulate all Words`: this allows the user to see how the program solves each 5 letter word. An average is displayed as well as further results in the `results.txt` file.

## How to Run

This program requires Python 3.10 or later to be installed on the user's device. To run the program, a file called `results.txt` must be placed in the same folder as the `main.py` file - this will allow the `Simulate all Words` functionality to work.

# Future Improvements / Things I am working on

- To get a success rate of closer to 100%.
- To make the program so you can find the algorithm's average with a certain starting word.
- To make a more detailed summary when running the WordleSolver, the program will output how many words have been eliminated after each guess if the user wants to know.

## Contact 

Should you want to know more about this project, or have any suggestions please contact me:
- Discord: morgan5556#4418
- Mail: morgan@morganlyons.xyz

## License

This is free software: you can redistribute it and/or modify it under the terms
of the GNU General Public License as published by the Free Software Foundation,
either version 3 of the License, or (at your option) any later version. It is
distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
the code.  If not, see http://www.gnu.org/licenses/.