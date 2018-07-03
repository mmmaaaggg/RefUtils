# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, create_engine, exc, orm, Table
from sqlalchemy.ext.declarative import declarative_base
from os.path import dirname

DBName = 'es_db'
Password = 'Pa5Svv()rd'
# mysql+mysqldb
# mysql+mysqlconnector
# mysql
DSNs = {
    'mysql': 'mysql+mysqlconnector://root:%s@localhost/%s' % (Password, DBName),
    'sqlite': 'sqlite:///:memory:',
}

Base = declarative_base()


class User(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    fullname = Column(String(20))
    password = Column(String(40))
    
    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (
            self.name, self.fullname, self.password)


class SQLAlchemyTest(object):
    
    def CreateIfNoTable(self, table):
        table.metadata.bind = self.eng
        if not table.exists():
            table.create()
        return table
        # try:
        #     tableret = Table(table.name, table.metadata, autoload=True)
        # except exc.NoSuchTableError:
        #     table.create()
        #     print 'Table %s is created' % table.name
        #     tableret = table
        # return tableret

    def __init__(self, dsn):
        try:
            eng = create_engine(dsn)
        except ImportError:
            raise RuntimeError()
        try:
            eng.connect()
        except exc.OperationalError:
            eng = create_engine(dirname(dsn))
            eng.execute('CREATE DTATBASE %s' % DBName).close()
            eng.create_engine(dsn)

        Session = orm.sessionmaker(bind=eng)
        self.ses = Session()
        self.eng = eng
        self.userTable = self.CreateIfNoTable(User.__table__)

    def init_db(self):
        # 找到 BaseModel 的所有子类，并在数据库中建立这些表
        Base.metadata.create_all(self.eng)
    
    def drop_db(self):
        # 找到 BaseModel 的所有子类，并在数据库中删除这些表
        Base.metadata.drop_all(self.eng)

    def insert(self):
        self.ses.add(User(name='nn', fullname='ffnn', password='passwd'))
    
    def insertBunch(self):
        self.ses.execute(
            User.__table__.insert(),
            [{'name': 'UName%d'%i ,'fullname': 'Ufullname', 'password':'passwd'} for i in range(10000)]
            )
        self.ses.commit()

    def update(self):
        # 第一种方法更新
        sql_str = User.__table__.update().where(User.name == 'nn').values(fullname='aaaaaaa')
        self.ses.execute(sql_str)
        # 第二种方法更新
        self.ses.query(User).filter(User.name == 'nn').update({User.fullname:'abc'})
        self.ses.commit()

def main():
    from distutils.log import warn as printf
    dbtype = 'sqlite'  # 'mysql' 'sqlite'
    printf('*** Connect to %r database ***' % DBName)
    try:
        orm = SQLAlchemyTest(DSNs[dbtype])
        orm.insert()
        orm.update()

    except RuntimeError:
        printf('\nError: %r not supported, exit' % dbtype)

if __name__ == '__main__':
    main()
