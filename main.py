import os
import shutil
import time
import tkinter as tk
from PIL import ImageTk, Image


class App:
    PARAMETRS = ['Создать директорию', 'Переименовать файл', 'Переименовать директорию', 'Выйти']

    def __init__(self, root, path):
        self.root = root
        self.path = path
        self.error_message = ''
        self.timestamp = False
        
        self.dirs = []
        self.files = []
        self.selected_file = ''

        self.height_window = self.root.winfo_screenheight()
        self.width_window = self.root.winfo_screenwidth() * 0.4
        
        self.get_dirs()
        self.get_files()
        self.total_files = len(self.files)
        self._select_file()
        self.dict_parameters = {i: parameters for i, parameters in enumerate(self.dirs + self.PARAMETRS, 1)}

        self.c = tk.Canvas(self.root, width=self.width_window, height=self.height_window)
        self.c.pack()
        self.main()

    def view_photo(self, image):
        img = Image.open(image)
        self.width_percent = self.width_window / float(img.size[0])
        self.height_size = int(float(img.size[1]) * float(self.width_percent))
        img = img.resize((int(self.width_window), self.height_size))
        self.imgtk = ImageTk.PhotoImage(img)
        self.c.create_image(self.width_window // 2, self.height_window // 2, image=self.imgtk)
        img.close()

    def get_dirs(self):
        self.dirs = []
        all_objects = os.listdir(self.path)
        for object in all_objects:
            path_dir = self.path + "/" + object
            if os.path.isdir(path_dir):
                self.dirs.append(path_dir)
    
    def get_files(self):
        all_objects = os.listdir(self.path)
        for object in all_objects:
            path_file = self.path + '/' + object
            if os.path.isfile(path_file):
                self.files.append(path_file)

    def rename_file(self):
        name = input('Введите новое имя: ')
        _, ext = os.path.splitext(self.selected_file)
        try:
            if self.timestamp:
                name += str(int(time.time()))
            os.rename(self.selected_file, f'{self.path}/{name}{ext}')
            self.selected_file = f'{self.path}/{name}{ext}'
        except FileExistsError:
            self.error_message = "Файл с таким именем уже существует"         
    
    def rename_dir(self, number_dir):
        name = input('Введите новое имя: ')
        
        try:
            os.rename(self.dict_parameters[number_dir], f'{self.path}/{name}')
            self.get_dirs()
            self._update_parameters()
        except FileExistsError:
            self.error_message = "Файл с таким именем уже существует"   

    def create_dir(self):
        name_dir = input('Введите название директории: ')
        try:
            os.mkdir(self.path + '/' + name_dir)
            self.get_dirs()
            self._update_parameters()
        except FileExistsError:
            self.error_message = 'Директория с таким названием уже существует'

    def _update_parameters(self):
        self.dict_parameters = {i: parameters for i, parameters in enumerate(self.dirs + self.PARAMETRS, 1)}

    def exit_app(self):
        self.root.destroy()

    def _select_file(self):
        self.selected_file = self.files.pop(0)

    def move_file(self, number_dir):
        try:
            shutil.move(self.selected_file,self.dict_parameters[number_dir])
            self._select_file()
            self.total_files -= 1
        except shutil.Error:
            self.error_message = 'Файл с таким именем уже существует в данной директории'

    def get_info_file(self):
        if self.error_message:
            print(f'Ошибка: {self.error_message}')
        self.error_message = ''
        print(f'Всего файлов в директории: {self.total_files}')
        file_size = round(os.path.getsize(self.selected_file) / 1_048_576, 3)
        print(f'Файл: {os.path.basename(self.selected_file)}')
        print(f'Размер файла (мб): {file_size}')
        
    def main(self):
        timestamp_flags = input('Ставить метку времени при изменении имени файла (д/н): ')
        while timestamp_flags.lower() not in ('д', 'н'):
            print('Введите либо "д", либо "н"')
            timestamp_flags = input('Ставить метку времени при изменении имени файла (д/н): ')
        if timestamp_flags == 'д':
            self.timestamp = True
        while True:
            os.system('cls')
            self.get_info_file()
            self.view_photo(self.selected_file)
            counter = 0
            for i in self.dict_parameters:
                print(f'{i} - {self.dict_parameters[i].split('/')[-1]}'.ljust(20), end=' ')
                counter += 1
                if counter == 3:
                    print('\n', end='')
                    counter = 0
            print()
            answer = input('Что сделать: ')
            
            if not answer.isdigit():
                self.error_message = 'Введите число'
                continue

            answer = int(answer)
            if answer <= len(self.dirs):
                self.move_file(answer)
            elif answer == len(self.dirs) + 1:
                self.create_dir()
            elif answer == len(self.dirs) + 2:
                self.rename_file()
            elif answer == len(self.dirs) + 3:
                number_dir = int(input('Введите номер директории: '))
                self.rename_dir(number_dir)
            elif answer == len(self.dirs) + 4:
                self.exit_app()
                return

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("-0+0")
    path = input('Введите путь к файлам и директориям: ')

    app = App(root, path)
    root.mainloop()
