import hashlib
import urllib2

from flask import render_template, flash, redirect
from app import app
from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db
#from app import app, db, lm
#from .forms import LoginForm
from .models import User, Server, Vm,Arch,Os,VmOs

from forms import UserForm,ServerForm,VmForm

@app.route('/')
@app.route('/index')
#@login_required
def index():
    user = g.user
    posts = [
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html',title='Home',user=user,posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if not g.user is None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'],ask_for_optional=[])
    return render_template('login.html',title='Sign In',form=form,providers=app.config['OPENID_PROVIDERS'])

@app.before_request
def before_request():
    g.user = current_user

@app.route('/createuser', methods=['GET','POST'])
def createuser():
  form = UserForm()

  if request.method == 'POST':
    if form.validate() == False:
      return render_template('user.html', form=form)
    else:
        passhash=hashlib.sha512(form.password.data).hexdigest()
        user=User(login=form.login.data,password=passhash,name=form.name.data)
        db.session.add(user)
        db.session.commit()
        return render_template('user.html', form=UserForm(formdata=None))

  elif request.method == 'GET':
    return render_template('user.html', form=form)

@app.route('/createserver', methods=['GET','POST'])
def createserver():
  form = ServerForm()

  if request.method == 'POST':
    if form.validate() == False:
      return render_template('server.html', form=form)
    else:
        arch = Arch.query.filter_by(id = form.arch.data).first()
        os = Os.query.filter_by(id = form.os.data).first()
        server=Server(hostname=form.hostname.data,ipv4=form.ipv4.data,port=form.port.data,arch=arch,os=os,cores=form.cores.data,ram=form.ram.data,hds=form.hds.data,cores_free=form.cores.data,ram_free=form.ram.data,hds_free=form.hds.data)
        db.session.add(server)
        db.session.commit()

        list = [(s.hostname, s.ipv4, s.port, s.cores, s.ram, s.hds) for s in Server.query.order_by('hostname')]
        return render_template('servers.html', servers=list)
        #return render_template('server.html', form=ServerForm(formdata=None),servers=list)

  elif request.method == 'GET':
    return render_template('server.html', form=form)

@app.route('/listservers', methods=['GET','POST'])
def listservers():
        list = [(s.hostname, s.ipv4, s.port, s.cores, s.ram, s.hds) for s in Server.query.order_by('hostname')]
        return render_template('servers.html', servers=list)


@app.route('/createvm', methods=['GET','POST'])
def createvm():
  form = VmForm()

  if request.method == 'POST':
    if form.validate() == False:
      return render_template('vm.html', form=form)
    else:
        user = User.query.filter_by(id = form.user.data).first()
        vmos = VmOs.query.filter_by(id = form.vmos.data).first()
        server = Server.query.filter_by(id = form.server.data).first()

        wsurl="http://%s:%s/createvm?name=%s&ostype=%s&ram=%s&cpus=%s&hds=%s" %(server.ipv4,server.port,form.name.data,vmos.name,form.ram.data,form.cores.data,form.hds.data)
        url=urllib2.Request(wsurl)
        ws=urllib2.urlopen(url).read()

        vm=Vm(name=form.name.data,
            cores=form.cores.data,
            ram=form.ram.data,
            hds=form.hds.data,
            vrde=form.vrde.data,
            vp=form.vp.data,
            server=server,
            vmos=vmos,
            user=user)
        db.session.add(vm)
        db.session.commit()

        vms = [(s.name, s.cores, s.hds, s.ram, s.vrde, s.vp, s.user.name,s.server.hostname, s.vmos.name) for s in Vm.query.order_by('name')]
        return render_template('vms.html', vms=vms,ws=ws)

  elif request.method == 'GET':
    return render_template('vm.html', form=form)

@app.route('/listvms', methods=['GET','POST'])
def listvms():
    vms = [(s.name, s.cores, s.hds, s.ram, s.vrde, s.vp, s.user.name,s.server.hostname, s.vmos.name) for s in Vm.query.order_by('name')]
    return render_template('vms.html', vms=vms)