import os
import time

frames = [
    """

           ( )
          /|\\
          \\|/
           |
           ^
          / \\
        _/   \\_
    """,
    """
        _       _
         \\_( )_/
           |
           |
           |
           ^
          / \\
        _/   \\_
    """,
    """

           ( )
          /|\\
          \\|/
           |
           ^
          / \\
        _/   \\_
    """,
    """

           ( )
          /|\\
          \\|/
           |
           ^
          / \\
        _/   \\/  
    """,
        """

           ( )
          /|\\
          \\|/
           |
           ^
          / \\
        _/   \\_
    """,
    """
    
           ( )
          /|\\
          \\|/
           |
           ^
          / \\
        _/   \\/  
    """,
        """

           ( )
          /|\\
          \\|/
           |
           ^
          / \\
        _/   \\_
    """,
    """
    
           ( )
          /|\\
          \\|/
           |
           ^
          / \\
        _/   \\/  
    """,
]

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def animate():
 # Adjust the range to repeat the animation more times if desired
    for frame in frames:
        clear_console()
        print(frame)
        time.sleep(1)

if __name__ == "__main__":
    animate()
