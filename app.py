from flask import Flask, render_template, request
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

from utils.fuzzy_logic import fuzzy_analysis, create_rule_graph

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
CHART_FOLDER = 'static/charts'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CHART_FOLDER'] = CHART_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CHART_FOLDER, exist_ok=True)

def create_summary_chart(results):

    labels = []
    values = []

    for i, r in enumerate(results):
        labels.append(f'Gambar {i+1}')
        values.append(r['percentage'])

    plt.figure(figsize=(8,5))

    bars = plt.bar(labels, values)

    plt.title('Perbandingan Persentase Hutan')
    plt.ylabel('Persentase (%)')
    plt.ylim(0,100)

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2,
                 yval + 1,
                 f'{yval:.1f}%',
                 ha='center')

    plt.savefig('static/charts/summary.png')
    plt.close()
def calculate_forest_percentage(image_path):
    img = cv2.imread(image_path)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_green = np.array([35, 40, 40])
    upper_green = np.array([90, 255, 255])

    mask = cv2.inRange(hsv, lower_green, upper_green)

    green_pixels = np.sum(mask > 0)
    total_pixels = mask.size

    percentage = (green_pixels / total_pixels) * 100

    return round(percentage, 2), mask


@app.route('/')
def index():
    create_rule_graph()
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():

    results = []

    files = request.files.getlist('images')

    for i, file in enumerate(files):

        if file.filename == '':
            continue

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        percentage, mask = calculate_forest_percentage(filepath)

        fuzzy_result = fuzzy_analysis(percentage, i)

        results.append({
            'filename': file.filename,
            'percentage': percentage,
            'category': fuzzy_result['category'],
            'defuzz': fuzzy_result['defuzz'],
            'calculation': fuzzy_result['calculation'],
            'chart': fuzzy_result['chart']
        })

    create_summary_chart(results)
    return render_template(
     'hasil.html',
     results=results,
     summary_chart='charts/summary.png'
    )


if __name__ == '__main__':
    app.run(debug=True)
