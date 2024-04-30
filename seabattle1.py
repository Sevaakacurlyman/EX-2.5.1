class BoardOutException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

class AlreadyShot(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

class Dot():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

class Ship:
    def __init__(self, length, nose_dot, direction, lives):
        self.length = length
        self.nose_dot = nose_dot
        self.direction = direction
        self. lives = lives

    def dots(self):
        dots = []
        if self.direction == "горизонтальное":
            for i in range(self.length):
                dots.append(Dot(self.nose_dot[0] + i, self.nose_dot[1]))
        elif self.direction == "вертикальное":
            for i in range(self.length):
                dots.append(Dot(self.nose_dot[0], self.nose_dot[1] + i))
        return dots


class Board:
    def __init__(self, hid=False, ships=[]):
        self.hid = hid
        self.ships = ships
        self.board = [['O' for _ in range(6)] for _ in range(6)]
        self.alive_ships = len(ships)

    def add_ship(self, ship):
        for dot in ship.dots():
            if self.out(dot):
                raise BoardOutException("Корабль выходит за пределы доски!")
            if self.board[dot.x][dot.y] != 'O':
                raise Exception("На этом месте уже есть корабль!")
            self.board[dot.x][dot.y] = '■'
        self.ships.append(ship)

    def contour(self, ship):
        for dot in ship.dots():
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    cur = Dot(dot.x + dx, dot.y + dy)
                    if not (dx == 0 and dy == 0) and not self.out(cur):
                        if self.board[cur.x][cur.y] != '■':
                            self.board[cur.x][cur.y] = '.'

    def out(self, dot):
        return not ((0 <= dot.x < 6) and (0 <= dot.y < 6))

    def shot(self, dot):
        if self.out(dot):
            raise BoardOutException("Выстрел за пределами игрового поля!")
        if self.board[dot.x][dot.y] in ['.', 'T']:
            raise Exception("Вы уже стреляли сюда!")

        for ship in self.ships:
            if dot in ship.dots():
                ship.lives -= 1
                self.board[dot.x][dot.y] = 'X'
                if ship.lives == 0:
                    self.alive_ships -= 1
                    self.contour(ship)
                    print("Корабль уничтожен!")
                    return False
                else:
                    print("Корабль подбит!")
                    return True

        self.board[dot.x][dot.y] = 'T'
        print("Промах!")
        return False

    def print_board(self):
        for i in self.board:
            print('|'.join(i))


class Player:
    def __init__(self,my_board, enemy_board):
        self.my_board = my_board
        self.enemy_board = enemy_board
    def ask(self):
        pass

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy_board.shot(target)
                return repeat
            except BoardOutException as e:
                print(e)
            except AlreadyShot as e:
                print(e)


import random

class AI(Player):
    def ask(self):
        dot = Dot(random.randint(0,6), random.randint(0,6))
        print(f'AI shot at {dot.x}, {dot.y}')
        return dot

class User (Player):
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()
            if len(cords) != 2:
                print("Нужно ввести 2 координаты!")
                continue

            x,y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                    print ("Введите числа!")
                    continue

            x, y = int(x) , int(y)

            return Dot(x,y)

class Game:
    def __init__(self):
        player = self.random_board()
        comp = self.random_board()
        comp.hid = True

        self.ai = AI (comp, player)
        self.user = User (player, comp)

    def random_board(self):
        board = Board ()
        lengths = [1,2,3,4]
        for length in lengths:
            while True:
                x = random.randint(0, 6)
                y = random.randint(0, 6)
                direction = random.choice(["горизонтальное","вертикальное"])
                ship = Ship (Dot(x,y), length, direction, length)
                try:
                    board.add_ship(ship)
                    break
                except BoardOutException:
                    continue

        return board


    def greet(self):
        print("Добро пожаловать в игру 'Морской бой в консоли!!!'")
        print("----------------------------------------------------")
        print("Формат ввода: 'x y' ")
        print(', где "x" - номер строки')
        print(', а "y" - номер столбца')
        print("----------------------------------------------------")
        print("Желаем приятной игры!")

    def loop(self):
        num = 0
        while True:
            print("-" * 20)
            print("Доска пользователя:")
            print(self.user.board)
            print("-" * 20)
            print("Доска компьютера:")
            print(self.ai.board)
            if num % 2 == 0:
                print("Ход пользователя!")
                repeat = self.user.move()
            else:
                print("Ход компьютера!")
                repeat = self.ai.move()
            if repeat:
                num -= 1
            if self.ai.board.count == 0:
                print("-" * 20)
                print("Пользователь выиграл!")
                break
            if self.user.board.count == 0:
                print("-" * 20)
                print("Компьютер выиграл!")
                break
            num += 1

    def start (self):
        self.greet()
        self.loop()

g = Game()
g.start()
