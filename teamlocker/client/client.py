# This is the code for the client program.

from ..teamlocker import magic

def run_client():
    print( f"The magic is {magic(100)}" )

if __name__ == "__main__":
    run_client()