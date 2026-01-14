import os
from pdf2image import convert_from_path
from PIL import Image

def convert_pdf_to_images(pdf_path: str, output_dir: str = "temp_images") -> list[str]:
    """
    Converts a PDF file to a series of images.
    Returns a list of paths to the saved images.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Convert PDF to list of PIL Image objects
    # Using 150 DPI to reduce token usage while maintaining readability
    images = convert_from_path(pdf_path, dpi=150)
    
    image_paths = []
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    
    for i, image in enumerate(images):
        image_path = os.path.join(output_dir, f"{base_name}_page_{i+1}.png")
        image.save(image_path, "PNG")
        image_paths.append(image_path)
        
    return image_paths
