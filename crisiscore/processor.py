from PIL import Image
import os
from tqdm import tqdm
from typing import List, Tuple, Optional
import logging

class ImageProcessor:
    """Core image processing functionality."""
    
    def __init__(self, input_dir: str = "input", output_dir: str = "output"):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self._setup_dirs()
        self._setup_logging()
        
    def _setup_dirs(self):
        """Create input and output directories if they don't exist."""
        os.makedirs(self.input_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
        
    def _setup_logging(self):
        """Configure logging."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('crisiscore.log'),
                logging.StreamHandler()
            ]
        )
        
    def process_image(self, image_path: str, operations: List[dict]) -> Optional[str]:
        """Process a single image with given operations."""
        try:
            with Image.open(image_path) as img:
                for op in operations:
                    if op['type'] == 'resize':
                        img = img.resize((op['width'], op['height']))
                    elif op['type'] == 'rotate':
                        img = img.rotate(op['angle'])
                    elif op['type'] == 'convert':
                        img = img.convert(op['mode'])
                
                output_path = os.path.join(
                    self.output_dir,
                    f"processed_{os.path.basename(image_path)}"
                )
                img.save(output_path)
                logging.info(f"Processed {image_path} -> {output_path}")
                return output_path
        except Exception as e:
            logging.error(f"Error processing {image_path}: {str(e)}")
            return None
            
    def batch_process(self, operations: List[dict]) -> List[Tuple[str, bool]]:
        """Process all images in input directory."""
        results = []
        image_files = [f for f in os.listdir(self.input_dir)
                      if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
        
        for image_file in tqdm(image_files, desc="Processing images"):
            input_path = os.path.join(self.input_dir, image_file)
            success = self.process_image(input_path, operations) is not None
            results.append((image_file, success))
            
        return results
