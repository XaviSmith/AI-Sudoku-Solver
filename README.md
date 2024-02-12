
# Sudoku AI Solver and generator


Capable of generating a valid sudoku puzzle at random and/or solving any valid sudoku puzzle using backtracking. 

Every puzzle generated will have only 1 solution.


Written in Python

**TODO:** 
- Generate executable 
- Have menu handle unexpected input 
- Allow user to specify number of blank spaces and MaxStackDepth for genrating puzzles 




## Documentation

[Documentation](https://linktodocumentation)

Choose a list of options from main menu to generate or solve a grid.

**1: Generate grid**  

Generate a grid at random. You can then choose to print it an a human readable format like below

``` 
 9  7  2 | 5  4  8 | 3  6  1 
 3  1  5 | 6  7  2 | 9  4  8 
 8  6  4 | 9  1  3 | 7  5  2 
-----------------------------
 6  3  1 | 8  9  4 | 2  7  5 
 7  5  9 | 2  6  1 | 8  3  4 
 2  4  8 | 3  5  7 | 1  9  6 
-----------------------------
 4  2  3 | 7  8  6 | 5  1  9 
 1  9  7 | 4  2  5 | 6  8  3 
 5  8  6 | 1  3  9 | 4  2  7 
 ```
 Or generate a puzzle from it. Every generated puzzle will only have one solution.
 
 Generated puzzles can be either printed in the same human readable format above like so
```
 9       |    4  8 | 3  6    
 3  1    | 6       | 9       
 8  6    | 9       | 7  5  2 
-----------------------------
 6  3  1 |    9  4 | 2     5 
    5  9 | 2  6  1 |       4 
 2       | 3  5    |    9  6 
-----------------------------
    2  3 | 7       | 5     9 
 1     7 | 4  2    | 6  8    
    8  6 | 1  3  9 |    2  7
```
 or printed to a 2D array the former can parse as detailed in the next section.
 

**2: Solve Grid**

Grids are passed in with the format:

```[[1,2,3,0,0,6,7,8,9], [row2], [row3], ..., [row9]]```

Where 0 is a blank space. Use the generator for an example