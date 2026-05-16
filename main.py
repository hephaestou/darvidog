"""
Soil Color Analyzer - Mobile App
Kivy-based camera app for field soil color analysis
Uses phone LED for consistent illumination
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.camera import Camera
from kivy.uix.image import Image
from kivy.uix.togglebutton import ToggleButton
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
import cv2
import numpy as np
from datetime import datetime
import os
from pathlib import Path

# Import flash control
try:
    from plyer import flash
    FLASH_AVAILABLE = True
except ImportError:
    FLASH_AVAILABLE = False
    print("Flash control not available (plyer not installed or not on mobile)")

# Import our soil analyzer
from soil_analyzer import SoilColorAnalyzer

class SoilColorApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.analyzer = SoilColorAnalyzer()
        self.camera = None
        self.current_result = None
        self.flash_on = False
        
        # Load dog bark sound - try both formats
        self.bark_sound = None
        sound_files = ['bark.wav', 'bark.mp3', 'woof.wav', 'woof.mp3']
        
        for sound_file in sound_files:
            if os.path.exists(sound_file):
                try:
                    self.bark_sound = SoundLoader.load(sound_file)
                    if self.bark_sound:
                        print(f"✓ Loaded bark sound: {sound_file}")
                        break
                except Exception as e:
                    print(f"Error loading {sound_file}: {e}")
        
        if not self.bark_sound:
            print("⚠ No bark sound found. Looking for: bark.wav, bark.mp3, woof.wav, or woof.mp3")
        
        # Create results directory
        self.results_dir = Path.home() / 'SoilColorResults'
        self.results_dir.mkdir(exist_ok=True)
    
    def build(self):
        # Main layout
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Logo and Title section
        header_layout = BoxLayout(
            orientation='vertical',
            size_hint=(1, 0.15),
            spacing=5
        )
        
        # Logo image
        try:
            from PIL import Image as PILImage
            import io
            
            # Load and fix orientation
            pil_img = PILImage.open('icon.png')
            
            # Handle EXIF orientation
            try:
                from PIL import ImageOps
                pil_img = ImageOps.exif_transpose(pil_img)
            except:
                pass
            
            # Save corrected version temporarily
            pil_img.save('icon_corrected.png')
            
            logo = Image(
                source='icon_corrected.png',
                size_hint=(1, 0.7),
                allow_stretch=True,
                keep_ratio=True
            )
            header_layout.add_widget(logo)
        except Exception as e:
            # If logo fails, show text instead
            print(f"Logo error: {e}")
            pass
        
        # Title with branding
        title = Label(
            text='[b]DARVIDOG[/b] Soil Analyser',
            size_hint=(1, 0.3),
            font_size='18sp',
            markup=True,
            color=(0.2, 0.2, 0.2, 1)
        )
        header_layout.add_widget(title)
        
        layout.add_widget(header_layout)
        
        # Instructions
        instructions = Label(
            text='Keep phone 15-20cm from soil\nLED provides consistent lighting',
            size_hint=(1, 0.06),
            font_size='12sp',
            color=(0.7, 0.7, 0.7, 1)
        )
        layout.add_widget(instructions)
        
        # Camera view
        self.camera = Camera(
            play=True,
            resolution=(640, 480),
            size_hint=(1, 0.5)
        )
        layout.add_widget(self.camera)
        
        # Flash toggle button
        self.flash_btn = ToggleButton(
            text='LED: OFF',
            size_hint=(1, 0.08),
            font_size='16sp',
            background_color=(0.5, 0.5, 0.5, 1)
        )
        self.flash_btn.bind(on_press=self.toggle_flash)
        layout.add_widget(self.flash_btn)
        
        # Turn on flash by default for consistent lighting
        Clock.schedule_once(lambda dt: self.flash_btn.trigger_action(), 0.5)
        
        # Results display
        self.result_label = Label(
            text='Point camera at soil sample\nTurn on LED for best results',
            size_hint=(1, 0.12),
            font_size='16sp',
            halign='center'
        )
        layout.add_widget(self.result_label)
        
        # Buttons layout
        button_layout = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.12),
            spacing=10
        )
        
        # Capture button
        capture_btn = Button(
            text='ANALYZE',
            font_size='18sp',
            bold=True,
            background_color=(0.2, 0.6, 0.2, 1)
        )
        capture_btn.bind(on_press=self.capture_and_analyze)
        button_layout.add_widget(capture_btn)
        
        # Save button
        save_btn = Button(
            text='SAVE',
            font_size='18sp',
            background_color=(0.2, 0.4, 0.8, 1)
        )
        save_btn.bind(on_press=self.save_result)
        button_layout.add_widget(save_btn)
        
        layout.add_widget(button_layout)
        
        return layout
    
    def toggle_flash(self, instance):
        """Toggle phone LED flash on/off"""
        if not FLASH_AVAILABLE:
            self.result_label.text = 'Flash not available\n(Testing on computer or flash not supported)'
            return
        
        try:
            if instance.state == 'down':
                # Turn flash ON
                flash.on()
                self.flash_on = True
                instance.text = 'LED: ON'
                instance.background_color = (1, 0.8, 0, 1)  # Yellow
                self.result_label.text = '✓ LED on - consistent lighting\nReady to analyze'
            else:
                # Turn flash OFF
                flash.off()
                self.flash_on = False
                instance.text = 'LED: OFF'
                instance.background_color = (0.5, 0.5, 0.5, 1)  # Gray
                self.result_label.text = 'LED off\nTurn on for accurate results'
        except Exception as e:
            self.result_label.text = f'Flash control error: {str(e)}'
    
    def capture_and_analyze(self, instance):
        """Capture current camera frame and analyze soil color"""
        
        # Play bark sound! 🐕
        if self.bark_sound:
            try:
                self.bark_sound.play()
                print("🐕 WUFF!")
            except Exception as e:
                print(f"Bark error: {e}")
        else:
            print("⚠ No bark sound loaded")
        
        # Check if flash is on
        if FLASH_AVAILABLE and not self.flash_on:
            self.result_label.text = '⚠ Warning: LED is off\nResults may vary with lighting'
        else:
            self.result_label.text = 'Analyzing...'
        
        # Get camera texture
        if not self.camera.texture:
            self.result_label.text = 'Camera not ready. Try again.'
            return
        
        # Convert texture to image
        texture = self.camera.texture
        pixels = texture.pixels
        size = texture.size
        
        # Convert to numpy array
        img_array = np.frombuffer(pixels, dtype=np.uint8)
        img_array = img_array.reshape(size[1], size[0], 4)  # RGBA
        
        # Convert RGBA to BGR (for OpenCV)
        img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGBA2BGR)
        
        # Flip vertically (Kivy camera is upside down)
        img_bgr = cv2.flip(img_bgr, 0)
        
        # Save temporary image
        temp_path = self.results_dir / 'temp_capture.jpg'
        cv2.imwrite(str(temp_path), img_bgr)
        
        # Analyze the image
        try:
            result = self.analyzer.analyze_image(temp_path)
            self.current_result = result
            
            # Display results
            munsell = result['munsell_notation']
            confidence = result['confidence']
            calibrated = result['calibrated']
            
            # Build result text
            result_text = f"MUNSELL: {munsell}\n"
            result_text += f"Confidence: {confidence}%\n"
            
            if calibrated:
                result_text += "✓ Scale detected"
            else:
                result_text += "⚠ No scale detected"
            
            if self.flash_on:
                result_text += " | LED: ON"
            
            self.result_label.text = result_text
            
        except Exception as e:
            self.result_label.text = f'Error: {str(e)}'
            self.current_result = None
    
    def save_result(self, instance):
        """Save current analysis result"""
        
        if not self.current_result:
            self.result_label.text = 'No result to save!\nCapture a photo first.'
            return
        
        # Generate filename with timestamp and Munsell notation
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        munsell_safe = self.current_result['munsell_notation'].replace('/', '_').replace(' ', '_')
        filename = f'soil_{timestamp}_{munsell_safe}'
        
        # Save photo
        photo_path = self.results_dir / f'{filename}.jpg'
        temp_path = self.results_dir / 'temp_capture.jpg'
        
        if temp_path.exists():
            import shutil
            shutil.copy(temp_path, photo_path)
        
        # Save JSON data (include lighting info)
        import json
        result_with_metadata = self.current_result.copy()
        result_with_metadata['led_flash_used'] = self.flash_on
        result_with_metadata['timestamp'] = timestamp
        
        json_path = self.results_dir / f'{filename}.json'
        with open(json_path, 'w') as f:
            json.dump(result_with_metadata, f, indent=2)
        
        # Update UI
        self.result_label.text = f'✓ Saved to:\n{self.results_dir}\n\nReady for next sample'
        
        # Reset after brief delay
        def reset_text(dt):
            if self.current_result:
                self.result_label.text = f"MUNSELL: {self.current_result['munsell_notation']}\nConfidence: {self.current_result['confidence']}%"
        
        Clock.schedule_once(reset_text, 2)
    
    def on_stop(self):
        """Clean up when app closes"""
        if FLASH_AVAILABLE and self.flash_on:
            try:
                flash.off()
            except:
                pass

def main():
    """Run the app"""
    SoilColorApp().run()

if __name__ == '__main__':
    main()
