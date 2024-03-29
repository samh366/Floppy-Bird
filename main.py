import pygame

from classes.player import Player
from classes.pipe import Pipe

### Run to start Floppy Bird! ###

class Game:
    def __init__(self):
        pygame.init()

        self.res = (700, 700)
        self.width, self.height = self.res
        self.mid = self.width//2
        self.screen = pygame.display.set_mode(self.res)
        icon = pygame.image.load("assets/icons/icon_128.png")
        pygame.display.set_icon(icon)
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