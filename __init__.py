from tkinter import *
import random
from PIL import Image, ImageTk
import time
DIR = r".\\"


class Card:
    def __init__(self, master, kind, num, row, col, board):
        self.master = master
        self.board = board
        self.kind = kind
        self.num = num
        self.state = "CLOSE"
        self.back_name = f"{DIR}{'img0'}.jpg"
        self.pic_name = f"{DIR}{self.kind}{self.num}.jpg"
        self.image = self.open_image(self.back_name)
        self.row = row
        self.col = col
        self.button = Button(master, image=self.image, bg="light blue")
        self.button.grid(row=row, column=col, ipadx=5, ipady=5)
        self.button.bind("<Button-1>", self.on_press)

    def on_press(self, event):
        if self.state == "CLOSE":
            self.state = "SHOW_PIC"
            self.image = self.open_image(self.pic_name)
            self.button.configure(image=self.image, bg="light blue")
            self.button.grid(row=self.row, column=self.col, ipadx=5, ipady=5)
            self.button.update()
            self.board.cards_open.append(self)

        self.board.check_cards_match()

    def reverse_card(self):
        self.state = "CLOSE"
        self.image = self.open_image(self.back_name)
        self.button.configure(image=self.image, bg="light blue")
        # self.button.grid(row=self.row, column=self.col,ipadx=5,ipady=5)

    def open_image(self, name):
        card_pic = Image.open(name)
        card_pic.thumbnail((100, 100))
        card_pic = ImageTk.PhotoImage(card_pic)
        return card_pic


class GameBord:
    cards_open = []
    all_cards_open = []

    def __init__(self, master, cards_kind, player1, player2):
        self.cards_frame = Frame(master)
        self.cards_frame.pack(side=LEFT)
        self.button_frame = Frame(master)
        self.button_frame.pack(side=TOP)
        self.score_frame = Frame(master)
        self.score_frame.pack(side=TOP)
        self.cards_num = 15  # defult
        self.cards_kind = cards_kind
        # self.row = 0
        # self.col = 0
        self.all_cards = []
        self.player1 = player1
        self.player2 = player2
        self.score1 = 0
        self.score2 = 0
        self.curr_player = 1
        self.cards_layout()
        self.add_game_options()

    def add_game_options(self):
        self.add_num_of_cards()
        self.add_new_game()
        self.add_name_and_score_of_players()

    def bold_player_name(self):
        if self.curr_player == self.player1:
            p1 = Label(self.score_frame, text=self.player1, fg="red")
        else:
            p1 = Label(self.score_frame, text=self.player1)

        if self.curr_player == self.player2:
            p2 = Label(self.score_frame, text=self.player2, fg="red")
        else:
            p2 = Label(self.score_frame, text=self.player2)

        return p1, p2

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def add_name_and_score_of_players(self):

        self.clear_frame(self.score_frame)

        space1 = Label(self.score_frame, text="")
        space1.pack(side=TOP)
        scores = Label(self.score_frame, text="Scores: ")
        scores.pack(side=TOP)

        score1 = Label(self.score_frame, text=self.score1)
        score2 = Label(self.score_frame, text=self.score2)

        p1, p2 = self.bold_player_name()
        p1.pack(side=TOP)
        score1.pack(side=TOP)
        p2.pack(side=TOP)
        score2.pack(side=TOP)

    def set_cars_num(self, event):
        self.cards_ungrid()
        self.cards_num = int(event)
        self.cards_layout()

    def add_new_game(self):
        new_game_button = Button(self.button_frame, text="New Game", command=self.cards_layout)
        new_game_button.pack(side=TOP)
        self.add_name_and_score_of_players()

    def add_num_of_cards(self):
        l = Label(self.button_frame, text="זוגות כרטיסים")
        variable = StringVar()
        variable.set(self.cards_num)
        w = OptionMenu(self.button_frame, variable, "10", "15", "20", command=self.set_cars_num)
        l.pack(side=TOP)
        w.pack(side=TOP)

    def cards_layout(self):
        self.score1 = 0
        self.score2 = 0
        self.cards_open.clear()
        self.curr_player = self.player1
        place_array = []
        for i in range(0, self.cards_num * 2):
            place_array.append(i)

        for pic_num in range(0, self.cards_num):
            for spone in ([0, 1]):
                rand_index = random.randint(0, len(place_array) - 1)
                random_place = place_array[rand_index]
                place_array.remove(random_place)
                row = (random_place // 10)
                col = (random_place % 10)
                card = Card(self.cards_frame, self.cards_kind, pic_num + 1, row, col, self)
                self.all_cards.append(card)

        self.add_name_and_score_of_players()

    def cards_ungrid(self):
        for card in self.all_cards:
            card.button.grid_remove()

    def update_score(self):
        if self.curr_player == self.player1:
            self.score1 += 1
        else:
            self.score2 += 1

    def switch_players(self):
        if self.curr_player == self.player1:
            self.curr_player = self.player2
        else:
            self.curr_player = self.player1

    def print_winner(self):
        self.clear_frame(self.cards_frame)

        if self.score1 == self.score2:
            result = Label(self.cards_frame, padx=300, pady=300, bg='red',
                           text='No player won: tie!', font=40)
            result.pack(side=TOP)
        elif self.score1 > self.score2:
            result = Label(self.cards_frame, text=f'The winner of the game is: {self.player1}', font=40,
                           padx=300, pady=300, bg='red')
            result.pack(side=TOP)
        else:
            result = Label(self.cards_frame, text=f'The winner of the game is: {self.player2}', font=40, padx=300,
                           pady=300, bg='red')
            result.pack(side=TOP)

    def check_cards_match(self):
        if len(self.cards_open) == 2:
            time.sleep(1)
            if self.cards_open[0].num == self.cards_open[1].num:
                self.cards_open[0].button.configure(state=DISABLED)
                self.cards_open[1].button.configure(state=DISABLED)
                self.update_score()
                self.all_cards_open.append(self.cards_open[0].num)
                if len(self.all_cards_open) == self.cards_num:
                    self.print_winner()

            else:
                self.cards_open[0].reverse_card()
                self.cards_open[1].reverse_card()
                self.switch_players()

            self.cards_open = []
            self.add_name_and_score_of_players()


def main():
    player1 = input('Enter Player1 Name: ')
    player2 = input('Enter Player2 Name: ')
    root = Tk()
    GameBord(root, "img", player1, player2)
    root.mainloop()


if __name__ == "__main__":
    main()
