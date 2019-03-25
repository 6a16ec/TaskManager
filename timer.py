import time
class event:
    def __init__(self, input_text, deadline):
        self.input_text = input_text
        self.deadline = deadline
        print(self.update())

    def update(self):
        current_time = int(time.time())
        delta_time = (self.deadline - current_time)
        delta_time = delta_time * (delta_time > 0)

        days, hours = int(delta_time / (60*60*24)), int(delta_time / (60*60)) % 24
        minutes, seconds = int(delta_time / (60)) % 60, delta_time % 60

        delta_str = f"{int(minutes / 10)}{minutes % 10}:{int(seconds / 10)}{seconds % 10}"
        if hours > 0:
            delta_str = f"{int(hours / 10)}{hours % 10}:" + delta_str

        return self.input_text.replace("{time}", delta_str)

if __name__ == "__main__":
    event("До конца осталось:\n{time}", 23442344)
    text = "До конца осталось:\n{time}"
    print(text.format(time = "123"))