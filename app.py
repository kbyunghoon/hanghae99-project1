from flask import Flask, render_template, jsonify, redirect, url_for
from flask_jwt_extended import *
from templates.login.login import login_blueprint
from templates.register.register import register_blueprint
from templates.ui.write import write_blueprint
from templates.main.main import main_blueprint
from templates.mypage.mypage import mypage_blueprint
from pymongo import MongoClient

app = Flask(__name__)

app.config.update(
			DEBUG = True,
			JWT_SECRET_KEY = "24Team"
)
jwt = JWTManager(app)

app.register_blueprint(login_blueprint)
app.register_blueprint(register_blueprint)
app.register_blueprint(write_blueprint)
app.register_blueprint(main_blueprint)
app.register_blueprint(mypage_blueprint)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = 'SPARTA'

#client = MongoClient('mongodb://test:test@localhost', 27017)
client = MongoClient('localhost',27017)
db =  client.dbGameTree


# HTML 화면 호출
@app.route('/')
def getMain():
    return render_template('/main/main.html')

@app.route('/login')
def getLogin():
    return render_template('/login/login.html')

@app.route('/register')
def getRegister():
    return render_template('/register/register.html')

# 마이페이지 호출
@app.route('/mypage')
def getMypage():
    return render_template('/mypage/mypage.html')

# 마이페이지 갱신
@app.route('/mypageUpdate')
def getMypageUpdate():
    return render_template('/mypage/mypageUpdate.html')

@app.route('/loginCheck', methods=['GET'])
@jwt_required()
def loginCheck():
    user_Check = get_jwt_identity()

    if user_Check is not None :
        return jsonify({'result': 'success', 'token': user_Check})
    else :
        return redirect(url_for('/'))


if __name__ == '__main__':
    app.run('0.0.0.0',port=5000, debug=True)



