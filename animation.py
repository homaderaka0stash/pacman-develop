import pygame


class Animation:
    def __init__(self, frames, speed: int):
        self.frames = [pygame.image.load(frame) for frame in frames]
        self.counter = 0
        self.cur_frame = 0
        self.speed = speed

    def get_next_frame(self):
        self.counter += 1
        self.cur_frame = self.counter // self.speed
        self.cur_frame %= len(self.frames)
        return self.frames[self.cur_frame]
