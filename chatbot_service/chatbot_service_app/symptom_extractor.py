from sentence_transformers import SentenceTransformer
import re
import json
import os
from typing import List, Dict, Set, Optional
import numpy as np
import logging

logger = logging.getLogger(__name__)

class SymptomExtractor:
    """Extract symptoms from Vietnamese medical text using NLP with JSON configuration"""
    
    def __init__(self, patterns_file: str = None):
        # Load Vietnamese sentence transformer
        self.encoder = SentenceTransformer('keepitreal/vietnamese-sbert')
        
        # Default patterns file path
        if patterns_file is None:
            patterns_file = os.path.join(os.path.dirname(__file__), 'data', 'symptom_patterns.json')
        
        self.patterns_file = patterns_file
        
        # Initialize pattern data
        self.symptom_patterns = {}
        self.severity_modifiers = {}
        self.duration_modifiers = {}
        self.negation_keywords = []
        self.emergency_keywords = []
        self.pattern_to_symptom = {}
        self.pattern_embeddings = None
        
        # Load patterns from JSON
        self.load_patterns()
        
        # Prepare for semantic matching
        self._prepare_semantic_matching()
    
    def load_patterns(self) -> bool:
        """Load symptom patterns from JSON file"""
        try:
            if not os.path.exists(self.patterns_file):
                logger.warning(f"Patterns file not found: {self.patterns_file}")
                self._load_default_patterns()
                return False
            
            with open(self.patterns_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Load main pattern data
            self.symptom_patterns = data.get('symptom_patterns', {})
            self.severity_modifiers = data.get('severity_modifiers', {})
            self.duration_modifiers = data.get('duration_modifiers', {})
            self.negation_keywords = data.get('negation_keywords', [])
            self.emergency_keywords = data.get('emergency_keywords', [])
            
            logger.info(f"Loaded {len(self.symptom_patterns)} symptom patterns from {self.patterns_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error loading patterns file: {e}")
            self._load_default_patterns()
            return False
    
    def _load_default_patterns(self):
        """Load minimal default patterns if JSON file fails"""
        logger.info("Loading minimal default patterns")
        self.symptom_patterns = {
            'đau_đầu': {
                'patterns': ['đau đầu', 'nhức đầu'],
                'category': 'neurological',
                'severity_indicators': {'severe': ['dữ dội'], 'mild': ['nhẹ']},
                'is_critical': False,
                'weight': 1.0
            },
            'sốt': {
                'patterns': ['sốt', 'nóng người'],
                'category': 'general',
                'severity_indicators': {'severe': ['sốt cao'], 'mild': ['sốt nhẹ']},
                'is_critical': False,
                'weight': 1.2
            }
        }
        self.severity_modifiers = {
            'mild': ['nhẹ', 'chút ít'],
            'moderate': ['vừa', 'trung bình'],
            'severe': ['nặng', 'dữ dội']
        }
    
    def _prepare_semantic_matching(self):
        """Prepare embeddings for semantic similarity matching"""
        try:
            # Create vocabulary from all patterns
            all_patterns = []
            self.pattern_to_symptom = {}
            
            for symptom_key, symptom_data in self.symptom_patterns.items():
                patterns = symptom_data.get('patterns', [])
                for pattern in patterns:
                    all_patterns.append(pattern)
                    self.pattern_to_symptom[pattern] = symptom_key
            
            if all_patterns:
                self.pattern_embeddings = self.encoder.encode(all_patterns)
                logger.info(f"Created embeddings for {len(all_patterns)} patterns")
            else:
                logger.warning("No patterns found for embedding creation")
                
        except Exception as e:
            logger.error(f"Error preparing semantic matching: {e}")
    
    def save_patterns(self, output_file: str = None) -> bool:
        """Save current patterns to JSON file"""
        try:
            if output_file is None:
                output_file = self.patterns_file
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            data = {
                'version': '1.0',
                'language': 'vi',
                'last_updated': '2025-06-10',
                'symptom_patterns': self.symptom_patterns,
                'severity_modifiers': self.severity_modifiers,
                'duration_modifiers': self.duration_modifiers,
                'negation_keywords': self.negation_keywords,
                'emergency_keywords': self.emergency_keywords
            }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Patterns saved to {output_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving patterns: {e}")
            return False
    
    def add_symptom_pattern(self, symptom_key: str, pattern_data: Dict) -> bool:
        """Add new symptom pattern dynamically"""
        try:
            # Validate pattern data
            required_fields = ['patterns', 'category']
            for field in required_fields:
                if field not in pattern_data:
                    raise ValueError(f"Missing required field: {field}")
            
            # Add to patterns
            self.symptom_patterns[symptom_key] = pattern_data
            
            # Update pattern mapping
            for pattern in pattern_data['patterns']:
                self.pattern_to_symptom[pattern] = symptom_key
            
            # Recreate embeddings
            self._prepare_semantic_matching()
            
            logger.info(f"Added new symptom pattern: {symptom_key}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding symptom pattern: {e}")
            return False
    
    def extract_symptoms(self, text: str) -> List[Dict[str, any]]:
        """Extract symptoms with enhanced pattern matching"""
        text = text.lower().strip()
        extracted_symptoms = []
        
        # Check for negation
        has_negation = self._check_negation(text)
        
        # Check for emergency keywords
        is_emergency = self._check_emergency(text)
        
        # 1. Direct pattern matching
        extracted_symptoms.extend(self._pattern_matching(text))
        
        # 2. Semantic similarity matching (if needed)
        if len(extracted_symptoms) < 2 and self.pattern_embeddings is not None:
            semantic_symptoms = self._semantic_matching(text)
            extracted_symptoms.extend(semantic_symptoms)
        
        # 3. Apply negation and emergency flags
        for symptom in extracted_symptoms:
            symptom['has_negation'] = has_negation
            symptom['is_emergency_context'] = is_emergency
            
            # Adjust severity for emergency context
            if is_emergency and symptom['severity'] != 'severe':
                symptom['severity'] = 'severe'
                symptom['emergency_adjusted'] = True
        
        # 4. Remove duplicates
        extracted_symptoms = self._remove_duplicates(extracted_symptoms)
        
        return extracted_symptoms
    
    def _pattern_matching(self, text: str) -> List[Dict]:
        """Direct pattern matching"""
        symptoms = []
        
        for symptom_key, symptom_data in self.symptom_patterns.items():
            patterns = symptom_data.get('patterns', [])
            
            for pattern in patterns:
                if pattern in text:
                    severity = self._assess_severity_enhanced(text, pattern, symptom_data)
                    duration = self._extract_duration_enhanced(text, pattern)
                    
                    symptoms.append({
                        'name': symptom_key.replace('_', ' '),
                        'original_key': symptom_key,
                        'pattern_matched': pattern,
                        'category': symptom_data.get('category', 'general'),
                        'severity': severity,
                        'duration': duration,
                        'context': self._extract_context(text, pattern),
                        'is_critical': symptom_data.get('is_critical', False),
                        'weight': symptom_data.get('weight', 1.0),
                        'extraction_method': 'pattern_matching'
                    })
                    break  # Only match first pattern for each symptom
        
        return symptoms
    
    def _semantic_matching(self, text: str, threshold: float = 0.6) -> List[Dict]:
        """Semantic similarity matching for missed symptoms"""
        symptoms = []
        
        try:
            text_embedding = self.encoder.encode([text])
            similarities = np.dot(text_embedding, self.pattern_embeddings.T)[0]
            
            # Get top similar patterns
            top_indices = np.argsort(similarities)[-5:][::-1]
            
            for idx in top_indices:
                if similarities[idx] > threshold:
                    patterns_list = list(self.pattern_to_symptom.keys())
                    pattern = patterns_list[idx]
                    symptom_key = self.pattern_to_symptom[pattern]
                    
                    # Check if not already extracted
                    if not any(s['original_key'] == symptom_key for s in symptoms):
                        symptom_data = self.symptom_patterns[symptom_key]
                        
                        symptoms.append({
                            'name': symptom_key.replace('_', ' '),
                            'original_key': symptom_key,
                            'pattern_matched': pattern,
                            'category': symptom_data.get('category', 'general'),
                            'severity': 'mild',  # Default for semantic matching
                            'duration': '',
                            'context': text,
                            'is_critical': symptom_data.get('is_critical', False),
                            'weight': symptom_data.get('weight', 1.0),
                            'similarity_score': similarities[idx],
                            'extraction_method': 'semantic_matching'
                        })
        
        except Exception as e:
            logger.error(f"Error in semantic matching: {e}")
        
        return symptoms
    
    def _assess_severity_enhanced(self, text: str, pattern: str, symptom_data: Dict) -> str:
        """Enhanced severity assessment using JSON patterns"""
        context = self._extract_context(text, pattern)
        
        # Check symptom-specific severity indicators
        severity_indicators = symptom_data.get('severity_indicators', {})
        
        for severity_level in ['severe', 'mild']:
            indicators = severity_indicators.get(severity_level, [])
            for indicator in indicators:
                if indicator in context:
                    return severity_level
        
        # Check global severity modifiers
        for severity_level, modifiers in self.severity_modifiers.items():
            for modifier in modifiers:
                if modifier in context:
                    return severity_level
        
        return 'moderate'  # Default
    
    def _extract_duration_enhanced(self, text: str, pattern: str) -> str:
        """Enhanced duration extraction"""
        context = self._extract_context(text, pattern, window=50)
        
        for duration_type, keywords in self.duration_modifiers.items():
            for keyword in keywords:
                if keyword in context:
                    return duration_type
        
        return ''  # No duration found
    
    def _check_negation(self, text: str) -> bool:
        """Check if text contains negation keywords"""
        for keyword in self.negation_keywords:
            if keyword in text:
                return True
        return False
    
    def _check_emergency(self, text: str) -> bool:
        """Check if text contains emergency keywords"""
        for keyword in self.emergency_keywords:
            if keyword in text:
                return True
        return False
    
    def _extract_context(self, text: str, pattern: str, window: int = 30) -> str:
        """Extract context around symptom mention"""
        start_idx = text.find(pattern)
        if start_idx == -1:
            return text
        
        context_start = max(0, start_idx - window)
        context_end = min(len(text), start_idx + len(pattern) + window)
        
        return text[context_start:context_end]
    
    def _remove_duplicates(self, symptoms: List[Dict]) -> List[Dict]:
        """Remove duplicate symptoms, prioritizing pattern matching over semantic"""
        seen_symptoms = set()
        unique_symptoms = []
        
        # Sort by extraction method (pattern matching first)
        symptoms.sort(key=lambda x: 0 if x['extraction_method'] == 'pattern_matching' else 1)
        
        for symptom in symptoms:
            symptom_key = symptom['original_key']
            if symptom_key not in seen_symptoms:
                seen_symptoms.add(symptom_key)
                unique_symptoms.append(symptom)
        
        return unique_symptoms
    
    def get_pattern_statistics(self) -> Dict:
        """Get statistics about loaded patterns"""
        stats = {
            'total_symptoms': len(self.symptom_patterns),
            'categories': {},
            'critical_symptoms': 0,
            'total_patterns': 0
        }
        
        for symptom_key, symptom_data in self.symptom_patterns.items():
            category = symptom_data.get('category', 'unknown')
            stats['categories'][category] = stats['categories'].get(category, 0) + 1
            
            if symptom_data.get('is_critical', False):
                stats['critical_symptoms'] += 1
            
            stats['total_patterns'] += len(symptom_data.get('patterns', []))
        
        return stats
    
    def validate_patterns(self) -> List[str]:
        """Validate pattern configuration and return issues"""
        issues = []
        
        required_fields = ['patterns', 'category']
        
        for symptom_key, symptom_data in self.symptom_patterns.items():
            # Check required fields
            for field in required_fields:
                if field not in symptom_data:
                    issues.append(f"Symptom '{symptom_key}' missing required field: {field}")
            
            # Check patterns are not empty
            patterns = symptom_data.get('patterns', [])
            if not patterns:
                issues.append(f"Symptom '{symptom_key}' has no patterns")
            
            # Check for duplicate patterns across symptoms
            for pattern in patterns:
                count = sum(1 for s_data in self.symptom_patterns.values() 
                           if pattern in s_data.get('patterns', []))
                if count > 1:
                    issues.append(f"Pattern '{pattern}' is duplicated across symptoms")
        
        return issues
    
    def reload_patterns(self) -> bool:
        """Reload patterns from file"""
        return self.load_patterns()