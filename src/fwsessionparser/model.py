import sqlalchemy as sa
from sqlalchemy.orm import mapper, relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import re
import datetime

Base = declarative_base()

class Session(Base):
    __tablename__ = 'sessions'
    
    id = sa.Column(sa.types.Integer, primary_key=True, nullable=False)
    timestamp = sa.Column(sa.types.DateTime, default=datetime.datetime.now)
    flows = relationship('Flow', backref='session')

    @classmethod
    def parse_output(cls, output, sa_session=None):
        sessions = []
        for values in re.findall(r'^id.*\n if.*\n if.*', output, re.MULTILINE):
            flows = []
            session = Session()

            for m in re.finditer(r'\n if \d+.*:(?P<src>.*/\d+)(?P<direction>->|<-)(?P<dst>\d+\..*/\d+)', values, re.MULTILINE):
                direction = m.group('direction')
                direction = direction.lower()
                if (direction == '<-'):
                    direction = 'in'
                elif (direction == '->'):
                    direction = 'out'
                session.flows.append(Flow.parse(m.group('src'), m.group('dst'), direction))
            sessions.append(session)
        
        if (sa_session):
            sa_session.add_all(sessions)

        return sessions

class Flow(Base):
    __tablename__ = 'flows'

    id = sa.Column(sa.types.Integer, primary_key=True, nullable=False)
    session_id = sa.Column(sa.types.Integer, sa.ForeignKey('sessions.id'))
    src_address = sa.Column(sa.types.Text)
    src_port = sa.Column(sa.types.Integer)
    dest_address = sa.Column(sa.types.Text)
    dest_port = sa.Column(sa.types.Integer)
    direction = sa.Column(sa.types.Enum(*['in', 'out']))

    def __init__(self, src_address, src_port, dest_address, dest_port, direction):
        self.src_address = src_address
        self.src_port = src_port
        self.dest_address = dest_address
        self.dest_port = dest_port
        self.direction = direction

    @classmethod
    def parse(cls, source, destination, direction):
        (src_address, src_port) = cls._split_address(source)
        (dest_address, dest_port) = cls._split_address(destination)
        return Flow(src_address, src_port, dest_address, dest_port, direction)

    @classmethod
    def _split_address(cls, address):
        (addr, port) = address.split('/')
        return (addr, int(port))

    source = property(fget=lambda self: "%s:%d" % (self.src_address, self.src_port), doc="Source address and port")
    destination = property(fget=lambda self: "%s:%d" % (self.dest_address, self.dest_port), doc="Destination address and port")

    def __repr__(self):
        return ("Flow(source='%s', destination='%s', direction='%s')" % (self.source, self.destination, self.direction))

    def __str__(self):
        return ("%s %s %s" % (self.source, self.direction, self.destination))

engine = sa.create_engine('sqlite:///session.db', echo=True)
Base.metadata.create_all(engine)
session = sessionmaker(engine)()
