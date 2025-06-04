import pygame
import random
import asyncio
import platform
import time

# Инициализация Pygame
pygame.init()
pygame.mixer.init()

# Настройки окна
WIDTH, HEIGHT = 1000, 700
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Игра Виселица - Средневековье")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
GRAY = (200, 200, 200)
BROWN = (139, 69, 19)
DARK_BROWN = (90, 45, 10)
ROPE_COLOR = (210, 180, 140)
SKIN_COLOR = (225, 180, 170)
CLOTH_COLOR = (100, 80, 60)

# Шрифты
FONT_LARGE = pygame.font.SysFont("Times New Roman", 64, italic=True)
FONT_MEDIUM = pygame.font.SysFont("Times New Roman", 48, italic=True)
FONT_SMALL = pygame.font.SysFont("Times New Roman", 32, italic=True)
FONT_BUTTON = pygame.font.SysFont("Times New Roman", 36, italic=True)

# Загрузка звуков
RIGHT_SOUND = pygame.mixer.Sound("assets/right.mp3")
WRONG_SOUND = pygame.mixer.Sound("assets/wrong.mp3")
WIN_SOUND = pygame.mixer.Sound("assets/win.mp3")
LOSE_SOUND = pygame.mixer.Sound("assets/loss.mp3")
MENU_MUSIC = pygame.mixer.Sound("assets/menu_music.mp3")
GAME_MUSIC = pygame.mixer.Sound("assets/game_music.mp3")
BUTTON_HOVER = pygame.mixer.Sound("assets/button_hover.mp3")
BEFORE_WINNING = pygame.mixer.Sound("assets/before_winning.mp3")

# Загрузка фоновых изображений
MENU_BACKGROUND = pygame.image.load("assets/menu.jpg")
MENU_BACKGROUND = pygame.transform.scale(MENU_BACKGROUND, (WIDTH, HEIGHT))
GAME_BACKGROUND = pygame.image.load("assets/game.jpg")
GAME_BACKGROUND = pygame.transform.scale(GAME_BACKGROUND, (WIDTH, HEIGHT))

# Слова по уровням сложности
EASY_WORDS = ["рыцарь", "щит", "конь", "меч", "знамя", "стрела", "лук"]
MEDIUM_WORDS = ["крепость", "дракон", "катапульта", "арбалет", "пламя", "оборона", "осада"]
HARD_WORDS = ["инквизитор", "фортификация", "язычество", "заклинание", "стратегия"]

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y + 20, width, height)
        self.text = text
        self.color = WHITE
        self.disabled = False
        self.hovered = False

    def draw(self, screen):
        text_surf = FONT_BUTTON.render(self.text, True, self.color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

        if self.disabled:
            pygame.draw.line(screen, RED, (text_rect.topleft[0], text_rect.topleft[1]),
                             (text_rect.bottomright[0], text_rect.bottomright[1]), 2)
            pygame.draw.line(screen, RED, (text_rect.topright[0], text_rect.topright[1]),
                             (text_rect.bottomleft[0], text_rect.bottomleft[1]), 2)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos) and not self.disabled

    def hover(self, pos):
        if not self.disabled:
            if self.rect.collidepoint(pos) and not self.hovered:
                self.hovered = True
                BUTTON_HOVER.play()
            elif not self.rect.collidepoint(pos):
                self.hovered = False
            self.color = WHITE

class HangmanGame:
    def __init__(self):
        self.state = "menu"
        self.word = ""
        self.guessed_letters = set()
        self.attempts_left = 6
        self.high_scores = []
        self.player_name = ""

        self.difficulty = None
        self.start_time = 0
        self.time_limit = 0

        self.buttons = {
            "menu": [
                Button(WIDTH // 2 - 150, HEIGHT // 2 - 150, 300, 60, "Начать игру"),
                Button(WIDTH // 2 - 150, HEIGHT // 2 - 50, 300, 60, "Таблица рекордов"),
                Button(WIDTH // 2 - 150, HEIGHT // 2 + 50, 300, 60, "Справка"),
                Button(WIDTH // 2 - 150, HEIGHT // 2 + 150, 300, 60, "Выход"),
            ],
            "difficulty": [
                Button(WIDTH // 2 - 150, HEIGHT // 2 - 100, 300, 60, "Лёгкий"),
                Button(WIDTH // 2 - 150, HEIGHT // 2, 300, 60, "Средний"),
                Button(WIDTH // 2 - 150, HEIGHT // 2 + 100, 300, 60, "Сложный"),
                Button(WIDTH // 2 - 150, HEIGHT // 2 + 200, 300, 60, "Назад")
            ],
            "game": [],
            "end": [],
            "help": [Button(WIDTH // 2 - 150, HEIGHT - 100, 300, 60, "Назад")],
            "high_scores": [Button(WIDTH // 2 - 150, HEIGHT - 100, 300, 60, "Назад")],
            "new_high_score": [Button(WIDTH // 2 - 150, HEIGHT // 2 + 100, 300, 60, "Сохранить")]
        }

        self.keyboard_layout = [
            ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к'],
            ['л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х'],
            ['ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']
        ]

        self.button_width, self.button_height = 50, 50
        self.button_spacing = 10
        self.keyboard_start_x = 100
        self.keyboard_start_y = 100

        MENU_MUSIC.play(-1)

    def start_new_game(self):
        pygame.mixer.stop()
        GAME_MUSIC.play(-1)

        if self.difficulty == "easy":
            self.word = random.choice(EASY_WORDS)
            self.time_limit = 180  # 3 минуты
        elif self.difficulty == "medium":
            self.word = random.choice(MEDIUM_WORDS)
            self.time_limit = 120  # 2 минуты
        else:
            self.word = random.choice(HARD_WORDS)
            self.time_limit = 60   # 1 минута

        self.guessed_letters.clear()
        self.attempts_left = 6
        self.start_time = time.time()
        self.state = "game"

        self.buttons["game"] = []
        for row_idx, row in enumerate(self.keyboard_layout):
            for col_idx, letter in enumerate(row):
                x = self.keyboard_start_x + col_idx * (self.button_width + self.button_spacing)
                y = self.keyboard_start_y + row_idx * (self.button_height + self.button_spacing)
                self.buttons["game"].append(Button(x, y, self.button_width, self.button_height, letter))

        self.restart_button = Button(WIDTH - 200, HEIGHT - 145, 150, 50, "Заново")
        self.exit_button = Button(WIDTH - 200, HEIGHT - 95, 150, 50, "Выход")
        self.buttons["game"].extend([self.restart_button, self.exit_button])

        self.buttons["end"] = [
            Button(WIDTH // 2 - 150, HEIGHT - 350, 150, 50, "Заново"),
            Button(WIDTH // 2 + 10, HEIGHT - 350, 150, 50, "Выход")
        ]

    def draw_word(self):
        elapsed_time = int(time.time() - self.start_time)
        remaining_time = max(0, self.time_limit - elapsed_time)
        minutes = remaining_time // 60
        seconds = remaining_time % 60
        time_text = f"Время: {minutes:02d}:{seconds:02d}"
        time_surface = FONT_MEDIUM.render(time_text, True, WHITE)
        SCREEN.blit(time_surface, (WIDTH - 300, 20))

        if self.state != "game":
            return

        x = 100
        y = HEIGHT - 400
        for letter in self.word:
            txt = FONT_LARGE.render(letter if letter in self.guessed_letters else "_", True, WHITE)
            SCREEN.blit(txt, (x, y))
            x += txt.get_width() + 10

        if remaining_time <= 0 and not self.check_win():
            self.state = "end"
            self.attempts_left = 0
            pygame.mixer.stop()
            LOSE_SOUND.play()

    def draw_hangman(self):
        stages = 6 - self.attempts_left
        base_x, base_y = WIDTH - 600, HEIGHT - 250
        human_x, human_y = base_x + 100, base_y + 180

        CLOTH_COLOR = (139, 0, 0)

        if stages >= 1:
            pygame.draw.rect(SCREEN, BROWN, (base_x, base_y + 200, 300, 20))
            for i in range(base_x, base_x + 300, 10):
                pygame.draw.line(SCREEN, DARK_BROWN, (i, base_y + 200), (i + 5, base_y + 220), 2)

        if stages >= 2:
            pygame.draw.rect(SCREEN, BROWN, (base_x + 90, base_y, 20, 200))
            for i in range(base_y, base_y + 200, 15):
                pygame.draw.line(SCREEN, DARK_BROWN, (base_x + 90, i), (base_x + 110, i + 5), 1)
            pygame.draw.line(SCREEN, BROWN, (base_x + 50, base_y + 200), (base_x + 90, base_y + 100), 10)
            pygame.draw.line(SCREEN, DARK_BROWN, (base_x + 50, base_y + 200), (base_x + 90, base_y + 100), 2)

        if stages >= 3:
            pygame.draw.rect(SCREEN, BROWN, (base_x + 90, base_y, 120, 20))
            for i in range(base_x + 90, base_x + 210, 10):
                pygame.draw.line(SCREEN, DARK_BROWN, (i, base_y), (i + 5, base_y + 20), 1)
            pygame.draw.rect(SCREEN, BROWN, (base_x + 190, base_y - 20, 20, 40))

        if stages >= 4:
            offset_x = 98
            offset_y = -20
            human_x_offset = human_x + offset_x
            human_y_offset = human_y + offset_y
            rope_top_x = base_x + 200
            rope_top_y = base_y
            pygame.draw.line(SCREEN, ROPE_COLOR, (rope_top_x, rope_top_y), (human_x + 98, human_y - 80), 5)

        if stages == 5:
            stool_x = base_x + 170
            stool_y = base_y + 168
            pygame.draw.rect(SCREEN, DARK_BROWN, (stool_x, stool_y, 60, 10))
            pygame.draw.rect(SCREEN, BROWN, (stool_x + 10, stool_y + 10, 10, 22))
            pygame.draw.rect(SCREEN, BROWN, (stool_x + 40, stool_y + 10, 10, 22))

            human_x_offset = human_x + 98
            human_y_offset = human_y - 20

            pygame.draw.circle(SCREEN, SKIN_COLOR, (human_x_offset, human_y_offset - 110), 15)
            pygame.draw.circle(SCREEN, BLACK, (human_x_offset - 5, human_y_offset - 115), 2)
            pygame.draw.circle(SCREEN, BLACK, (human_x_offset + 5, human_y_offset - 115), 2)
            pygame.draw.line(SCREEN, BLACK, (human_x_offset - 5, human_y_offset - 105),
                             (human_x_offset + 5, human_y_offset - 105), 2)

            pygame.draw.rect(SCREEN, CLOTH_COLOR, (human_x_offset - 15, human_y_offset - 95, 30, 60))
            pygame.draw.line(SCREEN, BLACK, (human_x_offset, human_y_offset - 95),
                             (human_x_offset, human_y_offset - 35), 3)

            pygame.draw.line(SCREEN, CLOTH_COLOR, (human_x_offset - 15, human_y_offset - 85),
                             (human_x_offset - 40, human_y_offset - 55), 8)
            pygame.draw.line(SCREEN, CLOTH_COLOR, (human_x_offset + 12, human_y_offset - 85),
                             (human_x_offset + 40, human_y_offset - 55), 8)

            pygame.draw.line(SCREEN, SKIN_COLOR, (human_x_offset - 40, human_y_offset - 55),
                             (human_x_offset - 45, human_y_offset - 50), 3)
            pygame.draw.line(SCREEN, SKIN_COLOR, (human_x_offset + 40, human_y_offset - 55),
                             (human_x_offset + 45, human_y_offset - 50), 3)

            pygame.draw.line(SCREEN, CLOTH_COLOR, (human_x_offset - 10, human_y_offset - 35),
                             (human_x_offset - 15, human_y_offset + 5), 6)
            pygame.draw.line(SCREEN, CLOTH_COLOR, (human_x_offset + 10, human_y_offset - 35),
                             (human_x_offset + 15, human_y_offset + 5), 6)
            pygame.draw.line(SCREEN, SKIN_COLOR, (human_x_offset - 10, human_y_offset + 5),
                             (human_x_offset - 20, human_y_offset + 10), 3)
            pygame.draw.line(SCREEN, SKIN_COLOR, (human_x_offset + 10, human_y_offset + 5),
                             (human_x_offset + 20, human_y_offset + 10), 3)

            pygame.draw.line(SCREEN, ROPE_COLOR, (human_x_offset - 5, human_y_offset - 95),
                             (human_x_offset + 5, human_y_offset - 95), 3)

        if stages >= 6:
            human_x_offset = human_x + 98
            human_y_offset = human_y - 20

            pygame.draw.circle(SCREEN, SKIN_COLOR, (human_x_offset, human_y_offset - 110), 15)
            pygame.draw.circle(SCREEN, BLACK, (human_x_offset - 5, human_y_offset - 115), 2)
            pygame.draw.circle(SCREEN, BLACK, (human_x_offset + 5, human_y_offset - 115), 2)
            pygame.draw.line(SCREEN, BLACK, (human_x_offset - 5, human_y_offset - 105),
                             (human_x_offset + 5, human_y_offset - 105), 2)

            pygame.draw.rect(SCREEN, CLOTH_COLOR, (human_x_offset - 15, human_y_offset - 95, 30, 60))
            pygame.draw.line(SCREEN, BLACK, (human_x_offset, human_y_offset - 95),
                             (human_x_offset, human_y_offset - 35), 3)

            pygame.draw.line(SCREEN, CLOTH_COLOR, (human_x_offset - 15, human_y_offset - 85),
                             (human_x_offset - 40, human_y_offset - 55), 8)
            pygame.draw.line(SCREEN, CLOTH_COLOR, (human_x_offset + 12, human_y_offset - 85),
                             (human_x_offset + 40, human_y_offset - 55), 8)

            pygame.draw.line(SCREEN, SKIN_COLOR, (human_x_offset - 40, human_y_offset - 55),
                             (human_x_offset - 45, human_y_offset - 50), 3)
            pygame.draw.line(SCREEN, SKIN_COLOR, (human_x_offset + 40, human_y_offset - 55),
                             (human_x_offset + 45, human_y_offset - 50), 3)

            pygame.draw.line(SCREEN, CLOTH_COLOR, (human_x_offset - 10, human_y_offset - 35),
                             (human_x_offset - 15, human_y_offset + 5), 6)
            pygame.draw.line(SCREEN, CLOTH_COLOR, (human_x_offset + 10, human_y_offset - 35),
                             (human_x_offset + 15, human_y_offset + 5), 6)
            pygame.draw.line(SCREEN, SKIN_COLOR, (human_x_offset - 10, human_y_offset + 5),
                             (human_x_offset - 20, human_y_offset + 10), 3)
            pygame.draw.line(SCREEN, SKIN_COLOR, (human_x_offset + 10, human_y_offset + 5),
                             (human_x_offset + 20, human_y_offset + 10), 3)

            pygame.draw.line(SCREEN, ROPE_COLOR, (human_x_offset - 5, human_y_offset - 95),
                             (human_x_offset + 5, human_y_offset - 95), 3)

    def check_win(self):
        return all(letter in self.guessed_letters for letter in self.word)

    def check_lose(self):
        return self.attempts_left <= 0 or time.time() - self.start_time > self.time_limit

    def update_loop(self):
        pos = pygame.mouse.get_pos()
        clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked = True
            if self.state == "new_high_score" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.player_name = self.player_name[:-1]
                elif event.key == pygame.K_RETURN:
                    if self.player_name:
                        self.high_scores.append((self.player_name, self.attempts_left))
                        self.high_scores.sort(key=lambda x: x[1], reverse=True)
                        if len(self.high_scores) > 10:
                            self.high_scores = self.high_scores[:10]
                        self.player_name = ""
                        self.state = "menu"
                elif len(self.player_name) < 10:
                    self.player_name += event.unicode

        if self.state in ["menu", "help", "high_scores", "new_high_score"]:
            SCREEN.blit(MENU_BACKGROUND, (0, 0))
        else:
            SCREEN.blit(GAME_BACKGROUND, (0, 0))

        if self.state == "menu":
            for btn in self.buttons["menu"]:
                btn.hover(pos)
                if clicked and btn.is_clicked(pos):
                    if btn.text == "Начать игру":
                        self.state = "difficulty"
                    elif btn.text == "Таблица рекордов":
                        self.state = "high_scores"
                    elif btn.text == "Справка":
                        self.state = "help"
                    elif btn.text == "Выход":
                        self.running = False
                btn.draw(SCREEN)

        elif self.state == "difficulty":
            for btn in self.buttons["difficulty"]:
                btn.hover(pos)
                if clicked and btn.is_clicked(pos):
                    if btn.text == "Лёгкий":
                        self.difficulty = "easy"
                        self.start_new_game()
                    elif btn.text == "Средний":
                        self.difficulty = "medium"
                        self.start_new_game()
                    elif btn.text == "Сложный":
                        self.difficulty = "hard"
                        self.start_new_game()
                    elif btn.text == "Назад":
                        self.state = "menu"
                btn.draw(SCREEN)

        elif self.state == "game":
            self.draw_word()
            self.draw_hangman()
            for btn in self.buttons["game"]:
                btn.hover(pos)
                if clicked and btn.is_clicked(pos):
                    if btn.text == "Заново":
                        self.start_new_game()
                        return
                    elif btn.text == "Выход":
                        self.state = "menu"
                        pygame.mixer.stop()
                        MENU_MUSIC.play(-1)
                        return
                    elif btn.text not in self.guessed_letters:
                        self.guessed_letters.add(btn.text)
                        btn.disabled = True
                        if btn.text not in self.word:
                            self.attempts_left -= 1
                            WRONG_SOUND.play()
                        else:
                            RIGHT_SOUND.play()
                            remaining_letters = set(self.word) - self.guessed_letters
                            if len(remaining_letters) == 1:
                                BEFORE_WINNING.play()
                        if self.check_win() or self.check_lose():
                            pygame.mixer.stop()
                            if self.check_win():
                                WIN_SOUND.play()
                            else:
                                LOSE_SOUND.play()
                            if self.check_win() and (not self.high_scores or self.attempts_left > self.high_scores[0][1]):
                                self.state = "new_high_score"
                            else:
                                self.state = "end"
                btn.draw(SCREEN)

        elif self.state == "end":
            self.draw_hangman()
            result_text = "Победа!" if self.check_win() else "Вы повешены!"
            result_surface = FONT_LARGE.render(result_text, True, RED)
            SCREEN.blit(result_surface, (WIDTH // 2 - result_surface.get_width() // 2, HEIGHT - 450))
            for btn in self.buttons["end"]:
                btn.hover(pos)
                if clicked and btn.is_clicked(pos):
                    if btn.text == "Заново":
                        self.start_new_game()
                    elif btn.text == "Выход":
                        self.state = "menu"
                        pygame.mixer.stop()
                        MENU_MUSIC.play(-1)
                btn.draw(SCREEN)

        elif self.state == "help":
            rules = [
                "Правила игры Виселица:",
                "1. Выберите подходящий уровень сложности.",
                "2. Угадайте слово, выбирая буквы.",
                "3. У вас есть 6 попыток угадать слово.",
                "4. Все слова связаны со Средневековьем.",
                "5. На каждом уровне сложности свой таймер.",
                "6. Если угадаете, ваш результат попадёт в таблицу рекордов!"
            ]
            for i, line in enumerate(rules):
                text_surface = FONT_SMALL.render(line, True, WHITE)
                SCREEN.blit(text_surface, (60, 60 + i * 40))
            for btn in self.buttons["help"]:
                btn.hover(pos)
                if clicked and btn.is_clicked(pos):
                    self.state = "menu"
                btn.draw(SCREEN)

        elif self.state == "high_scores":
            title = FONT_LARGE.render("Таблица рекордов", True, WHITE)
            SCREEN.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))
            for i, (name, score) in enumerate(self.high_scores):
                entry = f"{i+1}. {name}: {score} попыток осталось"
                text_surface = FONT_MEDIUM.render(entry, True, WHITE)
                SCREEN.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, 150 + i * 40))
            for btn in self.buttons["high_scores"]:
                btn.hover(pos)
                if clicked and btn.is_clicked(pos):
                    self.state = "menu"
                btn.draw(SCREEN)

        elif self.state == "new_high_score":
            congrats = FONT_LARGE.render("Новый рекорд!", True, WHITE)
            SCREEN.blit(congrats, (WIDTH // 2 - congrats.get_width() // 2, 50))
            prompt = FONT_MEDIUM.render("Введите ваше имя:", True, WHITE)
            SCREEN.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, 150))
            name_surface = FONT_MEDIUM.render(self.player_name, True, WHITE)
            SCREEN.blit(name_surface, (WIDTH // 2 - name_surface.get_width() // 2, 205))
            for btn in self.buttons["new_high_score"]:
                btn.hover(pos)
                if clicked and btn.is_clicked(pos):
                    if self.player_name:
                        self.high_scores.append((self.player_name, self.attempts_left))
                        self.high_scores.sort(key=lambda x: x[1], reverse=True)
                        if len(self.high_scores) > 10:
                            self.high_scores = self.high_scores[:10]
                        self.player_name = ""
                        self.state = "menu"
                        MENU_MUSIC.play(-1)
                btn.draw(SCREEN)

        pygame.display.flip()

    async def main(self):
        self.running = True
        while self.running:
            self.update_loop()
            await asyncio.sleep(1.0 / 60)

if platform.system() == "Emscripten":
    game = HangmanGame()
    asyncio.ensure_future(game.main())
else:
    if __name__ == "__main__":
        game = HangmanGame()
        asyncio.run(game.main())