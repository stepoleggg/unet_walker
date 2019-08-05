import cv2
import os
import re

def make_video(files, folder, name, fps=24):
    """
        Создает видео из изображений в папке data\predict
    """
    out = cv2.VideoWriter(f"video\{name}.mp4", cv2.VideoWriter_fourcc(*'mp4v'), fps, (1280, 720))
    files.sort(key = lambda x: int(re.search(r'\d+', x).group()))
    for file in files:
        print(f"data\predict\{folder}\{file}")
        out.write(cv2.imread(f"data\predict\{folder}\{file}"))
    out.release() 
    cv2.destroyAllWindows()
    print(f"Видео сохранено video\{name}.mp4")

folder = input("Введите название папки с png в data\predict\: ")
files = os.listdir(path=os.getcwd()+f"\data\predict\{folder}")
fps = input("Введите fps: ")
name = input("Введите имя видео для сохранения: ")
make_video(files, folder, name, fps=int(fps))