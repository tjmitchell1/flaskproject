from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/brackets', methods=['POST'])
def bracket_balancer():
    running_list = []
    opposite_char = {
        ')': '(',
        ']': '[',
        '}': '{'
    }
    for char in request.form['data']:
        if char in opposite_char:
            if len(running_list) > 0 and running_list[-1] == opposite_char[char]:
                del running_list[-1]
            else:
                return 'False'
        else:
            running_list.append(char)
    if len(running_list) != 0:
        return 'False'
    return 'True'
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
    
