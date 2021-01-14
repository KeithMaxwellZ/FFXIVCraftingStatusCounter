import tkinter as tk
from tkinter import ttk
import _thread
import os
import datetime
import json

from util import COLOR_DICT


class Counter:
    """
    记录信息与启动gui
    """
    def __init__(self):
        self.total = 1
        self.save_count = 0
        self.stat = {
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0,
            6: 0,
            7: 0,
            8: 0,
            9: 0,
            10: 0
        }

        # 检查与创建文件
        self.check_save_path()
        self.now = datetime.datetime.now()
        self.fname = f"data/{str(self.now).replace(':', '')}.txt"
        open(self.fname, "w", encoding="utf-8")

    def check_save_path(self):
        """
        检查文件夹是否存在
        :return:
        """
        if not os.path.isdir("data"):
            os.mkdir("data")

    def add_data(self, color: int):
        """
        添加状态数据
        :param color: 球色代码
        :return:
        """
        self.total += 1
        self.stat[color] += 1

        self.save_count += 1
        if self.save_count >= 10:
            self.save_data()
            self.save_count = 0

    def print_data(self):
        """
        测试用
        :return:
        """
        for i in range(1, 10):
            print(f"{COLOR_DICT[i]}: {self.stat[i]}")

    def run_gui(self):
        """
        启动gui
        :return:
        """
        print("started")
        # 创建窗口
        main_frame = tk.Tk()
        main_frame.wm_attributes("-alpha", 0.8)  # 透明度(0.0~1.0)
        # main_frame.wm_attributes("-toolwindow", True)  # 置为工具窗口(没有最大最小按钮)
        main_frame.wm_attributes("-topmost", True)  # 永远处于顶层

        # 创建表格控件
        table = ttk.Treeview(main_frame, show="headings")
        table["columns"] = ("品质", "次数", "比例")

        # 设置列
        table.column("品质", width=100, anchor=tk.CENTER)
        table.column("次数", width=100, anchor=tk.CENTER)
        table.column("比例", width=100, anchor=tk.CENTER)

        # 设置显示的表头名
        table.heading("品质", text="品质")
        table.heading("次数", text="次数")
        table.heading("比例", text="比例")

        # 添加数据
        for i in range(1, 10):
            table.insert("", i, values=(COLOR_DICT[i], 0, 0))
        table.pack(side=tk.LEFT, fill=tk.BOTH)

        # 刷新数据用的函数
        def refresh():
            for i in table.get_children():
                table.delete(i)

            for x in range(1, 10):
                table.insert("", x, f"item{x}",
                             values=(COLOR_DICT[x], self.stat[x], format(self.stat[x] / self.total, ".2f")))
            main_frame.after(100, refresh)

        # 设置刷新间隔 （）
        main_frame.after(100, refresh)
        main_frame.mainloop()

    def save_data(self):
        with open(self.fname, "w") as f:
            json.dump(self.stat, f)


# 测试用函数，可以无视
def test(counter: Counter):
    print("test")
    import random
    import time
    for i in range(100):
        counter.add_data(random.randint(1, 10))
        time.sleep(0.3)


# 测试用
if __name__ == "__main__":
    c = Counter()
    _thread.start_new_thread(test, (c,))
    c.run_gui()
