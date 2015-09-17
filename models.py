from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

from app import db
from config import SQLALCHEMY_DATABASE_URI

Base = declarative_base()

class User(db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    login = Column(String(25), nullable=False)
    password = Column(String(150), nullable=False)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
           return unicode(self.id)  # python 2
        except NameError:
           return str(self.id)  # python 3

    def __repr__(self):
        return '<User %r>' % (self.login)

class Os(db.Model):
    __tablename__ = 'os'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

class Arch(db.Model):
    __tablename__ = 'arch'
    id = Column(Integer, primary_key=True)
    name = Column(String(2), nullable=False)

class VmOs(db.Model):
    __tablename__ = 'vmos'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    description = Column(String(128), nullable=False)

class Server(db.Model):
    __tablename__ = 'server'
    id = Column(Integer, primary_key=True)
    hostname = Column(String(250))
    ipv4 = Column(String(15))
    port = Column(Integer, nullable=False)
    cores = Column(Integer, nullable=False)
    hds = Column(Integer, nullable=False)
    ram = Column(Integer, nullable=False)
    cores_free = Column(Integer, nullable=False)
    hds_free = Column(Integer, nullable=False)
    ram_free = Column(Integer, nullable=False)
    os_id = Column(Integer, ForeignKey('os.id'))
    os = relationship(Os)
    arch_id = Column(Integer, ForeignKey('arch.id'))
    arch = relationship(Arch)

class Vm(db.Model):
    __tablename__ = 'vm'
    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    cores = Column(Integer, nullable=False)
    hds = Column(Integer, nullable=False)
    ram = Column(Integer, nullable=False)
    vrde = Column(Boolean, nullable=False)
    vp = Column(Integer)
    server_id = Column(Integer, ForeignKey('server.id'))
    server = relationship(Server)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    vmos_id = Column(Integer, ForeignKey('vmos.id'))
    vmos = relationship(VmOs)

# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine(SQLALCHEMY_DATABASE_URI)

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
db.create_all()
#Base.metadata.create_all(engine)