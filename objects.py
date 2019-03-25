import database
import generate
import keyboard
import random
from query import query


class Objects:
    def __init__(self):
        self.type = type(self).__name__

    # def right_position(self, pos, count):
    #     max_pos = count - 1
    #     pos = pos - pos * int(pos > max_pos)
    #     pos = pos + (max_pos - pos) * int(pos < 0)
    #     return pos


class Tasks(Objects):

    def __init__(self):
        Objects.__init__(self)
        all_data = database.table("tasks").select_all(to_dict=True)
        self.all = [Task().get(data) for data in all_data]
        self.byid = {_task.id: _task for _task in self.all}

    def new(self, name):
        new_task = Task().create(name)
        self.add(new_task)
        return new_task

    def add(self, task):
        self.all.append(task)
        self.byid[task.id] = task


class UnusualTasks(Objects):
    def __init__(self):
        Objects.__init__(self)

    class orthoepy:
        def __init__(self, user_tid=None):
            self.user_tid = user_tid
            self.effect = "EDIT_MSG_AND_SEND_NEW"
            self.module = "orthoepy"
            self.event = "answer"
            self.vowels = "а, о, и, е, ё, э, ы, у, ю, я".replace(",", "").split()
            self.vowels_up = [vowel.upper() for vowel in self.vowels]
            self.word_types = self.all_words()
            self.word_count = sum([len(self.word_types[type]) for type in self.word_types.keys()])

        def new(self):
            number = random.randint(1, self.word_count)
            object = database.table("orthoepy").select("*", "id", number, to_dict=True)[0]
            word = object["word"]
            vowels_pos = [i for i, char in enumerate(word) if char in self.vowels]
            buttons = [word[0:num] + word[num].upper() + word[num + 1:] for num in vowels_pos]
            callback = [
                query.generate(self.effect, self.module, self.event,
                               user_tid=self.user_tid, word_id=object["id"], answer=bool(i + 1 == object["syllable"]))
                for i, num in enumerate(vowels_pos)
            ]
            return word, keyboard.inline(buttons, callback)

        def get_word(self):
            return ("звонит")

        def all_words(self):
            word_types = {}
            word_types["Имя существительное"] = """
             аэропОрты, неподвижн. ударение на 4-ом слоге
             бАнты, неподвижн. ударение на 1-ом слоге
             бОроду, вин.п.,только в этой форме ед.ч., ударение на 1-ом слоге
             бухгАлтеров, род.п.мн.ч., неподвижное, ударение на 2-ом слоге
             вероисповЕдание, от веру исповЕдать
             граждАнство
             дефИс, из нем.яз., где ударение на 2-ом слоге
             диспансЕр, слово пришло из англ. яз. Через посредство франц.яз., где  удар. всегда на последнем слоге
             договорЁнность
             докумЕнт
             досУг
             еретИк
             жалюзИ, из франц. яз., где удар. всегда на последнем слоге
             знАчимость, от прил. знАчимый
             Иксы, им.п. мн.ч., неподвижн. ударение
             каталОг, в одном ряду со словами диалОг,
             монолОг, некролОг т.п.
             квартАл, из нем. яз., где ударение на 2-ом слоге
             киломЕтр, в одном ряду со словами: сантимЕтр, децимЕтр, миллимЕтр…
             кОнусы, кОнусов, неподвиж. ударение на 1-м слоге во всех падежах в  ед. и мн. ч.
             корЫсть
             крАны, неподвижн. ударение на 1-ом слоге
             кремЕнь, кремнЯ, удар. во всех формах на последнем слоге, как и в  слове огОнь
             лЕкторы, лЕкторов, см. слово бант(ы)
             лыжнЯ
             мЕстностей, род.п. мн.ч., в одном ряду со словоформой пОчестей,  чЕлюстей…, но новостЕй
             мусоропровОд, в одном ряду со словами газопровОд, нефтепровОд, водопровОд
             намЕрение	
             нарОст
             нЕдруг
             недУг
             некролОг, см. каталОг
             нЕнависть
             нОвости, новостЕй, но: см. мЕстностей
             нОготь, нОгтя, неподвижн. ударение во всех формах ед.ч.
             Отрочество, от Отрок- подросток
             партЕр, из франц. яз., где удар. всегда на последнем слоге
             портфЕль
             пОручни
             придАное
             призЫв, в одном ряду со словами позЫв,
             отзЫв (посла), созЫв, но: Отзыв (на публикацию)
             свЁкла
             сирОты, им.п.мн.ч., ударение во всех формах мн.ч. только на 2-ом  слоге
             срЕдства, им.п.мн.ч.
             созЫв, см. призЫв
             стАтуя
             столЯр, в одном ряду со словами малЯр, доЯр, школЯр…
             тамОжня
             тОрты, тОртов
             цемЕнт
             цЕнтнер
             цепОчка
             шАрфы, см. бАнты
             шофЁр, в одном ряду со словами: киоскЁр, контролЁр…
             экспЕрт, из франц. яз., где ударение всегда на последнем слоге             
            """.split("\n")
            word_types["Имя прилагательное"] = """
             вернА, краткое прилаг. ж.р. знАчимый
             красИвее, прил.и нареч. в сравн.ст. 
             красИвейший, превосх.ст.
             кУхонный
             ловкА, краткое прилаг. ж.р.	 мозаИчный
             оптОвый
             прозорлИва, краткое прилаг. ж.р., в одном
             ряду со словами смазлИва, суетлИва,
             болтлИва..., но: прожОрлива
             слИвовый, образовано от слИва
            """.split("\n")
            word_types["Глагол"] = """
             баловАть, в одном ряду со словами баловАться, избаловАть,  разбаловАть…, но: бАловень судьбы брать-бралА
             брАться-бралАсь
             взять-взялА
             взЯться-взялАсь
             включИть-включИшь,
             включИт, включИм
             влИться-влилАсь
             ворвАться-ворвалАсь
             воспринЯть-воспринялА
             воссоздАть-воссоздалА
             вручИть-вручИт
             гнАть-гналА
             гнАться-гналАсь
             добрАть-добралА
             добрАться-добралАсь
             дождАться-дождалАсь
             дозвонИться-дозвонИтся,
             дозвонЯтся
             дозИровать
             ждать-ждалА
             жИться-жилОсь
             закУпорить
             занЯть-зАнял, занялА,
             зАняло, зАняли
             заперЕть-заперлА
             заперЕться-заперлАсь (на ключ, на замок и т.п.)
             звать-звалА, звонИть, звонИшь, звонИт, звонИм
             исчЕрпать
             клАсть-клАла
             клЕить
             крАсться — крАлась
             лгать-лгалА
             лить-лилА
             лИться-лилАсь
             наврАть-навралА
             наделИть-наделИт
             надорвАться-надорвалАсь
             назвАться-назвалАсь
             накренИться-накренИтся
             налИть-налилА
             нарвАть-нарвалА
             насорИть-насорИт
             начАть-нАчал, началА, нАчали
             обзвонИть-обзвонИт	 облегчИть-облегчИт
             облИться-облилАсь
             обнЯться-обнялАсь
             обогнАть-обогналА
             ободрАть-ободралА
             ободрИть
             ободрИться-ободрИшься
             обострИть
             одолжИть-одолжИт
             озлОбить
             оклЕить
             окружИть-окружИт
             опломбировАть, в одном ряду со словами формировАть,  нормировАть, сортировАть, премировАть…
             опОшлить
             освЕдомиться-освЕдомишься
             отбЫть-отбылА
             отдАть-отдалА
             откУпорить-откУпорил
             отозвАть-отозвалА
             отозвАться-отозвалАсь
             перезвонИть — перезвонИт
             перелИть-перелилА
             плодоносИть
             повторИть-повторИт
             позвАть-позвалА
             позвонИть-позвонИшь-позвонИт
             полИть-полилА
             положИть-положИл
             понЯть-понялА
             послАть-послАла
             прибЫть-прИбыл-прибылА-прИбыло
             принЯть-прИнял-прИняли-принялА
             принУдить
             рвАть-рвалА
             сверлИть-сверлИшь-сверлИт
             снЯть-снялА
             создАть-создалА
             сорвАть-сорвалА
             сорИть-сорИт
             убрАть-убралА
             убыстрИть
             углубИть
             укрепИть-укрепИт
             чЕрпать
             щемИть-щемИт
             щЁлкать
            """.split("\n")
            word_types["Причастие"] = """
              балОванный
             включЁнный-включЁн, см. низведЁнный
             довезЁнный
             зАгнутый
             зАнятый-занятА
             зАпертый-запертА
             заселЁнный-заселенА
             избалОванный, см. балОванный
             кормЯщий
             кровоточАщий
             молЯщий
             нажИвший
             нАжитый-нажитА
             налИвший-налитА
             нанЯвшийся	
             начАвший
             нАчатый
             низведЁнный-низведЁн, см. включЁнный…
             ободрЁнный-ободрЁн-ободренА
             обострЁнный
             отключЁнный
             определЁнный-определЁн
             отключЁнный
             повторЁнный
             поделЁнный
             понЯвший
             прИнятый
             приручЁнный
             прожИвший
             снЯтый-снятА
             сОгнутый
            """.split("\n")
            word_types["Деепричастие"] = """
             балУясь
             закУпорив
             начАв
             начАвшись	 отдАв
             поднЯв
             понЯв
             прибЫв
            """.split("\n")
            word_types["Наречие"] = """
             вОвремя
             добелА
             дОверху
             донЕльзя
             дОнизу
             дОсуха
             завИдно, в значении сказуемого	 зАгодя, разговорное
             зАсветло
             зАтемно
             красИвее, прил.и нареч. в сравн.ст.
             навЕрх
             надОлго
             ненадОлго
            """.split("\n")
            return word_types

        def config_orthoepy(self):
            for type in list(self.word_types.keys()):
                for line in self.word_types[type]:
                    self.add_word(line, type)

        def add_word(self, string, part_of_speech=None):
            string = string.replace("  ", " ").replace("    ", " ").replace("\n", "")
            words = string.replace(",", " ").replace("-", " ").split()
            work_words = [word for word in words if any(char in self.vowels_up for char in word)]
            for word in work_words:
                word_vowels = [char for char in word if char.lower() in self.vowels]
                if len(word_vowels) > 1:
                    for i, vowel in enumerate(word_vowels):
                        if vowel.isupper():
                            syllable = i + 1
                    word = word.lower()
                    database.table("orthoepy").insert(["word", "syllable", "description", "part_of_speech"],
                                                  [word, syllable, string, part_of_speech])


class Task:
    def get(self, data_dict: dict):
        [setattr(self, name, data_dict[name]) for name in data_dict.keys()]
        return self

    def create(self, name: str):
        database.table("tasks", logging=True).insert("name", name)
        data = database.table("tasks").select_by_max("*", "id", to_dict=True)[0]
        return self.get(data)

    def update(self, **kwargs):
        upd_fields, upd_values = list(kwargs.keys()), list(kwargs.values())
        database.table("tasks", logging=True).update("id", self.id, upd_fields, upd_values)
        [setattr(self, field, value) for (field, value) in zip(upd_fields, upd_values)]

    def keyboard(self, type=None):
        if type is None:
            result = generate.Task(self).main_kb()
        elif type == "main":
            result = generate.Task(self).main_kb()
        elif type == "task_type":
            result = generate.Task(self).task_type_kb()
        elif type == "periodicity":
            result = generate.Task(self).periodicity()
        elif type == "periodicity_everyweek":
            result = generate.Task(self).periodicity("everyweek")
        elif type == "duration":
            result = generate.Task(self).duration()
        elif type == "start_time":
            result = generate.Task(self).task_start_time()

        return keyboard.inline(*result)

    def message(self):
        return generate.Task(self).message()


if __name__ == "__main__":
    orthoepy = UnusualTasks().orthoepy()
    orthoepy.config_orthoepy()
