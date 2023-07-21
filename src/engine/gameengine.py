import pygame


class GameEngine(object):
    """Base game engine for Stuckfish and related projects"""

    def __init__(self) -> None:
        pygame.init()
        print("Starting game engine...")
