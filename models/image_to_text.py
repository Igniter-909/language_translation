# import os
# import cv2
# import numpy as np
# import pytesseract
# from PIL import Image
# from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
# import torch

# class ImageToTextConverter:
#     def __init__(self, use_ocr=True, use_caption=True):
#         """
#         Initialize OCR and Image Captioning models with robust error handling
        
#         Args:
#             use_ocr (bool): Enable Tesseract OCR extraction
#             use_caption (bool): Enable image captioning
#         """
#         # Determine cache directory
#         self.cache_dir = os.path.join(os.getcwd(), 'model_cache')
#         os.makedirs(self.cache_dir, exist_ok=True)
        
#         # OCR Model configuration
#         self.use_ocr = use_ocr
        
#         # Image Captioning Model configuration
#         self.use_caption = use_caption
#         self.caption_model = None
#         self.caption_processor = None
#         self.caption_tokenizer = None
        
#         # Initialize models
#         self._load_models()
    
#     def _load_models(self):
#         """
#         Load image captioning models with comprehensive error handling
#         """
#         try:
#             if self.use_caption:
#                 # Load Image Captioning Model
#                 self.caption_model = VisionEncoderDecoderModel.from_pretrained(
#                     "nlpconnect/vit-gpt2-image-captioning", 
#                     cache_dir=self.cache_dir,
#                     local_files_only=False
#                 )
                
#                 # Load Processor and Tokenizer
#                 self.caption_processor = ViTImageProcessor.from_pretrained(
#                     "nlpconnect/vit-gpt2-image-captioning", 
#                     cache_dir=self.cache_dir,
#                     local_files_only=False
#                 )
                
#                 self.caption_tokenizer = AutoTokenizer.from_pretrained(
#                     "nlpconnect/vit-gpt2-image-captioning", 
#                     cache_dir=self.cache_dir,
#                     local_files_only=False
#                 )
                
#                 # Ensure model is on appropriate device
#                 self.caption_model.to(self._get_device())
        
#         except Exception as e:
#             print(f"Error loading image captioning model: {e}")
#             print("Falling back to caption generation without pre-trained model.")
#             self.use_caption = False
    
#     def _get_device(self):
#         """
#         Determine the appropriate device for model inference
        
#         Returns:
#             torch.device: CUDA if available, else CPU
#         """
#         return torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
#     def ocr_extract(self, image_path):
#         """
#         Extract text from image using Tesseract OCR with advanced preprocessing
        
#         Args:
#             image_path (str): Path to the image file
        
#         Returns:
#             str: Extracted text or error message
#         """
#         if not self.use_ocr:
#             return "OCR is disabled"
        
#         try:
#             # Read image
#             image = cv2.imread(image_path)
            
#             if image is None:
#                 return "Error: Unable to read image"
            
#             # Convert to grayscale
#             gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
#             # Apply multiple preprocessing techniques
#             # 1. Thresholding
#             thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
            
#             # 2. Noise removal (optional)
#             denoised = cv2.fastNlMeansDenoising(thresh)
            
#             # Perform text extraction
#             text = pytesseract.image_to_string(denoised, config='--psm 6')
            
#             return text.strip() if text else "No text detected"
        
#         except Exception as e:
#             return f"OCR Error: {str(e)}"
    
#     def generate_caption(self, image_path):
#         """
#         Generate image caption using Vision Transformer
        
#         Args:
#             image_path (str): Path to the image file
        
#         Returns:
#             str: Image caption or error message
#         """
#         if not self.use_caption or self.caption_model is None:
#             return "Image captioning is disabled"
        
#         try:
#             # Open image
#             image = Image.open(image_path).convert('RGB')
            
#             # Prepare image
#             inputs = self.caption_processor(images=image, return_tensors="pt").to(self._get_device())
            
#             # Generate caption
#             outputs = self.caption_model.generate(**inputs)
            
#             # Decode caption
#             caption = self.caption_tokenizer.decode(outputs[0], skip_special_tokens=True)
            
#             return caption
        
#         except Exception as e:
#             return f"Caption Generation Error: {str(e)}"
    
#     def convert_image(self, image_file):
#         """
#         Convert uploaded image file with robust file handling
        
#         Args:
#             image_file (FileStorage): Uploaded image file
        
#         Returns:
#             str: Path to saved image file
#         """
#         try:
#             # Ensure uploads directory exists
#             uploads_dir = 'uploads/images'
#             os.makedirs(uploads_dir, exist_ok=True)
            
#             # Generate unique filename to prevent overwrites
#             filename = os.path.join(
#                 uploads_dir, 
#                 f"{os.urandom(16).hex()}_{image_file.filename}"
#             )
            
#             # Save file
#             image_file.save(filename)
            
#             return filename
        
#         except Exception as e:
#             print(f"Image Conversion Error: {e}")
#             return None
    
#     def process_image(self, image_file):
#         """
#         Comprehensive image processing method
        
#         Args:
#             image_file (FileStorage): Uploaded image file
        
#         Returns:
#             dict: Processing results including OCR and caption
#         """
#         # Convert image
#         image_path = self.convert_image(image_file)
        
#         if image_path is None:
#             return {
#                 "status": "error",
#                 "message": "Failed to save image"
#             }
        
#         # Extract results
#         ocr_text = self.ocr_extract(image_path)
#         caption = self.generate_caption(image_path)
        
#         return {
#             "status": "success",
#             "image_path": image_path,
#             "ocr_text": ocr_text,
#             "caption": caption
#         }