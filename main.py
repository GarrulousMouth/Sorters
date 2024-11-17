import os
import shutil
import time
import pathlib
import tkinter as tk
from PIL import ImageTk, Image


class PathAnalyzer:
    EXTENSIONS = {
        'video': ['mp4', 'mov', 'avi', 'mkv', 'wmv', '3gp', '3g2', 'mpg', 'mpeg', 'm4v', 
              'h264', 'flv', 'rm', 'swf', 'vob'],

        'audio': ['mp3', 'wav', 'ogg', 'flac', 'aif', 'mid', 'midi', 'mpa', 'wma', 'wpl',
              'cda'],

        'image': ['jpg', 'png', 'bmp', 'ai', 'psd', 'ico', 'jpeg', 'ps', 'svg', 'tif', 
              'tiff'],
    }

    def __init__(self, path):
        self.path = pathlib.Path(path)
        self.dirs = []
        self.files = []
        self.total_files = self._total_files()

        self.generator_files = self.get_files_generator()

    def get_dirs(self):
        self.dirs = [subdirs for subdirs in self.path.iterdir() if subdirs.is_dir()]
        return self.get_dirs

    def get_files(self):
        self.files = [files for files in self.path.iterdir() if files.is_file()]
        return self.files

    def _total_files(self):
        return len([files for files in self.path.iterdir() if files.is_file()])

    def get_files_generator(self):
        for object in self.path.iterdir():
            if object.is_file():
                yield object


class SorterImage(PathAnalyzer):

    def __init__(self, root, path):
        super().__init__(path)
        self.get_dirs()
        self.__add_func()
        
        self.root = root
        self.error_message = ''
        self.timestamp = False
        self._EXIT = False
        self.selected_file = ''
        self._select_file()

        self._DIRS_PARAMETRS = [['Создать директорию', self.create_dir], 
                               ['Переименовать директорию', self.rename_dir], 
                               ['Отмена']]
        self.dict_dirs_parameters = {i: parameters for i, parameters in enumerate(self._DIRS_PARAMETRS, 1)}
        self._FILE_PARAMETRS = [['Переименовать файл', self.rename_file], 
                               ['Удалить файл', self.remove_file], 
                               ['Отмена']]
        self.dict_file_parameters = {i: parameters for i, parameters in enumerate(self._FILE_PARAMETRS, 1)}
        self._PARAMETERS = [['Далее', self.next_file], 
                          ['Редактировать файл', self.edit_file], 
                          ['Редактировать директорию', self.edit_dir], 
                          ['Выйти', self.exit_app]]
        self.dict_parameters = {i: parameters for i, parameters in enumerate(self.dirs + self._PARAMETERS, 1)}
        
        self.height_window = self.root.winfo_screenheight()
        self.width_window = self.root.winfo_screenwidth() * 0.4

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

    def __add_func(self):
        self.dirs = list(map(lambda x: [x, self.move_file], self.dirs))

    def rename_file(self):
        name = input('Введите новое имя: ')
        ext = self.selected_file.suffix
        if self.timestamp:
            name += str(int(time.time()))
        path_file = self.path.joinpath(name).with_suffix(ext)
        if path_file.exists():
            self.error_message = f'Файл с именем <{path_file.name}> уже существует'
            return
        self.selected_file = self.selected_file.replace(path_file)          
    
    def rename_dir(self):
        number_dir = int(input('Введите номер директории: '))
        name = input('Введите новое имя: ')
        path_dir = self.path.joinpath(name)
        if path_dir.exists():
            self.error_message = f'Директория с именем <{path_dir.name}> уже существует'
            return
        self.dict_parameters[number_dir][0] = self.dict_parameters[number_dir][0].replace(path_dir)

    def create_dir(self):
        name_dir = input('Введите название директории: ')
        try:
            path_dir = self.path.joinpath(name_dir)
            path_dir.mkdir()
            self.get_dirs()
            self.__add_func()
            self._update_parameters()
        except FileExistsError:
            self.error_message = f'Директория с именем <{path_dir.name}> уже существует'

    def _update_parameters(self):
        self.dict_parameters = {i: parameters for i, parameters in enumerate(self.dirs + self._PARAMETERS, 1)}

    def exit_app(self):
        self.root.destroy()
        self._EXIT = True

    def _select_file(self):
        try:
            self.selected_file = next(self.generator_files)
            while self.selected_file.suffix[1:] not in self.EXTENSIONS['image']:
                self.selected_file = next(self.generator_files)
        except StopIteration:
            self.error_message = "Были обработаны все изображения в директории"

    def move_file(self, number_dir):
        try:
            shutil.move(self.selected_file,self.dict_parameters[number_dir][0])
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

    def edit_dir(self):
        print()
        for i in self.dict_dirs_parameters:
            print(f'{i} - {self.dict_dirs_parameters[i][0]}'.ljust(20), end=' ')
        print()
        answer = int(input('Что сделать: '))
        if answer == 3:
            return
        else:
            self.dict_dirs_parameters[answer][1]()

    def edit_file(self):
        print()
        for i in self.dict_file_parameters:
            print(f'{i} - {self.dict_file_parameters[i][0]}'.ljust(20), end=' ')
        print()
        answer = int(input('Что сделать: '))
        if answer == 3:
            return
        else:
            self.dict_file_parameters[answer][1]()

    def remove_file(self):
        print('1 - да     2 - нет')
        answer = int(input('Вы уверены, что хотите удалить безвозвратно файл? - '))
        if answer == 1:
            self.selected_file.unlink()
            self._select_file()
        return

    def next_file(self):
        self._select_file()

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
                if isinstance(self.dict_parameters[i][0], pathlib.WindowsPath):
                    print(f'{i} - {self.dict_parameters[i][0].name.split('/')[-1]}'.ljust(20), end=' ')
                else:
                    print(f'{i} - {self.dict_parameters[i][0]}'.ljust(20), end=' ')
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
                self.dict_parameters[answer][1](answer)
            else:
                self.dict_parameters[answer][1]()
            if self._EXIT:
                return

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("-0+0")
    path = input('Введите путь к файлам и директориям: ')
    app = SorterImage(root, path)
    root.mainloop()
