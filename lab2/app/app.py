from crypt import methods
from distutils.log import error
from tabnanny import check
from flask import Flask, render_template, request, make_response
import operator as op

app = Flask(__name__)
application = app

OPERATIONS = {'+': op.add, '-': op.sub, '*': op.mul, '/': op.truediv}

check_phone = ['0', '1', '2', '3', '4', '5', '6',
               '7', '8', '9', ' ', '(', ')', '-', '.', '+']
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
    error_msg = None
    phone = str(request.form.get('phone'))
    count = 0
    check = True
    for element_phone in phone:
        if element_phone in check_phone:
            if element_phone in count_num:
                count += 1
        else:
            check = False
        if count != 10 and (element_phone[0] != '+' or element_phone[0] != 8):
            error_msg = "Недопустимый ввод. Неверное количество цифр."
        if count != 11 and (element_phone[0] == '+' or element_phone[0] == 8):
            error_msg = "Недопустимый ввод. Неверное количество цифр."
        elif check == False:
            error_msg = "Недопустимый ввод. В номере телефона встречаются недопустимые символы"
    # if request.method == 'POST':
    #     try:
    #         phone = str(request.form.get('phone'))
    #         count = 0
    #         check = True
    #         for element_phone in phone:
    #             if element_phone in check_phone:
    #                 if element_phone in count_num:
    #                     count += 1
    #             else:
    #                 check = False
    #         # if count != 10 or (count != 11 and (element_phone[0] != '+' or element_phone[0] != 8)):
    #         #     error_msg = "Недопустимый ввод. Неверное количество цифр."
    #         # elif check == False:
    #         #     error_msg = "Недопустимый ввод. В номере телефона встречаются недопустимые символы"
    #     except ValueError:
    #         error_msg = "Недопустимый ввод. В номере телефона встречаются недопустимые символы"
    #     #     if count != 10 or (count != 11 and (element_phone[0] != '+' or element_phone[0] != 8)):
    #     #         error_msg = "Недопустимый ввод. Неверное количество цифр."
    #     #     elif check == False:
    #     #         error_msg = "Недопустимый ввод. В номере телефона встречаются недопустимые символы"

    return render_template('phone.html', error_msg=error_msg)
