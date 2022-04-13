from flask import Flask, render_template, request, make_response
import operator as op

app = Flask(__name__)
application = app

OPERATIONS = {'+': op.add, '-': op.sub, '*': op.mul, '/': op.truediv}

check_phone = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ' ', '(', ')', '-', '.', '+']
count_num = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


@app.route('/')
def index():
    url = request.url
    return render_template('index.html')


@app.route('/args')
def args():
    return render_template('args.html')


@app.route('/headers')
def headers():
    return render_template('headers.html')


@app.route('/form', methods=['GET', 'POST'])
def form():
    return render_template('form.html')


@app.route('/calc', methods=['GET', 'POST'])
def calc():
    result = None
    error_msg = None
    if request.method == 'POST':
        try:
            operand1 = float(request.form.get('operand1'))
            operand2 = float(request.form.get('operand2'))
            operation = request.form.get('operation')
            result = OPERATIONS[operation](operand1, operand2)
        except ValueError:
            error_msg = 'Нужно вводить только цифры'
        except ZeroDivisionError:
            error_msg = 'На ноль делить нельзя'

    return render_template('calc.html', operations=OPERATIONS, result=result, error_msg=error_msg)


@app.route('/cookies')
def cookies():
    response = make_response(render_template('cookies.html'))
    if request.cookies.get('name') is None:
        response.set_cookie('name', 'qq')
    else:
        response.set_cookie('name', 'qq', expires=0)
    return response


@app.route('/phone', methods=['GET', 'POST'])
def phone():
    error_invalid_symbol = None
    error_number_of_digits = None
    phone = str(request.form.get('phone'))
    count = 0
    check = True
    result = ''
    if request.method == 'POST':
        for element_phone in phone:
            if element_phone in check_phone:
                if element_phone in count_num:
                    count = count + 1
                    result = result + element_phone
            else:
                check = False
                error_invalid_symbol = "Недопустимый ввод. В номере телефона встречаются недопустимые символы"
        if count == 10:
            result = '8-' + result[0:3] + '-' + result[3:6] + '-' + result[6:8] + '-' + result[8:10]
            count += 1
        elif count == 11 and (phone.startswith('8') or phone.startswith('+7') or result[0] == '8') and check == True:
            result = "8-" + result[1:4] + '-' + result[4:7] + '-' + result[7:9] + '-' + result[9:11]
        elif count == 11 and not(phone.startswith('8') or phone.startswith('+7') or result[0] == '8') and check == True:
            check = False
            error_number_of_digits = 'Недопустимый ввод. Начало не с той цифры.'
        elif count != 11 and (phone.startswith('8') or phone.startswith('+7') or result[0] == '8') and check == True:
            check = False
            error_number_of_digits = 'Недопустимый ввод. Неверное количество цифр.'
    return render_template('phone.html', error_invalid_symbol=error_invalid_symbol, error_number_of_digits=error_number_of_digits, result=result)
