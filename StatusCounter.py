from win32gui import FindWindow  # 获取窗口句柄
from win32api import OpenProcess  # 创建进程句柄与关闭进程句柄
from win32con import PROCESS_ALL_ACCESS  # win32con里面放的是一些pywin32中的常量,我们导入我们需要的进程权限
from win32process import GetWindowThreadProcessId, EnumProcessModules  # 通过窗口句柄获取进程ID
import time
import _thread

from util import Memory64
from GUI import Counter


def get_processed_data():
    ret_color = m.ReadVirtualMemory64(ModuleBaseAddr_color, 4)
    ret_round = m.ReadVirtualMemory64(ModuleBaseAddr_round, 4)
    return [ret_color, ret_round]


# 从这里启动
if __name__ == '__main__':
    hwnd = FindWindow(None, "最终幻想XIV")  # 获取窗口句柄
    m = Memory64(hwnd)

    p_id = GetWindowThreadProcessId(hwnd)[1]
    processHandle = OpenProcess(PROCESS_ALL_ACCESS, False, p_id)
    modules = EnumProcessModules(processHandle)
    processHandle.close()
    program_base = int(modules[0])  # 基址

    color_base = 0x1CAB9A8 + 0x00A6300  # 球色
    round_base = 0x1CAB988 + 0x00A6300  # 回合

    ModuleBaseAddr_color = program_base + color_base
    ModuleBaseAddr_round = program_base + round_base

    current_round = 0

    crafting_color = {
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

    c = Counter()
    _thread.start_new_thread(c.run_gui, ())

    while True:
        processed_data = get_processed_data()
        if processed_data[1] != current_round:
            c.add_data(processed_data[0])
            current_round = processed_data[1]  # 当前回合替换
        time.sleep(0.5)
