import os
os.environ['KIVY_GL_BACKEND'] = 'sdl2'
os.environ['KIVY_WINDOW'] = 'sdl2'
os.environ['KIVY_METRICS_DENSITY'] = '1'
os.environ['KIVY_DPI'] = '96'

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from soil_analyzer import SoilColorAnalyzer

class TestApp(App):
    def build(self):
        self.analyzer = SoilColorAnalyzer()
        self.result_label = Label(
            text='Press button to test',
            font_size='20sp',
            halign='center'
        )
        btn = Button(
            text='Test Analysis',
            font_size='20sp',
            size_hint=(1, 0.2),
            background_color=(0.2, 0.6, 0.2, 1)
        )
        btn.bind(on_press=self.test)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        layout.add_widget(self.result_label)
        layout.add_widget(btn)
        return layout

    def test(self, instance):
        result = self.analyzer.analyze_color(100, 80, 60)
        self.result_label.text = f"Result: {result['munsell']}\nConfidence: {result['confidence']}%"

if __name__ == '__main__':
    TestApp().run()
