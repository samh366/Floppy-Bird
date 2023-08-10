import pygame

class Player:
    def __init__(self):
        self.height = 300
        self.xpos = 350
        self.vel = 0
        self.maxSpeed = 15
        self.flapTimer = 0

        self.dead = False

        self.size = (907//10, 802//10)
        self.hitBox = (60, 30)

        self.spriteIdle = pygame.transform.scale(pygame.image.load("assets//player//bird.png"), self.size)
        self.spriteFlap = pygame.transform.scale(pygame.image.load("assets//player//bird flap.png"), self.size)


    def updatePos(self):
        """Moves the player"""
        if not self.dead:
            self.vel += 0.35
            if self.vel > self.maxSpeed:
                self.vel = self.maxSpeed

            self.height += self.vel
            if self.height > 615:
                self.height = 615
                self.dead = True

            if self.height < -90:
                self.height = -90


    def jump(self):
        self.vel = -7
        self.flapTimer = 20

    
    def rotate(self):
        """Rotates the player's sprite based on speed"""
        angle = -60 * (self.vel/self.maxSpeed)
        if angle > 30:
            angle = 30
        if self.flapTimer == 0:
            return pygame.transform.rotate(self.spriteIdle, angle)
        else:
            return pygame.transform.rotate(self.spriteFlap, angle)


    def render(self, screen):
        """Renders the players sprite on the given surface"""
        rotatedSprite = self.rotate()
        rotatedRect = rotatedSprite.get_rect(center=(self.xpos, self.height))
        screen.blit(rotatedSprite, rotatedRect)

        # Debug, draws the player centre and hitbox
        # pygame.draw.circle(screen, (0, 0, 255), (self.xpos, self.height), 4)
        # pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(self.xpos-self.hitBox[0]//2, self.height-self.hitBox[1]//2, self.hitBox[0], self.hitBox[1]), width=2)

        if self.flapTimer != 0:
            self.flapTimer -= 1


    def reset(self):
        """Reset player values"""
        self.height = 300
        self.vel = 0
        self.dead = False