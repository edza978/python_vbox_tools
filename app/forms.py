"""
from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired
"""
from flask.ext.wtf import Form
from wtforms import TextField, IntegerField, TextAreaField, validators, ValidationError, PasswordField, SelectField, BooleanField
from .models import User, Server, Vm,Arch,Os,VmOs

class UserForm(Form):
  login = TextField("Login",  [validators.Required("Please enter your login.")])
  password = PasswordField('Password', [validators.Required("Please enter a password.")])
  name = TextField("Name",  [validators.Required("Please enter your name.")])

  def validate(self):
    if not Form.validate(self):
      return False

    user = User.query.filter_by(login = self.login.data.lower()).first()
    if user:
      self.login.errors.append("The login: %s is already taken" % self.login.data.lower())
      return False
    else:
      return True

class ServerForm(Form):
  hostname = TextField("Hostname",  [validators.Required("Please enter Server hostname.")])
  ipv4 = TextField("IPv4",  [validators.Required("Please enter Server IPv4.")])
  port = IntegerField("Port",  [validators.Required("Please enter Server IPv4.")])

  archs = [(a.id, a.name) for a in Arch.query.order_by('name')]
  arch = SelectField(u'Architecture', coerce=int, choices=archs, validators=[validators.Required("Please select an architecture.")])

  opsys = [(o.id, o.name) for o in Os.query.order_by('name')]
  os = SelectField(u'Operating System', coerce=int, choices=opsys, validators=[validators.Required("Please select an Operating System.")])

  cores = IntegerField("Cores",  [validators.Required("Please enter quantity of Cores of this Server.")])
  ram = IntegerField("RAM (GB)",  [validators.Required("Please enter quantity of RAM of this Server.")])
  hds = IntegerField("Harddisk space (GB)",  [validators.Required("Please enter quantity free space in harddisk of this Server.")])

  def validate(self):
    if not Form.validate(self):
      return False

    hostname = Server.query.filter_by(hostname = self.hostname.data.lower()).first()
    if hostname:
      self.hostname.errors.append("That hostname is already registered")
      return False
    else:
      ipv4 = Server.query.filter_by(ipv4 = self.ipv4.data).first()
      if ipv4:
        self.ipv4.errors.append("That ipv4 address is already registered")
        return False
      else:
        return True

class VmForm(Form):
  name = TextField("VM Name",  [validators.Required("Please enter the Name for this VM.")])
  cores = IntegerField("Cores",  [validators.Required("Please enter quantity of RAM for this VM.")])
  ram = IntegerField("Memory (MB)",  [validators.Required("Please enter quantity of RAM for this VM.")])
  hds = IntegerField("Harddisk Size (MB)",  [validators.Required("Please enter required size of  HDD for this VM.")])
  servers = [(s.id, s.hostname) for s in Server.query.order_by('hostname')]
  server = SelectField(u'Server', coerce=int, choices=servers, validators=[validators.Required("Please select a server to store this VM.")])
  users = [(u.id, u.name) for u in User.query.order_by('name')]
  user = SelectField(u'Owner', coerce=int, choices=users, validators=[validators.Required("Please select the owner of this VM.")])
  vrde = BooleanField("Enable VRDE",  [validators.Required("Please enter Server IPv4.")])
  vp = IntegerField("VRDE Port",  [validators.Required("Please enter VRDE port for this VM in the Server.")])
  opsys = [(o.id, o.name) for o in VmOs.query.order_by('name')]
  vmos = SelectField(u'Guess OS', coerce=int, choices=opsys, validators=[validators.Required("Please select an Operating System for this VM.")])

  def validate(self):
    if not Form.validate(self):
      return False

    name = Vm.query.filter_by(name = self.name.data.lower()).first()
    if name:
      self.name.errors.append("That name is already registered")
      return False
    else:
      return True