from kivy.logger import Logger
from kivy.core.window import Window
import logging
from othello_app import OthelloApp
Window.size = (640,700)

def main():
    OthelloApp().run()


if __name__ == "__main__":
    logging.Logger.manager.root = Logger
    main()
