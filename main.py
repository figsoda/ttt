from itertools import chain
import pygame as pg

BG = (31, 34, 39)
FG = (171, 179, 191)

WIDTH = 640
HEIGHT = 680

pg.font.init()
FONT = pg.font.SysFont("sans-serif", 40)

class State:
    def __init__(self):
        self.board = [[None] * 3 for _ in range(3)]
        self.turn = 1
        self.win = None

    def render(self):
        s = pg.Surface((WIDTH, HEIGHT))
        s.fill(BG)

        for x in range(20, WIDTH, 200):
            pg.draw.line(s, FG, (x, 20), (x, 620), 2)
            pg.draw.line(s, FG, (20, x), (620, x), 2)

        for gx, gs in enumerate(self.board):
            for gy, g in enumerate(gs):
                if not g: continue

                x = gx * 200 + 20
                y = gy * 200 + 20
                if g == 1:
                    pg.draw.line(s, FG, (x + 50, y + 50), (x + 150, y + 150), 2)
                    pg.draw.line(s, FG, (x + 150, y + 50), (x + 50, y + 150), 2)
                elif g == 2:
                    pg.draw.circle(s, FG, (x + 100, y + 100), 50, 2)

        if not self.win:
            msg = f"Player {self.turn}'s turn"
        elif self.win == 3:
            msg = "Draw! Click anywhere to restart"
        else:
            msg = f"Player {self.win} wins! Click anywhere to restart"
        text = FONT.render(msg, True, FG)
        s.blit(text, ((WIDTH - text.get_width()) / 2, 635))

        return s

def handle(st, ev):
    if ev.type == pg.MOUSEBUTTONUP:
        if st.win: return State()

        x, y = pg.mouse.get_pos()

        def get_grid(x):
            if x < 20: return None
            if x < 220: return 0
            if x < 420: return 1
            if x < 620: return 2

        gx = get_grid(x)
        gy = get_grid(y)

        if gx != None and gy != None:
            if not st.board[gx][gy]:
                st.board[gx][gy] = st.turn

                for a, b, c in [
                    *st.board,
                    *zip(*st.board),
                    (st.board[i][i] for i in range(3)),
                    (st.board[2][0], st.board[1][1], st.board[0][2]),
                ]:
                    if a and a == b and b == c:
                        st.win = st.turn
                        return st

                if all(chain(*st.board)):
                    st.win = 3
                    return st

                st.turn = 3 - st.turn

    return st

def main():
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    st = State()
    while True:
        for ev in pg.event.get():
            if ev.type == pg.QUIT: return
            st = handle(st, ev)
            screen.blit(st.render(), (0, 0))
            pg.display.update()

main()
