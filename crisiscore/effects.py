from PIL import Image, ImageEnhance, ImageFilter
from typing import Optional

class ImageEffects:
    @staticmethod
    def apply_filter(image: Image.Image, filter_type: str) -> Image.Image:
        """Apply various filters to the image."""
        filters = {
            'blur': ImageFilter.BLUR,
            'sharpen': ImageFilter.SHARPEN,
            'edge_enhance': ImageFilter.EDGE_ENHANCE,
            'emboss': ImageFilter.EMBOSS,
            'contour': ImageFilter.CONTOUR,
            'find_edges': ImageFilter.FIND_EDGES
        }
        return image.filter(filters.get(filter_type, ImageFilter.BLUR))
    
    @staticmethod
    def adjust_colors(image: Image.Image, brightness: float = 1.0,
                     contrast: float = 1.0, saturation: float = 1.0) -> Image.Image:
        """Adjust image color properties."""
        if brightness != 1.0:
            image = ImageEnhance.Brightness(image).enhance(brightness)
        if contrast != 1.0:
            image = ImageEnhance.Contrast(image).enhance(contrast)
        if saturation != 1.0:
            image = ImageEnhance.Color(image).enhance(saturation)
        return image
    
    @staticmethod
    def add_watermark(image: Image.Image, text: str, position: tuple = None,
                     opacity: float = 0.5) -> Image.Image:
        """Add text watermark to image."""
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
            
        # Create watermark layer
        watermark = Image.new('RGBA', image.size, (0,0,0,0))
        from PIL import ImageDraw, ImageFont
        draw = ImageDraw.Draw(watermark)
        
        # Calculate text size and position
        if position is None:
            position = (image.size[0] - 200, image.size[1] - 50)
            
        draw.text(position, text, fill=(255,255,255,int(255*opacity)))
        return Image.alpha_composite(image, watermark)
