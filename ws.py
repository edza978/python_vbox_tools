#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess  # Ejecución de comandos
from flask import Flask, request,jsonify,make_response

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/createvm', methods=['GET','POST'])
def createvm():
    arguments=['name','ostype','ram','cpus','hi','vrde','vp','iso','vdis','hds','vdi']
    vals={}
    ip=request.remote_addr
    vals['ip']=ip
    cmd=['python']
    cmd.append('createvm.py')
    for arg in arguments:
        val=request.args.get(arg)
        if(not val is None):
            vals[arg]=val
            if(arg=='name' or arg=='ram' or arg=='ostype'):
                cmd.append("%s" % val)
            else:
                cmd.append("-%s" % arg)
                cmd.append("%s" % val)

        else:
            pass
    #python createvm.py myvm Ubuntu_64 1024 -cpus 2 -hds 8192 -vdis $HOME/vdis -hi vboxnet0 -iso $HOME/ubuntu.iso
    print cmd
    res=subprocess.check_output(cmd)
    html="%s" % res
    return(make_response(html))

@app.route("/getmyip", methods=["GET"])
def getmyip():
    return jsonify({'ip': request.remote_addr}), 200

if __name__ == '__main__':
    app.run(debug=True,port=5555)
