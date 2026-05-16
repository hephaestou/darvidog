"""
Soil Color Analyzer - Mobile Version
Lightweight version for Android - no opencv/scipy needed
"""

import math

class SoilColorAnalyzer:
    def __init__(self):
        """Initialize the mobile soil color analyzer"""
        self.munsell_lookup = self._load_munsell_data()
    
    def _load_munsell_data(self):
        """Comprehensive Munsell soil color database"""
        return {
            # NEUTRAL COLORS
            'N 2/': {'L': 20, 'a': 0, 'b': 0},
            'N 3/': {'L': 30, 'a': 0, 'b': 0},
            'N 4/': {'L': 40, 'a': 0, 'b': 0},
            'N 5/': {'L': 50, 'a': 0, 'b': 0},
            'N 6/': {'L': 60, 'a': 0, 'b': 0},
            'N 7/': {'L': 70, 'a': 0, 'b': 0},
            'N 8/': {'L': 80, 'a': 0, 'b': 0},
            
            # 10YR (Most common soil colors)
            '10YR 1/1': {'L': 10, 'a': 0, 'b': 5},
            '10YR 2/1': {'L': 20, 'a': 0, 'b': 8},
            '10YR 2/2': {'L': 20, 'a': 3, 'b': 12},
            '10YR 3/1': {'L': 30, 'a': 0, 'b': 8},
            '10YR 3/2': {'L': 30, 'a': 5, 'b': 12},
            '10YR 3/3': {'L': 30, 'a': 7, 'b': 16},
            '10YR 3/4': {'L': 30, 'a': 10, 'b': 20},
            '10YR 3/6': {'L': 30, 'a': 13, 'b': 28},
            '10YR 4/1': {'L': 40, 'a': 0, 'b': 8},
            '10YR 4/2': {'L': 40, 'a': 5, 'b': 12},
            '10YR 4/3': {'L': 40, 'a': 8, 'b': 16},
            '10YR 4/4': {'L': 40, 'a': 12, 'b': 22},
            '10YR 4/6': {'L': 40, 'a': 15, 'b': 30},
            '10YR 5/1': {'L': 50, 'a': 0, 'b': 8},
            '10YR 5/2': {'L': 50, 'a': 5, 'b': 12},
            '10YR 5/3': {'L': 50, 'a': 8, 'b': 16},
            '10YR 5/4': {'L': 50, 'a': 12, 'b': 22},
            '10YR 5/6': {'L': 50, 'a': 15, 'b': 30},
            '10YR 5/8': {'L': 50, 'a': 18, 'b': 38},
            '10YR 6/1': {'L': 60, 'a': 0, 'b': 8},
            '10YR 6/2': {'L': 60, 'a': 5, 'b': 12},
            '10YR 6/3': {'L': 60, 'a': 8, 'b': 16},
            '10YR 6/4': {'L': 60, 'a': 12, 'b': 22},
            '10YR 6/6': {'L': 60, 'a': 15, 'b': 30},
            '10YR 6/8': {'L': 60, 'a': 18, 'b': 38},
            '10YR 7/1': {'L': 70, 'a': 0, 'b': 8},
            '10YR 7/2': {'L': 70, 'a': 5, 'b': 12},
            '10YR 7/3': {'L': 70, 'a': 8, 'b': 16},
            '10YR 7/4': {'L': 70, 'a': 12, 'b': 22},
            '10YR 7/6': {'L': 70, 'a': 15, 'b': 30},
            '10YR 8/1': {'L': 80, 'a': 0, 'b': 8},
            '10YR 8/2': {'L': 80, 'a': 5, 'b': 12},
            '10YR 8/3': {'L': 80, 'a': 8, 'b': 16},
            '10YR 8/4': {'L': 80, 'a': 12, 'b': 22},
            
            # 7.5YR (Reddish brown)
            '7.5YR 2/1': {'L': 20, 'a': 3, 'b': 8},
            '7.5YR 2/2': {'L': 20, 'a': 6, 'b': 12},
            '7.5YR 3/1': {'L': 30, 'a': 3, 'b': 8},
            '7.5YR 3/2': {'L': 30, 'a': 8, 'b': 12},
            '7.5YR 3/3': {'L': 30, 'a': 10, 'b': 16},
            '7.5YR 3/4': {'L': 30, 'a': 13, 'b': 20},
            '7.5YR 4/2': {'L': 40, 'a': 8, 'b': 12},
            '7.5YR 4/3': {'L': 40, 'a': 11, 'b': 16},
            '7.5YR 4/4': {'L': 40, 'a': 15, 'b': 22},
            '7.5YR 4/6': {'L': 40, 'a': 20, 'b': 30},
            '7.5YR 5/2': {'L': 50, 'a': 8, 'b': 12},
            '7.5YR 5/3': {'L': 50, 'a': 11, 'b': 16},
            '7.5YR 5/4': {'L': 50, 'a': 15, 'b': 22},
            '7.5YR 5/6': {'L': 50, 'a': 20, 'b': 30},
            '7.5YR 5/8': {'L': 50, 'a': 25, 'b': 38},
            '7.5YR 6/2': {'L': 60, 'a': 8, 'b': 12},
            '7.5YR 6/3': {'L': 60, 'a': 11, 'b': 16},
            '7.5YR 6/4': {'L': 60, 'a': 15, 'b': 22},
            '7.5YR 6/6': {'L': 60, 'a': 20, 'b': 30},
            '7.5YR 6/8': {'L': 60, 'a': 25, 'b': 38},
            '7.5YR 7/2': {'L': 70, 'a': 8, 'b': 12},
            '7.5YR 7/3': {'L': 70, 'a': 11, 'b': 16},
            '7.5YR 7/4': {'L': 70, 'a': 15, 'b': 22},
            '7.5YR 7/6': {'L': 70, 'a': 20, 'b': 30},
            '7.5YR 8/2': {'L': 80, 'a': 8, 'b': 12},
            '7.5YR 8/4': {'L': 80, 'a': 15, 'b': 22},
            
            # 5YR (Reddish)
            '5YR 2/1': {'L': 20, 'a': 5, 'b': 8},
            '5YR 2/2': {'L': 20, 'a': 8, 'b': 12},
            '5YR 3/1': {'L': 30, 'a': 5, 'b': 8},
            '5YR 3/2': {'L': 30, 'a': 10, 'b': 12},
            '5YR 3/3': {'L': 30, 'a': 12, 'b': 16},
            '5YR 3/4': {'L': 30, 'a': 16, 'b': 20},
            '5YR 4/1': {'L': 40, 'a': 5, 'b': 8},
            '5YR 4/2': {'L': 40, 'a': 10, 'b': 12},
            '5YR 4/3': {'L': 40, 'a': 13, 'b': 16},
            '5YR 4/4': {'L': 40, 'a': 17, 'b': 20},
            '5YR 4/6': {'L': 40, 'a': 23, 'b': 28},
            '5YR 5/2': {'L': 50, 'a': 10, 'b': 12},
            '5YR 5/3': {'L': 50, 'a': 13, 'b': 16},
            '5YR 5/4': {'L': 50, 'a': 17, 'b': 20},
            '5YR 5/6': {'L': 50, 'a': 23, 'b': 28},
            '5YR 5/8': {'L': 50, 'a': 28, 'b': 36},
            '5YR 6/3': {'L': 60, 'a': 13, 'b': 16},
            '5YR 6/4': {'L': 60, 'a': 17, 'b': 20},
            '5YR 6/6': {'L': 60, 'a': 23, 'b': 28},
            '5YR 6/8': {'L': 60, 'a': 28, 'b': 36},
            '5YR 7/3': {'L': 70, 'a': 13, 'b': 16},
            '5YR 7/4': {'L': 70, 'a': 17, 'b': 20},
            '5YR 7/6': {'L': 70, 'a': 23, 'b': 28},
            
            # 2.5YR (Very red)
            '2.5YR 2/2': {'L': 20, 'a': 8, 'b': 10},
            '2.5YR 3/2': {'L': 30, 'a': 12, 'b': 12},
            '2.5YR 3/4': {'L': 30, 'a': 18, 'b': 18},
            '2.5YR 3/6': {'L': 30, 'a': 25, 'b': 25},
            '2.5YR 4/2': {'L': 40, 'a': 12, 'b': 12},
            '2.5YR 4/4': {'L': 40, 'a': 20, 'b': 20},
            '2.5YR 4/6': {'L': 40, 'a': 28, 'b': 28},
            '2.5YR 4/8': {'L': 40, 'a': 35, 'b': 35},
            '2.5YR 5/4': {'L': 50, 'a': 20, 'b': 20},
            '2.5YR 5/6': {'L': 50, 'a': 28, 'b': 28},
            '2.5YR 5/8': {'L': 50, 'a': 35, 'b': 35},
            '2.5YR 6/6': {'L': 60, 'a': 28, 'b': 28},
            '2.5YR 6/8': {'L': 60, 'a': 35, 'b': 35},
            
            # 2.5Y (Yellowish)
            '2.5Y 2/1': {'L': 20, 'a': 0, 'b': 6},
            '2.5Y 3/1': {'L': 30, 'a': 0, 'b': 6},
            '2.5Y 3/2': {'L': 30, 'a': 2, 'b': 12},
            '2.5Y 4/1': {'L': 40, 'a': 0, 'b': 6},
            '2.5Y 4/2': {'L': 40, 'a': 2, 'b': 12},
            '2.5Y 4/3': {'L': 40, 'a': 3, 'b': 18},
            '2.5Y 4/4': {'L': 40, 'a': 5, 'b': 24},
            '2.5Y 5/2': {'L': 50, 'a': 2, 'b': 12},
            '2.5Y 5/3': {'L': 50, 'a': 3, 'b': 18},
            '2.5Y 5/4': {'L': 50, 'a': 5, 'b': 24},
            '2.5Y 5/6': {'L': 50, 'a': 7, 'b': 32},
            '2.5Y 6/2': {'L': 60, 'a': 2, 'b': 12},
            '2.5Y 6/3': {'L': 60, 'a': 3, 'b': 18},
            '2.5Y 6/4': {'L': 60, 'a': 5, 'b': 24},
            '2.5Y 6/6': {'L': 60, 'a': 7, 'b': 32},
            '2.5Y 7/2': {'L': 70, 'a': 2, 'b': 12},
            '2.5Y 7/3': {'L': 70, 'a': 3, 'b': 18},
            '2.5Y 7/4': {'L': 70, 'a': 5, 'b': 24},
            '2.5Y 8/2': {'L': 80, 'a': 2, 'b': 12},
            '2.5Y 8/3': {'L': 80, 'a': 3, 'b': 18},
            
            # 5Y (Yellow)
            '5Y 4/1': {'L': 40, 'a': -2, 'b': 8},
            '5Y 4/2': {'L': 40, 'a': -1, 'b': 14},
            '5Y 5/1': {'L': 50, 'a': -2, 'b': 8},
            '5Y 5/2': {'L': 50, 'a': -1, 'b': 14},
            '5Y 5/3': {'L': 50, 'a': 0, 'b': 20},
            '5Y 5/4': {'L': 50, 'a': 1, 'b': 26},
            '5Y 6/2': {'L': 60, 'a': -1, 'b': 14},
            '5Y 6/3': {'L': 60, 'a': 0, 'b': 20},
            '5Y 6/4': {'L': 60, 'a': 1, 'b': 26},
            '5Y 7/2': {'L': 70, 'a': -1, 'b': 14},
            '5Y 7/3': {'L': 70, 'a': 0, 'b': 20},
            '5Y 7/4': {'L': 70, 'a': 1, 'b': 26},
            '5Y 8/2': {'L': 80, 'a': -1, 'b': 14},
            '5Y 8/3': {'L': 80, 'a': 0, 'b': 20},
            
            # GLEY colors (waterlogged soils)
            'GLEY1 2/N': {'L': 20, 'a': 0, 'b': 0},
            'GLEY1 3/N': {'L': 30, 'a': 0, 'b': 0},
            'GLEY1 4/N': {'L': 40, 'a': 0, 'b': 0},
            'GLEY1 5/N': {'L': 50, 'a': 0, 'b': 0},
            'GLEY1 6/N': {'L': 60, 'a': 0, 'b': 0},
            'GLEY1 7/N': {'L': 70, 'a': 0, 'b': 0},
            'GLEY1 3/1': {'L': 30, 'a': -3, 'b': 2},
            'GLEY1 4/1': {'L': 40, 'a': -3, 'b': 2},
            'GLEY1 5/1': {'L': 50, 'a': -3, 'b': 2},
            'GLEY1 6/1': {'L': 60, 'a': -3, 'b': 2},
        }
    
    def rgb_to_lab(self, r, g, b):
        """
        Convert RGB (0-255) to LAB color space
        Pure Python implementation - no dependencies!
        """
        # Normalize RGB to 0-1
        r, g, b = r / 255.0, g / 255.0, b / 255.0
        
        # Convert to linear RGB
        def gamma_correction(channel):
            if channel <= 0.04045:
                return channel / 12.92
            else:
                return ((channel + 0.055) / 1.055) ** 2.4
        
        r = gamma_correction(r)
        g = gamma_correction(g)
        b = gamma_correction(b)
        
        # Convert to XYZ (D65 illuminant)
        x = r * 0.4124564 + g * 0.3575761 + b * 0.1804375
        y = r * 0.2126729 + g * 0.7151522 + b * 0.0721750
        z = r * 0.0193339 + g * 0.1191920 + b * 0.9503041
        
        # Normalize to D65 white point
        x = x / 0.95047
        y = y / 1.00000
        z = z / 1.08883
        
        # Convert to LAB
        def f(t):
            delta = 6.0 / 29.0
            if t > delta ** 3:
                return t ** (1.0 / 3.0)
            else:
                return t / (3 * delta ** 2) + 4.0 / 29.0
        
        fx = f(x)
        fy = f(y)
        fz = f(z)
        
        L = 116 * fy - 16
        a = 500 * (fx - fy)
        b_lab = 200 * (fy - fz)
        
        return L, a, b_lab
    
    def find_closest_munsell(self, L, a, b):
        """
        Find closest Munsell color using Euclidean distance in LAB space
        """
        min_distance = float('inf')
        closest_color = None
        
        for munsell_name, lab_values in self.munsell_lookup.items():
            # Calculate Euclidean distance in LAB space
            distance = math.sqrt(
                (L - lab_values['L']) ** 2 +
                (a - lab_values['a']) ** 2 +
                (b - lab_values['b']) ** 2
            )
            
            if distance < min_distance:
                min_distance = distance
                closest_color = munsell_name
        
        # Calculate confidence (inverse of distance, normalized)
        confidence = max(0, 100 - (min_distance * 2))
        
        return {
            'munsell': closest_color,
            'confidence': round(confidence, 1),
            'distance': round(min_distance, 2),
            'lab': {'L': round(L, 1), 'a': round(a, 1), 'b': round(b, 1)}
        }
    
    def analyze_color(self, r, g, b):
        """
        Analyze RGB color and return Munsell notation
        
        Args:
            r, g, b: RGB values (0-255)
            
        Returns:
            dict with munsell notation, confidence, and LAB values
        """
        # Convert to LAB
        L, a, b_lab = self.rgb_to_lab(r, g, b)
        
        # Find closest Munsell
        result = self.find_closest_munsell(L, a, b_lab)
        
        return result
    
    def analyze_image_region(self, rgb_array):
        """
        Analyze a region of pixels (for averaging)
        
        Args:
            rgb_array: List of (r, g, b) tuples
            
        Returns:
            dict with munsell notation and confidence
        """
        if not rgb_array:
            return None
        
        # Average the RGB values
        avg_r = sum(pixel[0] for pixel in rgb_array) / len(rgb_array)
        avg_g = sum(pixel[1] for pixel in rgb_array) / len(rgb_array)
        avg_b = sum(pixel[2] for pixel in rgb_array) / len(rgb_array)
        
        return self.analyze_color(int(avg_r), int(avg_g), int(avg_b))


def analyze_soil_from_rgb(r, g, b):
    """
    Convenience function for quick analysis
    
    Args:
        r, g, b: RGB values (0-255)
        
    Returns:
        Munsell notation string
    """
    analyzer = SoilColorAnalyzer()
    result = analyzer.analyze_color(r, g, b)
    return result['munsell']


# For testing
if __name__ == '__main__':
    analyzer = SoilColorAnalyzer()
    
    # Test with some common soil colors
    test_colors = [
        (70, 50, 30, "Dark brown soil"),
        (140, 110, 70, "Light brown soil"),
        (180, 140, 90, "Yellowish soil"),
        (50, 40, 35, "Very dark soil"),
    ]
    
    print("Mobile Soil Analyzer Test:")
    print("-" * 50)
    for r, g, b, description in test_colors:
        result = analyzer.analyze_color(r, g, b)
        print(f"\n{description}: RGB({r}, {g}, {b})")
        print(f"  Munsell: {result['munsell']}")
        print(f"  Confidence: {result['confidence']}%")
        print(f"  LAB: L={result['lab']['L']}, a={result['lab']['a']}, b={result['lab']['b']}")
