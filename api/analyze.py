from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import json
import base64
import io
from data_buddy.statistics_engine import StatisticalAnalyzer
from data_buddy import project_analyzer
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for serverless
import matplotlib.pyplot as plt

app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

@app.route('/api/analyze', methods=['POST', 'OPTIONS'])
def analyze():
    """
    Analyze CSV data with statistical rigor
    Returns: JSON with basic stats, confidence intervals, outliers, data quality
    """
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        # Get file from request
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'Empty filename'}), 400
        
        # Read and clean CSV
        df = pd.read_csv(file)
        
        if df.empty:
            return jsonify({'success': False, 'error': 'CSV is empty'}), 400
        
        # Clean data
        df = project_analyzer.universal_cleaner(df)
        
        # Get numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if not numeric_cols:
            return jsonify({'success': False, 'error': 'No numeric columns found'}), 400
        
        # Analyze first numeric column
        col = numeric_cols[0]
        data = df[col].dropna().values
        
        if len(data) == 0:
            return jsonify({'success': False, 'error': f'Column "{col}" has no valid data'}), 400
        
        # Run statistical analysis
        analyzer = StatisticalAnalyzer(data)
        report = analyzer.get_summary_report()
        
        # Add quality metrics to report
        quality = analyzer.get_data_quality_report()
        report['full_quality_report'] = quality
        
        # Generate visualization
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Histogram
        axes[0].hist(data, bins=20, color='skyblue', edgecolor='black', alpha=0.7)
        axes[0].axvline(report['basics']['mean'], color='red', linestyle='--', linewidth=2, label='Mean')
        axes[0].axvline(report['basics']['median'], color='green', linestyle='--', linewidth=2, label='Median')
        axes[0].set_xlabel(col)
        axes[0].set_ylabel('Frequency')
        axes[0].set_title(f'Distribution of {col}')
        axes[0].legend()
        axes[0].grid(alpha=0.3)
        
        # Box plot
        axes[1].boxplot(data, vert=True)
        axes[1].set_ylabel(col)
        axes[1].set_title('Box Plot (Outliers Visible)')
        axes[1].grid(alpha=0.3)
        
        plt.tight_layout()
        
        # Convert to base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        chart_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close(fig)
        
        # Build response
        response = {
            'success': True,
            'column_analyzed': col,
            'total_columns': len(numeric_cols),
            'available_columns': numeric_cols,
            'report': report,
            'chart': f'data:image/png;base64,{chart_base64}',
            'dataset_info': {
                'total_rows': len(df),
                'total_columns': len(df.columns),
                'columns': list(df.columns)
            }
        }
        
        return jsonify(response), 200
    
    except pd.errors.ParserError as e:
        return jsonify({'success': False, 'error': f'CSV parsing error: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': f'Server error: {str(e)}'}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'service': 'Data Buddy API v2'}), 200

if __name__ == '__main__':
    app.run(debug=False)
