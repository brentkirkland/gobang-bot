#!/usr/bin/python
import argparse
import numpy as np
from random import randint
import copy
import time;

class Game:

    def __init__(self, p, b):
        self.turn = 'D';
        if p:
            self.player = 'L'
        else:
            self.player = 'D'
        self.board_size = b;
        self.move_played = '--';
        self.count = -1;

    def generate_board(self):
        self.alphabet = [
            'a', 'b', 'c', 'd', 'e', 'f', 'g',
            'h', 'i', 'j', 'k', 'l', 'm', 'n',
            'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z'
            ];
        self.alphabet_dict = {
            'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6,
            'h':7, 'i':8, 'j':9, 'k':10, 'l':11, 'm':12, 'n':13,
            'o':14, 'p':15, 'q':16, 'r':17, 's':18, 't':19, 'u':20,
            'v':21, 'w':22, 'x':23, 'y':24, 'z':25
            };
        size = (self.board_size, self.board_size);
        self.board = np.zeros(size);

    def print_board(self):
        top_row = '\n     ';
        space = '   ';
        seperator = '   +';
        for i in range(0, self.board_size):
            seperator = seperator + '---+'
        for i in range(0, self.board_size):
            top_row = top_row + self.alphabet[i] + space;
        print top_row;
        print seperator;
        for i in range(0, self.board_size):
            if i >= 9:
                start = '' + str(i+1) + ' |'
            else:
                start = ' ' + str(i+1) + ' |'
            for j in range(0, self.board_size):
                if self.board[i][j] == 0:
                    start = start + '   |';
                else:
                    if self.board[i][j] == 1:
                        # 1 is always robo
                        if self.player == 'L':
                            start = start + ' D |';
                        else:
                            start = start + ' L |';
                    else:
                        if self.player == 'L':
                            start = start + ' L |';
                        else:
                            start = start + ' D |';
            print start;
            print seperator;

    def switch_turn(self):
        if self.turn == 'L':
            self.turn = 'D';
        else:
            self.turn = 'L';
        self.play_game();

    def random_move(self):
        x = -1;
        y = -1;
        while(True):
            x = randint(0, self.board_size-1);
            y = randint(0, self.board_size-1);
            if self.board[y][x] == 0:
                # print self.board;
                # print self.board[y][x]
                break;
        return x, y;

    def place_color(self, row, col, human=True):
        print 'from place color'
        print row;
        print col;
        if human:
            self.board[row][col] = -1
        else:
            self.board[row][col] = 1
        self.print_board();
        print self.board;
        self.switch_turn();

    def transform_to_board_format(self, x, y):
        col = self.alphabet[x];
        row = y+1;
        return col + str(row);

    def total_up(self, board):
        return self.sb(board, self.board_size)

    def sb(self, board, l):
        mystring = ''
        #rows
        for i in board:
            mystring += 'W'
            for x in i:
                if x == -1:
                    mystring += '2'
                else:
                    mystring += str(int(x));
        #columns
        for i in range(0, l):
            mystring += 'W'
            for j in range(0, l):
                if board[j][i] == -1:
                    mystring += '2'
                else:
                    mystring += str(int(board[j][i]))
        diags = [board[::-1,:].diagonal(i) for i in range(-1*(l-1),l)]
        diags.extend(board.diagonal(i) for i in range(l-1,l*-1,-1))

        x = [n.tolist() for n in diags];
        for z in x:
            mystring += 'W'
            for y in z:
                if y == -1:
                    mystring += '2'
                else:
                    mystring += str(int(y));

        total_me = mystring.count('00011')*100 + \
            mystring.count('11000')*100 + \
            mystring.count('010010')*200 + \
            mystring.count('01010')*250 + \
            mystring.count('00011000')*1000 + \
            mystring.count('10101')*500 + \
            mystring.count('11010')*600 + \
            mystring.count('10110')*600 + \
            mystring.count('11100')*500 + \
            mystring.count('00111')*500 + \
            mystring.count('01110')*3000 + \
            mystring.count('011010')*900 + \
            mystring.count('010110')*900 + \
            mystring.count('11011')*2000 + \
            mystring.count('10111')*3500 + \
            mystring.count('11101')*3500 + \
            mystring.count('11110')*6000 + \
            mystring.count('01111')*6000 + \
            mystring.count('011110')*100000 + \
            mystring.count('11111')*10000000;
        total_you = mystring.count('00022')*100 + \
            mystring.count('22000')*100 + \
            mystring.count('020020')*200 + \
            mystring.count('02020')*250 + \
            mystring.count('00022000')*1000 + \
            mystring.count('20202')*500 + \
            mystring.count('22020')*600 + \
            mystring.count('20220')*600 + \
            mystring.count('22200')*500 + \
            mystring.count('00222')*500 + \
            mystring.count('02220')*3000 + \
            mystring.count('022020')*900 + \
            mystring.count('020220')*900 + \
            mystring.count('22022')*2000 + \
            mystring.count('20222')*3500 + \
            mystring.count('22202')*3500 + \
            mystring.count('22220')*6000 + \
            mystring.count('02222')*6000 + \
            mystring.count('022220')*100000  + \
            mystring.count('22222')*10000000;

        total = total_me - total_you;
        return total;


    def move_two(self, board, a, b, n, player=True):
        if n == 0:
            total = self.total_up(board);
            return total;
        values = [];
        positions = [];
        if player:
            for i in range(0, self.board_size):
                for j in range(0, self.board_size):
                    if board[i][j] == 0:
                        # update board position
                        if b <= a:
                            return a;
                        board[i][j] = -1

                        val = self.move_two(board, a, b, n-1, False)
                        if val < b:
                            b = val;
                        board[i][j] = 0
            return b;
        else:
            for i in range(0, self.board_size):
                for j in range(0, self.board_size):
                    if board[i][j] == 0:
                        #update board positions
                        if b <= a:
                            return b;
                        board[i][j] = 1
                        val= self.move_two(board, a, b, n-1)
                        if val > a:
                            a = val;
                        board[i][j] = 0
            return a;

    def lets_make_moves(self, board, player=True):
        values = [];
        positions = [];
        pos = (0,0);
        z = 1;
        if self.count < int(self.board_size*2):
            z = 1;
        elif self.count < int(self.board_size*4):
            z = 2;
        else:
            z = 3;
        print self.count;
        print 'count';
        a = float('-inf');
        b = float('inf');
        for i in range(0, self.board_size):
            for j in range(0, self.board_size):
                if board[i][j] == 0:
                    board[i][j] = 1
                    val = self.move_two(board, a, b, z);
                    if val > a:
                        a = val;
                        pos = (i,j);
                    board[i][j] = 0

        return pos;

    def play_game(self):
        print 'Move played: ' + self.move_played;
        self.count = self.count + 1;
        if self.player != self.turn:
            print 'robos turn';
            if self.count == 0 and self.board[int(self.board_size/2)][int(self.board_size/2)] == 0:
                x = int(self.board_size/2);
                y = x;
                var = self.transform_to_board_format(x,x);
                self.move_played = var;
            else:
                y, x = self.lets_make_moves(self.board)
                var = self.transform_to_board_format(x,y);
                self.move_played = var;
            self.place_color(y, x, False)
        else:
            var = raw_input("Please enter move: ")
            self.move_played = var;
            col = self.alphabet_dict[var[0]]
            if len(var) > 2:
                first = var[1]
                second = var[2];
                together = first + second;
                row = int(together) - 1;
            else:
                row = int(var[1]) - 1;
            self.place_color(row, col)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='GoBang!');
    parser.add_argument('-n', type=int, help='Gameboard size', default=11);
    parser.add_argument('-l', help='Light player', action='store_true');
    args = parser.parse_args()
    g = Game(args.l, args.n)
    g.generate_board();
    g.print_board();
    g.play_game();
