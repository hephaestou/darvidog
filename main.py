import os
os.environ['KIVY_GL_BACKEND'] = 'sdl2'
os.environ['KIVY_WINDOW'] = 'sdl2'

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.camera import Camera
from soil_analyzer import SoilColorAnalyzer

class TestApp(App):
    def build(self):
        try:
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.CAMERA])
        except ImportError:
            pass

        self.analyzer = SoilColorAnalyzer()
        self.camera = None

        self.result_label = Label(
            text='Press Start Camera first',
            font_size='16sp',
            halign='center',
            size_hint=(1, 0.15)
        )

        try:
            self.camera = Camera(
                play=False,
                resolution=(640, 480),
                size_hint=(1, 0.55)
            )
        except Exception as e:
            self.result_label.text = f'Camera error: {str(e)}'

        btn_camera = Button(
            text='Start Camera',
            font_size='16sp',
            size_hint=(1, 0.15),
            background_color=(0.2, 0.4, 0.8, 1)
        )
        btn_camera.bind(on_press=self.start_camera)

        btn_analyze = Button(
            text='Analyse',
            font_size='16sp',
            size_hint=(1, 0.15),
            background_color=(0.2, 0.6, 0.2, 1)
        )
        btn_analyze.bind(on_press=self.analyze)

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(self.result_label)
        if self.camera:
            layout.add_widget(self.camera)
        layout.add_widget(btn_camera)
        layout.add_widget(btn_analyze)
        return layout

    def start_camera(self, instance):
        if self.camera:
            self.camera.play = True
            self.result_label.text = 'Camera started - point at soil'
        else:
            self.result_label.text = 'No camera available'

    def analyze(self, instance):
        if not self.camera or not self.camera.texture:
            self.result_label.text = 'Start camera first!'
            return

        texture = self.camera.texture
        pixels = texture.pixels
        width, height = map(int, texture.size)
        colorfmt = texture.colorfmt

        cx, cy = width // 2, height // 2
        sample = 30
        total_r = total_g = total_b = count = 0

        for y in range(max(0, cy - sample), min(height, cy + sample)):
            for x in range(max(0, cx - sample), min(width, cx + sample)):
                idx = (y * width + x) * 4
                if idx + 3 < len(pixels):
                    if colorfmt == 'bgra':
                        b = pixels[idx]
                        g = pixels[idx + 1]
                        r = pixels[idx + 2]
                    else:
                        r = pixels[idx]
                        g = pixels[idx + 1]
                        b = pixels[idx + 2]
                    total_r += r
                    total_g += g
                    total_b += b
                    count += 1

        if count == 0:
            self.result_label.text = 'Could not read image'
            return

        r = int(total_r / count)
        g = int(total_g / count)
        b = int(total_b / count)

        result = self.analyzer.analyze_color(r, g, b)
        self.result_label.text = (
            f"RGB: {r}, {g}, {b}\n"
            f"MUNSELL: {result.get('munsell', 'unknown')}\n"
            f"Confidence: {result.get('confidence', 0)}%"
        )

if __name__ == '__main__':
    TestApp().run()
