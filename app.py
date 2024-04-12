from flask import Flask, render_template, request

import get_ip
import multi_threading_code

app = Flask(__name__)



@app.route('/')
def index():
    myip = request.remote_addr
    return render_template('index.html', ip_address = myip)
    # return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan_ports():
    ip_address = request.form.get('IP')
    print(ip_address)
    known_scan_results = multi_threading_code.well_known_scan(ip_address)
    scan_results = multi_threading_code.multi_threading_scan(ip_address,(996,65536))
    # return jsonify(scan_results)
    return render_template('result.html', results = known_scan_results, unknown=scan_results)

if __name__ == "__main__":
    app.run(host="0.0.0.0")