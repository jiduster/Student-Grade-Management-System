from flask import Flask, request, make_response
import json, sys, configparser
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import text
from gevent import pywsgi

config = configparser.ConfigParser()
config.read(sys.argv[1], encoding='utf-8')

# 框架的初始化
app = Flask(__name__)

# 浏览器的安全策略
CORS(app, supports_credentials=True)

# 数据库初始化
mysql = SQLAlchemy()

# 下面这个是数据库通讯的固定的格式，需要牢记
# {数据库类型}+{驱动方式}：//{用户名}：{密码}@{地址}：{端口}/{数据库的名称}
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://%s:%s@%s:%d/%s' % (
    config.get('mysql', 'user'),
    config.get('mysql', 'password'),
    config.get('mysql', 'host'),
    config.getint('mysql', 'port'),
    config.get('mysql', 'database')
)
app.config['SQLALCHEMY_ECHO'] = config.getboolean('mysql', 'debug')
mysql.init_app(app)


# 数据库查询
def query(sql, param=None):
    results = mysql.session.execute(sql, param)
    # 将查询的结果遍历之后转换成字典返回, <key, val>按照数据自身和主键配对
    data = [dict(zip(results.keys(), result)) for result in results]
    return data


# 数据库写入
def execute(sql, param):
    result = mysql.session.execute(sql, param)
    mysql.session.commit()
    return result

# 登出
@app.route('/logout', methods=['POST'])
def logout():
    resp = response(0, "Log Out Successfully!")
    resp.delete_cookie('id')
    return resp


# 这个地方是一个中间件，用于对请求进行预处理
# 值得说明的是，由于通讯采用的是同种协议，所以说这里resp的参数和后端端发送数据的方式实际上是一样的
@app.before_request
def before_request():
    if request.path == '/login':
        return None
    # if request.cookies.get('id') is None:
    # return response(9999, "Please Login Again.")
    # return None


# 这个地方是一个中间件，用于对响应进行预处理
# 值得说明的是，由于通讯采用的是同种协议，所以说这里resp的参数和前端发送数据的方式实际上是一样的
# 可以完全照搬login.vue中的this.$axios内部的内容
@app.after_request
def after_request(resp):
    resp.headers["Content-Type"] = "application/json"
    return resp


@app.route('/post')
def hello_world():
    print(request.data)
    return "Hello World val:"


# 说明：如果是route的话默认采用的是get方法，而如果我们需要使用post方法的时候则需要显式表示
@app.route('/index')
def hello_index():
    return "Hello Index val:" + request.args.get("name")


# 统一API的数据格式
def response(code: int, message: str, data: any = None):
    body = {"code": code, "message": message, "data": {}}
    if data is not None:
        if hasattr(data, '__dict__'):
            body["data"] = data.__dict__
        else:
            body["data"] = data
    return make_response(json.dumps(body, ensure_ascii=False, sort_keys=True), 200)


# 教师端口的实现
# teachers = [{"name":"admin", "id":1, "password":1234}]
# teachers = [{"id": 1, "name": "zg", "password": "1234"}]
# teacher_num = 1
# teachers = []
# teacher_num = 0


# 登录接口的实现
@app.route('/login', methods=['POST'])
def login():
    # global teachers
    param = json.loads(request.data)
    print(param)

    if 'name' not in param:
        return response(1000, "请输入账户名")
    if 'password' not in param:
        return response(1001, "请输入密码")

    # if param['name'] == "admin" and param['password'] == "1234":
    #     respo = response(0, "Login successfully", {"name": param["name"], "password": param["password"]})
    #     # 说明： 函数set_cookie（）是设置用户数据为cookie，而参数max_age则是规定了cookie的有效时间
    #     respo.set_cookie("id", str(data["id"]), max_age=3600)
    #     return respo

    # 本地数组实现
    # for i in range(len(teachers)):
    #     if teachers[i]["name"] == data["name"] and teachers[i]["password"] == data["password"]:
    #         resp = response(0, "Login successfully", {"name": teachers[i]["name"], "password": teachers[i]["password"]})
    #         # 说明： 函数set_cookie（）是设置用户数据为cookie，而参数max_age则是规定了cookie的有效时间
    #         resp.set_cookie("id", str(teachers[i]["id"]), max_age=3600)
    #         return resp

    # 数据库实现
    # 在flask框架下面，我们的占位符号一般都是用‘：’来表征
    # s = param['name']
    # sql = text("SELECT t.* FROM dachen_offer.teachers t WHERE name = '" + s + "'")
    sql = text('''SELECT * FROM `teachers` WHERE name=:name''')

    ret = query(sql, {"name": param["name"]})
    print(f'ret: {ret}')
    if len(ret) > 0 and ret[0]["password"] == param["password"]:
        resp = response(0, "Login Success!", {'id': ret[0]["id"], 'name': ret[0]["name"]})
        resp.set_cookie("id", str(ret[0].get('id')), max_age=3600)
        return resp

    return response(1002, "登陆账号或密码不正确")


@app.route('/teacher_list', methods=['GET'])
def teacher_list():
    sql = text('''SELECT * FROM `teachers`''')
    lst = []
    ret = query(sql)
    if len(ret) > 0:
        for index, row in enumerate(ret):
            lst.append({"id": row["id"], "name": row["name"]})
    return response(0, "ok", lst)


@app.route('/teacher_add', methods=['POST'])
def teacher_add():
    # global teacher_num, teachers
    fields = []
    vals = {}
    if str(request.data) == '':
        return response(1, "Parameter Error")

    param = json.loads(request.data)

    if "name" not in param:
        return response(1, "Name cannot be Empty!")
    fields.append("name")
    vals["name"] = param["name"]

    if "password" not in param:
        return response(1, "Password cannot be Empty!")
    fields.append("password")
    vals["password"] = param["password"]

    usql = text('''SELECT * FROM `teachers` WHERE name=:name''')
    rets = query(usql, {"name": param["name"]})
    if len(rets) > 0:
        return response(1, "Username already exits")

    sql = text('''INSERT INTO `teachers`(%s) VALUES (:%s)''' % (','.join(fields), ",:".join(fields)))
    execute(sql, vals)
    return response(0, "add success")


# 学生删除接口
@app.route('/teacher_del', methods=['POST'])
def teacher_del():
    if str(request.data) == '':
        return response(1, "Parameter Error")

    param = json.loads(request.data)
    if "id" not in param:
        return response(1, "Parameter Error")

    sql = text('''DELETE FROM `teachers` WHERE id=:id''')
    execute(sql, {"id": param["id"]})

    return response(0, "Delete Success!")


# 教师修改接口
@app.route('/teacher_modify', methods=["POST"])
def teacher_modify():
    fields = []
    vals = {}
    if str(request.data) == '':
        return response(1, "Parameter Error")

    param = json.loads(request.data)

    if "id" not in param:
        return response(1, "Parameter Error")
    vals["id"] = param["id"]

    # 校检数据是否存在
    usql = text('''SELECT * FROM `teachers` WHERE id=:id''')
    rets = query(usql, {"id": param["id"]})
    if len(rets) == 0:
        return response(1, "The User to Update does not exists")

    # 查看待更新的账号是否已经存在，避免冲突
    nsql = text('''SELECT * FROM `teachers` WHERE name=:name''')
    nrets = query(nsql, {"name": param["name"]})
    if len(nrets) > 0 and nrets[0]['id'] != param['id']:
        return response(1, "该账户名已经被占用，请更换新账号名")

    if "name" in param:
        if param["name"] == '':
            return response(1, "Name cannot be Empty!")
        fields.append("name")
        vals["name"] = param["name"]

    if "password" in param:
        if param["password"] == '':
            return response(1, "Password cannot be Empty!")
        fields.append("password")
        vals["password"] = param["password"]

    sets = ['%s=:%s' % (field, field) for field in fields]
    sql = text('''UPDATE `teachers` SET %s WHERE id=:id''' % (','.join(sets)))
    execute(sql, vals)
    return response(0, "Modify Success!")


# 学生端口的实现
# students = [
#     {"id": 1, "name": 'Tom', "chinese": 100, "english": 92, "math": 90},
#     {"id": 2, "name": 'James', "chinese": 90, "english": 92, "math": 90}
# ]
# students = []
# stu_num = 0


# 按照id查找数组的数据
def find_by_id(array, id):
    for i in range(len(array)):
        if array[i]['id'] == id:
            return array[i]
    return None


# 按照id删除数组的数据
def del_by_id(array, id):
    for i in range(len(array)):
        if array[i]['id'] == id:
            del (array[i])
            return
    return


# 按照id修改数组的数据
def update_by_id(array, id, data):
    for i in range(len(array)):
        if array[i]['id'] == id:
            array[i] = data
            return
    return


@app.route('/student_list', methods=['GET'])
def student_list():
    data = []
    sql = text('''SELECT * FROM `students`''')
    rets = query(sql)
    if (len(rets)) > 0:
        for __, row in enumerate(rets):
            data.append({"id": row["id"], "name": row["name"], "english": float(row["english"]), "math": float(row["math"]), "chinese": float(row["chinese"])})
    return response(0, "ok", data)



@app.route('/student_add', methods=['POST'])
def student_add():
    fields = []
    vals = {}

    if str(request.data) == '':
        return response(1, "Parameter Error")

    param = json.loads(request.data)

    if "name" not in param:
        return response(1, "Name cannot be empty")
    fields.append("name")
    vals["name"] = str(param["name"])

    usql = text('''SELECT * FROM `students` WHERE name=:name''')
    ret = query(usql, {"name": param["name"]})
    if len(ret) > 0:
        return response(1, "Student Info Exists")

    if "chinese" in param:
        fields.append("chinese")
        vals["chinese"] = float(param["chinese"])
    if "math" in param:
        fields.append("math")
        vals["math"] = float(param["math"])
    if "english" in param:
        fields.append("english")
        vals["english"] = float(param["english"])

    sql = text('''INSERT INTO `students` (%s) VALUES (:%s)''' % (','.join(fields), ',:'.join(fields)))
    execute(sql, vals)

    return response(0, "Add Success")


# 学生删除接口
@app.route('/student_del', methods=['POST'])
def student_del():
    if str(request.data) == '':
        return response(1, "Parameter Error")

    param = json.loads(request.data)
    if "id" not in param:
        return response(1, "Parameter Error")

    sql = text('''DELETE FROM `students` WHERE id=:id''')
    execute(sql, {"id": param["id"]})
    return response(0, "Delete Success!")


# 学生修改接口
@app.route('/student_modify', methods=["POST"])
def student_modify():
    fields = []
    vals = {}

    if str(request.data) == '':
        return response(1, "Parameter Error")
    param = json.loads(request.data)
    if "id" not in param:
        return response(1, "Parameter Error")
    vals["id"] = param["id"]

    # 检查被修改的学生是否存在
    usql = text('''SELECT * FROM `students` WHERE id=:id''')
    urets = query(usql, {"id": param["id"]})
    if len(urets) == 0:
        return response(1, "The Student to Modify does not exist")

    # 检查被修改的学生的姓名是否为空或已经被别的学号占用
    if "name" not in param:
        return response(1, "Name Cannot be Empty!")
    nsql = text('''SELECT * FROM `students` WHERE name=:name''')
    nrets = query(nsql, {"name": param["name"]})
    if len(nrets) > 0 and nrets[0]["id"] != param["id"]:
        return response(1, "Student Name already Exists")

    fields.append("name")
    vals["name"] = param["name"]

    if "chinese" in param:
        fields.append("chinese")
        vals["chinese"] = float(param["chinese"])
    if "english" in param:
        fields.append("english")
        vals["english"] = float(param["english"])
    if "math" in param:
        fields.append("math")
        vals["math"] = float(param["math"])

    sets = ['%s=:%s' % (field, field) for field in fields]
    sql = text('''UPDATE `students` SET %s WHERE id=:id''' % (','.join(sets)))
    execute(sql, vals)
    return response(0, "Modify Success!")


if __name__ == '__main__':
    # app.run(port=9000)
    server = pywsgi.WSGIServer(('0.0.0.0', config.getint('server', 'port')), app)
    server.serve_forever()
