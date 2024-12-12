import argparse
import json
from .processor import ImageProcessor
import sys

def main():
    parser = argparse.ArgumentParser(description="CrisisCore Image Processor")
    parser.add_argument('--input', '-i', default='input',
                       help='Input directory containing images')
    parser.add_argument('--output', '-o', default='output',
                       help='Output directory for processed images')
    parser.add_argument('--operations', '-op', type=str,
                       help='JSON file containing processing operations')
    
    args = parser.parse_args()
    
    # Initialize processor
    processor = ImageProcessor(args.input, args.output)
    
    # Load operations
    try:
        with open(args.operations) as f:
            operations = json.load(f)
    except Exception as e:
        print(f"Error loading operations file: {e}")
        sys.exit(1)
    
    # Process images
    results = processor.batch_process(operations)
    
    # Print summary
    successful = sum(1 for _, success in results if success)
    print(f"\nProcessing complete:")
    print(f"Successfully processed: {successful}/{len(results)} images")

if __name__ == '__main__':
    main()
