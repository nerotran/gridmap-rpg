import pygame
import random
import characterTypes
import Assets
from os import path

pygame.init()

# Asset and text properties
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

# Display properties
FPS = 15 
display_width = 900
display_height = int(display_width * 2 / 3)
clock = pygame.time.Clock()
block_size = 48

# Create a game display
gameDisplay = pygame.display.set_mode([display_width, display_height])
gameDisplay.fill(white)
pygame.display.set_caption("Map")

# Images
img_dir = path.join(path.dirname(__file__), 'img')
backGroundImg = pygame.image.load(path.join(img_dir,
                                            "background.jpg")).convert_alpha()
backGroundImg = pygame.transform.scale(backGroundImg, (display_width, display_height))
tileImg = pygame.image.load(path.join(img_dir, "tile.png")).convert()
tileImg = pygame.transform.scale(tileImg, (block_size, block_size))
playerImg = pygame.image.load(path.join(img_dir, "Player.png")).convert_alpha()
playerImg = pygame.transform.scale(playerImg, (block_size, block_size))
caveImg = pygame.image.load(path.join(img_dir, "goblinsword.png")).convert_alpha()
caveImg = pygame.transform.scale(caveImg, (block_size, block_size))

backGroundRect = backGroundImg.get_rect()

# Sprites
all_sprites = pygame.sprite.Group()

def message_to_screen(msg, color, fontSize, x_axis, y_axis):
    font = pygame.font.SysFont(None, fontSize)
    screen_text = font.render(msg, True, color)
    gameDisplay.blit(screen_text, [x_axis, y_axis])

def makeBackground():
    gameDisplay.fill(white)
    gameDisplay.blit(backGroundImg, backGroundRect)

def battleStats(Player, enemy):
    message_to_screen("Your Level: " + str(Player.level), white, 30, display_width * 0.05, display_height / 8)
    message_to_screen("Your Strength: " + str(Player.attributes["strength"]), white, 30, display_width * 0.05,
                      display_height / 6)
    message_to_screen("Your Dexteriety: " + str(Player.attributes["dexteriety"]), white, 30, display_width * 0.05,
                      display_height / 5)
    message_to_screen("Your Constitution: " + str(Player.attributes["constitution"]), white, 30, display_width * 0.05,
                      display_height / 4.3)
    message_to_screen("Your HP: " + str(Player.hitPoint), white, 30, display_width * 0.05,
                      display_height / 3.5)
    message_to_screen("Your Experience: " + str(Player.experience), white, 30, display_width * 0.05,
                      display_height / 3)
    message_to_screen("Enemy Level: " + str(enemy.level), white, 30, display_width * 0.7, display_height / 8)
    message_to_screen("Enemy Strength: " + str(enemy.attributes["strength"]), white, 30, display_width * 0.7,
                      display_height / 6)
    message_to_screen("Enemy Dexteriety: " + str(enemy.attributes["dexteriety"]), white, 30, display_width * 0.7,
                      display_height / 5)
    message_to_screen("Enemy Constitution: " + str(enemy.attributes["constitution"]), white, 30, display_width * 0.7,
                      display_height / 4.3)
    message_to_screen("Enemy HP: " + str(enemy.hitPoint), white, 30, display_width * 0.7,
                      display_height / 3.5)

def playerStats(Player):
    message_to_screen("Your Level: " + str(Player.level), white, 30, display_width * 0.05, display_height / 8)
    message_to_screen("Your Strength: " + str(Player.attributes["strength"]), white, 30, display_width * 0.05,
                      display_height / 6)
    message_to_screen("Your Dexteriety: " + str(Player.attributes["dexteriety"]), white, 30, display_width * 0.05,
                      display_height / 5)
    message_to_screen("Your Constitution: " + str(Player.attributes["constitution"]), white, 30, display_width * 0.05,
                      display_height / 4.3)
    message_to_screen("Your HP: " + str(Player.hitPoint), white, 30, display_width * 0.05,
                      display_height / 3.5)
    message_to_screen("Your Experience: " + str(Player.experience), white, 30, display_width * 0.05,
                      display_height / 3)

def mapText(level, kills, goal):
    message_to_screen("Current level: " + str(level), red, 30, display_width / 1.25 , display_height / 32)
    message_to_screen("Goal: " + str(kills) + "/" + str(goal), red, 30, display_width / 1.25, display_height / 16)

def hpScreen(Player, hpRegain, hpRestored):

    makeBackground()
    message_to_screen("You regained " + str(hpRegain) + " HP.", white, 45, display_width / 3.2,
                      display_height / 1.5)
    message_to_screen("Press 'E' to go back to map.", red, 50, display_width / 3.5,
                      display_height / 1.2)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                hpRestored = False
                Player.hitPoint += hpRegain

    pygame.display.update()

    return hpRestored

def levelUpScreen(levelup, levelup2):

    makeBackground()
    message_to_screen("Congratulation! You leveled up.", white, 45, display_width / 3.2,
                      display_height / 1.5)
    message_to_screen("Press 'E' to check your new stat.", red, 50, display_width / 3.5,
                      display_height / 1.2)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                levelup = False
                levelup2 = True

    pygame.display.update()

    return levelup, levelup2

def winScreen(Player, enemy, kills):

    battleOver = False
    enemyDeath = False
    enemyDmg = True
    hpRestored = False

    makeBackground()
    message_to_screen("You won!", white, 45, display_width / 2.8,
                      display_height / 1.5)
    message_to_screen("Press 'E' to continue.", red, 50, display_width / 3,
                      display_height / 1.2)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                enemy.hitPoint = 1
                enemyDeath = True
                kills += 1
                battleOver = True
                enemyDmg = False

                if Player.level >= enemy.level:
                    Player.experience += 20
                else:
                    Player.experience += 20 * (enemy.level - Player.level + 1)

                hpRestored = True

    pygame.display.update()

    return battleOver, enemyDmg, hpRestored, enemyDeath, kills

def fledScreen(Player, enemy):
    fled = Player.fled(enemy)
    enemyDmg = False
    battleOver = False
    damage = 0
    if fled == True:
        while fled:
            makeBackground()
            message_to_screen("You sucessfully ran away", white, 45, display_width / 2.8,
                              display_height / 1.5)
            message_to_screen("Press 'E' to continue.", red, 50, display_width / 3,
                              display_height / 1.2)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        battleOver = True
                        fled = False

            pygame.display.update()
    else:
        while not fled:
            makeBackground()
            message_to_screen("You failed to run away", white, 45, display_width / 2.8,
                              display_height / 1.5)
            message_to_screen("Press 'E' to continue.", red, 50, display_width / 3,
                              display_height / 1.2)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        fled = True
                        enemyDmg = True
                        damage = enemy.attack(Player)
                        if str(damage) != "You missed":
                            damage += random.randint(-4, 5)
                            Player.hitPoint -= damage
            pygame.display.update()

    return battleOver, enemyDmg, damage

def playerAttack(Player, enemy, damage):

    dealtDmg = True
    enemyDmg = False

    makeBackground()
    battleStats(Player, enemy)
    if str(damage) != "You missed":
        message_to_screen("You dealt " + str(damage) + " damage.", white, 45, display_width / 2.8,
                          display_height / 1.5)
        message_to_screen("Press 'E' to continue.", red, 50, display_width / 3,
                          display_height / 1.2)
    else:
        message_to_screen(damage, white, 45, display_width / 2.8, display_height / 1.5)
        message_to_screen("Press 'E' to continue.", red, 50, display_width / 3,
                          display_height / 1.2)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                dealtDmg = False
                enemyDmg = True
                damage = enemy.attack(Player)
                if str(damage) != "You missed":
                    damage += random.randint(-4, 5)
                    Player.hitPoint -= damage
    pygame.display.update()

    return dealtDmg, enemyDmg, damage

def enemyAttack(Player, enemy, enemyDmg, damage):


    makeBackground()
    battleStats(Player, enemy)
    if str(damage) != "You missed":
        message_to_screen("The enemy dealt " + str(damage) + " damage.", white, 45, display_width / 2.8,
                          display_height / 1.5)
        message_to_screen("Press 'E' to continue.", red, 50, display_width / 3,
                          display_height / 1.2)
    else:
        message_to_screen("The enemy missed", white, 45, display_width / 2.8, display_height / 1.5)
        message_to_screen("Press 'E' to continue.", red, 50, display_width / 3,
                          display_height / 1.2)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                enemyDmg = False
    pygame.display.update()

    return enemyDmg

def statScreen(Player, levelup2):

    Player.playerLevelUp()
    Player.stats()
    makeBackground()
    playerStats(Player)
    message_to_screen("Press 'E' to go back to the map.", red, 50, display_width / 3,
                      display_height / 1.2)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                levelup2 = False

    pygame.display.update()

    return levelup2

def playerDie(Player, battleOver, gameOver):

    makeBackground()
    message_to_screen("You died.", white, 45, display_width / 2.8,
                      display_height / 1.5)
    message_to_screen("Press 'E' to restart.", red, 50, display_width / 3,
                      display_height / 1.2)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                Player.hitPoint += 1
                battleOver = True
                gameOver = True

    pygame.display.update()

    return battleOver, gameOver


def advanceLevel(Player, levelOver, level, nextLevel, hpRestored):

    expEarned = level * 100

    makeBackground()
    message_to_screen("You finished this level." ,
                      white, 45, display_width / 2.8, display_height / 1.5)
    message_to_screen("You earned " + str(expEarned) + " exp.", white, 45,
                      display_width / 2.8, display_height / 1.35)
    message_to_screen("Press 'E' to continue.", red, 50, display_width / 3,
                      display_height / 1.2)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                Player.experience += expEarned
                levelOver = True
                hpRestored = False
                nextLevel = False

    pygame.display.update()

    return levelOver, nextLevel, hpRestored

def update(board, level, kills, goal):

    makeBackground()
    mapText(level, kills, goal)
    grid_x = display_width / 10
    grid_y = display_height / 32

    for row in board:
        for space in row:
            tile = Assets.tiles(tileImg, grid_x, grid_y)
            all_sprites.add(tile)
            grid_x += block_size
        grid_y += block_size
        grid_x = display_width / 10

    grid_x = display_width / 10
    grid_y = display_height / 32

    for row in board:
        for space in row:
            if space == "player":
                player = Assets.Player(playerImg, grid_x, grid_y)
                all_sprites.add(player)
            if space == "cave":
                tile = Assets.Cave(caveImg, grid_x, grid_y)
                all_sprites.add(tile)
            grid_x += block_size
        grid_y += block_size
        grid_x = display_width / 10

    all_sprites.draw(gameDisplay)
    pygame.display.update()

def getCoordinate(x, y, board):
    x = x + 0
    y = len(board) - 1 - y
    return x, y

def battleScreen(Player, enemy, kills, goal, level):

    dealtDmg = False
    enemyDmg = False
    battleOver = False
    gameOver = False
    levelup = False
    levelup2 = False
    hpRestored = False
    enemyDeath = False
    nextLevel = False
    levelOver = False

    makeBackground()
    message_to_screen("Press 'A' to attack", red, 50, display_width * 0.05, display_height / 1.3)
    message_to_screen("Press 'Q' to run", red, 50, display_width * 0.05, display_height / 1.2)
    battleStats(Player, enemy)

    for battleEvent in pygame.event.get():
        if battleEvent.type == pygame.KEYDOWN:
            if battleEvent.key == pygame.K_a:
                dealtDmg = True
                damage = Player.attack(enemy)
                if str(damage) != "You missed":
                    damage += random.randint(-4, 5)
                    enemy.hitPoint -= damage
            elif battleEvent.key == pygame.K_q:
                battleOver, enemyDmg, damage = fledScreen(Player, enemy)



    while dealtDmg:
        dealtDmg, enemyDmg, damage = playerAttack(Player, enemy, damage)

    while enemy.hitPoint <= 0:
        battleOver, enemyDmg, hpRestored, enemyDeath, kills = winScreen(Player, enemy, kills)

    if kills == goal:
        nextLevel = True

    while nextLevel:
        levelOver, nextLevel, hpRestored = advanceLevel(Player, levelOver, level, nextLevel, hpRestored)

    if Player.experience >= Player.expToNextLevel:
        levelup = True

    hpRegain = random.randrange(int((Player.baseHitpoint * 0.1)),
                                int((Player.baseHitpoint * 0.2) + Player.attributes["constitution"] * 3))

    while hpRestored:

        hpRestored = hpScreen(Player, hpRegain, hpRestored)

    while levelup:

        levelup, levelup2 = levelUpScreen(levelup, levelup2)


    while levelup2:

        levelup2 = statScreen(Player, levelup2)


    while enemyDmg:
        enemyDmg = enemyAttack(Player, enemy, enemyDmg, damage)

    while Player.hitPoint <= 0:
        battleOver, gameOver = playerDie(Player, battleOver, gameOver)


    pygame.display.update()

    return levelOver, battleOver, gameOver, kills, enemyDeath


def game():
    main = True
    level = 1
    Player = characterTypes.player(2, 2, 2, 1)
    Player.stats()

    while main:

        clock.tick(FPS)
        onLevel = True
        goal = random.randint(1 + level, 3 + level)
        kills = 0
        loop = goal

        board = [["0"] * 12 for i in range(0, 12)]
        while loop > 0:
            x = random.randint(1, 11)
            y = random.randint(1, 11)
            pos_x, pos_y = getCoordinate(x, y, board)

            if board[pos_y][pos_x] != "cave":
                board[pos_y][pos_x] = "cave"
            else:
                loop += 1

            loop -= 1

        x = 0
        y = 0

        battle = False
        gameOver = False
        battleOver = False

        while onLevel:

            old_x = x
            old_y = y

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    onLevel = False
                    main = False

                if event.type == pygame.KEYDOWN:
                    board[pos_y][pos_x] = "0"
                    if event.key == pygame.K_UP and y < 11:
                        y += 1
                    elif event.key == pygame.K_DOWN and y > 0:
                        y -= 1
                    if event.key == pygame.K_RIGHT and x < 11 :
                        x += 1
                    elif event.key == pygame.K_LEFT and x > 0:
                        x -= 1

            pos_x,pos_y = getCoordinate(x, y, board)

            if board[pos_y][pos_x] == "cave":
                enemy = characterTypes.character(1, 1, 1, random.randint(Player.level, Player.level + 2))
                enemy.stats()
                battle = True
                enemyDeath = False

                while battle == True:
                    battleOver = False
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            battle = False
                            onLevel = False
                            main = False
                    levelOver, battleOver, gameOver, kills, enemyDeath = battleScreen(Player, enemy, kills, goal, level)
                    if battleOver == True:
                        battle = False
                        if enemyDeath == False:
                            x = old_x
                            y = old_y
                            pos_x, pos_y = getCoordinate(x, y, board)
                        board[pos_y][pos_x] = "player"
                        if gameOver == True:
                            onLevel = False
                            level = 1
                            Player = characterTypes.player(2, 2, 2, 1)
                            Player.stats()
                        elif levelOver == True:
                            Player.stats()
                            onLevel = False
                            level += 1
            else:
                board[pos_y][pos_x] = "player"

            update(board, level, kills, goal)
            clock.tick(FPS)

    pygame.quit()
    quit()



game()