from tkinter import *
from tkinter import messagebox
import random
import json


class HeatmapGenerator:
    """heatmap клавиш с ошибками

    Attributes:
        error_data (dict): Словарь, ключи которого - символы с ошибками, значения - количество ошибок
    """
    def __init__(self):
        self.error_data = {}

    def update_error_data(self, correct_word, user_input):
        """Данные об ошибках, сравнивая правильное слово с вводом пользователя

               Args:
                   correct_word (str): Правильное слово для ввода.
                   user_input (str): Введенное пользователем слово.
               """
        for expected_char, input_char in zip(correct_word, user_input):
            if expected_char != input_char:
                if expected_char not in self.error_data:
                    self.error_data[expected_char] = 0
                self.error_data[expected_char] += 1

    def generate_heatmap(self):
        # Сортировка словаря по значениям в порядке убывания и взятие первых трех элементов
        top_errors = sorted(self.error_data.items(), key=lambda item: item[1], reverse=True)[:3]
        heatmap = "Top 3 Keyboard Errors:\n"
        for char, count in top_errors:
            heatmap += f"{char}: {count}\n"
        return heatmap


class UserStats:
    """Управляет загрузкой, сохранением и обновлением пользовательской статистики.
            filename (str): Путь к файлу JSON для сохранения статистики.
            user_data (dict): Данные пользователя, загруженные из файла.
        """
    def __init__(self, filename='user_stats.json'):
        self.filename = filename
        self.user_data = self.load_stats()

    def load_stats(self):
        """Пользовательская статистика из файла JSON

        Returns:
            dict: Словарь с данными пользовательской статистики.
        """
        try:
            with open(self.filename, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_stats(self):
        """Текущая пользовательская статистика в файл JSON"""
        with open(self.filename, 'w') as file:
            json.dump(self.user_data, file, indent=4)

    def update_stats(self, session_results):
        """Обновляем статистику сессии и сохраняем"""
        self.user_data['sessions'] = self.user_data.get('sessions', []) + [session_results]
        self.save_stats()



class TypingTrainer:
    """Основной класс Игры

        master (Tk): Главное окно приложения.
        user_stats (UserStats): Управление статистикой пользователя.
        heatmap_generator (HeatmapGenerator): Генератор тепловой карты ошибок.
        attempts (int): Количество попыток пользователя.
        correct_word (int): Количество правильно введенных слов.
        wrong_word (int): Количество ошибочно введенных слов.
        timeleft (int): Оставшееся время сессии.
        i (int): Счетчик для анимации.
        words_amount (int): Количество введенных слов.
        word_list (list): Список слов для ввода.
    """
    def __init__(self, master):
        self.master = master
        self.master.title("Typing Trainer Game")
        self.master.iconbitmap("icon.ico")
        self.master.geometry("700x600+250+50")
        self.master.configure(background="azure")
        self.master.resizable(False, False)

        self.user_stats = UserStats()
        self.heatmap_generator = HeatmapGenerator()

        self.attemtps = 1
        self.correct_word = 0
        self.wrong_word = 0
        self.timeleft = 60
        self.i = 0
        self.words_amount = 0

        self.word_list = []
        self.load_words_from_files()

        self.init_widgets()
        self.slider()
        self.set_new_word()

        self.master.bind("<Return>", self.play_game)

    def load_words_from_files(self):
        filepath = r"C:\Users\Legion\PycharmProjects\TypingTrainer\.venv\sample.txt"
        with open(filepath, "r") as file:
            text = file.read()
            self.word_list = text.split()


    def init_widgets(self):
        # Установка и расположение всех виджетов
        self.logoImage = PhotoImage(file="clock.png")
        self.logoLabel = Label(self.master, image=self.logoImage, bg="azure")
        self.logoLabel.place(x=220, y=50)

        self.movingLabel = Label(self.master, text='', bg="azure",
                                 font=("Arial", 25, "bold"), width=35, fg='red')
        self.movingLabel.place(x=0, y=10)

        self.word_list_Label = Label(self.master, text='', bg="azure",
                                     font=("cooper black", 38, "italic bold"))
        self.word_list_Label.place(x=350, y=350, anchor=CENTER)

        self.wordLabel = Label(self.master, text='Words', bg="azure",
                               font=("Castellar", 22, "bold"))
        self.wordLabel.place(x=30, y=100)

        self.countLabel = Label(self.master, text='0', bg="azure",
                                font=("Castellar", 28, "bold"))
        self.countLabel.place(x=80, y=180)

        self.timeLabel = Label(self.master, text='Time Left', bg="azure",
                               font=("Castellar", 22, "bold"))
        self.timeLabel.place(x=510, y=100)

        self.time_countLabel = Label(self.master, text='60', bg="azure",
                                     font=("Castellar", 28, "bold"))
        self.time_countLabel.place(x=560, y=180)

        self.wordEntry = Entry(self.master, font=("Arial", 25, "bold"), bd=8, relief=SUNKEN, justify='center')
        self.wordEntry.place(x=190, y=390)
        self.wordEntry.focus_set()

        self.instructionLabel = Label(self.master, text='Type Word and Hit Enter', bg="azure",
                                      font=("Chiller", 28, "bold"), fg='firebrick1')
        self.instructionLabel.place(x=210, y=460)

        self.happypic = PhotoImage(file="happy_emoji.png")
        self.sadpic = PhotoImage(file="sad_emoji.png")

        self.emoji1Label = Label(self.master, bg="azure")
        self.emoji1Label.place(x=80, y=490)

        self.emoji2Label = Label(self.master, bg="azure")
        self.emoji2Label.place(x=540, y=490)

        self.master.bind("<Return>", self.play_game)

        self.heatmap_display = Label(self.master, text="", font=("Arial", 12), bg="azure")
        self.heatmap_display.place(x=25, y=320)

    def set_new_word(self):
        """ Установка нового слова для ввода пользователем  """
        if not self.word_list:
            self.instructionLabel.config(text="No words loaded!")
            return
        random.shuffle(self.word_list)
        self.word_list_Label.config(text=self.word_list[0])

    def slider(self):
        """ Отображение Анимированного текста """
        slider_text = 'Welcome to Typing Trainer Game'
        display_text = slider_text[:self.i % len(slider_text) + 1]
        self.i +=1
        self.movingLabel.config(text=display_text)
        self.movingLabel.after(250, self.slider)

    def timer(self):
        """ Реализация Таймера игры """
        if self.timeleft > 0:
            self.timeleft -= 1
            self.time_countLabel.config(text=self.timeleft)
            self.time_countLabel.after(1000, self.timer)
        else:
            self.end_game()


    def play_game(self, event):
        """ Обработка игры после ввода слова и нажатия клавиши Enter """
        user_input = self.wordEntry.get()
        if user_input:
            self.words_amount += 1
            self.countLabel.config(text=str(self.words_amount))
            self.instructionLabel.config(text='')
            if self.timeleft == 60:
                self.timer()
            self.check_word(user_input)
            self.heatmap_generator.update_error_data(self.word_list_Label['text'], user_input)
            self.update_heatmap_display()
            self.set_new_word()
            self.wordEntry.delete(0, END)

    def update_heatmap_display(self):
        """ Обновление тепловой карты после каждого случая ошибки """
        heatmap_info = self.heatmap_generator.generate_heatmap()
        self.heatmap_display.config(text=heatmap_info)


    def check_word(self, word):
        """ Сверка напечатаного и дейтсвительного слова """
        if word == self.word_list_Label['text']:
            self.correct_word += 1
        else:
            self.wrong_word += 1


    def set_new_word(self):
        """ Установка нового слова для ввода """
        if not self.word_list:
            self.instructionLabel.config(text="No words loaded!")
            return
        random.shuffle(self.word_list)
        self.word_list_Label.config(text=self.word_list[0])

    def end_game(self):
        """Завершает игровую сессию и обрабатывает результаты"""
        self.wordEntry.config(state=DISABLED)
        result = self.correct_word - self.wrong_word
        self.instructionLabel.config(
            text=f'Correct words: {self.correct_word}\n Wrong words: {self.wrong_word}\n Final Score: {result}')
        self.emoji1Label.config(image=self.happypic if result >= 15 else self.sadpic)
        self.emoji2Label.config(image=self.happypic if result >= 15 else self.sadpic)

        # heatmap с тремя наиболее частыми ошибками
        heatmap_info = self.heatmap_generator.generate_heatmap()
        self.heatmap_display.config(text=heatmap_info)

        # сохранение статистики
        self.user_stats.update_stats({
            'correct': self.correct_word,
            'wrong': self.wrong_word,
            'attempts': self.attemtps
        })

        if messagebox.askyesno('Confirm', 'Do you want to play again?'):
            self.reset_game()
            self.attemtps += 1

    def reset_game(self):
        """ Обнуление параметров для повторной игры """
        self.i = 0
        self.words_amount = 0
        self.correct_word = 0
        self.wrong_word = 0
        self.timeleft = 60
        self.countLabel.config(text='0')
        self.time_countLabel.config(text='60')
        self.wordEntry.config(state=NORMAL)
        self.instructionLabel.config(text='Type Word and Hit Enter')
        self.emoji1Label.config(image='')
        self.emoji2Label.config(image='')
        self.set_new_word()


if __name__ == "__main__":
    root = Tk()
    app = TypingTrainer(root)
    root.mainloop()