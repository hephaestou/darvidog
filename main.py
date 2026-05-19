import os
os.environ['KIVY_GL_BACKEND'] = 'sdl2'
os.environ['KIVY_WINDOW'] = 'sdl2'

from kivy.app import App
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout

class TestApp(App):
    def build(self):
        layout = BoxLayout()
        with layout.canvas.before:
            Color(1, 0, 0, 1)
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
        layout.add_widget(Label(text='DARVIDOG WORKING!', font_size='30sp', color=(1,1,1,1)))
        return layout

if __name__ == '__main__':
    TestApp().run()
