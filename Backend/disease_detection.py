"""
AI-Powered Plant Disease Detection Module
Uses Hugging Face models for plant disease identification
"""

import requests
import base64
import json
from typing import Dict, List, Optional, Tuple
from PIL import Image
import io
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PlantDiseaseDetector:
    """
    AI-powered plant disease detection using Hugging Face models
    """
    
    def __init__(self, api_key: str):
        """
        Initialize the disease detector
        
        Args:
            api_key: Hugging Face API key
        """
        self.api_key = api_key
        self.headers = {"Authorization": f"Bearer {api_key}"}
        
        # Disease treatment database
        self.disease_treatments = {
            "angular_leaf_spot": {
                "treatment": "Apply copper-based fungicide. Ensure proper spacing between plants for air circulation. Remove infected leaves immediately.",
                "prevention": "Use certified disease-free seeds. Practice crop rotation. Avoid overhead watering.",
                "severity": "Medium"
            },
            "bean_rust": {
                "treatment": "Apply sulfur-based fungicide. Remove infected plant parts. Improve air circulation around plants.",
                "prevention": "Plant resistant varieties. Avoid working with wet plants. Ensure good drainage.",
                "severity": "High"
            },
            "bacterial_blight": {
                "treatment": "Apply copper-based bactericide. Remove and destroy infected plants. Improve air circulation.",
                "prevention": "Use disease-free seeds. Practice crop rotation. Avoid overhead irrigation.",
                "severity": "High"
            },
            "powdery_mildew": {
                "treatment": "Apply sulfur or potassium bicarbonate fungicide. Improve air circulation. Remove infected leaves.",
                "prevention": "Plant resistant varieties. Ensure proper spacing. Avoid overhead watering.",
                "severity": "Medium"
            },
            "leaf_spot": {
                "treatment": "Apply fungicide containing chlorothalonil or mancozeb. Remove infected leaves. Improve drainage.",
                "prevention": "Use certified seeds. Practice crop rotation. Avoid working with wet plants.",
                "severity": "Low"
            },
            "healthy": {
                "treatment": "Your plant looks healthy! Continue current care practices.",
                "prevention": "Maintain proper watering, fertilization, and pest monitoring to keep plants healthy.",
                "severity": "None"
            },
            "default": {
                "treatment": "Consult with local agricultural extension officer. Apply general plant care practices.",
                "prevention": "Regular monitoring, proper nutrition, and timely pest management.",
                "severity": "Unknown"
            }
        }
        
        # Kerala-specific crop diseases
        self.kerala_crop_diseases = {
            "rice": ["bacterial_blight", "brown_spot", "blast", "sheath_blight"],
            "coconut": ["bud_rot", "leaf_spot", "root_wilt", "crown_choking"],
            "pepper": "anthracnose", "foot_rot", "pollu_disease", "quick_wilt",
            "cardamom": "azhukal", "katte_disease", "clump_rot", "leaf_spot",
            "rubber": "leaf_fall", "powdery_mildew", "anthracnose", "brown_bast",
            "banana": "panama_wilt", "sigatoka", "bunchy_top", "anthracnose"
        }
    
    def detect_disease(self, image_bytes: bytes) -> Dict:
        """
        Detect plant disease from image using Hugging Face API
        
        Args:
            image_bytes: Image data as bytes
            
        Returns:
            Dictionary containing disease detection results
        """
        try:
            # Convert image to base64
            img_b64 = base64.b64encode(image_bytes).decode()
            
            # Use multiple models for better accuracy
            models = [
                "linkanjarad/mobilenet_v2_1.0_224-plant-disease-identification",
                "microsoft/resnet-50",  # Fallback model
            ]
            
            for model in models:
                try:
                    response = self._query_model(model, img_b64)
                    if response and response.get('success'):
                        return response
                except Exception as e:
                    logger.warning(f"Model {model} failed: {str(e)}")
                    continue
            
            return {
                'success': False, 
                'error': 'All models failed to process the image'
            }
            
        except Exception as e:
            logger.error(f"Error in disease detection: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def _query_model(self, model_name: str, image_b64: str) -> Dict:
        """
        Query a specific Hugging Face model
        
        Args:
            model_name: Name of the Hugging Face model
            image_b64: Base64 encoded image
            
        Returns:
            Model response dictionary
        """
        url = f"https://api-inference.huggingface.co/models/{model_name}"
        
        response = requests.post(
            url,
            headers=self.headers,
            json={"inputs": image_b64},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                # Get the top prediction
                top_prediction = result[0]
                disease_name = top_prediction.get('label', 'unknown').lower().replace(' ', '_')
                confidence = top_prediction.get('score', 0) * 100
                
                # Get treatment information
                treatment_info = self.disease_treatments.get(
                    disease_name, 
                    self.disease_treatments['default']
                )
                
                return {
                    'disease': disease_name.replace('_', ' ').title(),
                    'confidence': round(confidence, 2),
                    'treatment': treatment_info['treatment'],
                    'prevention': treatment_info['prevention'],
                    'severity': treatment_info['severity'],
                    'success': True,
                    'model_used': model_name
                }
        
        return {'success': False, 'error': f'Model {model_name} returned invalid response'}
    
    def get_crop_specific_diseases(self, crop: str) -> List[str]:
        """
        Get common diseases for a specific crop in Kerala
        
        Args:
            crop: Name of the crop
            
        Returns:
            List of common diseases for the crop
        """
        return self.kerala_crop_diseases.get(crop.lower(), [])
    
    def get_disease_info(self, disease_name: str) -> Dict:
        """
        Get detailed information about a specific disease
        
        Args:
            disease_name: Name of the disease
            
        Returns:
            Dictionary with disease information
        """
        return self.disease_treatments.get(disease_name.lower(), self.disease_treatments['default'])
    
    def batch_detect(self, image_list: List[bytes]) -> List[Dict]:
        """
        Detect diseases in multiple images
        
        Args:
            image_list: List of image bytes
            
        Returns:
            List of detection results
        """
        results = []
        for image_bytes in image_list:
            result = self.detect_disease(image_bytes)
            results.append(result)
        return results
    
    def validate_image(self, image_bytes: bytes) -> Tuple[bool, str]:
        """
        Validate if the uploaded image is suitable for disease detection
        
        Args:
            image_bytes: Image data as bytes
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            # Try to open the image
            image = Image.open(io.BytesIO(image_bytes))
            
            # Check image size
            width, height = image.size
            if width < 100 or height < 100:
                return False, "Image too small. Please upload a larger image (minimum 100x100 pixels)."
            
            if width > 4000 or height > 4000:
                return False, "Image too large. Please upload a smaller image (maximum 4000x4000 pixels)."
            
            # Check image format
            if image.format not in ['JPEG', 'PNG', 'JPG']:
                return False, "Unsupported image format. Please upload JPEG or PNG images."
            
            return True, "Image is valid"
            
        except Exception as e:
            return False, f"Invalid image: {str(e)}"

# Example usage and testing
if __name__ == "__main__":
    # Initialize detector (replace with your API key)
    detector = PlantDiseaseDetector("your_huggingface_api_key_here")
    
    # Example: Load and test an image
    try:
        with open("test_plant_image.jpg", "rb") as f:
            image_bytes = f.read()
        
        # Validate image
        is_valid, message = detector.validate_image(image_bytes)
        if not is_valid:
            print(f"Image validation failed: {message}")
        else:
            print("Image is valid, proceeding with detection...")
            
            # Detect disease
            result = detector.detect_disease(image_bytes)
            
            if result['success']:
                print(f"Disease: {result['disease']}")
                print(f"Confidence: {result['confidence']}%")
                print(f"Treatment: {result['treatment']}")
                print(f"Prevention: {result['prevention']}")
                print(f"Severity: {result['severity']}")
            else:
                print(f"Detection failed: {result['error']}")
                
    except FileNotFoundError:
        print("Test image not found. Please provide a valid image file.")
    except Exception as e:
        print(f"Error: {str(e)}")
