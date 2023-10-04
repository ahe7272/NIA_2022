"""
타 과제 활용을 위한 코드 리펙토링

1. 중복 코드 최소화를 위한 객체 생성
2. 코드 가독성 개선 및 유지보수 용이성 개선
"""

import PySimpleGUI as sg
import os
from glob import glob
import cv2

class ImageProcessor:
    @staticmethod
    def clahe_image(img):
        b, g, r = cv2.split(img)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        clahe_b = ImageProcessor._apply_clahe_and_normalize(clahe, b)
        clahe_g = ImageProcessor._apply_clahe_and_normalize(clahe, g)
        clahe_r = ImageProcessor._apply_clahe_and_normalize(clahe, r)
        return cv2.merge((clahe_b, clahe_g, clahe_r))

    @staticmethod
    def _apply_clahe_and_normalize(clahe, channel):
        channel = clahe.apply(channel)
        return cv2.normalize(channel, None, 0, 255, cv2.NORM_MINMAX)

    @staticmethod
    def preprocess_img(image_path, savepath):
        imagenamejpg = os.path.split(image_path)[-1]
        image = cv2.imread(image_path)
        clahe_img = ImageProcessor.clahe_image(image)
        cv2.imwrite(os.path.join(savepath, imagenamejpg), clahe_img)

class MakeGUI:
    def __init__(self):
        self.window = self._makegui()

    def _makegui(self):
        sg.theme('DarkAmber')

        layout = [
            [sg.Text('데이터의 경로(폴더)', font=("Arial", 13, 'bold'), size=(40, 1))],
            [sg.InputText('Data Folder', font=("Arial", 13), size=(30,1), key='DataPath'), 
             sg.FolderBrowse('SELECT', font=("Arial", 13, 'bold'), size=(10, 1)), 
             sg.Button('Run', font=("Arial", 13, 'bold'), size=(10,1), key='Run')],
            [sg.ProgressBar(1, orientation='h', size=(40,20), key='progress')]
        ]

        return sg.Window('Clahe images', layout, element_justification='c', grab_anywhere=True).Finalize()

    def run(self):
        while True:    
            event, values = self.window.read()     
            progress_bar = self.window['progress']
            if event == 'Run':
                self._process_images(values['DataPath'], progress_bar)
            if event in (None, 'Exit'):
                break

    def _process_images(self, data_path, progress_bar):
        imagelist = glob(os.path.join(data_path, "*.jpg"))
        datalength = len(imagelist)
        progress_bar.UpdateBar(0, datalength)
        savepath = os.path.join(os.path.split(data_path)[0], f"{os.path.split(data_path)[1]}_clahed")
        os.makedirs(savepath, exist_ok=True)
        for idx, image in enumerate(imagelist, start=1):
            progress_bar.UpdateBar(idx, datalength)
            ImageProcessor.preprocess_img(image, savepath)
        if idx == datalength:
            sg.Popup('정제 완료^^!', font=("Arial", 13), keep_on_top=True)

if __name__ == "__main__":
    gui = MakeGUI()
    gui.run()
