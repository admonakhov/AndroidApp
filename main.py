from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.swiper import MDSwiper, MDSwiperItem
from kivymd.uix.selectioncontrol import MDCheckbox


from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast
import os, re

images = ['1.jpg', '2.jpg', '3.jpg']




class FileManager(MDBoxLayout):
    def __init__(self):
        super(FileManager, self).__init__()
        fm_btn = MDRectangleFlatButton(text='File Manager')
        fm_btn.bind(on_press=self.file_manager_open)
        self.add_widget(fm_btn)
        self.filelist = {}
        self.file_layout = MDGridLayout(rows=1, cols=3, padding=(20, 20), spacing=(10, 10))

        self.add_widget(self.file_layout)


    def file_manager_open(self, ev=None):
        self.file_manager = MDFileManager(exit_manager=self.exit_manager, select_path=self.select_path)
        self.file_manager.show('C://users//antmo')

    def select_path(self, path):
        self.exit_manager()
        self.is_pdf(path=path)
        self.look_files()
        toast(path)

    def exit_manager(self, *args):
        self.file_manager.close()

    def is_pdf(self, path):
        if os.path.isdir(path):
            for _path, folders, files in os.walk(path):
                for file in files:
                    match = re.findall(r'\w*.pdf',file)
                    if match:
                        self.filelist[match[0]] = _path+'//'+match[0]
        elif os.path.isfile(path):
            match = re.findall(r'\w*.pdf', path)
            if match:
                self.filelist[match[0]] = path+'//'+match[0]

    def look_files(self):
         self.file_layout.clear_widgets()
         self.file_layout.rows = 1
         for i, file in enumerate(self.filelist.keys()):
            self.file_layout.rows += 1
            if len(file) > 10:
                text ='...'+file[::-1][:10][::-1]
            else:
                text = file
            self.file_layout.add_widget(MDLabel(text=str(i+1), size_hint_y=0.3, size_hint_x=0.5))
            self.file_layout.add_widget(MDLabel(text=text, size_hint_y=0.3, size_hint_x=0.5))
            self.file_layout.add_widget(MDCheckbox(active=True))




class Swiper(MDSwiper):
    def __int__(self):
        super().__int__()

    def add_any_widget(self, widget):
        tmp = MDSwiperItem()
        tmp.add_widget(widget)
        self.add_widget(tmp)


class MainApp(MDApp):
    def __int__(self, **kwargs):
        super(MainApp, self).__int__(**kwargs)


    def build(self):
        fm = FileManager()
        swiper = Swiper()
        swiper.add_any_widget(fm)
        main_layout = MDBoxLayout()

        exit_btn = MDRectangleFlatButton(text='Exit', size_hint_y=0.5, size_hint_x=0.1)
        exit_btn.bind(on_press=exit)
        main_layout.add_widget(swiper)
        main_layout.add_widget(exit_btn)


        return main_layout




MainApp().run()
