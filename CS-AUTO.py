import pyautogui
import time
import threading
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog


class AutoReconnectApp:
    def __init__(self, root):
        self.root = root
        self.root.title("by Eterna1")
        self.root.geometry("500x350")
        self.root.resizable(False, False)

        # 设置中文字体
        self.style = ttk.Style()
        self.style.configure("TButton", font=("SimHei", 10))
        self.style.configure("TLabel", font=("SimHei", 12))
        self.style.configure("TEntry", font=("SimHei", 10))

        # 状态变量
        self.running = False
        self.thread = None
        # 两个点击坐标，默认先(1161,663)再(1008,1098)
        self.click_x1 = 1161
        self.click_y1 = 663
        self.click_x2 = 1008
        self.click_y2 = 1098
        self.interval = 150  # 默认间隔时间改为150秒

        # 游戏窗口标题（默认检测，不显示在UI）
        self.game_window_title = "反恐精英：全球攻势"

        # 创建UI元素
        self.create_widgets()

    def create_widgets(self):
        # 坐标设置区域 - 第一个点击位置
        coord_frame1 = ttk.LabelFrame(self.root, text="第一个点击坐标设置")
        coord_frame1.pack(pady=10, padx=10, fill=tk.X)

        ttk.Label(coord_frame1, text="X坐标:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.x1_entry = ttk.Entry(coord_frame1, width=10)
        self.x1_entry.insert(0, str(self.click_x1))
        self.x1_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(coord_frame1, text="Y坐标:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.y1_entry = ttk.Entry(coord_frame1, width=10)
        self.y1_entry.insert(0, str(self.click_y1))
        self.y1_entry.grid(row=0, column=3, padx=5, pady=5)

        self.get_coord1_btn = ttk.Button(
            coord_frame1,
            text="获取当前鼠标位置",
            command=lambda: self.get_current_coords(1)
        )
        self.get_coord1_btn.grid(row=0, column=4, padx=10, pady=5)

        # 坐标设置区域 - 第二个点击位置
        coord_frame2 = ttk.LabelFrame(self.root, text="第二个点击坐标设置")
        coord_frame2.pack(pady=5, padx=10, fill=tk.X)

        ttk.Label(coord_frame2, text="X坐标:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.x2_entry = ttk.Entry(coord_frame2, width=10)
        self.x2_entry.insert(0, str(self.click_x2))
        self.x2_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(coord_frame2, text="Y坐标:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.y2_entry = ttk.Entry(coord_frame2, width=10)
        self.y2_entry.insert(0, str(self.click_y2))
        self.y2_entry.grid(row=0, column=3, padx=5, pady=5)

        self.get_coord2_btn = ttk.Button(
            coord_frame2,
            text="获取当前鼠标位置",
            command=lambda: self.get_current_coords(2)
        )
        self.get_coord2_btn.grid(row=0, column=4, padx=10, pady=5)

        # 间隔时间设置
        interval_frame = ttk.LabelFrame(self.root, text="执行间隔设置(秒)")
        interval_frame.pack(pady=5, padx=10, fill=tk.X)

        ttk.Label(interval_frame, text="间隔时间:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.interval_entry = ttk.Entry(interval_frame, width=10)
        self.interval_entry.insert(0, str(self.interval))
        self.interval_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(interval_frame, text="秒(当前默认2分30秒=150秒)").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)

        # 状态标签
        self.status_label = ttk.Label(self.root, text="状态: 未运行", foreground="red")
        self.status_label.pack(pady=10)

        # 按钮框架
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)

        self.start_button = ttk.Button(
            button_frame,
            text="开始运行",
            command=self.start_operation,
            width=15
        )
        self.start_button.pack(side=tk.LEFT, padx=10)

        self.stop_button = ttk.Button(
            button_frame,
            text="结束运行",
            command=self.stop_operation,
            width=15,
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=10)

    def is_game_window_exists(self):
        """默认检测游戏窗口，不显示UI"""
        try:
            game_windows = pyautogui.getWindowsWithTitle(self.game_window_title)
            return len(game_windows) > 0
        except Exception:
            return False

    def get_current_coords(self, coord_number):
        messagebox.showinfo("提示", f"请在5秒内将鼠标移动到第{coord_number}个目标位置，程序将自动获取坐标")
        for i in range(5, 0, -1):
            self.update_status(f"即将在 {i} 秒后获取第{coord_number}个鼠标位置...")
            time.sleep(1)
        x, y = pyautogui.position()
        if coord_number == 1:
            self.x1_entry.delete(0, tk.END)
            self.x1_entry.insert(0, str(x))
            self.y1_entry.delete(0, tk.END)
            self.y1_entry.insert(0, str(y))
            self.click_x1 = x
            self.click_y1 = y
        else:
            self.x2_entry.delete(0, tk.END)
            self.x2_entry.insert(0, str(x))
            self.y2_entry.delete(0, tk.END)
            self.y2_entry.insert(0, str(y))
            self.click_x2 = x
            self.click_y2 = y
        self.update_status(f"已获取第{coord_number}个鼠标位置: ({x}, {y})")

    def bring_window_to_front(self, window_title):
        try:
            window = pyautogui.getWindowsWithTitle(window_title)[0]
            window.activate()
            window.moveTo(0, 0)
            window.maximize()
            self.update_status(f"窗口 '{window_title}' 已激活并最大化")
        except IndexError:
            self.update_status(f"未找到窗口: '{window_title}'", is_error=True)
        except Exception as e:
            self.update_status(f"激活窗口错误: {str(e)}", is_error=True)
        time.sleep(0.3)

    def click_button(self, x, y, number):
        try:
            pyautogui.click(x, y)
            self.update_status(f"已点击第{number}个坐标 ({x}, {y})")
        except Exception as e:
            self.update_status(f"第{number}个点击操作错误: {str(e)}", is_error=True)
        time.sleep(0.3)

    def minimize_window(self, window_title):
        try:
            window = pyautogui.getWindowsWithTitle(window_title)[0]
            window.minimize()
            self.update_status(f"窗口 '{window_title}' 已最小化")
        except IndexError:
            self.update_status(f"未找到窗口: '{window_title}'", is_error=True)
        except Exception as e:
            self.update_status(f"最小化窗口错误: {str(e)}", is_error=True)
        time.sleep(0.3)

    def operation_loop(self):
        while self.running:
            # 检测游戏窗口，不存在则自动停止
            if not self.is_game_window_exists():
                self.update_status(f"未检测到游戏窗口，自动停止操作", is_error=True)
                self.stop_operation()
                break

            try:
                self.click_x1 = int(self.x1_entry.get())
                self.click_y1 = int(self.y1_entry.get())
                self.click_x2 = int(self.x2_entry.get())
                self.click_y2 = int(self.y2_entry.get())
                self.interval = int(self.interval_entry.get())

                self.bring_window_to_front("完美世界竞技平台")
                self.click_button(self.click_x1, self.click_y1, 1)
                self.click_button(self.click_x2, self.click_y2, 2)
                self.minimize_window("反恐精英：全球攻势")
                self.minimize_window("完美世界竞技平台")

                # 等待期间每10秒检测一次窗口
                remaining = self.interval
                while remaining > 0 and self.running:
                    if remaining % 10 == 0 and not self.is_game_window_exists():
                        self.update_status(f"等待期间游戏窗口关闭，自动停止", is_error=True)
                        self.stop_operation()
                        return
                    self.update_status(f"等待中，下次执行还有 {remaining} 秒")
                    time.sleep(1)
                    remaining -= 1
            except ValueError:
                self.update_status("输入的坐标或间隔时间无效，请检查设置", is_error=True)
                time.sleep(5)
            except Exception as e:
                self.update_status(f"操作出错: {str(e)}", is_error=True)
                time.sleep(5)

        self.update_status("操作已停止", is_error=False)

    def start_operation(self):
        if not self.running:
            # 启动前检测游戏窗口
            if not self.is_game_window_exists():
                messagebox.showwarning("警告", "未检测到游戏窗口！\n请先启动游戏后再运行")
                return

            try:
                int(self.x1_entry.get())
                int(self.y1_entry.get())
                int(self.x2_entry.get())
                int(self.y2_entry.get())
                int(self.interval_entry.get())

                self.running = True
                self.start_button.config(state=tk.DISABLED)
                self.stop_button.config(state=tk.NORMAL)
                self.get_coord1_btn.config(state=tk.DISABLED)
                self.get_coord2_btn.config(state=tk.DISABLED)
                self.thread = threading.Thread(target=self.operation_loop, daemon=True)
                self.thread.start()
                self.update_status("操作已启动", is_error=False)
            except ValueError:
                messagebox.showerror("输入错误", "请确保所有坐标和间隔时间都是有效的数字")

    def stop_operation(self):
        if self.running:
            self.running = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.get_coord1_btn.config(state=tk.NORMAL)
            self.get_coord2_btn.config(state=tk.NORMAL)
            if self.thread and self.thread.is_alive():
                self.thread.join(timeout=5.0)

    def update_status(self, message, is_error=False):
        def update():
            self.status_label.config(text=f"状态: {message}")
            self.status_label.config(foreground="red" if is_error else "green")
        self.root.after(0, update)

    def on_close(self):
        if self.running:
            if messagebox.askyesno("确认", "操作正在运行中，确定要退出吗？"):
                self.stop_operation()
                self.root.destroy()
        else:
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = AutoReconnectApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()