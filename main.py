#!/usr/bin/env python3

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.popup import Popup
from random import randint


class AI:
    # h == level; neskor pridaj moznost vyberu levelu; min h je 2. 
    def __init__(self, btns: list, turn='O', h=10, init=True):
        self.init = init

        self.indexes = []
        if init:
            for btn in btns:
                self.indexes.append(btn.text if btn.text != '' else None)
        else:
            self.indexes = btns

        self.turn = turn
        self.h = h
        self.__end = self._win_pos()
        print(self.__end)

    def calc(self):
        def calc_for(player):
            lines = 0
            player = 'X' if player == 'O' else 'O'
            for i in {0, 3, 6}:
                if self.indexes[i] != player and self.indexes[i + 1] != player and self.indexes[i + 2] != player:
                    lines += 1
            for i in range(3):
                if self.indexes[i] != player and self.indexes[i + 3] != player and self.indexes[i + 6] != player:
                    lines += 1
            if self.indexes[0] != player and self.indexes[4] != player and self.indexes[8] != player:
                lines += 1
            if self.indexes[2] != player and self.indexes[4] != player and self.indexes[6] != player:
                lines += 1
            return lines
        player = self.turn
        oponent = 'X' if self.turn == 'O' else 'O'
        score = calc_for(player) - calc_for(oponent)
        return score

    def move(self):
        if self.h != 0 and not self.__end:
            if self.turn == 'O':
                vals = []
                for i, val in enumerate(self.indexes):
                    if val is None:
                        temp = self.indexes.copy()
                        temp[i] = 'O'
                        print(temp)
                        ai = AI(temp, turn='X', h=self.h - 1, init=False)
                        vals.append((ai.move(), i))
                winner = max(vals, key=lambda x: x[0])
                if self.init:
                    return winner[1]
                else:
                    return winner[0]

            else:
                vals = []
                for i, val in enumerate(self.indexes):
                    if val is None:
                        temp = self.indexes.copy()
                        temp[i] = 'X'
                        print(temp)
                        ai = AI(temp, turn='O', h=self.h - 1, init=False)
                        vals.append((ai.move(), i))
                print(vals)
                winner = min(vals, key=lambda x: x[0])
                if self.init:
                    return winner[1]
                else:
                    return winner[0]
        else:
            if isinstance(self.__end, int):
                return self.__end
            else:
                return self.calc()

    def _win_pos(self):
        for player in {'X', 'O'}:
            for i in {0, 3, 6}:
                if self.indexes[i] == player and self.indexes[i + 1] == player and self.indexes[i + 2] == player:
                    if player == 'O':
                        return 10000
                    else:
                        return -10000
            for i in range(3):
                if self.indexes[i] == player and self.indexes[i + 3] == player and self.indexes[i + 6] == player:
                    if player == 'O':
                        return 10000
                    else:
                        return -10000
            if self.indexes[0] == player and self.indexes[4] == player and self.indexes[8] == player:
                if player == 'O':
                    return 10000
                else:
                    return -10000
            if self.indexes[2] == player and self.indexes[4] == player and self.indexes[6] == player:
                if player == 'O':
                    return 10000
                else:
                    return -10000
        else:
            for i in self.indexes:
                if i is None:
                    return False
            else:
                return True


class Game(Screen):

    player1 = NumericProperty()
    player2 = NumericProperty()
    status = StringProperty()

    def __init__(self, multiplayer=False, sm=None, **kwargs):
        super().__init__(**kwargs)
        self.btns = []
        # 0 = kruzok ; 1 = iksko
        self.turn = randint(0, 1) if multiplayer else 1
        self.__multi = multiplayer

        content = BoxLayout(orientation='vertical')
        self.status_label = Label(text=str(self.status))
        content.add_widget(self.status_label)
        dismiss_btns = BoxLayout(orientation='horizontal')
        dismiss_btns.add_widget(
            Button(text='RESTART', on_press=lambda i: self.restart()))
        dismiss_btns.add_widget(Button(
            text='EXIT', on_press=lambda i: self.exit(sm)))
        content.add_widget(dismiss_btns)
        self.pop = Popup(title='GAME OVER', content=content,
                         size_hint=(0.5, 0.2), pos_hint={'y': 0.75}, auto_dismiss=False)

        main_layout = BoxLayout(orientation='vertical')

        row_1 = BoxLayout(orientation='horizontal', spacing=20)

        self.X = Label(text='X', font_size=50)
        self.X.underline = True if self.turn == 1 else False
        row_1.add_widget(self.X)

        self.O = Label(text='O', font_size=50)
        self.O.underline = True if self.turn == 0 else False
        row_1.add_widget(self.O)

        main_layout.add_widget(row_1)

        row_2 = GridLayout(rows=3, cols=3)
        row_2.size_hint = (0.5, 1.0)
        row_2.pos_hint = {'x': 0.25}
        for i in range(9):
            btn = Button(font_size=30)
            btn.bind(on_press=self.key_stroke)
            self.btns.append(btn)
            row_2.add_widget(btn)
        main_layout.add_widget(row_2)

        row_3 = BoxLayout(orientation='horizontal')
        self._player1_label = Label(text=str(self.player1))
        self._player1_label.font_size = 40
        row_3.add_widget(self._player1_label)
        self._player2_label = Label(text=str(self.player2))
        self._player2_label.font_size = 40
        row_3.add_widget(self._player2_label)
        main_layout.add_widget(row_3)

        self.add_widget(main_layout)

    def key_stroke(self, instance):
        if self.turn == 0:
            if instance.text == '':
                self.turn = 1
                instance.text = 'O'
                self.X.underline = True
                self.O.underline = False
                win = self.check_win()
                if not win:
                    pass
                elif win == 'Draw':
                    self.status = 'Draw'
                    self.pop.open()
                else:
                    self.status = 'Winner is O'
                    self.player2 += 1
                    self.pop.open()

        else:
            if self.__multi:
                if instance.text == '':
                    self.turn = 0
                    instance.text = 'X'
                    self.X.underline = False
                    self.O.underline = True
                    win = self.check_win()
                    if not win:
                        pass
                    elif win == 'Draw':
                        self.status = 'Draw'
                        self.pop.open()
                    else:
                        self.status = 'Winner is X'
                        self.player1 += 1
                        self.pop.open()
            else:
                if instance.text == '':
                    self.turn = 1
                    instance.text = 'X'
                    self.X.underline = False
                    self.O.underline = True
                    win = self.check_win()
                    if not win:
                        index_of_O = AI(self.btns, init=True).move()
                        if self.btns[index_of_O].text == '':
                            self.btns[index_of_O].text = 'O'
                            self.X.underline = True
                            self.O.underline = False
                        win = self.check_win()
                        if not win:
                            pass
                        elif win == 'Draw':
                            self.status = 'Draw'
                            self.X.underline = True
                            self.O.underline = False
                            self.pop.open()
                        else:
                            self.status = 'Winner is O'
                            self.player2 += 1
                            self.pop.open()
                    elif win == 'Draw':
                        self.status = 'Draw'
                        self.X.underline = True
                        self.O.underline = False
                        self.pop.open()
                    else:
                        self.status = 'Winner is X'
                        self.player1 += 1
                        self.pop.open()

    def check_win(self):
        for i in {0, 3, 6}:
            if self.btns[i].text == self.btns[i + 1].text == self.btns[i + 2].text:
                if (self.btns[i].text != '') and (self.btns[i + 1].text != '') and (self.btns[i + 2].text != ''):
                    return self.btns[i].text
        for i in range(3):
            if self.btns[i].text == self.btns[i + 3].text == self.btns[i + 6].text:
                if (self.btns[i].text != '') and (self.btns[i + 3].text != '') and (self.btns[i + 6].text != ''):
                    return self.btns[i].text
        if self.btns[0].text == self.btns[4].text == self.btns[8].text:
            return self.btns[0].text
        if self.btns[2].text == self.btns[4].text == self.btns[6].text:
            return self.btns[2].text
        for i in self.btns:
            if i.text == '':
                return False
        else:
            return 'Draw'

    def restart(self):
        for btn in self.btns:
            btn.text = ''
        if self.__multi:
            self.turn = randint(0, 1)
        else:
            self.turn = 1
            self.X.underline = True
            self.O.underline = False
        self.pop.dismiss()

    def exit(self, sm):
        sm.switch_to(Menu(sm))
        self.pop.dismiss()

    def on_player1(self, instance, value):
        self._player1_label.text = str(value)

    def on_player2(self, instance, value):
        self._player2_label.text = str(value)

    def on_status(self, instance, value):
        self.status_label.text = value


class Menu(Screen):
    def __init__(self, sm, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(spacing=10, orientation='vertical')
        self.add_widget(layout)

        image = Image(source='tictoc-pos-rgb.png')
        layout.add_widget(image)

        singel = Button(text='Singel')
        singel.font_size = 25
        singel.background_color = (0, 0, 0, 0)
        singel.color = (0, 0, 1, 1)
        singel.size_hint = (0.5, 1.0)
        singel.pos_hint = {'x': 0.25}
        singel.bind(on_press=lambda instance: sm.switch_to(Game(sm=sm)))
        layout.add_widget(singel)

        multi = Button(text='Multi')
        multi.font_size = 25
        multi.background_color = (0, 0, 0, 0)
        multi.color = (1, 0, 0, 1)
        multi.size_hint = (0.5, 1.0)
        multi.pos_hint = {'x': 0.25}
        multi.bind(on_press=lambda instance: sm.switch_to(
            Game(multiplayer=True, sm=sm)))
        layout.add_widget(multi)


class TicToc(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Menu(sm))
        return sm


if __name__ == '__main__':
    TicToc().run()
