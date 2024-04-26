import subprocess
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    output = None
    if request.method == 'POST':
        ip_address = request.form['ip_address']
        try:
            response = subprocess.check_output(['sudo', 'fail2ban-client', 'unban', ip_address], encoding='UTF-8', stderr=subprocess.STDOUT)

            try:
                response = int(response)
                if response == 1:
                    output = f"IP address {ip_address} successfully unblocked!"
                elif response == 0:
                    output = f"IP address {ip_address} is not blocked. Nothing to do."
                else:
                    output = f"Something strange... You need to contact your system administrator. The following int response was received: \"{response}\""
            except ValueError:
                output = f"Something strange... You need to contact your system administrator. The following non int response was received: \"{response}\""

        except subprocess.CalledProcessError as e:
            output = f"ERROR: Failed to unblock IP address {ip_address} with error: \n{e.output}"
    return render_template('index.html', output=output)

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="127.0.0.1", port=8086)
