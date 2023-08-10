import pygame
import random

class Pipe:
    lowerPipe = pygame.transform.scale(pygame.image.load("assets/bg/pipe.png"), (int(90*1.2), int(600*1.2)))
    upperPipe = pygame.transform.rotate(lowerPipe, 180)
    width = 108
    spacing = 70
    speed = 2

    def __init__(self, xpos):
        self.originalXPos = xpos
        self.pos = xpos
        
        self.pointGiven = False

        self.randomiseCentre()
        

    def move(self):
        """Moves the pipe, looping round if off screen"""
        self.pos -= self.speed
        if self.pos <= -350:
            self.pos += 1400
            self.randomiseCentre()
            self.pointGiven = False


    def randomiseCentre(self):
        """Get new random centre"""
        self.centre = random.randint(200, 500)


    def render(self, screen):
        """Draws the pipe on screen"""
        lowerRect = Pipe.lowerPipe.get_rect(center=(self.pos, self.centre + 360 + Pipe.spacing))
        upperRect = Pipe.upperPipe.get_rect(center=(self.pos, self.centre - 360 - Pipe.spacing))
        screen.blit(Pipe.lowerPipe, lowerRect)
        screen.blit(Pipe.upperPipe, upperRect)


    def justPassed(self):
        """Returns True if the player has just passed this pipe"""
        if self.pos < 300 and not self.pointGiven:
            self.pointGiven = True
            if Pipe.speed < 3:
                Pipe.speed += 0.2
            return True
        return False


    def reset(self):
        """Resets pipe data"""
        self.pos = self.originalXPos
        self.pointGiven = False
        self.randomiseCentre()
        Pipe.speed = 2