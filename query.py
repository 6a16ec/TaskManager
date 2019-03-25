from builtins import setattr, enumerate, int, str, type, list, map, dict, len
import re

class query:

        # \____|_____|_____<INIT>____|____|____/ #
    def args_by(self = None):
        args_by_module_and_event, args_by_module, args_by_event = dict(), dict(), dict()

        # -- # ---- # -- #
        args_by_module_and_event["main_timer"] = ["duration"]
        args_by_module_and_event["task_update"] = ["task_id", "parameter", "value"]
        args_by_module_and_event["task_keyboard"] = ["task_id", "type"]
        # -- # ---- # -- #
        args_by_event["scroll_left"] = ["from_pos"]
        args_by_event["scroll_right"] = ["from_pos"]
        # -- # ---- # -- #
        args_by_module["orthoepy"] = ["user_tid", "word_id", "answer"]

        return (args_by_module_and_event, args_by_module, args_by_event)

    def __init__(self, query, full = True):
        self.query = query
        effect = re.search(r"#[^ ]+", query)
        if effect:
            self.effect = effect.group()[1:]
        else:
            self.effect = "NOTHING"
        if full:
            self.module = re.search(r"@[^ ]+", query).group()[1:]
            self.event = re.search(r"[$][^ ]+", query).group()[1:]
            self.variables = self.parse_variables()

            self.args_by_module_and_event, self.args_by_module, self.args_by_event = self.args_by()
            self.useful_variables()


        # \____|_____|_____<VARIABLES>____|____|____/ #

    def parse_variables(self):
        vars = re.search(r"[(].+[)]", self.query)
        if vars:
            vars_str = vars.group()[1:-1]
            variables = vars_str.replace(" ", "").split(",")
            variables = list(map(self.right_type, variables))
            return variables
        else:
            return list()

    def useful_variables(self):
        names = []
        if f"{self.module}_{self.event}" in self.args_by_module_and_event:
            names = self.args_by_module_and_event[f"{self.module}_{self.event}"]
        elif self.event in self.args_by_event:
            names = self.args_by_event[self.event]
        elif self.module in self.args_by_module:
            names = self.args_by_module[self.module]
        if names:
            [setattr(self, name, self.variables[i]) for (i, name) in enumerate(names)]


        # \____|_____|_____<HELPS>____|____|____/ #
    def right_type(self, string):
        if string.lstrip("-").isdigit():
            return int(string)
        if string == "True" or string == "False":
            return (string == "True")
        if string == "None":
            return None
        return string


        # \____|_____|_____<OTHER>____|____|____/ #
    def generate(effect, module, event, **kwargs):
        names = []
        args_by_module_and_event, args_by_module, args_by_event = query.args_by()

        if f"{module}_{event}" in args_by_module_and_event:
            names = args_by_module_and_event[f"{module}_{event}"]
        elif event in args_by_event:
            names = args_by_event[event]
        elif module in args_by_module:
            names = args_by_module[module]

        if names:
            variables = [kwargs[name] if name in kwargs.keys() else None for name in names]
            vars_str = ", ".join([str(var) for var in variables])
            return (f"#{effect} @{module} ${event} ({vars_str})")
        else:
            return (f"#{effect} @{module} ${event}")

if __name__ == "__main__":
    # info = query("#NEW_MSG @main $timer (5)")
    # print(info.duration)
    print(query.generate("EDIT_KB", "task", "update", task_id=0, parameter = "type", type=2))


    # info = query("#TEXT_KB_PHOTO @categories $test (12345, phooooto)")
    # print(info.variables)
    # print(info.position, info.photo_mid)
    # print(query.generate("EDIT_TEXT_KB_PHOTO", "categories", "lol", photo_mid = "testanem"))
    #
    # info = query("#TEXT_KB_PHOTO @main $add_category")
    # print(info.variables)
    #
    # print(query.generate("NEW_MSG", "main", "add_category"))
