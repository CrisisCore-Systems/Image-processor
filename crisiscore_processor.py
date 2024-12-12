import os
import sys
from PIL import Image, ImageEnhance, ImageFilter
from datetime import datetime
import json
from colorama import init, Fore, Style
from tqdm import tqdm
import logging
import shutil
from typing import Optional, Dict, List
import time

# Initialize colorama for cross-platform color support
init()

class CCTheme:
    PRIMARY = Fore.GREEN + Style.BRIGHT
    SECONDARY = Fore.CYAN + Style.BRIGHT
    ACCENT = Fore.MAGENTA + Style.BRIGHT
    WARN = Fore.YELLOW + Style.BRIGHT
    ERROR = Fore.RED + Style.BRIGHT
    RESET = Style.RESET_ALL
    
    @staticmethod
    def primary(text): return f"{CCTheme.PRIMARY}{text}{CCTheme.RESET}"
    
    @staticmethod
    def secondary(text): return f"{CCTheme.SECONDARY}{text}{CCTheme.RESET}"
    
    @staticmethod
    def accent(text): return f"{CCTheme.ACCENT}{text}{CCTheme.RESET}"

class ImageProcessor:
    def __init__(self):
        self.supported_formats = {'.jpg', '.jpeg', '.png', '.webp'}
        self.history = []
        self.load_history()

    def load_history(self):
        try:
            if os.path.exists('cc_history.json'):
                with open('cc_history.json', 'r') as f:
                    self.history = json.load(f)
        except Exception as e:
            logging.error(f"History load failed: {e}")
            self.history = []

    def save_history(self):
        try:
            with open('cc_history.json', 'w') as f:
                json.dump(self.history[-100:], f)  # Keep last 100 operations
        except Exception as e:
            logging.error(f"History save failed: {e}")

    def process_image(self, input_path: str, operation: str, **kwargs) -> Optional[str]:
        try:
            with Image.open(input_path) as img:
                output_path = self._generate_output_path(input_path, operation)
                
                if operation == 'convert':
                    img.save(output_path, format=kwargs['format'])
                elif operation == 'resize':
                    resized = img.resize((kwargs['width'], kwargs['height']))
                    resized.save(output_path)
                elif operation == 'rotate':
                    rotated = img.rotate(kwargs['angle'], expand=True)
                    rotated.save(output_path)
                elif operation == 'enhance':
                    enhanced = self._apply_enhancement(img, kwargs['enhancement_type'], kwargs['factor'])
                    enhanced.save(output_path)
                
                self._record_operation(input_path, output_path, operation, kwargs)
                return output_path
        except Exception as e:
            logging.error(f"Processing error: {e}")
            return None

    def _generate_output_path(self, input_path: str, operation: str) -> str:
        directory = os.path.dirname(input_path)
        filename = os.path.basename(input_path)
        name, ext = os.path.splitext(filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return os.path.join(directory, f"{name}_{operation}_{timestamp}{ext}")

    def _record_operation(self, input_path: str, output_path: str, operation: str, params: Dict):
        self.history.append({
            'timestamp': datetime.now().isoformat(),
            'operation': operation,
            'input': input_path,
            'output': output_path,
            'parameters': params
        })
        self.save_history()

    @staticmethod
    def _apply_enhancement(img: Image.Image, enhancement_type: str, factor: float) -> Image.Image:
        enhancer_map = {
            'brightness': ImageEnhance.Brightness,
            'contrast': ImageEnhance.Contrast,
            'sharpness': ImageEnhance.Sharpness,
            'color': ImageEnhance.Color
        }
        enhancer = enhancer_map[enhancement_type](img)
        return enhancer.enhance(factor)

class FileExplorer:
    def __init__(self):
        self.current_path = os.path.abspath(os.getcwd())
        self.supported_formats = {'.jpg', '.jpeg', '.png', '.webp'}

    def get_directory_content(self) -> tuple[list, list]:
        try:
            items = sorted(os.listdir(self.current_path))
            folders = [d for d in items if os.path.isdir(os.path.join(self.current_path, d))]
            files = [f for f in items if os.path.isfile(os.path.join(self.current_path, f)) 
                    and os.path.splitext(f)[1].lower() in self.supported_formats]
            return folders, files
        except Exception as e:
            logging.error(f"Error reading directory: {e}")
            return [], []

    def navigate(self, selection: str) -> bool:
        try:
            if selection == '..':
                new_path = os.path.dirname(self.current_path)
            else:
                new_path = os.path.join(self.current_path, selection)
            
            if os.path.exists(new_path) and os.path.isdir(new_path):
                os.chdir(new_path)
                self.current_path = new_path
                return True
            return False
        except Exception as e:
            logging.error(f"Navigation error: {e}")
            return False

    def get_file_info(self, filename: str) -> Dict:
        path = os.path.join(self.current_path, filename)
        try:
            stats = os.stat(path)
            return {
                'size': self.format_size(stats.st_size),
                'modified': datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M'),
                'type': os.path.splitext(filename)[1][1:].upper()
            }
        except Exception as e:
            logging.error(f"Error getting file info: {e}")
            return {'size': 'N/A', 'modified': 'N/A', 'type': 'N/A'}

    @staticmethod
    def format_size(size: int) -> str:
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f}{unit}"
            size /= 1024
        return f"{size:.1f}TB"

class CrisisCoreCLI:
    def __init__(self):
        self.processor = ImageProcessor()
        self.explorer = FileExplorer()
        self.setup_logging()
        self.status = "READY"
        self.current_operation = "BROWSING"

    def setup_logging(self):
        logging.basicConfig(
            filename='crisiscore.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def clear_screen(self):
        os.system('clear' if os.name != 'nt' else 'cls')

    def print_header(self):
        print(f"\n{CCTheme.PRIMARY}╔══════════════════════════════════════════════════════════╗")
        print(f"║               CRISISCORE SYSTEMS IMAGE PROCESSOR           ║")
        print(f"║                     [STATUS: {self.status}]                     ║")
        print(f"╚══════════════════════════════════════════════════════════╝{CCTheme.RESET}")

    def print_menu(self):
        print(f"\n{CCTheme.secondary('Available Operations:')}")
        print(f"{CCTheme.PRIMARY}╔════════════════════════════════╗")
        print(f"║{CCTheme.RESET} 1. Browse Files               {CCTheme.PRIMARY}║")
        print(f"║{CCTheme.RESET} 2. Convert Format             {CCTheme.PRIMARY}║")
        print(f"║{CCTheme.RESET} 3. Resize Image               {CCTheme.PRIMARY}║")
        print(f"║{CCTheme.RESET} 4. Rotate Image               {CCTheme.PRIMARY}║")
        print(f"║{CCTheme.RESET} 5. Enhance Image              {CCTheme.PRIMARY}║")
        print(f"║{CCTheme.RESET} 6. View History               {CCTheme.PRIMARY}║")
        print(f"║{CCTheme.RESET} 7. Exit                       {CCTheme.PRIMARY}║")
        print(f"╚════════════════════════════════╝{CCTheme.RESET}")

    def show_progress(self, operation: str):
        with tqdm(
            total=100,
            desc=CCTheme.secondary(f"Processing"),
            bar_format='{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt}',
            colour='green'
        ) as pbar:
            for _ in range(100):
                time.sleep(0.01)
                pbar.update(1)

    def browse_files(self) -> Optional[str]:
        while True:
            self.clear_screen()
            self.print_header()
            folders, files = self.explorer.get_directory_content()
            
            print(f"\n{CCTheme.secondary('Current Location:')}")
            print(f"{CCTheme.PRIMARY}{self.explorer.current_path}{CCTheme.RESET}")
            
            print(f"\n{CCTheme.secondary('Navigation:')}")
            print("0. Return to Main Menu")
            print(".. Go Up")
            
            if folders:
                print(f"\n{CCTheme.secondary('Folders:')}")
                for i, folder in enumerate(folders, 1):
                    print(f"{i}. 📁 {folder}")
            
            if files:
                print(f"\n{CCTheme.secondary('Images:')}")
                print(f"{'ID':3} {'Name':30} {'Size':10} {'Type':6} {'Modified':19}")
                for i, file in enumerate(files, len(folders) + 1):
                    info = self.explorer.get_file_info(file)
                    print(f"{i:<3} {file[:30]:30} {info['size']:10} {info['type']:6} {info['modified']}")
            
            choice = input(f"\n{CCTheme.secondary('Enter selection (0 to return):')} ").strip()
            
            if choice == '0':
                return None
            elif choice == '..':
                self.explorer.navigate('..')
                continue
                
            try:
                index = int(choice)
                if 1 <= index <= len(folders):
                    folder_name = folders[index-1]
                    self.explorer.navigate(folder_name)
                elif len(folders) < index <= len(folders) + len(files):
                    file_name = files[index-len(folders)-1]
                    return os.path.join(self.explorer.current_path, file_name)
                else:
                    print(CCTheme.ERROR + "Invalid selection!" + CCTheme.RESET)
                    input("Press Enter to continue...")
            except ValueError:
                print(CCTheme.ERROR + "Please enter a number!" + CCTheme.RESET)
                input("Press Enter to continue...")

    def run(self):
        while True:
            try:
                self.clear_screen()
                self.print_header()
                self.print_menu()
                
                choice = input(f"\n{CCTheme.secondary('Select operation:')} ").strip()
                
                if choice == '1':
                    self.browse_files()
                elif choice == '2':
                    self.convert_format()
                elif choice == '3':
                    self.resize_image()
                elif choice == '4':
                    self.rotate_image()
                elif choice == '5':
                    self.enhance_image()
                elif choice == '6':
                    self.view_history()
                elif choice == '7':
                    print(f"\n{CCTheme.secondary('Exiting...')}")
                    break
                else:
                    print(CCTheme.ERROR + "Invalid selection!" + CCTheme.RESET)
                    input("Press Enter to continue...")
                    
            except KeyboardInterrupt:
                print(f"\n{CCTheme.WARN}Operation cancelled.{CCTheme.RESET}")
                break
            except Exception as e:
                logging.error(f"Unexpected error: {e}")
                print(f"\n{CCTheme.ERROR}An error occurred! Check crisiscore.log for details.{CCTheme.RESET}")
                input("Press Enter to continue...")

if __name__ == '__main__':
    try:
        cli = CrisisCoreCLI()
        cli.run()
    except Exception as e:
        logging.error(f"Application error: {e}")
        print(CCTheme.ERROR + "A critical error occurred. Check crisiscore.log for details." + CCTheme.RESET)
