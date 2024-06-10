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

def animate():
 # Adjust the range to repeat the animation more times if desired

        for frame in frames:
            os.system('cls')
            print(frame)
            time.sleep(0.5)


if __name__ == "__main__":
    animate()
