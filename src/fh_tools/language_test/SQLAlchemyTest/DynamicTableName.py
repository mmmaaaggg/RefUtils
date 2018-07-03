# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, Float, String, DateTime, create_engine, exc, orm, Table, UniqueConstraint, MetaData
from sqlalchemy.ext.declarative import declarative_base
from Quant import ORM

sa = ORM.ORMUtils()
metadata = MetaData()
# mytable = Table("mytable", metadata,
#                 Column('mytable_id', Integer, primary_key=True),
#                 Column('value', String(50))
#            )
Base = declarative_base()
class MyTable(Base):
    __tablename__ = 'mytable'
    mytable_id = Column('mytable_id', Integer, primary_key=True)
    value = Column('value', String(50))
    
    def __repr__(self):
        return "<mytable(mytable_id='%s', value='%s')>" % (
            self.mytable_id, self.value)
mytable = MyTable.__table__
mytable.metadata.bind = sa.eng
try:
    mytable.create(checkfirst=False)
except exc.ProgrammingError as exp: 
    print('表已经存在了')
    mytable.create(checkfirst=True)
print('table create %s' % mytable.name)

mytable.name = 'mytable2'
mytable.create(checkfirst=True)
print('table create %s' % mytable.name)

