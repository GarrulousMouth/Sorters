from pathanalyzer import *

path_dirs = {'audio': 'audio', 'video': 'video', 'image': 'image'}

def create_dirs(path, auto=False):
    list_dir = ['image', 'audio', 'video'] if auto else path_dirs.values()
    for name in list_dir:
        new_path = path.joinpath(name)
        if not new_path.exists():
            new_path.mkdir()

def sorter_files(path):
    for file in path.generator_files:
        for key in path.EXTENSIONS:
            if file.suffix[1:].lower() in path.EXTENSIONS[key] and path_dirs[key]:
                # print(path.path.joinpath(path_dirs[key]))
                shutil.move(file, path.path.joinpath(path_dirs[key]))


if __name__ == '__main__':
    path = input('Введите путь к файлам и директориям: ')
    object_path = PathAnalyzer(path)
    path =  object_path.path
    print('Будут созданы папки - audio, video, image')
    auto_dirs = input('Создать автоматически папки? (д/н): ')
    auto = False
    if auto_dirs == 'д':
        auto = True
    else:
        print('Если директории отсутствуют, то будут созданы')
        path_dirs['audio'] = input('Введите название директоии с аудио: ')
        path_dirs['video'] = input('Введите название директоии с видео: ')
        path_dirs['image'] = input('Введите название директоии с изображениями: ')
    create_dirs(path, auto)
    sorter_files(object_path)
    




    