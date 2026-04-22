import base64
from io import BytesIO

import matplotlib.pyplot as plt
import pandas as pd
from flask import Flask, jsonify, render_template, request

from data_buddy import StatisticalAnalyzer

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max file


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/analyze", methods=["POST"])
def analyze():
    try:
        file = request.files["file"]
        df = pd.read_csv(file)

        numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()

        if not numeric_cols:
            return jsonify({"error": "No numeric columns found"}), 400

        col = numeric_cols[0]
        data = df[col].dropna().values

        analyzer = StatisticalAnalyzer(data)
        report = analyzer.get_summary_report()

        # Create chart
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.hist(data, bins=20, color="skyblue", edgecolor="black")
        ax.set_title(f"Distribution of {col}")

        buffer = BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        chart_base64 = base64.b64encode(buffer.getvalue()).decode()

        return jsonify(
            {
                "success": True,
                "report": report,
                "chart": f"data:image/png;base64,{chart_base64}",
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
