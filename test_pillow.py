from PIL import Image, features
import os

def check_pillow():
    print("=== Pillow Configuration ===")
    print(f"\nPillow Version: {Image.__version__}")
    
    print("\nSupported Features:")
    for feature in features.get_supported_features():
        print(f"✓ {feature}")
    
    print("\nSupported Formats:")
    for format in sorted(Image.SAVE.keys()):
        print(f"✓ {format}")
    
    # Test image creation and saving
    print("\nTesting Image Operations:")
    try:
        # Create test directory
        os.makedirs('test_images', exist_ok=True)
        
        # Create and save test image
        img = Image.new('RGB', (100, 100), color='red')
        
        # Test formats
        formats = [('PNG', 'png'), ('JPEG', 'jpg'), ('WEBP', 'webp')]
        for format_name, ext in formats:
            try:
                test_file = f'test_images/test.{ext}'
                img.save(test_file)
                print(f"✓ Successfully saved {format_name} image")
                # Verify we can read it back
                Image.open(test_file).verify()
                print(f"✓ Successfully verified {format_name} image")
            except Exception as e:
                print(f"✗ Failed {format_name}: {str(e)}")
            
    except Exception as e:
        print(f"✗ Test failed: {str(e)}")

if __name__ == '__main__':
    check_pillow()
