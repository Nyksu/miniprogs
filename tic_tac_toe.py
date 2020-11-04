# tic tac toe game
# игра в крестики и нолики

from functools import reduce

class gamecell:
    def __init__(self, index):
        self._state = ' '
        self._index = index

    @property
    def index(self):
        return self._index
    
    @property
    def state(self):
        return self._state
    
    @state.setter
    def state(self, state):
        if self._state == ' ':
            self._state = state if state in ('X', 'O') else ' '
    
    def clear(self):
        self._state = ' '

    def __str__(self):
        return self._state

class tictactoeField:
    def __init__(self):
        self.cells = [[gamecell(j + k + 2*j) for k in range(3)] for j in range(3)]
        self.plaindict = {c.index:c for c in sum([list(a) for a in self.cells],[])}
    
    def setstate(self, cellindex, state):
        self.plaindict[cellindex].state = state

    def getstate(self, cellindex):
        return self.plaindict[cellindex].state

    def isWinLine(self, line_cell):
        if len(line_cell) > 1 :
            r = self.plaindict[line_cell[0]].state
            if r != ' ':
                return reduce(lambda s, c: s and self.plaindict[c].state == r , line_cell, True)

    def checkWin(self):
        tests = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), 
                (3, 5, 8), (0, 4, 8), (2, 4, 6))
        for t in tests:
            if self.isWinLine(t):
                return t

    def __str__(self):
        res = '-' * 5 + '\n'
        for s in self.cells:
            res += '|'.join(map(lambda c: str(c) if c.state != ' ' else str(c.index), s)) + '\n' + '-' * 5 + '\n'
        return res


comand = ""
stepindex = 0
signs = ['X', 'O']
gameField = tictactoeField()
print('Игра крестики-нолики. \n')

while True:
    print(gameField)
    comand = input(f"Ваш ({signs[stepindex % 2]}) ход! (номер ячейки от 0 до 8): ").strip()
    if comand in ['q', 'Q', 'exit', 'quit', 'e', 'E']:
        print('Вы вышли из игры. До свидания!')
        break
    elif comand in ['c', 'C', 'clear']:
        for _, c in gameField.plaindict.items():
            c.clear()
        print('Игра обнулилась! Начнём сначала!')
        stepindex = 0
        continue
    elif comand and comand[0].isdigit():
        cellnum = int(comand[0])
        if cellnum < 9:
            if gameField.getstate(cellnum) == ' ':
                gameField.setstate(cellnum, signs[stepindex % 2])
                stepindex += 1
                #проверка на выйгрыш
                test = gameField.checkWin()
                if test:
                    print('*' * 40)
                    print(f'Выйграл игрок {signs[stepindex % 2]}! Линия {test} заполнена!')
                    print('*' * 40)
                    for _, c in gameField.plaindict.items():
                        c.clear()
                    print('\n Игра обнулилась! Начнём сначала!')
                    stepindex = 0
                continue
            else:
                print(f'Неверный выбор! Ячейка {cellnum} занята!')
                continue
        else:
            print(f'Неверный выбор! Ячейки {cellnum} не существует!')
            continue
    else:
        print(f'Не распознанная команда: {comand}!')


