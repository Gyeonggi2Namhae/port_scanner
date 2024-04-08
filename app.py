from flask import Flask, render_template, request
import jsonify

import get_ip
import scan

app = Flask(__name__)

myip = get_ip.get_ip()

@app.route('/')
def index():
    print("aa")
    return render_template('index.html', ip_address = myip)
    # return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan_ports():
    ip_address = request.form.get('IP')
    print(ip_address)
    scan_results = scan.well_known_port_scan(ip_address)
    # return jsonify(scan_results)
    return render_template('result.html', results = scan_results)

if __name__ == "__main__":
    app.run(host="0.0.0.0")