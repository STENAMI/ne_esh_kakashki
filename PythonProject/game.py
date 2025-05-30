import pygame
import sys
import random
import time

pygame.init()

# Загрузка изображений (замените пути на свои)
player_image = pygame.image.load("images/cute.png")
desired_width = 100
desired_height = 100
player_image = pygame.transform.scale(player_image, (desired_width, desired_height))
player_rect = player_image.get_rect()

shield_image = pygame.image.load("images/shield.png")
shield_image = pygame.transform.scale(shield_image, (50, 50))
bonus_image = pygame.image.load("images/bonus.png")
bonus_image = pygame.transform.scale(bonus_image, (50, 50))
my_object_image = pygame.image.load("images/kaka.png")
desired_width_obj, desired_height_obj = 50, 50
my_object_image = pygame.transform.scale(my_object_image, (desired_width_obj, desired_height_obj))

WIDTH, HEIGHT = 600, 800

font = pygame.font.SysFont(None, 36)


def game_loop():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Не ешь какашки котик")
    clock = pygame.time.Clock()

    player_x = WIDTH // 2 - player_rect.width // 2
    player_y = HEIGHT - player_rect.height - 10

    speed = 5

    obstacles = []

    ADD_OBSTACLE_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(ADD_OBSTACLE_EVENT, 1500)

    score = 0

    # Эффекты щита и бонуса
    shield_active = False
    shield_end_time = 0

    bonus_active = False
    bonus_end_time = 0

    game_over = False

    while not game_over:
        current_time = int(time.time())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == ADD_OBSTACLE_EVENT:
                obstacle_type = random.choice(['normal', 'shield', 'bonus'])
                obstacle_width = random.randint(30, 70)
                obstacle_height = random.randint(30, 70)
                obstacle_x = random.randint(0, WIDTH - obstacle_width)
                obstacle_y = -obstacle_height
                rect = pygame.Rect(obstacle_x, obstacle_y, obstacle_width, obstacle_height)
                if obstacle_type == 'normal':
                    obstacles.append({'rect': rect, 'type': 'normal', 'image': my_object_image})
                elif obstacle_type == 'shield':
                    obstacles.append({'rect': rect, 'type': 'shield', 'image': shield_image})
                elif obstacle_type == 'bonus':
                    obstacles.append({'rect': rect, 'type': 'bonus', 'image': bonus_image})

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= speed
        if keys[pygame.K_RIGHT]:
            player_x += speed
        if keys[pygame.K_UP]:
            player_y -= speed
        if keys[pygame.K_DOWN]:
            player_y += speed

        # Ограничение внутри окна
        if player_x < 0:
            player_x = 0
        elif player_x + player_rect.width > WIDTH:
            player_x = WIDTH - player_rect.width

        if player_y < 0:
            player_y = 0
        elif player_y + player_rect.height > HEIGHT:
            player_y = HEIGHT - player_rect.height

        # Обновление препятствий и проверка столкновений
        for obstacle in obstacles[:]:
            obstacle['rect'].y += random.randint(3, 7)

            # Проверка столкновения с игроком с учетом щита
            player_rect_moved = pygame.Rect(player_x, player_y, player_rect.width, player_rect.height)
            if obstacle['rect'].colliderect(player_rect_moved):
                if obstacle['type'] == 'normal':
                    if shield_active:
                        obstacles.remove(obstacle)
                    else:
                        game_over = True
                elif obstacle['type'] == 'shield':
                    shield_active = True
                    shield_end_time = current_time + 5
                    obstacles.remove(obstacle)
                elif obstacle['type'] == 'bonus':
                    bonus_active = True
                    bonus_end_time = current_time + 5
                    score += 10
                    obstacles.remove(obstacle)

            # Удаляем за нижней границей и увеличиваем счет за прохождение мимо них
            if obstacle['rect'].y > HEIGHT:
                obstacles.remove(obstacle)
                score += 1

        # Проверка истечения времени эффектов и их отключение
        if shield_active and current_time >= shield_end_time:
            shield_active = False

        if bonus_active and current_time >= bonus_end_time:
            bonus_active = False

        # Отрисовка сцены
        screen.fill((255, 255, 255))
        screen.blit(player_image, (player_x, player_y))
        for obstacle in obstacles:
            screen.blit(obstacle['image'], (obstacle['rect'].x, int(obstacle['rect'].y)))

        # Отображение очков и статуса щита/бонуса (по желанию)
        score_text = font.render(f"Очки: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        if shield_active:
            shield_text = font.render("Щит активен!", True, (0, 128, 0))
            screen.blit(shield_text, (10, 50))

        if bonus_active:
            bonus_text = font.render("Бонус активен!", True, (128, 0, 128))
            screen.blit(bonus_text, (10, 80))

        pygame.display.flip()
        clock.tick(60)

    return score  # возвращаем результат при завершении игры


def show_game_over_screen(score):
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    font_large = pygame.font.SysFont(None, 48)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Нажмите R чтобы играть заново
                    return True
                elif event.key == pygame.K_q:  # Q чтобы выйти из игры полностью
                    return False

        screen.fill((200, 200, 200))

        text1 = font_large.render("Игра окончена", True, (0, 0, 0))
        text2 = font.render(f"Очки: {score}", True, (0, 0, 0))
        text3 = font.render("Нажмите R чтобы играть заново", True, (0, 0, 0))
        text4 = font.render("Нажмите Q чтобы выйти", True, (0, 0, 0))

        screen.blit(text1, (WIDTH // 2 - text1.get_width() // 2, HEIGHT // 3))
        screen.blit(text2, (WIDTH // 2 - text2.get_width() // 2, HEIGHT // 3 + 50))
        screen.blit(text3, (WIDTH // 2 - text3.get_width() // 2, HEIGHT // 3 + 100))
        screen.blit(text4, (WIDTH // 2 - text4.get_width() // 2, HEIGHT // 3 + 150))

        pygame.display.flip()


# Основной цикл запуска игр и меню повторного запуска
while True:
    final_score = game_loop()
    play_again = show_game_over_screen(final_score)
    if not play_again:
        break

pygame.quit()
sys.exit()
import pygame
import sys
import random
import time

pygame.init()

# Загрузка изображений (замените пути на свои)
player_image = pygame.image.load(r'C:\Users\ULTRA\Documents\GitHub\ne_esh_kakashki\cute.png')
desired_width = 100
desired_height = 100
player_image = pygame.transform.scale(player_image, (desired_width, desired_height))
player_rect = player_image.get_rect()

shield_image = pygame.image.load(r'C:\Users\ULTRA\Documents\GitHub\ne_esh_kakashki\shield.png')
shield_image = pygame.transform.scale(shield_image, (50, 50))
bonus_image = pygame.image.load(r'C:\Users\ULTRA\Documents\GitHub\ne_esh_kakashki\bonus.png')
bonus_image = pygame.transform.scale(bonus_image, (50, 50))
my_object_image = pygame.image.load(r'C:\Users\ULTRA\Documents\GitHub\ne_esh_kakashki\kaka.png')
desired_width_obj, desired_height_obj = 50, 50
my_object_image = pygame.transform.scale(my_object_image, (desired_width_obj, desired_height_obj))

WIDTH, HEIGHT = 600, 800

font = pygame.font.SysFont(None, 36)


def game_loop():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Не ешь какашки котик")
    clock = pygame.time.Clock()

    player_x = WIDTH // 2 - player_rect.width // 2
    player_y = HEIGHT - player_rect.height - 10

    speed = 5

    obstacles = []

    ADD_OBSTACLE_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(ADD_OBSTACLE_EVENT, 1500)

    score = 0

    # Эффекты щита и бонуса
    shield_active = False
    shield_end_time = 0

    bonus_active = False
    bonus_end_time = 0

    game_over = False

    while not game_over:
        current_time = int(time.time())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == ADD_OBSTACLE_EVENT:
                obstacle_type = random.choice(['normal', 'shield', 'bonus'])
                obstacle_width = random.randint(30, 70)
                obstacle_height = random.randint(30, 70)
                obstacle_x = random.randint(0, WIDTH - obstacle_width)
                obstacle_y = -obstacle_height
                rect = pygame.Rect(obstacle_x, obstacle_y, obstacle_width, obstacle_height)
                if obstacle_type == 'normal':
                    obstacles.append({'rect': rect, 'type': 'normal', 'image': my_object_image})
                elif obstacle_type == 'shield':
                    obstacles.append({'rect': rect, 'type': 'shield', 'image': shield_image})
                elif obstacle_type == 'bonus':
                    obstacles.append({'rect': rect, 'type': 'bonus', 'image': bonus_image})

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= speed
        if keys[pygame.K_RIGHT]:
            player_x += speed
        if keys[pygame.K_UP]:
            player_y -= speed
        if keys[pygame.K_DOWN]:
            player_y += speed

        # Ограничение внутри окна
        if player_x < 0:
            player_x = 0
        elif player_x + player_rect.width > WIDTH:
            player_x = WIDTH - player_rect.width

        if player_y < 0:
            player_y = 0
        elif player_y + player_rect.height > HEIGHT:
            player_y = HEIGHT - player_rect.height

        # Обновление препятствий и проверка столкновений
        for obstacle in obstacles[:]:
            obstacle['rect'].y += random.randint(3, 7)

            # Проверка столкновения с игроком с учетом щита
            player_rect_moved = pygame.Rect(player_x, player_y, player_rect.width, player_rect.height)
            if obstacle['rect'].colliderect(player_rect_moved):
                if obstacle['type'] == 'normal':
                    if shield_active:
                        obstacles.remove(obstacle)
                    else:
                        game_over = True
                elif obstacle['type'] == 'shield':
                    shield_active = True
                    shield_end_time = current_time + 5
                    obstacles.remove(obstacle)
                elif obstacle['type'] == 'bonus':
                    bonus_active = True
                    bonus_end_time = current_time + 5
                    score += 10
                    obstacles.remove(obstacle)

            # Удаляем за нижней границей и увеличиваем счет за прохождение мимо них
            if obstacle['rect'].y > HEIGHT:
                obstacles.remove(obstacle)
                score += 1

        # Проверка истечения времени эффектов и их отключение
        if shield_active and current_time >= shield_end_time:
            shield_active = False

        if bonus_active and current_time >= bonus_end_time:
            bonus_active = False

        # Отрисовка сцены
        screen.fill((255, 255, 255))
        screen.blit(player_image, (player_x, player_y))
        for obstacle in obstacles:
            screen.blit(obstacle['image'], (obstacle['rect'].x, int(obstacle['rect'].y)))

        # Отображение очков и статуса щита/бонуса (по желанию)
        score_text = font.render(f"Очки: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        if shield_active:
            shield_text = font.render("Щит активен!", True, (0, 128, 0))
            screen.blit(shield_text, (10, 50))

        if bonus_active:
            bonus_text = font.render("Бонус активен!", True, (128, 0, 128))
            screen.blit(bonus_text, (10, 80))

        pygame.display.flip()
        clock.tick(60)

    return score  # возвращаем результат при завершении игры


def show_game_over_screen(score):
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    font_large = pygame.font.SysFont(None, 48)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Нажмите R чтобы играть заново
                    return True
                elif event.key == pygame.K_q:  # Q чтобы выйти из игры полностью
                    return False

        screen.fill((200, 200, 200))

        text1 = font_large.render("Игра окончена", True, (0, 0, 0))
        text2 = font.render(f"Очки: {score}", True, (0, 0, 0))
        text3 = font.render("Нажмите R чтобы играть заново", True, (0, 0, 0))
        text4 = font.render("Нажмите Q чтобы выйти", True, (0, 0, 0))

        screen.blit(text1, (WIDTH // 2 - text1.get_width() // 2, HEIGHT // 3))
        screen.blit(text2, (WIDTH // 2 - text2.get_width() // 2, HEIGHT // 3 + 50))
        screen.blit(text3, (WIDTH // 2 - text3.get_width() // 2, HEIGHT // 3 + 100))
        screen.blit(text4, (WIDTH // 2 - text4.get_width() // 2, HEIGHT // 3 + 150))

        pygame.display.flip()


# Основной цикл запуска игр и меню повторного запуска
while True:
    final_score = game_loop()
    play_again = show_game_over_screen(final_score)
    if not play_again:
        break

pygame.quit()
sys.exit()
