import re
from typing import List, Dict, Optional
import json

class SafetyFilter:
    def __init__(self):
        # Load predefined harmful patterns
        self.harmful_patterns = {
            'explicit_content': [
                r'\b(sex|porn|nude|explicit)\b',
                r'\b(kill|murder|suicide|abuse)\b',
                r'\b(hate|racist|sexist|homophobic)\b'
            ],
            'personal_info': [
                r'\b(ssn|social security|credit card|password)\b',
                r'\b(address|phone|email|@)\b'
            ],
            'harmful_instructions': [
                r'\b(hack|exploit|bypass|crack)\b',
                r'\b(illegal|unlawful|criminal)\b'
            ]
        }
        
        # Compile regex patterns
        self.compiled_patterns = {
            category: [re.compile(pattern, re.IGNORECASE) 
                      for pattern in patterns]
            for category, patterns in self.harmful_patterns.items()
        }
        
        # Warning messages for different categories
        self.warning_messages = {
            'explicit_content': "This content may contain explicit or harmful material.",
            'personal_info': "This content may contain personal or sensitive information.",
            'harmful_instructions': "This content may contain harmful or illegal instructions."
        }

    def check_content(self, text: str) -> Dict[str, any]:
        """
        Check content for potentially harmful patterns.
        Returns a dictionary with safety check results.
        """
        results = {
            'is_safe': True,
            'warnings': [],
            'flagged_categories': set()
        }
        
        # Check each category of patterns
        for category, patterns in self.compiled_patterns.items():
            for pattern in patterns:
                if pattern.search(text):
                    results['is_safe'] = False
                    results['flagged_categories'].add(category)
                    if self.warning_messages[category] not in results['warnings']:
                        results['warnings'].append(self.warning_messages[category])
        
        return results

    def filter_instruction(self, instruction: str) -> Dict[str, any]:
        """
        Filter an instruction before it's processed by the model.
        """
        return self.check_content(instruction)

    def filter_output(self, output: str) -> Dict[str, any]:
        """
        Filter model output before it's shown to the user.
        """
        return self.check_content(output)

    def get_safety_report(self, text: str) -> str:
        """
        Generate a human-readable safety report.
        """
        results = self.check_content(text)
        if results['is_safe']:
            return "Content passed safety checks."
        
        report = "Safety Warnings:\n"
        for warning in results['warnings']:
            report += f"- {warning}\n"
        return report

# Example usage
if __name__ == "__main__":
    filter = SafetyFilter()
    
    # Test cases
    test_cases = [
        "Write a program to calculate the sum of two numbers",
        "How to hack into a computer system",
        "My email is test@example.com and my password is 123456"
    ]
    
    for test in test_cases:
        print(f"\nTesting: {test}")
        print(filter.get_safety_report(test)) 