# Safety Features for Stanford Alpaca

This directory contains safety features that can be used with the Stanford Alpaca model without modifying the original codebase. These features implement Phases 1, 2, and 3 of our safety improvements.

## Components

### Phase 1 Components

#### 1. Safety Filter (`safety_filter.py`)
A content filtering system that checks for potentially harmful content in both instructions and model outputs.

Features:
- Pattern-based content filtering
- Multiple categories of harmful content detection
- Warning message generation
- Safety reporting

#### 2. Safety Wrapper (`safety_wrapper.py`)
A wrapper class that can be used with the existing model to add safety checks without modifying the original code.

Features:
- Pre-generation safety checks
- Post-generation safety checks
- Comprehensive safety reporting
- Error handling

### Phase 2 Components

#### 1. Bias Detector (`bias_detector.py`)
A comprehensive bias detection system that identifies various types of biases in model outputs.

Features:
- Gender bias detection
- Racial bias detection
- Cultural bias detection
- Context-aware bias analysis
- Bias scoring and reporting

#### 2. Safety Evaluator (`safety_evaluator.py`)
A framework for evaluating model responses against safety and bias criteria.

Features:
- Combined safety and bias evaluation
- Scoring system
- Evaluation history tracking
- Detailed reporting
- Statistical analysis

#### 3. Safety Monitor (`safety_monitor.py`)
A real-time monitoring system for model outputs.

Features:
- Real-time safety monitoring
- Alert system
- Batch processing
- Logging and statistics
- Customizable alert handlers

### Phase 3 Components

#### 1. Advanced Safety Monitor (`advanced_safety_monitor.py`)
An enhanced monitoring system with advanced analytics and anomaly detection.

Features:
- Trend analysis and visualization
- Anomaly detection using statistical methods
- Category-based statistics
- Performance metrics tracking
- Comprehensive reporting

#### 2. Safety Dashboard (`safety_dashboard.py`)
A web-based dashboard for real-time monitoring and visualization of safety metrics.

Features:
- Real-time metrics display
- Interactive trend plots
- Category distribution visualization
- Performance monitoring
- Alert history
- Responsive design

## Usage

### Basic Usage with Safety Wrapper

```python
from safety_wrapper import SafetyWrapper
from your_model import YourModel  # Your existing model

# Initialize your model
model = YourModel()

# Create safety wrapper
safe_model = SafetyWrapper(model)

# Generate with safety checks
result = safe_model.generate("Your instruction here")

# Check results
if result['is_safe']:
    print(result['response'])
else:
    print("Safety warnings:", result['safety_warnings'])
```

### Using Bias Detection

```python
from bias_detector import BiasDetector

detector = BiasDetector()
report = detector.get_bias_report("Text to analyze")
print(report)
```

### Using Safety Evaluation

```python
from safety_evaluator import SafetyEvaluator

evaluator = SafetyEvaluator("evaluations.log")
evaluation = evaluator.evaluate_response(
    instruction="Your instruction",
    response="Model's response"
)
print(evaluator.get_evaluation_report(evaluation))
```

### Using Advanced Safety Monitoring

```python
from advanced_safety_monitor import AdvancedSafetyMonitor

# Create monitor with custom alert handler
def handle_alert(alert_type, details):
    print(f"Alert: {alert_type}")
    print(f"Details: {details}")

monitor = AdvancedSafetyMonitor(alert_threshold=0.7)
monitor.add_alert_handler(handle_alert)

# Monitor responses
monitor.monitor_response("Your instruction", "Model's response")

# Get comprehensive report
print(monitor.get_monitoring_report())
```

### Using the Safety Dashboard

```python
from safety_dashboard import run_dashboard

# Start the dashboard
run_dashboard()
```

Then open your web browser and navigate to `http://localhost:5000` to view the dashboard.

## Requirements

- Python 3.7+
- Flask
- Plotly
- NumPy
- jQuery (included via CDN)
- Bootstrap (included via CDN)

## Installation

1. Install the required Python packages:
```bash
pip install flask plotly numpy
```

2. Create the templates directory and copy the dashboard template:
```bash
mkdir templates
cp dashboard.html templates/
```

3. Run the safety dashboard:
```bash
python safety_dashboard.py
```

## Safety Categories

### Content Safety
- Explicit content
- Personal information
- Harmful instructions

### Bias Categories
- Gender bias
- Racial bias
- Cultural bias
- Occupational stereotypes
- Socioeconomic bias

## Monitoring and Alerts

The safety monitor provides:
- Real-time safety scoring
- Bias detection
- Alert thresholds
- Custom alert handlers
- Logging and statistics

## Best Practices

1. Always use the safety wrapper when deploying the model
2. Monitor safety warnings and adjust patterns as needed
3. Regularly update the harmful patterns list
4. Log safety incidents for analysis
5. Consider user feedback for improving safety measures
6. Use the bias detector to identify and address biases
7. Monitor model outputs in real-time
8. Set appropriate alert thresholds
9. Review safety statistics regularly

## Limitations

- Pattern-based filtering may have false positives/negatives
- New types of harmful content may not be caught
- Context-dependent safety concerns may be missed
- Language-specific patterns may need adjustment
- Bias detection may not catch all forms of bias
- Real-time monitoring adds some latency

## Future Improvements

- Machine learning-based content filtering
- Context-aware safety checks
- User feedback integration
- Automated pattern updates
- Multi-language support
- Advanced bias detection
- Real-time bias mitigation
- Automated safety tuning

## Contributing

We welcome contributions to improve the safety features. Please feel free to submit pull requests or open issues to discuss potential improvements.

## License

This project is licensed under the same terms as the Stanford Alpaca project. 