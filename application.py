import os

from flask import Flask,make_response,request
from flask_socketio import SocketIO, emit
from flask import render_template, jsonify

list=[]
MS=[]
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

if __name__ == '__main__':
    socketio.run(app)


@app.route("/",methods=['GET','POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')#用户名

        resp = make_response(render_template('index.html', username=name))
        resp.set_cookie('username', name)
        resp.set_cookie('is_set', '1')
        return resp
    #return "Project 2: TODO"
    else:
        cookie = request.cookies.get('is_set')
        if not cookie:
            return  render_template('index.html')
        elif cookie == '1':
            name = request.cookies.get('username')
            return render_template("index.html",username=name)




@app.route("/cookie")
def set_cookie():
    resp = make_response("this is to set cookie")
    # resp.set_cookie('username','wu')
    return resp


@app.route("/request")
def resp_cookie():
    resp = request.cookies.get('username')
    return resp


@app.route("/channel",methods=['GET','POST'])
def List_channel():
    name=request.cookies.get("username")
    list.append(name)
    if request.method == 'POST':
        mes = request.form.get("mes")  # 发送的message

        us = request.form.get("us")
        str = us + ":" + mes
        MS.append(str)
        event_name = "message"
        broadcasted_data = {'data': mes}
        print("publish msg==>", broadcasted_data)
        socketio.emit(event_name, str, broadcast=True  )
        # emit(event_name, str, broadcast=True  )

        return render_template("channel.html",arr=list,mes=MS)
    else:
        return render_template("channel.html",arr=list)


@app.route('/push',methods=['GET','POST'])
def push_once():
    socketio.emit("message", MS[0], broadcast=True  )
    return 'send msg successful!'


@socketio.on('receive message'  )
def test_message(message):
    print('receive message', message)
    # emit('message', {'data': message['data']})


@socketio.on('connect'  )
def connected_msg():
    """客户端连接"""
    print('client connected!', request.sid)
    socketio.emit('abcde', 'hello', namespace="/test")


@socketio.on('disconnect')
def disconnect_msg():
    """客户端离开"""
    print('client disconnected!')
