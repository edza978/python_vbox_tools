from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
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
        return '<User %r>' % (self.nickname)

class Server(Base):
    __tablename__ = 'server'
    id = Column(Integer, primary_key=True)
    hostname = Column(String(250))
    ipv4 = Column(String(15))
    port = Column(Integer, nullable=False)
    cores = Column(Integer, nullable=False)
    hds = Column(Integer, nullable=False)
    ram = Column(Integer, nullable=False)

class Vm(Base):
    __tablename__ = 'vm'
    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    vrde = Column(Boolean, nullable=False)
    vp = Column(Integer)
    cores = Column(Integer, nullable=False)
    hds = Column(Integer, nullable=False)
    ram = Column(Integer, nullable=False)
    server_id = Column(Integer, ForeignKey('server.id'))
    server = relationship(Server)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///vbox.db')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)