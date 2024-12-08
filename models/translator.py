from transformers import MBartForConditionalGeneration, MBart50TokenizerFast

class LanguageTranslator:
    def __init__(self):
        # Initialize the model and tokenizer
        self.model = MBartForConditionalGeneration.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")
        self.tokenizer = MBart50TokenizerFast.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")
    
    def translate(self, text, source_lang, target_lang):
        """
        Translate text between languages
        
        Args:
            text (str): Text to translate
            source_lang (str): Source language code
            target_lang (str): Target language code
        
        Returns:
            str: Translated text
        """
        # Set source and target language
        self.tokenizer.src_lang = source_lang
        
        # Encode the input text
        inputs = self.tokenizer(text, return_tensors="pt")
        
        # Generate translation
        generated_tokens = self.model.generate(
            **inputs,
            forced_bos_token_id=self.tokenizer.lang_code_to_id[target_lang]
        )
        
        # Decode the translation
        translation = self.tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
        
        return translation

# Language code mappings
LANGUAGE_CODES = {
    'english': 'en_XX',
    'hindi': 'hi_IN',
    'malayalam': 'ml_IN',
    'telugu': 'te_IN'
}