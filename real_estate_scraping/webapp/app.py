
import subprocess
import os
import json
import threading
from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

import subprocess
import os
import json
import threading
status_file = 'scraping_status.json' 
results_file = 'results.csv' 
@app.route('/')
def index():
    
    return render_template('index.html')

@app.route('/save-data', methods=['POST'])
def save_data():
    data = request.json
    print(data) 
    data['minArea'] = data.get('minArea') or '0'
    data['maxArea'] = data.get('maxArea') or '0'
    data['minPrice'] = data.get('minPrice') or '0'
    data['maxPrice'] = data.get('maxPrice') or '0'
    data['beds'] = data.get('beds') or 'All'
    data['baths'] = data.get('baths') or 'All'

    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)
    threading.Thread(target=start_scraping).start()

    return jsonify({'status': 'success', 'message': 'Scraping started successfully!'})
def start_scraping():
    status_file = 'status.json'  
    results_file = 'results.json'  
    
    with open(status_file, 'w') as f:
        json.dump({'status': 'in_progress'}, f)
    
   
    subprocess.run(['scrapy', 'crawl', 'property'], check=True)
    
    with open(status_file, 'w') as f:
        json.dump({'status': 'complete'}, f)

if __name__ == '__main__':
    app.run(debug=True)
