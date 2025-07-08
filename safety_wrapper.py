from typing import Dict, Any, Optional
from safety_filter import SafetyFilter

class SafetyWrapper:
    def __init__(self, model):
        """
        Initialize the safety wrapper with a model instance.
        
        Args:
            model: The original model instance to wrap
        """
        self.model = model
        self.safety_filter = SafetyFilter()
        
    def generate(self, instruction: str, **kwargs) -> Dict[str, Any]:
        """
        Generate a response with safety checks.
        
        Args:
            instruction: The input instruction
            **kwargs: Additional arguments to pass to the model
            
        Returns:
            Dictionary containing the response and safety information
        """
        # Check instruction safety
        instruction_safety = self.safety_filter.filter_instruction(instruction)
        
        if not instruction_safety['is_safe']:
            return {
                'response': None,
                'safety_warnings': instruction_safety['warnings'],
                'is_safe': False,
                'error': 'Unsafe instruction detected'
            }
        
        # Generate response using original model
        try:
            response = self.model.generate(instruction, **kwargs)
            
            # Check response safety
            response_safety = self.safety_filter.filter_output(response)
            
            return {
                'response': response,
                'safety_warnings': response_safety['warnings'],
                'is_safe': response_safety['is_safe'],
                'error': None
            }
            
        except Exception as e:
            return {
                'response': None,
                'safety_warnings': [],
                'is_safe': False,
                'error': str(e)
            }
    
    def get_safety_report(self, text: str) -> str:
        """
        Get a safety report for any text.
        
        Args:
            text: The text to analyze
            
        Returns:
            A human-readable safety report
        """
        return self.safety_filter.get_safety_report(text)

# Example usage
if __name__ == "__main__":
    # This is just an example - in real usage, you would pass your actual model
    class DummyModel:
        def generate(self, instruction, **kwargs):
            return f"Response to: {instruction}"
    
    # Create wrapper with dummy model
    wrapper = SafetyWrapper(DummyModel())
    
    # Test cases
    test_instructions = [
        "Write a program to calculate the sum of two numbers",
        "How to hack into a computer system",
        "My email is test@example.com and my password is 123456"
    ]
    
    for instruction in test_instructions:
        print(f"\nTesting instruction: {instruction}")
        result = wrapper.generate(instruction)
        print(f"Response: {result['response']}")
        print(f"Safety warnings: {result['safety_warnings']}")
        print(f"Is safe: {result['is_safe']}")
        if result['error']:
            print(f"Error: {result['error']}") 