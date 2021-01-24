import random, image, time, lcd, array, utime
from collections import namedtuple

lcd.init()

Point = namedtuple('Point', ['x', 'y'])

DELAY = 0.05
BLOCK_SIZE = 15

COLOR_APPLE = (255, 0, 0)
COLOR_SNAKE = (0, 255, 0)
COLOR_BACKGROUND = (0, 0, 0)

class Game:
    def __init__(self, w, h):
        self.w = w // BLOCK_SIZE
        self.h = h // BLOCK_SIZE
        self.img = image.Image()
        self.reset()


    def reset(self):
        self.score = 0
        self.direction = 0
        self.head = Point(self.w // 2, self.h // 2)
        self.snake = [self.head, Point(self.head.x - 1, self.head.y), Point(self.head.x - 2, self.head.y)]
        self.apple = self.place_apple()
        # initial drawing
        self.img.clear()
        self.draw_dot(self.apple, COLOR_APPLE)
        for pt in self.snake:
            self.draw_dot(pt, COLOR_SNAKE)
        lcd.display(self.img)


    def place_apple(self):
        while True:
            x = random.randint(0, self.w - 1)
            y = random.randint(0, self.h - 1)
            if not Point(x, y) in self.snake:
                return Point(x, y)


    def play(self):
        # choose random turn for now
        turn = random.randint(-1, 1)
        self.direction = (self.direction + turn) % 4

        # move head
        x = self.head.x
        y = self.head.y
        if self.direction == 0:
            x += 1
        elif self.direction == 1:
            y += 1
        elif self.direction == 2:
            x -= 1
        elif self.direction == 3:
            y -= 1
        self.head = Point(x, y)

        # check walls and self
        if self.head.x < 0 or self.head.x >= self.w or self.head.y < 0 or self.head.y >= self.h:
            return True, self.score
        elif self.head in self.snake:
            return True, self.score

        self.snake.insert(0, self.head)
        self.draw_dot(self.head, COLOR_SNAKE)
        if self.head == self.apple:
            self.score += 1
            self.apple = self.place_apple()
            self.draw_dot(self.apple, COLOR_APPLE)
        else:
            lost_tail = self.snake.pop()
            self.draw_dot(lost_tail, COLOR_BACKGROUND)

        lcd.display(self.img)
        return False, self.score


    def draw_dot(self, point, color):
        self.img.draw_circle((point.x * BLOCK_SIZE) + (BLOCK_SIZE // 2), (point.y * BLOCK_SIZE) + (BLOCK_SIZE // 2), BLOCK_SIZE // 2, color, fill=True)


game = Game(lcd.width(), lcd.height())
while True:
    while True:
        utime.sleep(DELAY)
        game_over, score = game.play()
        if game_over:
            break;
    lcd.clear()
    lcd.draw_string(lcd.width() // 4, lcd.height() // 2, "GAME OVER", lcd.RED, lcd.BLACK)
    lcd.draw_string(lcd.width() // 4, lcd.height() * 2 // 3, "Score: {}".format(score), lcd.RED, lcd.BLACK)
    utime.sleep(1)
    game.reset()
