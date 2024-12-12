from crisiscore.processor import ImageProcessor

def main():
    # Initialize processor
    processor = ImageProcessor("input", "output")
    
    # Define operations
    operations = [
        {"type": "resize", "width": 800, "height": 600},
        {"type": "rotate", "angle": 90},
        {"type": "convert", "mode": "RGB"}
    ]
    
    # Process images
    results = processor.batch_process(operations)
    
    # Print results
    for image_name, success in results:
        status = "✓" if success else "✗"
        print(f"{status} {image_name}")

if __name__ == '__main__':
    main()
