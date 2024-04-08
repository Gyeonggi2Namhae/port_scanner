from flask import Flask, render_template, request
import jsonify

import get_ip
import scan

app = Flask(__name__)

myip = get_ip.get_ip()

@app.route('/')
def index():
    return render_template('index.html', ip_address = myip)
    # return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan_ports():
    ip_address = request.json.get('IP')
    scan_results = scan.well_known_port_scan(ip_address)
    return jsonify(scan_results)

if __name__ == "__main__":
    app.run()