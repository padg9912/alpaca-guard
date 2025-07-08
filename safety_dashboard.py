import os
import json
from flask import Flask, render_template, jsonify, request, send_file
import plotly
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import csv
import io
from datetime import datetime

LOG_FILE = 'advanced_safety_monitor.log'

app = Flask(__name__)

def parse_log_file():
    evaluations = []
    alerts = []
    if not os.path.exists(LOG_FILE):
        return evaluations, alerts
    with open(LOG_FILE, 'r') as f:
        for line in f:
            try:
                if 'Evaluation:' in line:
                    data = json.loads(line.split('Evaluation: ', 1)[1])
                    evaluations.append(data)
                elif 'Safety Alert' in line:
                    # Parse alert type and details
                    alert_type = 'Flagged' if 'low_safety_score' in line else 'Anomaly'
                    try:
                        details = json.loads(line.split(': ', 2)[-1])
                    except Exception:
                        details = {}
                    alerts.append({
                        'type': alert_type,
                        'time': details.get('timestamp', ''),
                        'message': str(details),
                        'level': 'danger' if alert_type == 'Flagged' else 'warning',
                        'details': details
                    })
            except Exception:
                continue
    # Only keep the most recent 20 alerts
    alerts = alerts[-20:][::-1]
    return evaluations, alerts

def get_metrics_from_evaluations(evaluations, alerts):
    # Compute metrics from evaluations
    total_requests = len(evaluations)
    flagged_requests = sum(1 for e in evaluations if e.get('overall_score', 1.0) < 0.7)
    anomalies_detected = sum(1 for a in alerts if a['type'] == 'Anomaly')
    flag_rate = (flagged_requests / total_requests * 100) if total_requests else 0.0
    # Category distribution
    category_distribution = {}
    for e in evaluations:
        for cat in e.get('bias_categories', []):
            category_distribution[cat] = category_distribution.get(cat, 0) + 1
    # Trend data
    safety_scores = [e.get('safety_score', 1.0) for e in evaluations]
    bias_scores = [e.get('bias_score', 1.0) for e in evaluations]
    overall_scores = [e.get('overall_score', 1.0) for e in evaluations]
    # Performance metrics (simulate, as we don't have real response times)
    perf = {
        'average_response_time': 0.0,
        'p95_response_time': 0.0,
        'min_response_time': 0.0,
        'max_response_time': 0.0,
        'median_response_time': 0.0,
    }
    # Category stats
    category_stats = {cat: {'count': count, 'average_score': 0.0} for cat, count in category_distribution.items()}
    # Trends
    trends = {
        'safety_scores': {'mean': sum(safety_scores)/len(safety_scores) if safety_scores else 0.0, 'std': 0.0, 'trend': 0.0},
        'bias_scores': {'mean': sum(bias_scores)/len(bias_scores) if bias_scores else 0.0, 'std': 0.0, 'trend': 0.0},
        'overall_scores': {'mean': sum(overall_scores)/len(overall_scores) if overall_scores else 0.0, 'std': 0.0, 'trend': 0.0},
    }
    return {
        'total_requests': total_requests,
        'flagged_requests': flagged_requests,
        'anomalies_detected': anomalies_detected,
        'flag_rate': flag_rate,
        'category_distribution': category_distribution,
        'trend_data': {
            'safety_scores': safety_scores,
            'bias_scores': bias_scores,
            'overall_scores': overall_scores,
        },
        'category_stats': category_stats,
        'performance': perf,
        'trends': trends,
        'recent_alerts': alerts,
        'evaluations': evaluations,
    }

def moving_average(data, window=5):
    if len(data) < window:
        return data
    return [sum(data[i-window+1:i+1])/window for i in range(window-1, len(data))]

def create_trend_plot(metrics, window=5):
    """Create a plot showing safety score trends (raw + smoothed)."""
    fig = make_subplots(rows=2, cols=1, subplot_titles=('Safety Scores', 'Category Distribution'))
    # Raw data
    raw_safety = metrics['trend_data']['safety_scores']
    raw_bias = metrics['trend_data']['bias_scores']
    # Smoothed data
    smooth_safety = moving_average(raw_safety, window)
    smooth_bias = moving_average(raw_bias, window)
    # Add raw and smoothed
    fig.add_trace(go.Scatter(y=raw_safety, name='Raw Safety', line=dict(color='blue', dash='dot')), row=1, col=1)
    fig.add_trace(go.Scatter(y=smooth_safety, name='Smoothed Safety', line=dict(color='blue', width=3)), row=1, col=1)
    fig.add_trace(go.Scatter(y=raw_bias, name='Raw Bias', line=dict(color='red', dash='dot')), row=1, col=1)
    fig.add_trace(go.Scatter(y=smooth_bias, name='Smoothed Bias', line=dict(color='red', width=3)), row=1, col=1)
    # Category distribution
    categories = list(metrics['category_distribution'].keys())
    values = list(metrics['category_distribution'].values())
    fig.add_trace(go.Bar(x=categories, y=values, name='Category Distribution'), row=2, col=1)
    fig.update_layout(height=800, title_text="Safety Monitoring Dashboard")
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

@app.route('/')
def index():
    """Render the main dashboard page."""
    return render_template('dashboard.html')

@app.route('/metrics')
def get_metrics():
    """Get current metrics as JSON."""
    evaluations, alerts = parse_log_file()
    metrics = get_metrics_from_evaluations(evaluations, alerts)
    return jsonify(metrics)

@app.route('/plot')
def get_plot():
    """Get the trend plot as JSON."""
    evaluations, alerts = parse_log_file()
    metrics = get_metrics_from_evaluations(evaluations, alerts)
    return create_trend_plot(metrics, window=5)

@app.route('/details/<int:idx>')
def get_details(idx):
    evaluations, _ = parse_log_file()
    if 0 <= idx < len(evaluations):
        return jsonify(evaluations[idx])
    return jsonify({'error': 'Not found'}), 404

@app.route('/export/csv')
def export_csv():
    evaluations, _ = parse_log_file()
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=list(evaluations[0].keys()) if evaluations else [])
    writer.writeheader()
    for row in evaluations:
        writer.writerow(row)
    output.seek(0)
    return send_file(io.BytesIO(output.getvalue().encode()), mimetype='text/csv', as_attachment=True, download_name='evaluations.csv')

@app.route('/export/json')
def export_json():
    evaluations, _ = parse_log_file()
    return jsonify(evaluations)

if __name__ == '__main__':
    # To use the dashboard with real data, call monitor.monitor_response(instruction, response)
    # from your inference or deployment script whenever the model generates a response.
    app.run(host='127.0.0.1', port=5000, debug=True)

 