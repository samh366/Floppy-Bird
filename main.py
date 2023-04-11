import pygame
import random

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


class Game:
    def __init__(self):
        pygame.init()

        self.res = (700, 700)
        self.width, self.height = self.res
        self.mid = self.width//2
        self.screen = pygame.display.set_mode(self.res)
        pygame.display.set_caption("Floppy Bird")
        pygame.display.flip()
        self.clock = pygame.time.Clock()

        self.running = True
        self.playing = False
        self.score = 0
        self.loadHighscore()    # Get highest score
        self.displaynewHighscore = False

        self.player = Player()

        self.titleFont = pygame.font.Font("assets/font/title.TTF", 70)
        self.scoreFont = pygame.font.Font("assets/font/score.TTF", 40)
        self.deathFont = pygame.font.Font("assets/font/death.OTF", 25)

        # Sprites
        self.city = pygame.image.load("assets/bg/city.png")
        self.bush = pygame.transform.scale(pygame.image.load("assets/bg/bush.png"), (200, 80))
        self.floor = pygame.image.load("assets/bg/floor.png")
        self.sand = pygame.image.load("assets/bg/sand.png")

        # Parallax values
        self.cityParallax = 0
        self.bushParallax = 0
        self.floorParallax = 0

        self.initText()
        self.createPipes()
        self.main()


    def mainMenu(self):
        """Main Menu Screen"""
        # Draw player
        self.player.render(self.screen)
        # Show title in the middle of the screen
        self.screen.blit(self.text["title shadow"], (self.mid-self.text["title shadow"].get_width()//2+10, 50+10))
        self.screen.blit(self.text["title"], (self.mid-self.text["title"].get_width()//2, 50))
        self.showHighscore()
        # Press to start
        self.screen.blit(self.text["press to start shadow"], (self.mid-self.text["press to start shadow"].get_width()//2+5, 450+5))
        self.screen.blit(self.text["press to start"], (self.mid-self.text["press to start"].get_width()//2, 450))


    def playGame(self):
        """Run game operations"""
        if not self.player.dead:
            # Move player
            self.player.updatePos()

            # Move pipes, and check if player has hit or passed one
            if self.playerHitPipe():
                self.player.dead = True

        # Draw pipes
        for pipe in self.pipes:
            pipe.render(self.screen)

        # Draw player
        self.player.render(self.screen)

        # Draw score
        self.drawScore()

        if self.player.dead:
            # Record highscore
            if self.score > self.highScore:
                self.highScore = self.score
                self.recordHighscore()
                self.displaynewHighscore = True
            
            self.showDeathMessage()



    def main(self):
        """Main game loop"""
        while self.running:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_SPACE, pygame.K_w, pygame.K_UP] and not self.player.dead:
                        self.playing = True
                        self.player.jump()

                    if event.key == pygame.K_RETURN and self.player.dead == True:
                        self.reset()
                    
                    if event.key == pygame.K_BACKSPACE and self.player.dead == True:
                        self.reset()
                        self.playing = False


            self.screen.fill((73, 139, 245))
            self.drawBackground(move=(not self.player.dead))

            if self.playing:
                self.playGame()
            else:
                self.mainMenu()

            self.drawFloor(move=(not self.player.dead))

            pygame.display.flip()
            self.clock.tick(60)

        
    def recordHighscore(self):
        with open("dat.file", "w") as saveFile:
            saveFile.write(str(self.highScore))


    def loadHighscore(self):
        try:
            with open("dat.file", "r") as saveFile:
                self.highScore = int(saveFile.read())
        
        except (FileNotFoundError, ValueError) as e:
            self.highScore = 0
            self.recordHighscore()
    
    def showHighscore(self):
        self.screen.blit(self.text["high score shadow"], (self.mid-self.text["high score"].get_width()//2+5, 350+5))
        self.screen.blit(self.text["high score"], (self.mid-self.text["high score"].get_width()//2, 350))
        score = self.deathFont.render(str(self.highScore), True, (255, 255, 255))
        shadow = self.deathFont.render(str(self.highScore), True, (0, 0, 0))
        self.screen.blit(shadow, (self.mid-shadow.get_width()//2+5, 387+5))
        self.screen.blit(score, (self.mid-score.get_width()//2, 387))



    def initText(self):
        """
        Renders the unmoving text that needs to be displayed.
        Rendering it all at once when the program starts is more efficient that rendering every frame.
        """

        self.text = {
            "title" : self.titleFont.render("Floppy Bird!", True, (235, 224, 21)),
            "title shadow" : self.titleFont.render("Floppy Bird!", True, (169, 16, 16)),
            "high score" : self.deathFont.render("High Score:", True, (255, 255, 255)),
            "high score shadow" : self.deathFont.render("High Score:", True, (0, 0, 0)),
            "new high score" : self.deathFont.render("New High Score!", True, (169, 16, 16)),
            "new high score shadow" :  self.deathFont.render("New High Score!", True, (235, 224, 21)),
            "press to start" : self.deathFont.render("Press SPACE to start!", True, (255, 255, 255)),
            "press to start shadow" : self.deathFont.render("Press SPACE to start!", True, (0, 0, 0)),

            "death" : [
                self.deathFont.render("You Died!", True, (255, 255, 255)),
                self.deathFont.render("Press ENTER to play again", True, (255, 255, 255)),
                self.deathFont.render("Press BACKSPACE for main menu", True, (255, 255, 255))
            ],
            "death shadow" : [
                self.deathFont.render("You Died!", True, (0, 0, 0)),
                self.deathFont.render("Press ENTER to play again", True, (0, 0, 0)),
                self.deathFont.render("Press BACKSPACE for main menu", True, (0, 0, 0))
            ]
        }


    def createPipes(self):
        """Creates the pipe data when the game is first loaded"""
        self.pipes = []
        for i in range(4):
            self.pipes.append(Pipe(800 + i*350))

    
    def playerHitPipe(self):
        """Checks if the player has hit a pipe"""
        for pipe in self.pipes:
            pipe.move()

            # Check if player hitbox is clipping pipe hitbox
            if self.player.xpos-self.player.hitBox[0]//2-Pipe.width//2 <= pipe.pos <= self.player.xpos+self.player.hitBox[0]//2+Pipe.width//2:
                if pipe.centre+Pipe.spacing-self.player.hitBox[1]//2 <= self.player.height or self.player.height <= pipe.centre-Pipe.spacing+self.player.hitBox[1]//2:
                    return True
             
            if pipe.justPassed():
                self.score += 1


    def drawScore(self):
        """Draws the score text"""
        white = self.scoreFont.render(str(self.score), True, (255, 255, 255))
        shadow = self.scoreFont.render(str(self.score), True, (0, 0, 0))
        whiteBox = white.get_rect(center=(self.res[0]//2, self.res[1]//2-300))
        shadowBox = shadow.get_rect(center=(self.res[0]//2+5, self.res[1]//2-295))

        self.screen.blit(shadow, shadowBox)
        self.screen.blit(white, whiteBox)


    def showDeathMessage(self):
        """Shows a death message"""
        # Print all the death message information
        # Print shadows first, then text
        for type in ["death shadow", "death"]:
            for i, line in enumerate(self.text[type]):
                if type == "death shadow":
                    self.screen.blit(line, (self.mid-line.get_width()//2+5, 300+(i*50)+5))
                else:
                    self.screen.blit(line, (self.mid-line.get_width()//2, 300+(i*50)))
        
        if self.displaynewHighscore == True:
            self.screen.blit(self.text["new high score shadow"], (self.mid-self.text["new high score shadow"].get_width()//2+5, 500+5))
            self.screen.blit(self.text["new high score"], (self.mid-self.text["new high score"].get_width()//2, 500))


    def reset(self):
        """Resets the game"""
        self.player.reset()
        for pipe in self.pipes:
            pipe.reset()

        self.score = 0
        self.displaynewHighscore = False

    
    def drawFloor(self, move=True):
        """Draws the floor"""
        if move == True:
            self.floorParallax += Pipe.speed
            if self.floorParallax > 306:
                self.floorParallax -= 306

        # Sand
        for i in range(4):
            self.screen.blit(self.sand, (700-int(self.floorParallax)-i*306, 650))

        # Green floor
        for i in range(4):
            self.screen.blit(self.floor, (700-int(self.floorParallax)-i*306, 650))


    def drawBackground(self, move=True):
        """Moves and draws the background sprites"""

        if move == True:
            # Move city
            self.cityParallax += 0.3
            if self.cityParallax > 216:
                self.cityParallax -= 216

            # Move bush
            self.bushParallax += 0.5
            if self.bushParallax > 200:
                self.bushParallax -= 200

        # Draw city
        for i in range(5):
            self.screen.blit(self.city, (700-int(self.cityParallax)-i*216, 530))

        # Draw bush
        for i in range(6):
            self.screen.blit(self.bush, (700-int(self.bushParallax)-i*200, 570))


if __name__ == "__main__":
    game = Game()

    pygame.quit()
    quit()