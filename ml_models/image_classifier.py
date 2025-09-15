"""
Image Classification ML Model for Skin Conditions
Trained to classify skin conditions, wounds, and abnormalities from images
"""
import numpy as np
import cv2
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import EfficientNetB0, MobileNetV2
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
import joblib
import os
import logging
from typing import List, Dict, Tuple, Any
import json
from PIL import Image
import io

logger = logging.getLogger(__name__)

class SkinConditionClassifier:
    def __init__(self, model_path: str = "ml_models/trained_models/"):
        self.model_path = model_path
        self.model = None
        self.class_names = [
            'normal_skin',
            'acne',
            'eczema',
            'psoriasis',
            'rash',
            'wound',
            'burn',
            'bruise',
            'allergic_reaction',
            'fungal_infection',
            'bacterial_infection',
            'mole',
            'wart',
            'hives',
            'rosacea'
        ]
        
        self.condition_descriptions = {
            'normal_skin': 'Healthy skin with no visible abnormalities',
            'acne': 'Inflammatory skin condition with pimples, blackheads, and whiteheads',
            'eczema': 'Chronic skin condition causing inflammation, itching, and redness',
            'psoriasis': 'Autoimmune condition causing thick, scaly patches on the skin',
            'rash': 'General term for skin irritation or inflammation',
            'wound': 'Break in the skin, such as cuts, scrapes, or lacerations',
            'burn': 'Skin damage caused by heat, chemicals, or radiation',
            'bruise': 'Discoloration of skin due to broken blood vessels',
            'allergic_reaction': 'Skin reaction to allergens, often causing redness and itching',
            'fungal_infection': 'Infection caused by fungi, often appearing as ring-shaped lesions',
            'bacterial_infection': 'Infection caused by bacteria, often with pus and inflammation',
            'mole': 'Pigmented spot on the skin, usually benign',
            'wart': 'Small, rough growth caused by viral infection',
            'hives': 'Raised, itchy welts on the skin, often due to allergic reaction',
            'rosacea': 'Chronic skin condition causing facial redness and visible blood vessels'
        }
        
        self.severity_levels = {
            'normal_skin': 'low',
            'acne': 'low',
            'eczema': 'moderate',
            'psoriasis': 'moderate',
            'rash': 'moderate',
            'wound': 'moderate',
            'burn': 'high',
            'bruise': 'low',
            'allergic_reaction': 'moderate',
            'fungal_infection': 'moderate',
            'bacterial_infection': 'high',
            'mole': 'low',
            'wart': 'low',
            'hives': 'moderate',
            'rosacea': 'low'
        }
    
    def create_model(self, input_shape: Tuple[int, int, int] = (224, 224, 3)) -> keras.Model:
        """Create a CNN model for skin condition classification"""
        
        # Use EfficientNetB0 as base model
        base_model = EfficientNetB0(
            weights='imagenet',
            include_top=False,
            input_shape=input_shape
        )
        
        # Freeze base model layers initially
        base_model.trainable = False
        
        # Add custom classification head
        model = models.Sequential([
            base_model,
            layers.GlobalAveragePooling2D(),
            layers.Dropout(0.2),
            layers.Dense(512, activation='relu'),
            layers.Dropout(0.3),
            layers.Dense(256, activation='relu'),
            layers.Dropout(0.2),
            layers.Dense(len(self.class_names), activation='softmax')
        ])
        
        # Compile the model
        model.compile(
            optimizer=Adam(learning_rate=0.001),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def create_synthetic_data(self, num_samples_per_class: int = 100) -> Tuple[np.ndarray, np.ndarray]:
        """Create synthetic training data for skin conditions"""
        logger.info("Creating synthetic training data...")
        
        images = []
        labels = []
        
        for class_idx, class_name in enumerate(self.class_names):
            for i in range(num_samples_per_class):
                # Generate synthetic image based on condition type
                image = self._generate_synthetic_image(class_name)
                images.append(image)
                labels.append(class_idx)
        
        images = np.array(images)
        labels = np.array(labels)
        
        # Convert labels to categorical
        labels = tf.keras.utils.to_categorical(labels, num_classes=len(self.class_names))
        
        return images, labels
    
    def _generate_synthetic_image(self, condition: str) -> np.ndarray:
        """Generate synthetic image for a specific skin condition"""
        # Create base skin tone
        base_image = np.random.randint(180, 220, (224, 224, 3), dtype=np.uint8)
        
        # Add noise for texture
        noise = np.random.normal(0, 10, (224, 224, 3))
        base_image = np.clip(base_image + noise, 0, 255).astype(np.uint8)
        
        # Add condition-specific features
        if condition == 'acne':
            # Add red spots and bumps
            for _ in range(np.random.randint(3, 8)):
                center = (np.random.randint(50, 174), np.random.randint(50, 174))
                cv2.circle(base_image, center, np.random.randint(5, 15), (255, 100, 100), -1)
        
        elif condition == 'eczema':
            # Add red, inflamed patches
            for _ in range(np.random.randint(2, 5)):
                center = (np.random.randint(50, 174), np.random.randint(50, 174))
                cv2.circle(base_image, center, np.random.randint(20, 40), (200, 50, 50), -1)
        
        elif condition == 'rash':
            # Add scattered red spots
            for _ in range(np.random.randint(5, 15)):
                center = (np.random.randint(30, 194), np.random.randint(30, 194))
                cv2.circle(base_image, center, np.random.randint(3, 8), (255, 150, 150), -1)
        
        elif condition == 'wound':
            # Add irregular wound shape
            points = np.array([
                [np.random.randint(50, 174), np.random.randint(50, 174)],
                [np.random.randint(50, 174), np.random.randint(50, 174)],
                [np.random.randint(50, 174), np.random.randint(50, 174)],
                [np.random.randint(50, 174), np.random.randint(50, 174)]
            ], np.int32)
            cv2.fillPoly(base_image, [points], (150, 100, 100))
        
        elif condition == 'burn':
            # Add burn-like discoloration
            center = (np.random.randint(50, 174), np.random.randint(50, 174))
            cv2.circle(base_image, center, np.random.randint(15, 30), (100, 50, 50), -1)
        
        elif condition == 'bruise':
            # Add purple/blue discoloration
            center = (np.random.randint(50, 174), np.random.randint(50, 174))
            cv2.circle(base_image, center, np.random.randint(20, 35), (100, 50, 150), -1)
        
        elif condition == 'allergic_reaction':
            # Add red, raised areas
            for _ in range(np.random.randint(3, 7)):
                center = (np.random.randint(50, 174), np.random.randint(50, 174))
                cv2.circle(base_image, center, np.random.randint(8, 18), (255, 100, 100), -1)
        
        elif condition == 'fungal_infection':
            # Add ring-like pattern
            center = (np.random.randint(50, 174), np.random.randint(50, 174))
            cv2.circle(base_image, center, np.random.randint(15, 25), (150, 100, 100), 3)
        
        elif condition == 'bacterial_infection':
            # Add pus-like appearance
            center = (np.random.randint(50, 174), np.random.randint(50, 174))
            cv2.circle(base_image, center, np.random.randint(10, 20), (255, 255, 200), -1)
        
        elif condition == 'mole':
            # Add dark spot
            center = (np.random.randint(50, 174), np.random.randint(50, 174))
            cv2.circle(base_image, center, np.random.randint(5, 12), (50, 50, 50), -1)
        
        elif condition == 'wart':
            # Add raised, rough texture
            center = (np.random.randint(50, 174), np.random.randint(50, 174))
            cv2.circle(base_image, center, np.random.randint(8, 15), (200, 180, 160), -1)
        
        elif condition == 'hives':
            # Add raised, itchy welts
            for _ in range(np.random.randint(4, 10)):
                center = (np.random.randint(50, 174), np.random.randint(50, 174))
                cv2.circle(base_image, center, np.random.randint(6, 12), (255, 200, 200), -1)
        
        elif condition == 'rosacea':
            # Add facial redness
            center = (112, 112)  # Center of image
            cv2.circle(base_image, center, np.random.randint(30, 50), (255, 150, 150), -1)
        
        # Add some random variations
        base_image = cv2.GaussianBlur(base_image, (3, 3), 0)
        
        return base_image
    
    def train_model(self, X: np.ndarray, y: np.ndarray) -> Dict[str, Any]:
        """Train the skin condition classification model"""
        logger.info("Starting model training...")
        
        # Create the model
        self.model = self.create_model()
        
        # Split the data
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=np.argmax(y, axis=1)
        )
        
        # Data augmentation
        datagen = ImageDataGenerator(
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            horizontal_flip=True,
            zoom_range=0.2,
            brightness_range=[0.8, 1.2]
        )
        
        # Callbacks
        callbacks = [
            EarlyStopping(patience=10, restore_best_weights=True),
            ReduceLROnPlateau(factor=0.5, patience=5)
        ]
        
        # Train the model
        history = self.model.fit(
            datagen.flow(X_train, y_train, batch_size=32),
            steps_per_epoch=len(X_train) // 32,
            epochs=50,
            validation_data=(X_test, y_test),
            callbacks=callbacks,
            verbose=1
        )
        
        # Evaluate the model
        test_loss, test_accuracy = self.model.evaluate(X_test, y_test, verbose=0)
        
        logger.info(f"Test accuracy: {test_accuracy:.4f}")
        
        # Save the model
        self.save_model()
        
        return {
            'test_accuracy': test_accuracy,
            'test_loss': test_loss,
            'history': history.history
        }
    
    def predict_condition(self, image: np.ndarray) -> Dict[str, Any]:
        """Predict skin condition from image"""
        if self.model is None:
            self.load_model()
        
        # Preprocess the image
        processed_image = self.preprocess_image(image)
        
        # Make prediction
        predictions = self.model.predict(processed_image, verbose=0)
        prediction_proba = predictions[0]
        
        # Get top 3 predictions
        top_indices = np.argsort(prediction_proba)[-3:][::-1]
        
        results = []
        for idx in top_indices:
            condition = self.class_names[idx]
            probability = prediction_proba[idx]
            
            results.append({
                'condition_name': condition.replace('_', ' ').title(),
                'probability': float(probability),
                'description': self.condition_descriptions[condition],
                'severity': self.severity_levels[condition]
            })
        
        return {
            'possible_conditions': results,
            'confidence_score': float(max(prediction_proba)),
            'primary_condition': results[0] if results else None
        }
    
    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """Preprocess image for model input"""
        # Resize to model input size
        image = cv2.resize(image, (224, 224))
        
        # Normalize pixel values
        image = image.astype(np.float32) / 255.0
        
        # Add batch dimension
        image = np.expand_dims(image, axis=0)
        
        return image
    
    def detect_features(self, image: np.ndarray) -> List[Dict[str, Any]]:
        """Detect visual features in the image"""
        features = []
        
        # Convert to different color spaces
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Detect redness
        red_features = self._detect_redness(hsv)
        features.extend(red_features)
        
        # Detect texture abnormalities
        texture_features = self._detect_texture_abnormalities(gray)
        features.extend(texture_features)
        
        # Detect edges and contours
        edge_features = self._detect_edges_and_contours(gray)
        features.extend(edge_features)
        
        return features
    
    def _detect_redness(self, hsv_image: np.ndarray) -> List[Dict[str, Any]]:
        """Detect areas of redness in the image"""
        features = []
        
        # Define range for red colors in HSV
        lower_red1 = np.array([0, 50, 50])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([170, 50, 50])
        upper_red2 = np.array([180, 255, 255])
        
        # Create masks for red areas
        mask1 = cv2.inRange(hsv_image, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv_image, lower_red2, upper_red2)
        red_mask = mask1 + mask2
        
        # Find contours
        contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 100:  # Filter small areas
                confidence = min(area / 10000, 1.0)
                x, y, w, h = cv2.boundingRect(contour)
                
                features.append({
                    'feature_type': 'redness',
                    'confidence': confidence,
                    'location': {'x': int(x), 'y': int(y), 'width': int(w), 'height': int(h)},
                    'description': f'Red area detected with {confidence:.2f} confidence'
                })
        
        return features
    
    def _detect_texture_abnormalities(self, gray_image: np.ndarray) -> List[Dict[str, Any]]:
        """Detect texture abnormalities"""
        features = []
        
        # Calculate texture using Local Binary Pattern approximation
        kernel = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])
        texture_response = cv2.filter2D(gray_image, cv2.CV_64F, kernel)
        texture_variance = np.var(texture_response)
        
        if texture_variance > 1000:
            confidence = min(texture_variance / 5000, 1.0)
            features.append({
                'feature_type': 'texture_abnormality',
                'confidence': confidence,
                'location': None,
                'description': f'Abnormal texture pattern detected with {confidence:.2f} confidence'
            })
        
        return features
    
    def _detect_edges_and_contours(self, gray_image: np.ndarray) -> List[Dict[str, Any]]:
        """Detect edges and contours"""
        features = []
        
        # Edge detection
        edges = cv2.Canny(gray_image, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 200:
                # Calculate roundness
                perimeter = cv2.arcLength(contour, True)
                if perimeter > 0:
                    roundness = 4 * np.pi * area / (perimeter * perimeter)
                    
                    if roundness > 0.3:
                        confidence = min(roundness * area / 5000, 1.0)
                        x, y, w, h = cv2.boundingRect(contour)
                        
                        features.append({
                            'feature_type': 'irregular_shape',
                            'confidence': confidence,
                            'location': {'x': int(x), 'y': int(y), 'width': int(w), 'height': int(h)},
                            'description': f'Irregular shape detected with {confidence:.2f} confidence'
                        })
        
        return features
    
    def save_model(self):
        """Save the trained model"""
        os.makedirs(self.model_path, exist_ok=True)
        
        # Save the model
        self.model.save(os.path.join(self.model_path, 'skin_classifier.h5'))
        
        # Save class names and metadata
        metadata = {
            'class_names': self.class_names,
            'condition_descriptions': self.condition_descriptions,
            'severity_levels': self.severity_levels
        }
        
        with open(os.path.join(self.model_path, 'skin_classifier_metadata.json'), 'w') as f:
            json.dump(metadata, f, indent=2)
        
        logger.info(f"Model saved to {self.model_path}")
    
    def load_model(self):
        """Load the trained model"""
        try:
            self.model = keras.models.load_model(os.path.join(self.model_path, 'skin_classifier.h5'))
            
            # Load metadata
            with open(os.path.join(self.model_path, 'skin_classifier_metadata.json'), 'r') as f:
                metadata = json.load(f)
                self.class_names = metadata['class_names']
                self.condition_descriptions = metadata['condition_descriptions']
                self.severity_levels = metadata['severity_levels']
            
            logger.info("Model loaded successfully")
        except FileNotFoundError:
            logger.warning("Model files not found. Training new model...")
            self.train_from_scratch()
    
    def train_from_scratch(self):
        """Train a new model from scratch"""
        X, y = self.create_synthetic_data()
        self.train_model(X, y)

# Training script
if __name__ == "__main__":
    classifier = SkinConditionClassifier()
    
    # Create and train the model
    X, y = classifier.create_synthetic_data()
    results = classifier.train_model(X, y)
    
    print("Training completed!")
    print(f"Test accuracy: {results['test_accuracy']:.4f}")
    
    # Test the model
    test_image = classifier._generate_synthetic_image('acne')
    prediction = classifier.predict_condition(test_image)
    print(f"\nTest prediction: {prediction}")
