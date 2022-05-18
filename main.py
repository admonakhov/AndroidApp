import os
import re
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.swiper import MDSwiper, MDSwiperItem


width = 500
height = 1000


def add_widgets(parent, childs):
    for child in childs:
        parent.add_widget(child)

class FileManager(MDGridLayout):
    def __init__(self):
        super(FileManager, self).__init__()

        self.cols = 1
        self.rows = 2

        fm_btn = MDRectangleFlatButton(text='Choose files')
        btns = MDGridLayout(cols=2, rows=1, size_hint_y=None)
        add_widgets(btns, [fm_btn])

        self.filelist = {}
        self.file_layout = MDGridLayout(rows=1, cols=3, size_hint_x=None, width=width)
        add_widgets(self, [self.file_layout, btns])
        fm_btn.bind(on_press=self.file_manager_open)


    def accept_callback(self,  ev):
        self.checked_files = []
        for file in self.filelist.keys():
            if (self.filelist[file][1].active):
                self.checked_files.append(self.filelist[file][0])


    def file_manager_open(self, ev=None):
        self.file_manager = MDFileManager(exit_manager=self.exit_manager, select_path=self.select_path)
        self.file_manager.show('/home/ant')

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
                    match = re.findall(r'\w*.pdf', file)
                    if match:
                        self.filelist[match[0]] = _path+'/'+match[0]
                        self.filelist[match[0]] = []
                        self.filelist[match[0]].append(_path+'/'+match[0])
        elif os.path.isfile(path):
            match = re.findall(r'\w*.pdf', path)
            if match:
                self.filelist[match[0]] = path+'/'+match[0]
                self.filelist[match[0]] = []
                self.filelist[match[0]].append(path+'/'+match[0])

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
            self.filelist[file].append(MDCheckbox(active=True))
            self.filelist[file][1].bind(on_press=self.accept_callback)
            self.file_layout.add_widget(self.filelist[file][1])

class Editor(MDBoxLayout):
    def __init__(self):
        super(Editor, self).__init__()


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
        editor = Editor()
        swiper = Swiper()
        swiper.add_any_widget(fm)
        swiper.add_any_widget(editor)
        main_layout = MDBoxLayout()
        main_layout.add_widget(swiper)
        return main_layout


MainApp().run()
