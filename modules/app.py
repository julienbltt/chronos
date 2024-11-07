import tkinter as tk
from tkinter import messagebox as mb
import datetime as dt

import utils.logger as logger

import modules.taskmanager as tm
import modules.csveditor as csveditor

app_logger = logger.get("app")
debug_logger = logger.get("debug")


class ChronosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Time Reporting")
        self.root.resizable(False, False)

        # States
        self.day_started = False
        self.task_started = False

        # Variables
        self.ts_start_day = None
        self.ts_end_day = None
        self.ts_delta_day = None
        self.ts_start_task = None
        self.ts_end_task = None
        self.ts_delta_task = None
        self.task_name = tk.StringVar()
        self.task_name.set("")
        self.db_file = tm.VAR_DIRECTORY_PATH / "tasks.csv"

        # Initialization widgets
        self.main_frm = tk.Frame(self.root)
        self.main_frm.pack(fill=tk.BOTH, expand=True)

        self.btn_start_day = tk.Button(self.main_frm, text="Commencer la journée", command=self.start_day)
        self.btn_start_day.grid(row=0, column=0, padx=10, pady=10, sticky=tk.NSEW)

        if self.ts_delta_day:
            self.lbl_last_day = tk.Label(
                self.main_frm,
                text=f"Durée du dernière jour : {self.ts_delta_day.seconds//3600:02}:{(self.ts_delta_day.seconds//60)%60:02}"
            )
            self.lbl_last_day.grid(row=1, column=0, padx=10, pady=10, sticky=tk.NSEW)
        else:
            self.lbl_last_day = None

        self.update_task_timer()

    def start_day(self):
        debug_logger.debug("Start day button triggered.")
        if not self.day_started:
            self.day_started = True

            # Get timestamp of starting day
            self.ts_start_day = dt.datetime.now()

            # Update main window widgets
            self.btn_start_day.destroy()

            self.lbl_ts_start_day = tk.Label(
                self.main_frm,
                text=f"Début de journée : {self.ts_start_day.strftime("%H:%M")}"
            )
            self.lbl_ts_start_day.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky=tk.EW)

            self.btn_start_task = tk.Button(self.main_frm, text="Commencer", command=self.start_task)
            self.btn_start_task.grid(row=1, column=0, padx=10, pady=0, sticky=tk.EW)

            self.btn_stop_task = tk.Button(self.main_frm, text="Terminer", command=self.stop_task, state=tk.DISABLED)
            self.btn_stop_task.grid(row=1, column=1, padx=10, pady=0, sticky=tk.EW)

            self.lbl_task_name = tk.Label(self.main_frm, text="Tâche en cours : ")
            self.lbl_task_name.grid(row=2, column=0, padx=5, pady=0, sticky=tk.E)

            self.etr_task_name = tk.Entry(self.main_frm, textvariable=self.task_name)
            self.etr_task_name.grid(row=2, column=1, padx=5, pady=0, sticky=tk.W)

            self.lbl_task_delay = tk.Label(self.main_frm, text="Durée : ")
            self.lbl_task_delay.grid(row=3, column=0, padx=5, pady=0, sticky=tk.E)
            self.lbl_task_time = tk.Label(
                self.main_frm,
                text="00:00"
            )
            self.lbl_task_time.grid(row=3, column=1, padx=5, pady=0, sticky=tk.W)

            self.btn_list_tasks = tk.Button(self.main_frm, text="Liste des tâches", command=self.display_tasks)
            self.btn_list_tasks.grid(row=4, column=0, padx=0, pady=10, sticky=tk.SW)

            self.btn_end_day = tk.Button(self.main_frm, text="Terminer la journée", command=self.end_day)
            self.btn_end_day.grid(row=4, column=1, padx=0, pady=10, sticky=tk.SE)

            app_logger.info("Day start.")

    def display_tasks(self):
        if self.db_file.exists():
            csveditor.CSVEditorWindow(self.root, self.db_file)
        else:
            mb.showerror("Error", "Tasks list file not found.")

    def start_task(self):
        debug_logger.debug("Start task button triggered.")
        if self.day_started and not self.task_started:
            if self.task_name.get() != "":
                self.create_task()
            else:
                mb.showerror("Create task error", "The name of the task is empty.")


    def create_task(self):
        debug_logger.debug("Update create task triggered.")
        if not self.task_started:
            self.task_started = True

            # Get timestamp of starting task.
            self.ts_start_task = dt.datetime.now()
            debug_logger.debug("Task start at: " + self.ts_start_task.strftime("%H:%M"))

            # Update task entry in main window.
            self.etr_task_name.config(state=tk.DISABLED)

            # Update task buttons
            self.btn_start_task.config(state=tk.DISABLED)
            self.btn_stop_task.config(state=tk.NORMAL)
            self.btn_end_day.config(state=tk.DISABLED)

            # Destroy external window.
            # self.win_task.destroy()

            # Update task timer
            self.update_task_timer()

            app_logger.info("New task named: " + self.task_name.get() + " have started at " + self.ts_start_task.strftime("%H:%M"))

    def update_task_timer(self):
        debug_logger.debug("Update task timer triggered.")
        if self.task_started:
            self.ts_delta_task = dt.datetime.now() - self.ts_start_task
            self.lbl_task_time.config(text=f"{self.ts_delta_task.seconds//3600:02}:{(self.ts_delta_task.seconds//60)%60:02}")
            self.root.after(60000, self.update_task_timer)

    def stop_task(self):
        debug_logger.debug("Stop task button triggered.")
        if self.task_started:
            self.task_started = False

            self.ts_end_task = dt.datetime.now()

            # Saving task
            task_info = {
                "name": self.task_name.get(),
                "date": self.ts_start_day.strftime("%Y-%m-%d"),
                "begin": self.ts_start_task.strftime("%H:%M"),
                "end": self.ts_end_task.strftime("%H:%M"),
                "delay": f"{self.ts_delta_task.seconds // 3600:02}:{(self.ts_delta_task.seconds // 60) % 60:02}"
            }
            tm.add_data(task_info, self.db_file)

            # Update widgets main window
            self.task_name.set("")
            self.etr_task_name.config(state=tk.NORMAL)

            self.btn_stop_task.config(state=tk.DISABLED)
            self.btn_start_task.config(state=tk.NORMAL)
            self.btn_end_day.config(state=tk.NORMAL)

            self.lbl_task_time.config(text=f"00:00")



    def end_day(self):
        debug_logger.debug("End day button triggered.")
        if self.day_started and self.ts_start_day:
            self.day_started = False
            self.ts_end_day = dt.datetime.now()
            debug_logger.debug("Day finished at " + self.ts_end_day.strftime("%H:%M"))
            self.ts_delta_day = self.ts_end_day - self.ts_start_day
            debug_logger.debug(f"Day during {self.ts_delta_day.seconds//3600:02}:{(self.ts_delta_day.seconds//60)%60:02}")

            # Update widgets of main window
            self.lbl_ts_start_day.destroy()
            self.btn_start_task.destroy()
            self.btn_stop_task.destroy()
            self.lbl_task_name.destroy()
            self.etr_task_name.destroy()
            self.btn_list_tasks.destroy()
            self.btn_end_day.destroy()
            self.lbl_task_delay.destroy()
            self.lbl_task_time.destroy()

            self.btn_start_day = tk.Button(self.main_frm, text="Commencer la journée", command=self.start_day)
            self.btn_start_day.grid(row=0, column=0, padx=10, pady=10, sticky=tk.NSEW)

            if self.lbl_last_day:
                self.lbl_last_day.config(
                    text=f"Durée du dernière jour : {self.ts_delta_day.seconds//3600:02}:{(self.ts_delta_day.seconds//60)%60:02}"
                )
            else:
                self.lbl_last_day = tk.Label(
                    self.main_frm,
                    text=f"Durée du dernière jour : {self.ts_delta_day.seconds//3600:02}:{(self.ts_delta_day.seconds//60)%60:02}"
                )
                self.lbl_last_day.grid(row=1, column=0, padx=10, pady=10, sticky=tk.NSEW)

            app_logger.info("Day finished")
