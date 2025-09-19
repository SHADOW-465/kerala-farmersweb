"""
AI Chatbot Assistant with Multilingual Support
Uses Hugging Face models for natural language processing
"""

import requests
import json
from typing import Dict, List, Optional, Tuple
import logging
from datetime import datetime
import re
import random

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIChatbotAssistant:
    """
    AI-powered chatbot assistant for farmers with multilingual support
    """
    
    def __init__(self, api_key: str):
        """
        Initialize the chatbot assistant
        
        Args:
            api_key: Hugging Face API key
        """
        self.api_key = api_key
        self.headers = {"Authorization": f"Bearer {api_key}"}
        
        # Language detection and support
        self.supported_languages = {
            'en': 'English',
            'ml': 'Malayalam', 
            'ta': 'Tamil',
            'hi': 'Hindi',
            'te': 'Telugu',
            'kn': 'Kannada'
        }
        
        # Knowledge base for common farming queries
        self.farming_knowledge = {
            'weather': {
                'en': "Weather conditions are crucial for farming. Check local weather forecasts regularly and plan your farming activities accordingly.",
                'ml': "കാലാവസ്ഥാ സാഹചര്യങ്ങൾ കാർഷികത്തിന് വളരെ പ്രധാനമാണ്. പ്രാദേശിക കാലാവസ്ഥാ പ്രവചനങ്ങൾ പതിവായി പരിശോധിച്ച് നിങ്ങളുടെ കാർഷിക പ്രവർത്തനങ്ങൾ ആസൂത്രണം ചെയ്യുക.",
                'ta': "வானிலை நிலைமைகள் விவசாயத்திற்கு மிகவும் முக்கியமானவை. உள்ளூர் வானிலை முன்னறிவிப்புகளை தவறாமல் பார்த்து உங்கள் விவசாய நடவடிக்கைகளை திட்டமிடுங்கள்.",
                'hi': "मौसम की स्थिति खेती के लिए बहुत महत्वपूर्ण है। स्थानीय मौसम पूर्वानुमानों को नियमित रूप से जांचें और अपनी खेती की गतिविधियों की योजना बनाएं।"
            },
            'soil_health': {
                'en': "Healthy soil is the foundation of good farming. Test your soil regularly, maintain proper pH levels, and add organic matter to improve soil structure.",
                'ml': "ആരോഗ്യമുള്ള മണ്ണാണ് നല്ല കാർഷികത്തിന്റെ അടിസ്ഥാനം. നിങ്ങളുടെ മണ്ണ് പതിവായി പരിശോധിക്കുക, ശരിയായ pH നിലകൾ നിലനിർത്തുക, മണ്ണിന്റെ ഘടന മെച്ചപ്പെടുത്താൻ ജൈവ വസ്തുക്കൾ ചേർക്കുക.",
                'ta': "ஆரோக்கியமான மண் நல்ல விவசாயத்தின் அடித்தளம். உங்கள் மண்ணை தவறாமல் சோதனை செய்யுங்கள், சரியான pH அளவுகளை பராமரிக்கவும், மண் அமைப்பை மேம்படுத்த கரிமப் பொருட்களை சேர்க்கவும்.",
                'hi': "स्वस्थ मिट्टी अच्छी खेती की नींव है। अपनी मिट्टी का नियमित रूप से परीक्षण करें, उचित pH स्तर बनाए रखें, और मिट्टी की संरचना में सुधार के लिए जैविक पदार्थ मिलाएं।"
            },
            'pest_control': {
                'en': "Integrated Pest Management (IPM) is the best approach. Use biological controls, crop rotation, and chemical pesticides only as a last resort.",
                'ml': "സമഗ്ര കീടനിയന്ത്രണം (IPM) ഏറ്റവും നല്ല സമീപനമാണ്. ജൈവ നിയന്ത്രണങ്ങൾ, വിള കറക്കൽ എന്നിവ ഉപയോഗിക്കുക, രാസ കീടനാശിനികൾ അവസാന ഉപാധിയായി മാത്രം ഉപയോഗിക്കുക.",
                'ta': "ஒருங்கிணைந்த பூச்சி மேலாண்மை (IPM) சிறந்த அணுகுமுறை. உயிரியல் கட்டுப்பாடுகள், பயிர் சுழற்சி ஆகியவற்றை பயன்படுத்துங்கள், வேதியியல் பூச்சிக்கொல்லிகள் கடைசி வழியாக மட்டுமே பயன்படுத்துங்கள்.",
                'hi': "एकीकृत कीट प्रबंधन (IPM) सबसे अच्छा तरीका है। जैविक नियंत्रण, फसल चक्रण का उपयोग करें, और रासायनिक कीटनाशकों का उपयोग केवल अंतिम उपाय के रूप में करें।"
            },
            'irrigation': {
                'en': "Efficient irrigation saves water and improves crop yield. Use drip irrigation, mulching, and water according to crop needs and soil moisture levels.",
                'ml': "കാര്യക്ഷമമായ നനയ്ക്കൽ വെള്ളം ലാഭിക്കുകയും വിള വിളവ് മെച്ചപ്പെടുത്തുകയും ചെയ്യുന്നു. ഡ്രിപ്പ് നനയ്ക്കൽ, മൾച്ചിംഗ് എന്നിവ ഉപയോഗിക്കുക, വിളയുടെ ആവശ്യങ്ങൾക്കും മണ്ണിന്റെ ഈർപ്പത്തിനും അനുസരിച്ച് വെള്ളം നൽകുക.",
                'ta': "திறமையான நீர்ப்பாசனம் தண்ணீரை சேமிக்கிறது மற்றும் பயிர் விளைச்சலை மேம்படுத்துகிறது. சொட்டு நீர்ப்பாசனம், மல்ச்சிங் ஆகியவற்றை பயன்படுத்துங்கள், பயிரின் தேவைகள் மற்றும் மண்ணின் ஈரப்பதத்திற்கு ஏற்ப நீர் கொடுங்கள்.",
                'hi': "कुशल सिंचाई पानी बचाती है और फसल की पैदावार बढ़ाती है। ड्रिप सिंचाई, मल्चिंग का उपयोग करें, और फसल की जरूरतों और मिट्टी की नमी के स्तर के अनुसार पानी दें।"
            },
            'fertilizer': {
                'en': "Use fertilizers based on soil test results. Apply the right amount at the right time. Consider organic fertilizers for sustainable farming.",
                'ml': "മണ്ണ് പരിശോധണ ഫലങ്ങളെ അടിസ്ഥാനമാക്കി വളങ്ങൾ ഉപയോഗിക്കുക. ശരിയായ സമയത്ത് ശരിയായ അളവിൽ പ്രയോഗിക്കുക. സുസ്ഥിര കാർഷികത്തിന് ജൈവ വളങ്ങൾ പരിഗണിക്കുക.",
                'ta': "மண் சோதனை முடிவுகளின் அடிப்படையில் உரங்களை பயன்படுத்துங்கள். சரியான நேரத்தில் சரியான அளவு பயன்படுத்துங்கள். நிலையான விவசாயத்திற்கு கரிம உரங்களை கருத்தில் கொள்ளுங்கள்.",
                'hi': "मिट्टी के परीक्षण परिणामों के आधार पर उर्वरकों का उपयोग करें। सही समय पर सही मात्रा में लगाएं। सतत खेती के लिए जैविक उर्वरकों पर विचार करें।"
            }
        }
        
        # Common queries and responses
        self.common_queries = {
            'greeting': {
                'en': ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"],
                'ml': ["നമസ്കാരം", "ഹലോ", "ഹായ്", "സുപ്രഭാതം", "സുപ്രഭാതം", "സായാഹ്നം"],
                'ta': ["வணக்கம்", "ஹலோ", "ஹாய்", "காலை வணக்கம்", "மதிய வணக்கம்", "மாலை வணக்கம்"],
                'hi': ["नमस्ते", "हैलो", "हाय", "सुप्रभात", "नमस्कार", "शुभ संध्या"]
            },
            'help': {
                'en': ["help", "assist", "support", "what can you do"],
                'ml': ["സഹായം", "സഹായിക്കുക", "പിന്തുണ", "നിങ്ങൾക്ക് എന്ത് ചെയ്യാൻ കഴിയും"],
                'ta': ["உதவி", "உதவுங்கள்", "ஆதரவு", "நீங்கள் என்ன செய்ய முடியும்"],
                'hi': ["मदद", "सहायता", "समर्थन", "आप क्या कर सकते हैं"]
            },
            'weather': {
                'en': ["weather", "rain", "temperature", "humidity", "forecast"],
                'ml': ["കാലാവസ്ഥ", "മഴ", "താപനില", "ആർദ്രത", "പ്രവചനം"],
                'ta': ["வானிலை", "மழை", "வெப்பநிலை", "ஈரப்பதம்", "முன்னறிவிப்பு"],
                'hi': ["मौसम", "बारिश", "तापमान", "नमी", "पूर्वानुमान"]
            }
        }
        
        # Response templates
        self.response_templates = {
            'greeting': {
                'en': "Hello! I'm your AI farming assistant. How can I help you with your farming needs today?",
                'ml': "ഹലോ! ഞാൻ നിങ്ങളുടെ AI കാർഷിക സഹായിയാണ്. ഇന്ന് നിങ്ങളുടെ കാർഷിക ആവശ്യങ്ങളിൽ എങ്ങനെ സഹായിക്കാം?",
                'ta': "வணக்கம்! நான் உங்கள் AI விவசாய உதவியாளர். இன்று உங்கள் விவசாய தேவைகளில் எப்படி உதவ முடியும்?",
                'hi': "नमस्ते! मैं आपका AI कृषि सहायक हूं। आज आपकी कृषि आवश्यकताओं में मैं कैसे मदद कर सकता हूं?"
            },
            'help': {
                'en': "I can help you with:\n• Weather information and forecasts\n• Crop recommendations\n• Plant disease detection\n• Soil health advice\n• Pest control tips\n• Irrigation guidance\n• Fertilizer recommendations\n• Government schemes information\n\nWhat would you like to know?",
                'ml': "എനിക്ക് സഹായിക്കാൻ കഴിയും:\n• കാലാവസ്ഥാ വിവരങ്ങളും പ്രവചനങ്ങളും\n• വിള നിർദ്ദേശങ്ങൾ\n• ചെടി രോഗം കണ്ടെത്തൽ\n• മണ്ണ് ആരോഗ്യ ഉപദേശം\n• കീടനിയന്ത്രണ നുറുങ്ങുകൾ\n• നനയ്ക്കൽ മാർഗദർശനം\n• വള നിർദ്ദേശങ്ങൾ\n• സർക്കാർ പദ്ധതി വിവരങ്ങൾ\n\nനിങ്ങൾക്ക് എന്ത് അറിയണം?",
                'ta': "நான் உதவ முடியும்:\n• வானிலை தகவல்கள் மற்றும் முன்னறிவிப்புகள்\n• பயிர் பரிந்துரைகள்\n• தாவர நோய் கண்டறிதல்\n• மண் ஆரோக்கிய ஆலோசனை\n• பூச்சி கட்டுப்பாட்டு குறிப்புகள்\n• நீர்ப்பாசன வழிகாட்டுதல்\n• உர பரிந்துரைகள்\n• அரசு திட்ட தகவல்கள்\n\nஉங்களுக்கு என்ன தெரிய வேண்டும்?",
                'hi': "मैं आपकी मदद कर सकता हूं:\n• मौसम की जानकारी और पूर्वानुमान\n• फसल की सिफारिशें\n• पौधों की बीमारी का पता लगाना\n• मिट्टी के स्वास्थ्य की सलाह\n• कीट नियंत्रण के टिप्स\n• सिंचाई मार्गदर्शन\n• उर्वरक सिफारिशें\n• सरकारी योजनाओं की जानकारी\n\nआप क्या जानना चाहते हैं?"
            }
        }
    
    def detect_language(self, text: str) -> str:
        """
        Detect the language of the input text
        
        Args:
            text: Input text
            
        Returns:
            Language code (en, ml, ta, hi, etc.)
        """
        # Simple language detection based on character patterns
        text_lower = text.lower()
        
        # Malayalam detection (Malayalam script)
        if any('\u0D00' <= char <= '\u0D7F' for char in text):
            return 'ml'
        
        # Tamil detection (Tamil script)
        if any('\u0B80' <= char <= '\u0BFF' for char in text):
            return 'ta'
        
        # Hindi detection (Devanagari script)
        if any('\u0900' <= char <= '\u097F' for char in text):
            return 'hi'
        
        # Telugu detection (Telugu script)
        if any('\u0C00' <= char <= '\u0C7F' for char in text):
            return 'te'
        
        # Kannada detection (Kannada script)
        if any('\u0C80' <= char <= '\u0CFF' for char in text):
            return 'kn'
        
        # Default to English if no script detected
        return 'en'
    
    def classify_query_intent(self, text: str, language: str = 'en') -> str:
        """
        Classify the intent of the user query
        
        Args:
            text: User query text
            language: Language code
            
        Returns:
            Intent category
        """
        text_lower = text.lower()
        
        # Check for greeting
        for greeting in self.common_queries['greeting'].get(language, self.common_queries['greeting']['en']):
            if greeting in text_lower:
                return 'greeting'
        
        # Check for help request
        for help_word in self.common_queries['help'].get(language, self.common_queries['help']['en']):
            if help_word in text_lower:
                return 'help'
        
        # Check for weather-related queries
        for weather_word in self.common_queries['weather'].get(language, self.common_queries['weather']['en']):
            if weather_word in text_lower:
                return 'weather'
        
        # Check for specific farming topics
        farming_keywords = {
            'soil_health': ['soil', 'ph', 'nutrient', 'fertilizer', 'compost'],
            'pest_control': ['pest', 'insect', 'disease', 'spray', 'pesticide'],
            'irrigation': ['water', 'irrigation', 'drip', 'sprinkler', 'moisture'],
            'crop_advice': ['crop', 'plant', 'seed', 'harvest', 'yield'],
            'market': ['price', 'market', 'sell', 'buy', 'cost']
        }
        
        for topic, keywords in farming_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return topic
        
        return 'general'
    
    def generate_response(self, query: str, language: str = None) -> Dict:
        """
        Generate AI response to user query
        
        Args:
            query: User query
            language: Language code (auto-detected if not provided)
            
        Returns:
            Dictionary with response and metadata
        """
        try:
            # Detect language if not provided
            if language is None:
                language = self.detect_language(query)
            
            # Classify query intent
            intent = self.classify_query_intent(query, language)
            
            # Generate response based on intent
            if intent == 'greeting':
                response = self.response_templates['greeting'].get(language, self.response_templates['greeting']['en'])
            elif intent == 'help':
                response = self.response_templates['help'].get(language, self.response_templates['help']['en'])
            elif intent in self.farming_knowledge:
                response = self.farming_knowledge[intent].get(language, self.farming_knowledge[intent]['en'])
            else:
                # Use Hugging Face model for general queries
                response = self._get_ai_response(query, language)
            
            return {
                'response': response,
                'language': language,
                'intent': intent,
                'timestamp': datetime.now().isoformat(),
                'success': True
            }
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return {
                'response': "I'm sorry, I encountered an error. Please try again or contact support.",
                'language': language or 'en',
                'intent': 'error',
                'timestamp': datetime.now().isoformat(),
                'success': False,
                'error': str(e)
            }
    
    def _get_ai_response(self, query: str, language: str) -> str:
        """
        Get AI response using Hugging Face models
        
        Args:
            query: User query
            language: Language code
            
        Returns:
            AI-generated response
        """
        try:
            # Use different models based on language
            model_mapping = {
                'en': 'microsoft/DialoGPT-medium',
                'ml': 'ai4bharat/indic-bert',
                'ta': 'ai4bharat/indic-bert',
                'hi': 'ai4bharat/indic-bert',
                'te': 'ai4bharat/indic-bert',
                'kn': 'ai4bharat/indic-bert'
            }
            
            model = model_mapping.get(language, 'microsoft/DialoGPT-medium')
            
            # Prepare query for the model
            if language != 'en':
                # For non-English languages, add context
                context_query = f"Farming question in {self.supported_languages.get(language, 'English')}: {query}"
            else:
                context_query = f"Farming question: {query}"
            
            # Query the model
            response = self._query_huggingface_model(model, context_query)
            
            if response and response.get('success'):
                return response['text']
            else:
                # Fallback response
                return self._get_fallback_response(query, language)
                
        except Exception as e:
            logger.error(f"Error getting AI response: {str(e)}")
            return self._get_fallback_response(query, language)
    
    def _query_huggingface_model(self, model: str, query: str) -> Dict:
        """
        Query Hugging Face model for response
        
        Args:
            model: Model name
            query: Input query
            
        Returns:
            Model response
        """
        try:
            url = f"https://api-inference.huggingface.co/models/{model}"
            
            response = requests.post(
                url,
                headers=self.headers,
                json={"inputs": query},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return {
                        'success': True,
                        'text': result[0].get('generated_text', 'Sorry, I could not generate a response.')
                    }
            
            return {'success': False, 'error': 'Model query failed'}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _get_fallback_response(self, query: str, language: str) -> str:
        """
        Get fallback response when AI models fail
        
        Args:
            query: User query
            language: Language code
            
        Returns:
            Fallback response
        """
        fallback_responses = {
            'en': "I understand you're asking about farming. While I'm processing your specific question, here are some general farming tips: Check your soil health regularly, monitor weather conditions, and follow sustainable farming practices. For more specific help, please contact your local agricultural extension officer.",
            'ml': "നിങ്ങൾ കാർഷികത്തെക്കുറിച്ച് ചോദിക്കുന്നുവെന്ന് ഞാൻ മനസ്സിലാക്കുന്നു. നിങ്ങളുടെ പ്രത്യേക ചോദ്യം പ്രോസസ്സ് ചെയ്യുമ്പോൾ, ചില പൊതുവായ കാർഷിക നുറുങ്ങുകൾ ഇതാ: നിങ്ങളുടെ മണ്ണിന്റെ ആരോഗ്യം പതിവായി പരിശോധിക്കുക, കാലാവസ്ഥാ സാഹചര്യങ്ങൾ നിരീക്ഷിക്കുക, സുസ്ഥിര കാർഷിക രീതികൾ പിന്തുടരുക. കൂടുതൽ പ്രത്യേക സഹായത്തിന്, ദയവായി നിങ്ങളുടെ പ്രാദേശിക കാർഷിക വിപുലീകരണ ഉദ്യോഗസ്ഥനെ ബന്ധപ്പെടുക.",
            'ta': "நீங்கள் விவசாயத்தைப் பற்றி கேட்கிறீர்கள் என்பதை நான் புரிந்துகொள்கிறேன். உங்கள் குறிப்பிட்ட கேள்வியை செயலாக்கும்போது, சில பொதுவான விவசாய குறிப்புகள் இங்கே: உங்கள் மண்ணின் ஆரோக்கியத்தை தவறாமல் சோதனை செய்யுங்கள், வானிலை நிலைமைகளை கண்காணிக்கவும், நிலையான விவசாய நடைமுறைகளை பின்பற்றுங்கள். மேலும் குறிப்பிட்ட உதவிக்கு, தயவுசெய்து உங்கள் உள்ளூர் விவசாய விரிவாக்க அதிகாரியைத் தொடர்பு கொள்ளுங்கள்.",
            'hi': "मैं समझता हूं कि आप खेती के बारे में पूछ रहे हैं। जब मैं आपके विशिष्ट प्रश्न को संसाधित कर रहा हूं, तो यहां कुछ सामान्य कृषि सुझाव हैं: अपनी मिट्टी के स्वास्थ्य की नियमित जांच करें, मौसम की स्थिति की निगरानी करें, और सतत कृषि प्रथाओं का पालन करें। अधिक विशिष्ट सहायता के लिए, कृपया अपने स्थानीय कृषि विस्तार अधिकारी से संपर्क करें।"
        }
        
        return fallback_responses.get(language, fallback_responses['en'])
    
    def get_supported_languages(self) -> Dict[str, str]:
        """Get list of supported languages"""
        return self.supported_languages
    
    def add_custom_knowledge(self, topic: str, responses: Dict[str, str]):
        """
        Add custom knowledge to the chatbot
        
        Args:
            topic: Topic name
            responses: Dictionary of language-specific responses
        """
        self.farming_knowledge[topic] = responses
        logger.info(f"Added custom knowledge for topic: {topic}")
    
    def get_conversation_history(self, user_id: str) -> List[Dict]:
        """
        Get conversation history for a user (placeholder for future implementation)
        
        Args:
            user_id: User identifier
            
        Returns:
            List of conversation messages
        """
        # This would typically connect to a database
        # For now, return empty list
        return []

# Example usage and testing
if __name__ == "__main__":
    # Initialize chatbot (replace with your API key)
    chatbot = AIChatbotAssistant("your_huggingface_api_key_here")
    
    # Test queries in different languages
    test_queries = [
        "Hello, I need help with my rice crop",
        "നമസ്കാരം, എന്റെ നെല്ല് വിളയിൽ സഹായം വേണം",
        "வணக்கம், எனது நெல் பயிரில் உதவி வேண்டும்",
        "नमस्ते, मुझे अपनी चावल की फसल में मदद चाहिए",
        "What should I do about pests in my garden?",
        "How can I improve my soil health?"
    ]
    
    print("AI Chatbot Assistant - Test Results")
    print("=" * 50)
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        result = chatbot.generate_response(query)
        print(f"Language: {result['language']}")
        print(f"Intent: {result['intent']}")
        print(f"Response: {result['response']}")
        print("-" * 30)
