from sentence_transformers import SentenceTransformer
import re
from typing import List, Dict, Set
import numpy as np

class SymptomExtractor:
    """Extract symptoms from Vietnamese medical text using NLP"""
    
    def __init__(self):
        # Load Vietnamese sentence transformer
        self.encoder = SentenceTransformer('keepitreal/vietnamese-sbert')
        
        # Comprehensive Vietnamese medical symptom patterns
        self.symptom_patterns = {
            'đau_đầu': {
                'patterns': ['đau đầu', 'nhức đầu', 'đau nửa đầu', 'migraine', 'đầu đau'],
                'category': 'neurological',
                'severity_indicators': ['dữ dội', 'khủng khiếp', 'không chịu nổi']
            },
            'sốt': {
                'patterns': ['sốt', 'nóng người', 'ấm người', 'nhiệt độ cao', 'bị nóng'],
                'category': 'general',
                'severity_indicators': ['sốt cao', 'sốt nhiều', 'trên 39']
            },
            'ho': {
                'patterns': ['ho', 'ke', 'ho khan', 'ho có đờm', 'ho ra máu', 'bị ho'],
                'category': 'respiratory',
                'severity_indicators': ['ho nhiều', 'ho liên tục', 'ho ra máu']
            },
            'buồn_nôn': {
                'patterns': ['buồn nôn', 'nôn', 'muốn nôn', 'ói', 'cảm giác nôn'],
                'category': 'gastrointestinal',
                'severity_indicators': ['nôn nhiều', 'nôn liên tục']
            },
            'đau_bụng': {
                'patterns': ['đau bụng', 'đau dạ dày', 'quặn bụng', 'cứng bụng', 'bụng đau'],
                'category': 'gastrointestinal',
                'severity_indicators': ['đau dữ dội', 'quặn thắt', 'không chịu nổi']
            },
            'khó_thở': {
                'patterns': ['khó thở', 'thở khó', 'ngạt thở', 'hụt hơi', 'thở gấp'],
                'category': 'respiratory',
                'severity_indicators': ['rất khó thở', 'không thở được', 'ngạt']
            },
            'chóng_mặt': {
                'patterns': ['chóng mặt', 'hoa mắt', 'choáng váng', 'lảo đảo', 'mất thăng bằng'],
                'category': 'neurological',
                'severity_indicators': ['chóng mặt dữ dội', 'ngất xỉu']
            },
            'mệt_mỏi': {
                'patterns': ['mệt mỏi', 'mệt', 'uể oải', 'kiệt sức', 'không có sức'],
                'category': 'general',
                'severity_indicators': ['rất mệt', 'kiệt sức']
            },
            'đau_ngực': {
                'patterns': ['đau ngực', 'tức ngực', 'ngực đau', 'đau tim'],
                'category': 'cardiovascular',
                'severity_indicators': ['đau ngực dữ dội', 'đau như đâm', 'rất đau']
            },
            'tiêu_chảy': {
                'patterns': ['tiêu chảy', 'đi lỏng', 'đi ngoài nhiều', 'lỏng bụng'],
                'category': 'gastrointestinal',
                'severity_indicators': ['tiêu chảy nhiều', 'đi lỏng liên tục']
            },
            'đau_họng': {
                'patterns': ['đau họng', 'rát họng', 'khàn giọng', 'nuốt đau'],
                'category': 'respiratory',
                'severity_indicators': ['đau họng dữ dội', 'không nuốt được']
            },
            'chảy_nước_mũi': {
                'patterns': ['chảy nước mũi', 'sổ mũi', 'nghẹt mũi', 'tắc mũi'],
                'category': 'respiratory',
                'severity_indicators': ['chảy nhiều', 'nghẹt hoàn toàn']
            },
            'đau_khớp': {
                'patterns': ['đau khớp', 'nhức khớp', 'cứng khớp', 'sưng khớp'],
                'category': 'musculoskeletal',
                'severity_indicators': ['đau khớp dữ dội', 'không cử động được']
            },
            'phát_ban': {
                'patterns': ['phát ban', 'nổi mề đay', 'ngứa', 'da đỏ', 'ban đỏ'],
                'category': 'dermatological',
                'severity_indicators': ['ban rộng', 'ngứa dữ dội']
            }
        }
        
        # Create symptom vocabulary for semantic matching
        self.symptom_vocab = list(self.symptom_patterns.keys())
        all_patterns = []
        for symptom_data in self.symptom_patterns.values():
            all_patterns.extend(symptom_data['patterns'])
        
        self.pattern_embeddings = self.encoder.encode(all_patterns)
        self.pattern_to_symptom = {}
        
        for symptom, data in self.symptom_patterns.items():
            for pattern in data['patterns']:
                self.pattern_to_symptom[pattern] = symptom
    
    def extract_symptoms(self, text: str) -> List[Dict[str, any]]:
        """Extract symptoms with severity and context"""
        text = text.lower().strip()
        extracted_symptoms = []
        
        # Direct pattern matching
        for symptom_key, symptom_data in self.symptom_patterns.items():
            for pattern in symptom_data['patterns']:
                if pattern in text:
                    severity = self._assess_severity(text, pattern, symptom_data['severity_indicators'])
                    
                    extracted_symptoms.append({
                        'name': symptom_key.replace('_', ' '),
                        'pattern_matched': pattern,
                        'category': symptom_data['category'],
                        'severity': severity,
                        'context': self._extract_context(text, pattern)
                    })
                    break
        
        # Semantic similarity matching for missed symptoms
        if len(extracted_symptoms) < 2:
            text_embedding = self.encoder.encode([text])
            similarities = np.dot(text_embedding, self.pattern_embeddings.T)[0]
            
            top_indices = np.argsort(similarities)[-5:][::-1]
            for idx in top_indices:
                if similarities[idx] > 0.6:  # Threshold
                    pattern = list(self.pattern_to_symptom.keys())[idx]
                    symptom_key = self.pattern_to_symptom[pattern]
                    
                    # Check if not already extracted
                    if not any(s['name'] == symptom_key.replace('_', ' ') for s in extracted_symptoms):
                        extracted_symptoms.append({
                            'name': symptom_key.replace('_', ' '),
                            'pattern_matched': pattern,
                            'category': self.symptom_patterns[symptom_key]['category'],
                            'severity': 'mild',
                            'context': text,
                            'similarity_score': similarities[idx]
                        })
        
        return extracted_symptoms
    
    def _assess_severity(self, text: str, pattern: str, severity_indicators: List[str]) -> str:
        """Assess severity of symptom based on context"""
        context = self._extract_context(text, pattern)
        
        # Check for severity indicators
        for indicator in severity_indicators:
            if indicator in context:
                return 'severe'
        
        # Check for mild indicators
        mild_indicators = ['chút ít', 'nhẹ', 'hơi', 'ít']
        for indicator in mild_indicators:
            if indicator in context:
                return 'mild'
        
        return 'moderate'
    
    def _extract_context(self, text: str, pattern: str, window: int = 30) -> str:
        """Extract context around symptom mention"""
        start_idx = text.find(pattern)
        if start_idx == -1:
            return text
        
        context_start = max(0, start_idx - window)
        context_end = min(len(text), start_idx + len(pattern) + window)
        
        return text[context_start:context_end]