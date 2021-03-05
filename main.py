from itertools import chain
from pygame import Surface, display, draw, event, font, mouse
import pygame as pg
import sys

BG = 31, 34, 39
FG = 171, 179, 191

WIDTH = 640
HEIGHT = 680

font.init()
FONT = font.SysFont("sans-serif", 40)

class State:
    def __init__(self): self.reset()

    def reset(self):
        self.board = [[None] * 3 for _ in range(3)]
        self.turn = 1
        self.win = None

    def handle(self, ev):
        if ev.type == pg.MOUSEBUTTONUP:
            if self.win:
                self.reset()
                return

            x, y = mouse.get_pos()

            def get_grid(x):
                if x < 20: return
                if x < 220: return 0
                if x < 420: return 1
                if x < 620: return 2

            gx = get_grid(x)
            gy = get_grid(y)

            if gx != None and gy != None and not self.board[gx][gy]:
                self.board[gx][gy] = self.turn

                for a, b, c in [
                    *self.board,
                    *zip(*self.board),
                    (self.board[i][i] for i in range(3)),
                    (self.board[2][0], self.board[1][1], self.board[0][2]),
                ]:
                    if a and a == b and b == c:
                        self.win = self.turn
                        return

                if all(chain(*self.board)):
                    self.win = 3
                else:
                    self.turn = 3 - self.turn

    def render(self):
        s = Surface((WIDTH, HEIGHT))
        s.fill(BG)

        for x in range(20, WIDTH, 200):
            draw.line(s, FG, (x, 20), (x, 620), 2)
            draw.line(s, FG, (20, x), (620, x), 2)

        for gx, gs in enumerate(self.board):
            for gy, g in enumerate(gs):
                if not g: continue

                x = gx * 200 + 20
                y = gy * 200 + 20
                if g == 1:
                    draw.line(s, FG, (x + 50, y + 50), (x + 150, y + 150), 2)
                    draw.line(s, FG, (x + 150, y + 50), (x + 50, y + 150), 2)
                else:
                    draw.circle(s, FG, (x + 100, y + 100), 50, 2)

        if not self.win:
            msg = f"Player {self.turn}'s turn"
        elif self.win == 3:
            msg = "Draw! Click anywhere to restart"
        else:
            msg = f"Player {self.win} wins! Click anywhere to restart"
        text = FONT.render(msg, True, FG)
        s.blit(text, ((WIDTH - text.get_width()) / 2, 635))

        return s

pg.init()
screen = display.set_mode((WIDTH, HEIGHT))
st = State()
while True:
    for ev in event.get():
        if ev.type == pg.QUIT: sys.exit()
        st.handle(ev)
        screen.blit(st.render(), (0, 0))
        display.update()
