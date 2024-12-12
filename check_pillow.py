from PIL import Image, features
import os

def check_pillow():
    print("=== Pillow Configuration ===")
    print(f"Pillow Version: {Image.__version__}")
    
    print("\nSupported Features:")
    supported_features = features.get_supported_features()
    for feature in supported_features:
        print(f"✓ {feature}")
    
    print("\nSupported Formats:")
    for format in sorted(Image.SAVE.keys()):
        print(f"✓ {format}")
    
    print("\nSystem Libraries:")
    libraries = {
        'libjpeg': 'JPEG',
        'libwebp': 'WEBP',
        'libpng': 'PNG'
    }
    
    for lib, format_name in libraries.items():
        path = f"/data/data/com.termux/files/usr/lib/{lib}.so"
        status = "Found" if os.path.exists(path) else "Missing"
        print(f"{format_name}: {status} ({lib})")

if __name__ == '__main__':
    check_pillow()
