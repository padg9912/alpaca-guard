from advanced_safety_monitor import AdvancedSafetyMonitor
import time

# Dummy model for demonstration
class DummyModel:
    def generate(self, instruction):
        return f"Echo: {instruction} (This is a dummy response)"

if __name__ == '__main__':
    model = DummyModel()
    monitor = AdvancedSafetyMonitor()
    print("Type 'exit' to quit.")
    while True:
        instruction = input("Enter instruction: ")
        if instruction.strip().lower() == 'exit':
            break
        response = model.generate(instruction)
        print("Model response:", response)
        monitor.monitor_response(instruction, response)
        time.sleep(0.5)  # Simulate processing delay 