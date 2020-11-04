from tkinter import *

level_example = """
###########
#@  %%    #
#   %     #
#  %%%    #
# %%$%%   #
#  %%%    #
#   %     #
#   %     #
#   %     #
###########
"""

helplines = """
Игра Bomberman lt (NxU) 2020

Правила и инструкция к игре.
Суть игры - необходимо двигая игрока (@) собрать все монеты ($).
(%) - это мягкие стены, которые можно разрушит бомбой (*) (необходимо ее установить).
Бомба сработает на третьем ходе после установки, образовав взрывную волну (+), которая
и разрушает мягкие стены. Однако взрывная волна может и убить игрока.

Для перемещения персонажа используйте кнопки [<--],[-->],[^] и [v].
Для установки бомбы - кнопка [*]
Прямо в этом редакторе можно составить новую или изменить стандартную схему.
Что бы играть в своей схеме - нажмите кнопку [Start creating level]
"""

ElementsDict = {'@':{'fam':'player', 'passable':True, 'interactable':True},
                '#':{'fam':'wall', 'passable':False, 'interactable':False},
                '%':{'fam':'soft_wall', 'passable':False, 'interactable':True},
                '$':{'fam':'coin', 'passable':True, 'interactable':True},
                '+':{'fam':'heatwave', 'passable':True, 'interactable':True},
                '*':{'fam':'bomb', 'passable':True, 'interactable':False}}

gen_id = 0

def get_next_id():
    global gen_id
    gen_id += 1
    return gen_id

def get_coords_around(center):
    res = [center]
    x, y = center
    if x > 0:
        res.append((x-1, y))
    res.append((x+1, y))
    if y > 0:
        res.append((x, y-1))
    res.append((x, y+1))
    return res


class GameElement():
    def __init__(self, famely_char, x, y):
        self.id = get_next_id()
        self.char = famely_char
        self.coords = {'x': x, 'y': y}

    def coord_get(self):
        return (self.coords['x'], self.coords['y'])

    def famaly_name(self):
        return ElementsDict[self.famaly_name]['fam']
    
    def coord_set(self, cc):
        self.coords['x'] = cc[0]
        self.coords['y'] = cc[1]
    
    def isPassable(self):
        return ElementsDict[self.char]['passable']
        
    def isInteractable(self):
        return ElementsDict[self.char]['interactable']


class GamePlayer(GameElement):
    def __init__(self, *args):
        self.__coins = 0
        super().__init__(*args)
    
    def add_coin(self):
        self.__coins += 1
        return self.coins

    @property
    def coins(self):
        return self.__coins


class GameBomb(GameElement):
    def __init__(self, *args, power=3, life_time=3):
        self.power = power
        self.life_time = life_time
        super().__init__(*args)
    
    def isbang(self):
        if self.life_time:
            self.life_time -= 1
        return not self.life_time and self.power


class GameField():
    gameElements = []
    player = None
    power = 3
    life_time = 3
    
    @classmethod
    def get_objects_by_coords(cls, position):
        res = []
        for el in cls.gameElements:
            if el.coord_get() == position:
                res.append(el)
        return res
    
    @classmethod
    def addElement(cls, famely_char, x, y):
        pointGuest = cls.get_objects_by_coords((x, y))
        yes = True
        if pointGuest:
            yes = False
            if ElementsDict[famely_char]['passable']:
                if all([el.isPassable() for el in pointGuest]):
                    yes = True
                elif famely_char == '+' and [el for el in pointGuest if el.char == '%']:
                    yes = True
        if yes:
            obj = None
            if famely_char == '*':
                obj = GameBomb(famely_char, x, y, power=cls.power, life_time=cls.life_time)
            elif famely_char == '@':
                obj = GamePlayer(famely_char, x, y)
                cls.player = obj
            else:
                obj = GameElement(famely_char, x, y)
            if obj:
                cls.gameElements.append(obj)
    
    @classmethod
    def getNomElement(cls, el):
        res = None
        try:
            res = cls.gameElements.index(el)
        except ValueError:
            res = -1
        return res

    @classmethod
    def delElement(cls, el):
        nom = cls.getNomElement(el)
        if nom >= 0:
            cls.gameElements.pop(nom)
        del el

    @classmethod
    def delElementList(cls, elemenList):
        for el in elemenList:
            cls.delElement(el)
    
    @classmethod
    def clearElements(cls):
        cls.player = None
        while cls.gameElements:
            ob = cls.gameElements.pop() 
            del ob
    
    @classmethod
    def getMaxCoord(cls):
        xmax = max([el.coords['x'] for el in cls.gameElements])
        ymax = max([el.coords['y'] for el in cls.gameElements])
        return (xmax, ymax)

    @classmethod
    def GameMapToText(cls):
        mxy = cls.getMaxCoord()
        print('max', mxy)
        matr = []
        for x in range(mxy[1]+1):
            matr.append([' ' for y in range(mxy[0]+1)])
        for el in cls.gameElements:
            matr[el.coords['y']][el.coords['x']] = el.char
        ss = ''
        for l in matr:
            ss += ''.join(l) + '\n'
        return ss

    @classmethod
    def testGo(cls, x, y):
        result = True
        objs = cls.get_objects_by_coords((x, y))
        if objs:
            result = False
            if all([ElementsDict[el.char]['passable'] for el in objs]):
                result = True
        return result

    @classmethod
    def playerUp(cls):
        y = cls.player.coords['y']
        if y:
            if cls.testGo(cls.player.coords['x'], y - 1):
                cls.player.coords['y'] -= 1
                return True
        return False

    @classmethod
    def playerDown(cls):
        y = cls.player.coords['y']
        if cls.testGo(cls.player.coords['x'], y + 1):
            cls.player.coords['y'] += 1
            return True
        return False

    @classmethod
    def playerLeft(cls):
        x = cls.player.coords['x']
        if x:
            if cls.testGo(x - 1, cls.player.coords['y']):
                cls.player.coords['x'] -= 1
                return True
        return False

    @classmethod
    def playerRight(cls):
        x = cls.player.coords['x']
        if cls.testGo(x + 1, cls.player.coords['y']):
            cls.player.coords['x'] += 1
            return True
        return False

    @classmethod
    def iteractionCell(cls, iList):
        delbuf = []
        if len(set(['@','+']) & set([o.char for o in iList])) > 1:
            return True # Конец игре. Игрока убило.
        if len(set(['@','$']) & set([o.char for o in iList])) > 1:
            coins = [o for o in iList if o.char == '$']
            cls.player.coins += len(coins)
            delbuf.extend(coins)
        if len(set(['%','+']) & set([o.char for o in iList])) > 1:
            elems = [o for o in iList if o.char == '%' or o.char == '+']
            delbuf.extend(elems)
        cls.delElementList(delbuf)
    
    @classmethod
    def getElementsGroup(cls, fam):
        return [o for o in cls.gameElements if o.char == fam]

    @classmethod
    def iteraction(cls):
        delbuf = []
        #проверить есть ли где то еще взрывная волна
        heatwaves = cls.getElementsGroup('+')
        for hw in heatwaves:
            if cls.iteractionCell(cls.get_objects_by_coords(hw.coord_get())):
                print('Бабах!')
                cls.endGame('+')
                return None
            if hw:
                delbuf.append(hw)
        #проверить есть ли где то бомбы и не пора ли им взрываться?
        bombs = cls.getElementsGroup('*')
        for bb in bombs:
            if bb.isbang():
                delbuf.append(bb)
                for xy in get_coords_around(bb.coord_get()):
                    cls.addElement('+', xy[0], xy[1])
        #проверить остались ли где то ещё монеты? Если нет - завершить программу.
        if len(cls.getElementsGroup('$')) == 0:
            cls.endGame('$')
            print('Монет больше нет!')
        else:
            cls.delElementList(delbuf)
    
    @classmethod
    def endGame(cls, simbol):
        cls.clearElements()
        global textbox
        textbox.delete('1.0', 'end')
        if simbol == '+':
            print('Игра окончена! Вы проиграли! Взрыв бомбы вас убил!')
            textbox.insert('1.0', 'Игра окончена! Вы проиграли! Взрыв бомбы вас убил!')
        elif simbol == '$':
            print('Игра окончена! Вы победили! Собраны все монетки на уровне!')
            textbox.insert('1.0', 'Игра окончена! Вы победили! Собраны все монетки на уровне!')

    @classmethod
    def doStepGame(cls, up=0, down=0, left=0, right=0):
        if len(cls.gameElements): 
            r = 0
            if up: 
                r += cls.playerUp()
                print('пошли вверх...')
            elif down: 
                r += cls.playerDown()
                print('пошли вниз...')
            elif left: 
                r += cls.playerLeft()
                print('пошли налево...')
            elif right: 
                r += cls.playerRight()
                print('пошли направо...')
            if r == 0:
                print('мимо...')
                return None
            cc = cls.player.coord_get()
            objs = cls.get_objects_by_coords(cc)
            if len(objs) > 1:
                iList = list(filter(lambda o: ElementsDict[o.char]['interactable'], objs))
                if len(iList) > 1:
                    if cls.iteractionCell(iList):
                        cls.endGame('+')
                        return None
            cls.iteraction()
            if len(cls.gameElements):
                Loadtextmap(cls.GameMapToText(), loading=False)

def textToGameMap(textmap):
    lines = textmap.splitlines()
    if len(lines) > 0:
        while lines.count(""):
            lines.pop(lines.index(""))
        GameField.clearElements()
        for i, lev in enumerate(lines):
            for j, cc in enumerate(lev):
                if cc and cc in ElementsDict.keys():
                    GameField.addElement(cc,j,i)

def Loadtextmap(lev, loading=True):
    global textbox
    textbox.delete('1.0', 'end')
    textbox.insert('1.0', lev)
    if loading:
        maptxt = textbox.get('1.0', 'end')
        textToGameMap(maptxt)
        print(f'Загружено {len(GameField.gameElements)} элементов карты. \n')
    print(textbox.get('1.0', 'end'))

def Quit(ev):
    GameField.endGame('-')
    global root
    root.destroy()

def LoadNewLevel(ev):
    Loadtextmap(level_example.strip())

def StartLevels(ev):
    global textbox
    maptxt = textbox.get('1.0', 'end')
    Loadtextmap(maptxt.strip())

def ShowHelp(ev):
    global textbox
    global helplines
    textbox.delete('1.0', 'end') 
    textbox.insert('1.0', helplines)

def GoUp(ev):
    GameField.doStepGame(up=1)

def GoDown(ev):
    GameField.doStepGame(down=1)

def GoLeft(ev):
    GameField.doStepGame(left=1)

def GoRight(ev):
    GameField.doStepGame(right=1)

def SetBomb(ev):
    if GameField.gameElements and GameField.player:
        GameField.addElement('*',GameField.player.coords['x'],GameField.player.coords['y'])
        GameField.doStepGame()


root = Tk()

panelFrame = Frame(root, height = 60, bg = 'gray')
textFrame = Frame(root, height = 340, width = 600)

panelFrame.pack(side = 'top', fill = 'x')
textFrame.pack(side = 'bottom', fill = 'both', expand = 1)

textbox = Text(textFrame, font="Courier 20", wrap='word')
scrollbar = Scrollbar(textFrame)

scrollbar['command'] = textbox.yview
textbox['yscrollcommand'] = scrollbar.set

textbox.pack(side = 'left', fill = 'both', expand = 1)
scrollbar.pack(side = 'right', fill = 'y')

newBtn = Button(panelFrame, text = 'New')
startBtn = Button(panelFrame, text = 'Start creating level')
quitBtn = Button(panelFrame, text = 'Quit')
leftBtn = Button(panelFrame, text = '<--')
riteBtn = Button(panelFrame, text = '-->')
upBtn = Button(panelFrame, text = '^')
botBtn = Button(panelFrame, text = 'v')
bombBtn = Button(panelFrame, text = '*')
helpBtn = Button(panelFrame, text = '?')

quitBtn.bind("<Button-1>", Quit)
newBtn.bind("<Button-1>", LoadNewLevel)
startBtn.bind("<Button-1>", StartLevels)
leftBtn.bind("<Button-1>", GoLeft)
riteBtn.bind("<Button-1>", GoRight)
upBtn.bind("<Button-1>", GoUp)
botBtn.bind("<Button-1>", GoDown)
bombBtn.bind("<Button-1>", SetBomb)
helpBtn.bind("<Button-1>", ShowHelp)

newBtn.place(x = 10, y = 10, width = 40, height = 40)
startBtn.place(x = 60, y = 10, width = 130, height = 40)
quitBtn.place(x = 200, y = 10, width = 40, height = 40)
leftBtn.place(x = 300, y = 10, width = 40, height = 40)
riteBtn.place(x = 350, y = 10, width = 40, height = 40)
upBtn.place(x = 400, y = 10, width = 40, height = 40)
botBtn.place(x = 450, y = 10, width = 40, height = 40)
bombBtn.place(x = 500, y = 10, width = 40, height = 40)
helpBtn.place(x = 600, y = 10, width = 40, height = 40)

root.mainloop()
