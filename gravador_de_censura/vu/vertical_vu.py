import math, time
import tkinter
import traceback
from threading import Thread


class Led:
    def __init__(
        self,
        color_on=None,
        color_off=None,
        value=0,
        frame=None,
        width=None,
        height=None,
        orientation=None,
    ):

        self.height = height
        self.width = width
        self.color_on = color_on
        self.color_off = color_off
        self.value = value
        self.frame = frame
        border = 2
        self.frame_led = tkinter.Frame(
            self.frame,
            width=self.width,
            height=self.height,
            borderwidth=0,
            relief=tkinter.GROOVE,
            bg="#000000",
        )
        self.frame_led.pack_propagate(False)
        if orientation == "H":
            self.frame_led.pack(side=tkinter.RIGHT)
        else:
            self.frame_led.pack(side=tkinter.TOP)

        self.led = tkinter.Frame(
            self.frame_led,
            width=self.width - border,
            height=self.height - border,
            pady=border,
            padx=border,
        )
        self.led.pack(side=tkinter.RIGHT)
        self.set(self.value - 1)

    def set(self, value):

        if value < self.value:
            self.led.configure(bg=self.color_off)
        else:
            self.led.configure(bg=self.color_on)


class Vu(Thread):

    def __init__(
        self, master, frame, width, height, player=None, orientation="H", daemon=True
    ):

        super().__init__(daemon=daemon)

        self.n = 20
        self.master = master
        self.frame_l = tkinter.Frame(frame)
        self.frame_r = tkinter.Frame(frame)
        if orientation == "H":
            self.frame_l.pack(side=tkinter.TOP)
            self.frame_r.pack(side=tkinter.BOTTOM)
        else:
            self.frame_l.pack(side=tkinter.LEFT)
            self.frame_r.pack(side=tkinter.RIGHT)
        self.width = width
        self.height = height
        self.player = player
        self.running = True
        # self.text_l = tkinter.StringVar(self.frame, '0 DBFS')
        # self.text_r = tkinter.StringVar(self.frame, '0 DBFS')
        self.green_on = "#22FF22"
        self.yellow_on = "#FFFF22"
        self.red_on = "#FF2222"
        self.leds_l = []
        self.leds_r = []

        self.green_off = "#229922"
        self.yellow_off = "#999922"
        self.red_off = "#992222"

        self.start()

        for i in range(self.n):
            if i == 0:
                self.leds_l.append(
                    Led(
                        frame=self.frame_l,
                        color_on=self.red_on,
                        color_off=self.red_off,
                        value=0 - i,
                        width=self.width / 2,
                        height=int(self.height / self.n),
                        orientation=orientation,
                    )
                )
                self.leds_r.append(
                    Led(
                        frame=self.frame_r,
                        color_on=self.red_on,
                        color_off=self.red_off,
                        value=0 - i,
                        width=self.width / 2,
                        height=int(self.height / self.n),
                        orientation=orientation,
                    )
                )
            elif i <= 2:
                self.leds_l.append(
                    Led(
                        frame=self.frame_l,
                        color_on=self.yellow_on,
                        color_off=self.yellow_off,
                        value=0 - i,
                        width=self.width / 2,
                        height=int(self.height / self.n),
                        orientation=orientation,
                    )
                )
                self.leds_r.append(
                    Led(
                        frame=self.frame_r,
                        color_on=self.yellow_on,
                        color_off=self.yellow_off,
                        value=0 - i,
                        width=self.width / 2,
                        height=int(self.height / self.n),
                        orientation=orientation,
                    )
                )
            else:
                self.leds_l.append(
                    Led(
                        frame=self.frame_l,
                        color_on=self.green_on,
                        color_off=self.green_off,
                        value=0 - i,
                        width=self.width / 2,
                        height=int(self.height / self.n),
                        orientation=orientation,
                    )
                )
                self.leds_r.append(
                    Led(
                        frame=self.frame_r,
                        color_on=self.green_on,
                        color_off=self.green_off,
                        value=0 - i,
                        width=self.width / 2,
                        height=int(self.height / self.n),
                        orientation=orientation,
                    )
                )

    def set(self, percent):

        dbfs_l = self.DBFS(percent[0])
        dbfs_r = self.DBFS(percent[1])

        for i in range(self.n):
            self.leds_l[i].set(dbfs_l)
            self.leds_r[i].set(dbfs_r)

    def set_player(self, player):
        if self.player:
            self.player.set_vu(False)
        if player:
            player.set_vu(True)
        self.player = player

    def set_running(self, b):
        self.running = b

    def string_DBFS(self, percent):

        return str(int(20 * math.log10(percent))) if percent > 0 else -120

    def DBFS(self, percent):
        if percent > 1:
            percent = 1
        return 20 * math.log10(percent) if percent > 0 else -120

    def draw(self):
        pass

    def run(self):
        time.sleep(1)
        while self.running:
            time.sleep(0.05)
            if self.player:
                try:
                    self.set(self.player.vu_value)
                except Exception as e:
                    print(type(e))
                    print(e.args)
                    traceback.print_exc()

        self.running = False

        print("Vu bar encerrada.")
