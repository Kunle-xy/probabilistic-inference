# Import libraries
from flask import Flask, redirect, request, render_template, url_for
import main
import subprocess

# Instantiate Flask functionality
app = Flask(__name__)
data = {}
# Define the home page route

def helper(item):
    return  [int(x) for x in item.split(",")]

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == 'POST':
        # Get the transaction data from the form
        line1a = helper(request.form['line1a'])
        line2a = helper(request.form['line2a'])
        line1b = helper(request.form['line1b'])
        line2b = helper(request.form['line2b'])
        weight_1 = request.form['weight_1']
        weight_2 = request.form['weight_2']


        # Create a dictionary object to send to the template
        data['line1'] = line1a + line1b
        data['line2'] = line2a + line2b
        data['weight_1'] = float(weight_1)
        data['weight_2'] = float(weight_2)

        # Redirect the user to the home page
        return redirect(url_for("get_plots"))

    # Render the form template to display the add transaction form
    return render_template("index.html")

# Define the get plots route
@app.route("/plots", methods=["GET", "POST"])
def get_plots():

    try:
        result = subprocess.call(['python', 'main.py', "--line_1", str(data['line1'])[1:-1], \
                    "--line_2", str(data['line2'])[1:-1], "--weight_1", str(data['weight_1']), \
                        "--weight_2", str(data['weight_2'])], text=True)

    except subprocess.CalledProcessError as e:
        return f'Error: {e}'

    return render_template("index2.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)