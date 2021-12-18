from logger import console
from curses import wrapper

if __name__ == '__main__':
    wrapper(console.run)
