# Python Maze Generator
**Description:** This python program will generate a maze with the PyGame library to display the maze. I created this algorithm to challenge myself, during my self protection quarantine from Covid-19.

![Program screenshot](./screenshot.jpg)

## Algorithm Explained:
- The program will generate a 2D Array based on the desired # of rows and columns.
- Using a recursive function named `startBranch`, a number is placed at random coordinates in the `mazeArray`.
- That starting position determines which direction in can expand to, and branches out.
- Each branch created will also branch out after placing a given number into the 2D Array. Note, the 'given number' is the current position in the path being created, and when you count up from the starting position (which is always 1), you will see the maze.
- Then, the 'branch' function calls for the next spot of the maze path to be made, by moving into a random possible position (From any of 4 directions: up, down, left, or right).
-  Each branch will expand as far as possible, creating the random path (a.k.a the maze!).

## Extra Information:
**Modify the code:** Use the [Trinket](https://trinket.io/pygame/6310965376) service to edit and remix the code live in the browser *(without setting up pygame)*

>*Set up Pygame to run the code locally:* [Add Pygame](https://stackoverflow.com/questions/28453854/add-pygame-module-in-pycharm-id)

*Note:* This program was started on 3/22/2020 7:54 PM and completed on 3/23/2020 at 6:38 PM.