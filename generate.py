import keyboard
from query import query


class Default:
    def none_callback(self):
        return query.generate("NOTHING", ".", ".")


class Task(Default):
    def __init__(self, task):
        self.task = task
        self.menu_query = query.generate("EDIT_KB", "task", "keyboard", task_id=self.task.id, type="main")
        self.none_callback = query.generate("NOTHING", ".", ".")

    def message(self):
        print("generated text!")
        text = (
            f"***\ _ _ _ _ _<TASK #{self.task.id}> _ _ _ _ _ /***\n"
            f"{self.task.name}"
        )
        return text

    def main_kb(self):
        buttons, callback = [], []
        if self.task.type is None:
            return self.task_type_kb()
        elif self.task.type == 0:
            buttons.append(["Выбор типа задачи"])
            callback.append([query.generate("EDIT_KB", "task", "keyboard", task_id=self.task.id, type="task_type")])
            buttons.append(["&Время начала", "&Время конца"])
            callback.append([
                query.generate("EDIT_KB", "task", "keyboard", task_id=self.task.id, type="start_time"),
                query.generate("EDIT_KB", "task", "keyboard", task_id=self.task.id, type="end_time")
            ])
            buttons.append(["&Продолжительность"])
            callback.append([query.generate("EDIT_KB", "task", "keyboard", task_id=self.task.id, type="duration")])
            buttons.append(["Периодичность"])
            callback.append([query.generate("EDIT_KB", "task", "keyboard", task_id=self.task.id, type="periodicity")])
        elif self.task.type == 1:
            buttons.append(["Выбор типа задачи"])
            callback.append([query.generate("EDIT_KB", "task", "keyboard", task_id=self.task.id, type="task_type")])
        elif self.task.type == 2:
            buttons.append(["Выбор типа задачи"])
            callback.append([query.generate("EDIT_KB", "task", "keyboard", task_id=self.task.id, type="task_type")])

        return buttons, callback

    def task_type_kb(self):
        buttons, callback = [], []
        buttons.append(["[hh:mm-time]"])
        callback.append([query.generate("EDIT_KB", "task", "update", task_id=self.task.id, parameter="type", value=0)])
        buttons.append(["result-orientation"])
        callback.append([query.generate("EDIT_KB", "task", "update", task_id=self.task.id, parameter="type", value=1)])
        buttons.append(["ONE-STEP-JOB"])
        callback.append([query.generate("EDIT_KB", "task", "update", task_id=self.task.id, parameter="type", value=2)])

        if self.task.type is not None:
            buttons[self.task.type] = ["|*| " + buttons[self.task.type][0] + " |*|"]
            callback[self.task.type] = [self.menu_query]

        return buttons, callback

    def periodicity(self, type=None):
        buttons, callback = [], []
        if type == None:
            buttons.append(["&Ежедневно", "Еженедельно"])
            callback.append([
                self.none_callback(),
                query.generate("EDIT_KB", "task", "keyboard", task_id=self.task.id, type="periodicity_everyweek")
            ])
            buttons.append(["&Ежемесячно", "&Ежегодно"])
            callback.append([self.none_callback(), self.none_callback()])
            buttons.append(["Назад"])
            callback.append([self.menu_query])
        elif type=="everyweek":
            buttons.append(["SUN", "MON", "TUE", "WED"])
            callback.append([self.none_callback(), self.none_callback(), self.none_callback(), self.none_callback()])
            buttons.append(["TUE", "FRI", "SAT"])
            callback.append([self.none_callback(), self.none_callback(), self.none_callback()])
            buttons.append(["Назад"])
            callback.append([query.generate("EDIT_KB", "task", "keyboard", task_id=self.task.id, type="periodicity")])

        return buttons, callback

    def duration(self):
        buttons, callback = [], []

        # buttons.append(["---", "HOURS", "---"])
        # callback.append([self.none_callback, self.none_callback, self.none_callback])
        buttons.append(["\ _ _ _ _ _  11 HOURS _ _ _ _ _ /"])
        callback.append([self.none_callback])
        buttons.append(["-1", " 0 ", "+1"])
        callback.append([self.none_callback, self.none_callback, self.none_callback])
        buttons.append(["+2", "+3", "+4"])
        callback.append([self.none_callback, self.none_callback, self.none_callback])
        buttons.append(["\ _ _ _ _ _ 15 MINUTES _ _ _ _ _ /"])
        callback.append([self.none_callback])
        buttons.append(["-5", " 0 ", "+5"])
        callback.append([self.none_callback, self.none_callback, self.none_callback])
        buttons.append(["+10", "+15", "+30", "+45"])
        callback.append([self.none_callback, self.none_callback, self.none_callback, self.none_callback])
        buttons.append(["Назад"])
        callback.append([self.menu_query])

        return buttons, callback

    def task_start_time(self):
        buttons, callback = [], []
        buttons.append(["Выбор месяца"])
        callback.append([query.generate("EDIT_KB", "task", "keyboard", task_id=self.task.id, type="123")])
        buttons.append(["Выбор недели"])
        callback.append([query.generate("EDIT_KB", "task", "keyboard", task_id=self.task.id, type="123")])
        buttons.append(["Выбор дня"])
        callback.append([query.generate("EDIT_KB", "task", "keyboard", task_id=self.task.id, type="123")])

        return buttons, callback


class generate_all:
    def __init__(self, permissions=None):
        self.permissions = permissions

    def right_keyboard(self, buttons, callback, reply, inline):
        if reply:
            return keyboard.reply(buttons)
        elif inline:
            return keyboard.inline(buttons, callback)
        else:
            return buttons, callback

    def main(self):
        return self.main_msg(), self.main_kb(inline=True)

    def main_msg(self):
        return ("Управлять своей жизнью просто")

    def main_kb(self, reply=False, inline=False):
        buttons, callback = [], []
        buttons.append(["Create TASK"])
        callback.append([
            query.generate("NEW_MSG", "main", "create_task")
        ])
        buttons.append(["WORK FLOW"])
        callback.append([
            query.generate("NEW_MSG", "main", "work_flow")
        ])
        return self.right_keyboard(buttons, callback, reply, inline)

    class any:
        def __init__(self, reply=False, inline=False):
            self.reply, self.inline = reply, inline
            self.buttons, self.callback = [], []
            self.text = str()

        def gen(self):
            return self.text, self.keyboard

        def add_line(self, buttons, callback):
            self.buttons.append(buttons)
            self.callback.append(callback)

        def right_keyboard(self):
            if self.reply:
                self.keyboard = keyboard.reply(self.buttons)
            elif self.inline:
                self.keyboard = keyboard.inline(self.buttons, self.callback)
            else:
                self.keyboard = self.buttons, self.callback

    class task(any):
        def __init__(self, task):
            any.__init__(self, inline=True)
            self.buttons, self.callback = [], []
            self.reply = False
            self.inline = True
            self.task = task
            self.gen_msg()
            self.gen_kb()
            self.right_keyboard()

        def gen_msg(self):
            self.text = (
                f"***TASK #{self.task.id}\n***"
                f"{self.task.name}"
            )

        def gen_kb(self):
            buttons, callback = [], []
            if self.task.type == None:
                self.gen_kb_type()
            else:
                buttons.append(["Тип задачи"])
                callback.append([query.generate("EDIT_KB", "task", "select_type")])
                if self.task.type == 0:
                    buttons.append(["Время начала", "Время окончания"])
                    callback.append([
                        query.generate("EDIT_KB", "task", "select_start_time"),
                        query.generate("EDIT_KB", "task", "select_end_time")
                    ])

                buttons.append(["Продолжительность"])
                callback.append([query.generate("EDIT_KB", "task", "select_duration")])
            self.buttons += buttons
            self.callback += callback

        def gen_kb_type(self):
            buttons, callback = [], []

            buttons.append(["[hh:mm-time]"])
            callback.append(
                [query.generate("EDIT_KB", "task", "update", task_id=self.task.id, parameter="type", value=0)])
            buttons.append(["result-orientation"])
            callback.append(
                [query.generate("EDIT_KB", "task", "update", task_id=self.task.id, parameter="type", value=1)])
            buttons.append(["ONE-STEP-JOB"])
            callback.append(
                [query.generate("EDIT_KB", "task", "update", task_id=self.task.id, parameter="type", value=2)])

            print(f"\n\n{self.task.type}\n\n")
            if self.task.type != None:
                print("okokok")
                buttons[self.task.type] = ["--"] + buttons[self.task.type] + ["--"]
                none_callback = query.generate("NOTHING", ".", ".")
                callback[self.task.type] = [none_callback, none_callback, none_callback]

            self.buttons += buttons
            self.callback += callback

    def scroll_kb(self, pos, count, module="objects", reply=False, inline=False):
        buttons, callback = [], []
        buttons.append(["<<", f"{pos+1}/{count}", ">>"])
        callback.append([
            query.generate("EDIT_MSG_AND_KB", module, "scroll_left", from_pos=pos),
            query.generate("EDIT_KB", module, "select_from_all"),
            query.generate("EDIT_MSG_AND_KB", module, "scroll_right", from_pos=pos)
        ])
        return self.right_keyboard(buttons, callback, reply, inline)

    def select_from_all_kb(self, pos, count, module="objects", reply=False, inline=False):
        buttons, callback = [], []

        # no more than 8 buttons per line
        count_lines = count // 8 + int(count % 8 != 0)
        lines = [8 for i in range(count_lines)]
        extra = (8 * count_lines) - count

        # distribution extra
        i = count_lines - 1
        while extra > 0:
            lines[i] -= 1;
            extra -= 1
            i = int(i > 0) * (i - 1) + int(i == 0) * (count_lines - 1)

        pos_now = 0
        for line_len in lines:
            line_text, line_callback = [], []
            for i in range(line_len):
                line_text.append(f"{pos_now+1}")
                if pos_now != pos:
                    line_callback.append(
                        query.generate("EDIT_MSG_AND_KB", module, "select", pos=pos_now)
                    )
                else:
                    line_callback.append(
                        query.generate("EDIT_KB", module, "return_to_scroll")
                    )
                pos_now += 1
            buttons.append(line_text)
            callback.append(line_callback)

        return self.right_keyboard(buttons, callback, reply, inline)

    def new_timer(self):
        return self.new_timer_msg(), self.new_timer_kb(inline=True)

    def new_timer_msg(self):
        text = "Выберите прожолжительность таймера"
        return text

    def new_timer_kb(self, reply=False, inline=False):
        buttons, callback = [], []
        buttons.append(["5 минут", "10 минут", "15 минут"])
        callback.append([
            query.generate("NEW_MSG", "main", "timer", duration=5),
            query.generate("NEW_MSG", "main", "timer", duration=10),
            query.generate("NEW_MSG", "main", "timer", duration=15)
        ])
        buttons.append(["30 минут", "60 минут"])
        callback.append([
            query.generate("NEW_MSG", "main", "timer", duration=30),
            query.generate("NEW_MSG", "main", "timer", duration=60)
        ])
        return self.right_keyboard(buttons, callback, reply, inline)

    def set_timer(self):
        return self.__set_timer_msg__(), None

    def __set_timer_msg__(self):
        return ("До окончания осталось:\n{time}")
