import unittest
from crisiscore.processor import ImageProcessor
from PIL import Image
import os
import shutil
import json

class TestImageProcessor(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test"""
        self.test_dir = "test_files"
        self.input_dir = os.path.join(self.test_dir, "input")
        self.output_dir = os.path.join(self.test_dir, "output")
        
        # Create test directories
        os.makedirs(self.input_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Create test image
        self.test_image = os.path.join(self.input_dir, "test.png")
        img = Image.new('RGB', (100, 100), color='red')
        img.save(self.test_image)
        
        # Initialize processor
        self.processor = ImageProcessor(self.input_dir, self.output_dir)
        
    def tearDown(self):
        """Clean up test environment after each test"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_resize_operation(self):
        """Test image resize operation"""
        operations = [{"type": "resize", "width": 50, "height": 50}]
        output_path = self.processor.process_image(self.test_image, operations)
        
        self.assertIsNotNone(output_path)
        with Image.open(output_path) as img:
            self.assertEqual(img.size, (50, 50))
    
    def test_rotate_operation(self):
        """Test image rotation operation"""
        operations = [{"type": "rotate", "angle": 90}]
        output_path = self.processor.process_image(self.test_image, operations)
        
        self.assertIsNotNone(output_path)
    
    def test_convert_operation(self):
        """Test image mode conversion"""
        operations = [{"type": "convert", "mode": "L"}]
        output_path = self.processor.process_image(self.test_image, operations)
        
        self.assertIsNotNone(output_path)
        with Image.open(output_path) as img:
            self.assertEqual(img.mode, "L")
    
    def test_batch_processing(self):
        """Test batch processing functionality"""
        # Create additional test image
        img = Image.new('RGB', (100, 100), color='blue')
        img.save(os.path.join(self.input_dir, "test2.png"))
        
        operations = [{"type": "resize", "width": 50, "height": 50}]
        results = self.processor.batch_process(operations)
        
        self.assertEqual(len(results), 2)
        self.assertTrue(all(success for _, success in results))

if __name__ == '__main__':
    unittest.main()
