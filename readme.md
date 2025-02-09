# Welcome to ChessEngine v1.0.0 - Ben Hickman
## Notes:
This Chess Engine utilizes both 64 index (8x8 board) and 120 index (10x12 board) data structures to represent the state of the board.
This allows for easier searching when generating moves as the 120 index includes out of bounds tiles as a halting point when analysing down files and across ranks to determine legal moves.

The following mapping shows how an index translated from the 64 based structure converts to the 120 based structure. Please note that the white pieces begin on the lower indices (index 0 for 64 based, and index 21 for 120 based.)

```
square64ToSquare120:
                        White
        A    B    C    D    E    F    G    H
      +----+----+----+----+----+----+----+----+
    1 | 21 | 22 | 23 | 24 | 25 | 26 | 27 | 28 | 1
      +----+----+----+----+----+----+----+----+
    2 | 31 | 32 | 33 | 34 | 35 | 36 | 37 | 38 | 2
      +----+----+----+----+----+----+----+----+
    3 | 41 | 42 | 43 | 44 | 45 | 46 | 47 | 48 | 3
R     +----+----+----+----+----+----+----+----+
A   4 | 51 | 52 | 53 | 54 | 55 | 56 | 57 | 58 | 4
N     +----+----+----+----+----+----+----+----+
K   5 | 61 | 62 | 63 | 64 | 65 | 66 | 67 | 68 | 5
      +----+----+----+----+----+----+----+----+
    6 | 71 | 72 | 73 | 74 | 75 | 76 | 77 | 78 | 6
      +----+----+----+----+----+----+----+----+
    7 | 81 | 82 | 83 | 84 | 85 | 86 | 87 | 88 | 7
      +----+----+----+----+----+----+----+----+
    8 | 91 | 92 | 93 | 94 | 95 | 96 | 97 | 98 | 8
      +----+----+----+----+----+----+----+----+
  FILE  A    B    C    D    E    F    G    H
                        Black

The full board with out of bounds tiles is visualized as such:

   0  | 1  | 2  | 3  | 4  | 5  | 6  | 7  | 8  | 9
   --   --   --   --   --   --   --   --   --   --
   10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19
   -- +----+----+----+----+----+----+----+----+ -- 
   20 | 21 | 22 | 23 | 24 | 25 | 26 | 27 | 28 | 29
   -- +----+----+----+----+----+----+----+----+ -- 
   30 | 31 | 32 | 33 | 34 | 35 | 36 | 37 | 38 | 39
   -- +----+----+----+----+----+----+----+----+ -- 
   40 | 41 | 42 | 43 | 44 | 45 | 46 | 47 | 48 | 49
   -- +----+----+----+----+----+----+----+----+ -- 
   50 | 51 | 52 | 53 | 54 | 55 | 56 | 57 | 58 | 59
   -- +----+----+----+----+----+----+----+----+ -- 
   60 | 61 | 62 | 63 | 64 | 65 | 66 | 67 | 68 | 69
   -- +----+----+----+----+----+----+----+----+ -- 
   70 | 71 | 72 | 73 | 74 | 75 | 76 | 77 | 78 | 79
   -- +----+----+----+----+----+----+----+----+ -- 
   80 | 81 | 82 | 83 | 84 | 85 | 86 | 87 | 88 | 89
   -- +----+----+----+----+----+----+----+----+ -- 
   90 | 91 | 92 | 93 | 94 | 95 | 96 | 97 | 98 | 99
   -- +----+----+----+----+----+----+----+----+ -- 
   100| 101| 102| 103| 104| 105| 106| 107| 108| 109
   --   --   --   --   --   --   --   --   --   --
   110| 111| 112| 113| 114| 115| 116| 117| 118| 119
```