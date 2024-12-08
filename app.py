import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import logging

# Import models
from models.translator import LanguageTranslator, LANGUAGE_CODES
# from models.speech_to_text import SpeechToTextConverter
# from models.image_to_text import ImageToTextConverter

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Flask Application Configuration
app = Flask(__name__)

# Configuration settings
app.config.update(
    SECRET_KEY='hacsvtyfwebasihcgtyfvbasyug'
    # UPLOAD_FOLDER='uploads',
    # MAX_CONTENT_LENGTH=16 * 1024 * 1024,  # 16 MB max file size
    # ALLOWED_EXTENSIONS={
    #     'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 
    #     'wav', 'mp3', 'ogg', 'flac', 
    #     'mp4', 'avi', 'mkv'
    #}
)

# Ensure upload directories exist
# os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'audio'), exist_ok=True)
# os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'images'), exist_ok=True)

# Initialize models
translator = LanguageTranslator()
# speech_converter = SpeechToTextConverter()
# image_converter = ImageToTextConverter()

# Utility Functions
def allowed_file(filename):
    """
    Check if the uploaded file has an allowed extension
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Main Routes
@app.route('/')
def index():
    """
    Main landing page with navigation
    """
    return render_template('index.html')

# Translation Routes
@app.route('/translate', methods=['POST'])
def translate():
    """
    Translation endpoint supporting multiple languages
    """
    try:
        data = request.get_json()
        
        # Validate input
        if not all(key in data for key in ['text', 'source_lang', 'target_lang']):
            return jsonify({"error": "Missing required parameters"}), 400
        
        # Get language codes
        source_code = LANGUAGE_CODES.get(data['source_lang'].lower())
        target_code = LANGUAGE_CODES.get(data['target_lang'].lower())
        
        if not source_code or not target_code:
            return jsonify({"error": "Invalid language"}), 400
        
        # Perform translation
        translation = translator.translate(
            data['text'], 
            source_lang=source_code, 
            target_lang=target_code
        )
        
        return jsonify({
            "original_text": data['text'],
            "translated_text": translation,
            "source_lang": data['source_lang'],
            "target_lang": data['target_lang']
        })
    
    except Exception as e:
        logger.error(f"Translation error: {str(e)}")
        return jsonify({"error": "Translation failed"}), 500

# Speech to Text Routes
# @app.route('/speech-to-text', methods=['POST'])
# def speech_to_text():
#     """
#     Speech to Text conversion endpoint
#     """
#     try:
#         # Check if file is present
#         if 'audio' not in request.files:
#             return jsonify({"error": "No audio file uploaded"}), 400
        
#         audio_file = request.files['audio']
        
#         # Check if filename is empty
#         if audio_file.filename == '':
#             return jsonify({"error": "No selected file"}), 400
        
#         # Check file extension
#         if audio_file and allowed_file(audio_file.filename):
#             # Secure filename
#             filename = secure_filename(audio_file.filename)
            
#             # Save file
#             file_path = os.path.join(
#                 app.config['UPLOAD_FOLDER'], 
#                 'audio', 
#                 filename
#             )
#             audio_file.save(file_path)
            
#             # Transcribe audio
#             transcription = speech_converter.transcribe(file_path)
            
#             # Log successful transcription
#             logger.info(f"Successfully transcribed audio: {filename}")
            
#             return jsonify({
#                 "transcription": transcription['text'],
#                 "language": transcription['language'],
#                 "filename": filename
#             })
        
#         return jsonify({"error": "Invalid file type"}), 400
    
#     except Exception as e:
#         logger.error(f"Speech to text conversion error: {str(e)}")
#         return jsonify({"error": "Conversion failed"}), 500

# # Image to Text Routes
# @app.route('/image-to-text', methods=['POST'])
# def image_to_text():
#     """
#     Image to Text conversion endpoint with comprehensive processing
#     """
#     try:
#         # Check if file is present
#         if 'image' not in request.files:
#             return jsonify({"error": "No image file uploaded"}), 400
        
#         image_file = request.files['image']
        
#         # Check if filename is empty
#         if image_file.filename == '':
#             return jsonify({"error": "No selected file"}), 400
        
#         # Check file extension
#         if image_file and allowed_file(image_file.filename):
#             # Process the image using the new method
#             result = image_converter.process_image(image_file)
            
#             # Check processing status
#             if result.get('status') == 'error':
#                 return jsonify({"error": result.get('message', "Image processing failed")}), 400
            
#             # Log successful conversion
#             logger.info(f"Successfully processed image: {result['image_path']}")
            
#             return jsonify({
#                 "ocr_text": result.get('ocr_text', ''),
#                 "image_caption": result.get('caption', ''),
#                 "image_path": result.get('image_path', ''),
#                 "filename": os.path.basename(result.get('image_path', ''))
#             })
        
#         return jsonify({"error": "Invalid file type"}), 400
    
#     except Exception as e:
#         logger.error(f"Image to text conversion error: {str(e)}")
#         return jsonify({"error": "Conversion failed"}), 500

# Error Handlers
@app.errorhandler(413)
def request_entity_too_large(error):
    """
    Handle file size exceeded error
    """
    return jsonify({"error": "File too large. Maximum size is 16 MB"}), 413

@app.errorhandler(404)
def page_not_found(error):
    """
    Handle 404 errors
    """
    return jsonify({"error": "Page not found"}), 404

@app.errorhandler(500)
def internal_server_error(error):
    """
    Handle internal server errors
    """
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({"error": "Internal server error"}), 500

# Application Entry Point
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',  # Listen on all available interfaces
        port=5000,       # Standard Flask development port
        debug=True       # Enable debug mode
    )