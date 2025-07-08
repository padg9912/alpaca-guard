from typing import Dict, List, Any
import re
from collections import defaultdict

class BiasDetector:
    def __init__(self):
        # Define bias categories and their associated patterns
        self.bias_patterns = {
            'gender_bias': {
                'patterns': [
                    r'\b(he|she|his|her|him|man|woman|men|women)\b',
                    r'\b(male|female|masculine|feminine)\b',
                    r'\b(boy|girl|guy|gal)\b'
                ],
                'context_words': {
                    'stereotypes': [
                        'emotional', 'logical', 'nurturing', 'aggressive',
                        'sensitive', 'strong', 'weak', 'bossy', 'assertive'
                    ],
                    'occupations': [
                        'nurse', 'doctor', 'engineer', 'teacher',
                        'secretary', 'CEO', 'nanny', 'scientist'
                    ]
                }
            },
            'racial_bias': {
                'patterns': [
                    r'\b(race|ethnicity|nationality)\b',
                    r'\b(black|white|asian|hispanic|african|european)\b'
                ],
                'context_words': {
                    'stereotypes': [
                        'intelligent', 'athletic', 'musical', 'hardworking',
                        'lazy', 'criminal', 'successful', 'poor'
                    ]
                }
            },
            'cultural_bias': {
                'patterns': [
                    r'\b(culture|cultural|tradition|custom)\b',
                    r'\b(western|eastern|oriental|occidental)\b'
                ],
                'context_words': {
                    'stereotypes': [
                        'modern', 'traditional', 'progressive', 'backward',
                        'advanced', 'primitive', 'civilized', 'uncivilized'
                    ]
                }
            }
        }
        
        # Compile regex patterns
        self.compiled_patterns = {
            category: [re.compile(pattern, re.IGNORECASE) 
                      for pattern in data['patterns']]
            for category, data in self.bias_patterns.items()
        }

    def detect_bias(self, text: str) -> Dict[str, Any]:
        """
        Detect potential biases in the text.
        
        Args:
            text: The text to analyze
            
        Returns:
            Dictionary containing bias detection results
        """
        results = {
            'has_bias': False,
            'bias_categories': defaultdict(list),
            'bias_score': 0.0,
            'detailed_analysis': {}
        }
        
        # Check each category
        for category, data in self.bias_patterns.items():
            category_results = {
                'detected': False,
                'patterns_found': [],
                'stereotypes_found': [],
                'context': []
            }
            
            # Check for pattern matches
            for pattern in self.compiled_patterns[category]:
                matches = pattern.finditer(text)
                for match in matches:
                    category_results['detected'] = True
                    category_results['patterns_found'].append(match.group())
                    
                    # Get context around the match
                    start = max(0, match.start() - 50)
                    end = min(len(text), match.end() + 50)
                    context = text[start:end]
                    category_results['context'].append(context)
            
            # Check for stereotype words in context
            for stereotype in data['context_words']['stereotypes']:
                if re.search(r'\b' + stereotype + r'\b', text, re.IGNORECASE):
                    category_results['stereotypes_found'].append(stereotype)
            
            if category_results['detected']:
                results['has_bias'] = True
                results['bias_categories'][category] = category_results
                results['detailed_analysis'][category] = category_results
        
        # Calculate bias score (simple implementation)
        if results['has_bias']:
            total_patterns = sum(len(cat['patterns_found']) 
                               for cat in results['bias_categories'].values())
            total_stereotypes = sum(len(cat['stereotypes_found']) 
                                  for cat in results['bias_categories'].values())
            results['bias_score'] = (total_patterns + total_stereotypes) / 10.0
        
        return results

    def get_bias_report(self, text: str) -> str:
        """
        Generate a human-readable bias report.
        
        Args:
            text: The text to analyze
            
        Returns:
            A formatted bias report
        """
        results = self.detect_bias(text)
        
        if not results['has_bias']:
            return "No significant bias detected in the text."
        
        report = "Bias Detection Report:\n"
        report += f"Overall Bias Score: {results['bias_score']:.2f}\n\n"
        
        for category, analysis in results['detailed_analysis'].items():
            report += f"{category.replace('_', ' ').title()}:\n"
            if analysis['patterns_found']:
                report += f"- Found patterns: {', '.join(analysis['patterns_found'])}\n"
            if analysis['stereotypes_found']:
                report += f"- Found stereotypes: {', '.join(analysis['stereotypes_found'])}\n"
            report += "\n"
        
        return report

# Example usage
if __name__ == "__main__":
    detector = BiasDetector()
    
    test_cases = [
        "The nurse was very nurturing and emotional, while the doctor was logical and assertive.",
        "The Asian student was very intelligent and hardworking.",
        "The traditional Eastern culture is backward compared to modern Western society."
    ]
    
    for test in test_cases:
        print(f"\nTesting: {test}")
        print(detector.get_bias_report(test)) 