import os
os.environ['KIVY_GL_BACKEND'] = 'sdl2'
os.environ['KIVY_WINDOW'] = 'sdl2'
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.camera import Camera
from kivy.uix.image import Image
from kivy.uix.togglebutton import ToggleButton
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
import os
from pathlib import Path
from datetime import datetime
import json

try:
    from plyer import flash
    FLASH_AVAILABLE = True
except ImportError:
    FLASH_AVAILABLE = False

from soil_analyzer import SoilColorAnalyzer

class SoilColorApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.analyzer = SoilColorAnalyzer()
        self.camera = None
        self.current_result = None
        self.flash_on = False
        self.bark_sound = None
        for sound_file in ['bark.wav', 'bark.mp3']:
            if os.path.exists(sound_file):
                try:
                    self.bark_sound = SoundLoader.load(sound_file)
                    if self.bark_sound:
                        break
                except Exception:
                    pass
        self.results_dir = Path.home() / 'SoilColorResults'
        self.results_dir.mkdir(exist_ok=True)

    def build(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        header_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.15), spacing=5)
        try:
            logo = Image(source='icon_corrected.png', size_hint=(1, 0.7), allow_stretch=True, keep_ratio=True)
            header_layout.add_widget(logo)
        except Exception:
            pass
        title = Label(text='[b]DARVIDOG[/b] Soil Analyser', size_hint=(1, 0.3), font_size='18sp', markup=True, color=(0.2, 0.2, 0.2, 1))
        header_layout.add_widget(title)
        layout.add_widget(header_layout)
        instructions = Label(text='Keep phone 15-20cm from soil\nLED provides consistent lighting', size_hint=(1, 0.06), font_size='12sp', color=(0.7, 0.7, 0.7, 1))
        layout.add_widget(instructions)
        try:
            self.camera = Camera(play=True, resolution=(640, 480), size_hint=(1, 0.5))
            layout.add_widget(self.camera)
        except Exception as e:
            self.camera = None
            layout.add_widget(Label(text=f'Camera error: {str(e)}', size_hint=(1, 0.5)))
        self.flash_btn = ToggleButton(text='LED: OFF', size_hint=(1, 0.08), font_size='16sp', background_color=(0.5, 0.5, 0.5, 1))
        self.flash_btn.bind(on_press=self.toggle_flash)
        layout.add_widget(self.flash_btn)
        Clock.schedule_once(lambda dt: self.flash_btn.trigger_action(), 0.5)
        self.result_label = Label(text='Point camera at soil sample\nTurn on LED for best results', size_hint=(1, 0.12), font_size='16sp', halign='center')
        layout.add_widget(self.result_label)
        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.12), spacing=10)
        capture_btn = Button(text='ANALYZE', font_size='18sp', bold=True, background_color=(0.2, 0.6, 0.2, 1))
        capture_btn.bind(on_press=self.capture_and_analyze)
        button_layout.add_widget(capture_btn)
        save_btn = Button(text='SAVE', font_size='18sp', background_color=(0.2, 0.4, 0.8, 1))
        save_btn.bind(on_press=self.save_result)
        button_layout.add_widget(save_btn)
        layout.add_widget(button_layout)
        return layout

    def toggle_flash(self, instance):
        if not FLASH_AVAILABLE:
            self.result_label.text = 'Flash not available'
            return
        try:
            if instance.state == 'down':
                flash.on()
                self.flash_on = True
                instance.text = 'LED: ON'
                instance.background_color = (1, 0.8, 0, 1)
                self.result_label.text = 'LED on - Ready to analyze'
            else:
                flash.off()
                self.flash_on = False
                instance.text = 'LED: OFF'
                instance.background_color = (0.5, 0.5, 0.5, 1)
                self.result_label.text = 'LED off'
        except Exception as e:
            self.result_label.text = f'Flash error: {str(e)}'

    def capture_and_analyze(self, instance):
        if self.bark_sound:
            try:
                self.bark_sound.play()
            except Exception:
                pass
        if not self.camera or not self.camera.texture:
            self.result_label.text = 'Camera not ready. Try again.'
            return
        self.result_label.text = 'Analyzing...'
        texture = self.camera.texture
        pixels = texture.pixels
        width, height = texture.size
        total_r = total_g = total_b = count = 0
        cx, cy = width // 2, height // 2
        sample = 50
        for y in range(cy - sample, cy + sample):
            for x in range(cx - sample, cx + sample):
                idx = (y * width + x) * 4
                if idx + 2 < len(pixels):
                    total_r += pixels[idx]
                    total_g += pixels[idx + 1]
                    total_b += pixels[idx + 2]
                    count += 1
        if count == 0:
            self.result_label.text = 'Could not read image'
            return
        avg_r = int(total_r / count)
        avg_g = int(total_g / count)
        avg_b = int(total_b / count)
        try:
            result = self.analyzer.analyze_color(avg_r, avg_g, avg_b)
            self.current_result = {
                'munsell_notation': result['munsell'],
                'confidence': result['confidence'],
                'rgb': {'r': avg_r, 'g': avg_g, 'b': avg_b}
            }
            self.result_label.text = f"MUNSELL: {result['munsell']}\nConfidence: {result['confidence']}%"
        except Exception as e:
            self.result_label.text = f'Error: {str(e)}'

    def save_result(self, instance):
        if not self.current_result:
            self.result_label.text = 'No result to save!\nCapture a photo first.'
            return
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        munsell_safe = self.current_result['munsell_notation'].replace('/', '_').replace(' ', '_')
        filename = f'soil_{timestamp}_{munsell_safe}'
        result_with_metadata = self.current_result.copy()
        result_with_metadata['led_flash_used'] = self.flash_on
        result_with_metadata['timestamp'] = timestamp
        json_path = self.results_dir / f'{filename}.json'
        with open(json_path, 'w') as f:
            json.dump(result_with_metadata, f, indent=2)
        self.result_label.text = 'Saved!\nReady for next sample'

    def on_stop(self):
        if FLASH_AVAILABLE and self.flash_on:
            try:
                flash.off()
            except Exception:
                pass

def main():
    SoilColorApp().run()

if __name__ == '__main__':
    main()
