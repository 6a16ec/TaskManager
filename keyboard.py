from aiogram import types

class Keyboard:
    def __init__(self, user_id = 0, name = "example"):
        if(name == "example"):
            self.text_array = [["example"], ["example", "example"], ["example", "example", "example"]]
            self.callback_array = [["example"], ["example", "example"], ["example", "example", "example"]]

    def remove(self):
        return None

class Reply(Keyboard):
    def get(self, resize_keyboard = True):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard = resize_keyboard)
        for line in self.text_array:
            keyboard.row(*line)
        return keyboard

    def remove(self):
        keyboard = types.ReplyKeyboardRemove()
        return keyboard

class Inline(Keyboard):

    def button(self, i, j):
        text = self.text_array[i][j]
        callback_data = self.callback_array[i][j]
        button = types.InlineKeyboardButton(text = text, callback_data = callback_data)
        return button

    def get(self):
        keyboard = types.InlineKeyboardMarkup()
        for i in range(len(self.text_array)):
            line = []
            for j in range(len(self.text_array[i])):
                line.append(self.button(i, j))
            keyboard.row(*line)
        return keyboard
