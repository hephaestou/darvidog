import os

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.camera import Camera
from kivy.uix.image import Image
from kivy.clock import Clock
from soil_analyzer import SoilColorAnalyzer

class DarvidogApp(App):
    def build(self):
        try:
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.CAMERA])
        except ImportError:
            pass

        self.analyzer = SoilColorAnalyzer()
        self.camera = None
        self.torch_on = False

        layout = BoxLayout(orientation='vertical', padding=8, spacing=6)

        # Header
        header = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=10)
        try:
            logo = Image(source='icon_corrected.png', size_hint=(0.15, 1), allow_stretch=True, keep_ratio=True)
            header.add_widget(logo)
        except Exception:
            pass

        title = Label(text='[b]DARVIDOG[/b] Soil Analyser', font_size='18sp', markup=True, color=(1, 1, 1, 1), halign='left', valign='middle', size_hint=(0.85, 1))
        title.bind(size=title.setter('text_size'))
        header.add_widget(title)
        layout.add_widget(header)

        # Camera
        try:
            self.camera = Camera(play=False, resolution=(640, 480), size_hint=(1, 0.55))
            self.camera.rotation = -90
            layout.add_widget(self.camera)
        except Exception as e:
            layout.add_widget(Label(text=f'Camera error: {str(e)}', size_hint=(1, 0.55)))

        # Results
        self.result_label = Label(
            text='Tap Start Camera then Analyse',
            font_size='13sp',
            halign='center',
            valign='middle',
            size_hint=(1, 0.12),
            color=(0.9, 0.9, 0.9, 1)
        )
        self.result_label.bind(size=self.result_label.setter('text_size'))
        layout.add_widget(self.result_label)

        # Buttons
        btn_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.23), spacing=8)

        self.btn_camera = Button(text='Start Camera', font_size='12sp', background_color=(0.2, 0.4, 0.8, 1), background_normal='')
        self.btn_camera.bind(on_press=self.toggle_camera)
        btn_layout.add_widget(self.btn_camera)

        self.btn_torch = Button(text='Flash ON', font_size='12sp', background_color=(0.5, 0.5, 0, 1), background_normal='')
        self.btn_torch.bind(on_press=self.toggle_torch)
        btn_layout.add_widget(self.btn_torch)

        btn_analyze = Button(text='Analyse', font_size='12sp', background_color=(0.2, 0.6, 0.2, 1), background_normal='')
        btn_analyze.bind(on_press=self.analyze)
        btn_layout.add_widget(btn_analyze)

        layout.add_widget(btn_layout)
        return layout

    def toggle_camera(self, instance):
        if not self.camera:
            self.result_label.text = 'No camera available'
            return
        if not self.camera.play:
            self.camera.play = True
            self.btn_camera.text = 'Stop Camera'
            self.btn_camera.background_color = (0.8, 0.2, 0.2, 1)
            self.result_label.text = 'Camera ready - point at soil and tap Analyse'
        else:
            self.camera.play = False
            self.btn_camera.text = 'Start Camera'
            self.btn_camera.background_color = (0.2, 0.4, 0.8, 1)
            self.result_label.text = 'Camera stopped'

    def toggle_torch(self, instance):
        try:
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Context = autoclass('android.content.Context')
            context = PythonActivity.mActivity
            manager = context.getSystemService(Context.CAMERA_SERVICE)
            camera_ids = manager.getCameraIdList()
            if not camera_ids:
                self.result_label.text = 'No camera found for flash'
                return
            new_state = not self.torch_on
            manager.setTorchMode(camera_ids[0], new_state)
            self.torch_on = new_state
            if self.torch_on:
                instance.text = 'Flash OFF'
                instance.background_color = (1, 0.8, 0, 1)
            else:
                instance.text = 'Flash ON'
                instance.background_color = (0.5, 0.5, 0, 1)
        except Exception as e:
            self.result_label.text = f'Flash error: {str(e)}'

    def analyze(self, instance):
        if not self.camera or not self.camera.play:
            self.result_label.text = 'Tap Start Camera first!'
            return
        Clock.schedule_once(self._do_analyze, 0.1)

    def _do_analyze(self, dt):
        if not self.camera.texture:
            self.result_label.text = 'No image yet - wait a moment'
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
                        b, g, r = pixels[idx], pixels[idx+1], pixels[idx+2]
                    else:
                        r, g, b = pixels[idx], pixels[idx+1], pixels[idx+2]
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
            f"MUNSELL: {result.get('munsell', 'unknown')} "
            f"Confidence: {result.get('confidence', 0)}%\n"
            f"RGB: {r},{g},{b} Format: {colorfmt}"
        )

    def on_stop(self):
        if self.torch_on:
            try:
                from jnius import autoclass
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                Context = autoclass('android.content.Context')
                context = PythonActivity.mActivity
                manager = context.getSystemService(Context.CAMERA_SERVICE)
                manager.setTorchMode(manager.getCameraIdList()[0], False)
            except Exception:
                pass

if __name__ == '__main__':
    DarvidogApp().run()
