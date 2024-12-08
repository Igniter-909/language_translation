# import os
# import whisper
# import numpy as np

# class SpeechToTextConverter:
#     def __init__(self, model_size='base'):
#         """
#         Initialize Whisper model
        
#         Args:
#             model_size (str): Size of the Whisper model 
#             Options: 'tiny', 'base', 'small', 'medium', 'large'
#         """
#         self.model = whisper.load_model(model_size)
    
#     def transcribe(self, audio_path, language='en'):
#         """
#         Transcribe audio file
        
#         Args:
#             audio_path (str): Path to the audio file
#             language (str): Language of the audio (optional)
        
#         Returns:
#             dict: Transcription results
#         """
#         # Transcribe the audio
#         result = self.model.transcribe(
#             audio_path, 
#             language=language, 
#             fp16=False  # Disable FP16 if not using CUDA
#         )
        
#         return {
#             'text': result['text'],
#             'language': result['language'],
#             'segments': result['segments']
#         }
    
#     def convert_audio(self, audio_file):
#         """
#         Convert uploaded audio file to a format Whisper can process
        
#         Args:
#             audio_file (FileStorage): Uploaded audio file
        
#         Returns:
#             str: Path to converted audio file
#         """
#         # Ensure uploads directory exists
#         os.makedirs('uploads/audio', exist_ok=True)
        
#         # Generate unique filename
#         filename = os.path.join('uploads/audio', audio_file.filename)
#         audio_file.save(filename)
        
#         return filename