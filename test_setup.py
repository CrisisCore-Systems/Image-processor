from PIL import Image
import os

def create_test_image():
    # Create a simple test image
    img = Image.new('RGB', (100, 100), color='red')
    
    try:
        # Create test_images directory if it doesn't exist
        os.makedirs('test_images', exist_ok=True)
        
        # Try saving in different formats
        formats = [
            ('PNG', 'test_images/test.png'),
            ('JPEG', 'test_images/test.jpg'),
            ('WebP', 'test_images/test.webp')
        ]
        
        for format_name, filepath in formats:
            try:
                img.save(filepath)
                print(f"✓ Successfully created {filepath}")
            except Exception as e:
                print(f"✗ Failed to create {filepath}: {str(e)}")
                
        print("\nSupported formats:", ', '.join(Image.SAVE.keys()))
        
    except Exception as e:
        print(f"Error creating test images: {str(e)}")

if __name__ == '__main__':
    print("PIL/Pillow version:", Image.__version__)
    print("Supported features:", ', '.join(Image.core.get_supported_versions()))
    create_test_image()
