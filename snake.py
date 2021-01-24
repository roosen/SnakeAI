import random, image, time, lcd, array, utime, math
from collections import namedtuple


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
        self.vision()
        lcd.display(self.img)


    def place_apple(self):
        while True:
            x = random.randint(0, self.w - 1)
            y = random.randint(0, self.h - 1)
            if not Point(x, y) in self.snake:
                return Point(x, y)


    def play(self, action):
        self.direction = (self.direction + action) % 4

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

        self.vision()
        lcd.display(self.img)
        return False, self.score


    def draw_dot(self, point, color):
        self.img.draw_circle((point.x * BLOCK_SIZE) + (BLOCK_SIZE // 2), (point.y * BLOCK_SIZE) + (BLOCK_SIZE // 2), BLOCK_SIZE // 2, color, fill=True)


    def vision(self):
        # look left, front, right and determine the distance to the first obstacle
        x_same_y = [s.x for s in self.snake if s.y == self.head.y]
        x_same_y.sort()
        x_same_y.insert(0, -1)
        x_same_y.append(self.w)
        i_head_x = x_same_y.index(self.head.x)
        dx_l = self.head.x - x_same_y[i_head_x - 1]
        dx_r = x_same_y[i_head_x + 1] - self.head.x
        y_same_x = [s.y for s in self.snake if s.x == self.head.x]
        y_same_x.sort()
        y_same_x.insert(0, -1)
        y_same_x.append(self.h)
        i_head_y = y_same_x.index(self.head.y)
        dy_u = self.head.y - y_same_x[i_head_y - 1]
        dy_d = y_same_x[i_head_y + 1] - self.head.y
        d = [dx_r, dy_d, dx_l, dy_u]
        front = d[self.direction]
        right = d[(self.direction + 1) % 4]
        left = d[(self.direction - 1) % 4]
        # look how far the apple is
        d_apple = math.sqrt(((self.head.x - self.apple.x) ** 2) + ((self.head.y - self.apple.y) ** 2))
        self.observation = [1/left, 1/front, 1/right, 1/d_apple]


if __name__ == '__main__':
    lcd.init()
    game = Game(lcd.width(), lcd.height())

    while True:
        while True:
            utime.sleep(DELAY)
            # choose random turn for now
            action = random.randint(-1, 1)
            game_over, score = game.play(action)
            if game_over:
                break;
            print(game.observation)
        lcd.clear()
        lcd.draw_string(lcd.width() // 4, lcd.height() // 2, "GAME OVER", lcd.RED, lcd.BLACK)
        lcd.draw_string(lcd.width() // 4, lcd.height() * 2 // 3, "Score: {}".format(score), lcd.RED, lcd.BLACK)
        utime.sleep(1)
        game.reset()
