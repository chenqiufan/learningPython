import random
from flask_sqlalchemy import SQLAlchemy,SignallingSession,get_state
from flask import Flask
from sqlalchemy import orm

app = Flask(__name__)

# 多库连接
app.config["SQLALCHEMY_BINDS"] = {
    "master": "mysql+pymysql://root:mysql@localhost:3306/test39",  # 主库
    "slave1": "mysql+pymysql://root:mysql@localhost:8306/test39",  # 从库1
    "slave2": "mysql+pymysql://root:mysql@localhost:3306/test39",  # 从库2
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

# 自定义session,继承于SignallingSession 重写get_bind方法，实现读写分离
class RoutingSession(SignallingSession):
    def __init__(self,*args,**kwargs):
        super(RoutingSession,self).__init__(*args,**kwargs)

    def get_bind(self, mapper=None, clause=None):
        # 每次数据库操作(增删改查及事务操作)都会调用该方法, 来获取对应的数据库引擎(访问的数据库)
        state = get_state(self.app)
        if mapper is not None:
            try:
                persist_selectable = mapper.persist_selectable
            except AttributeError:
                persist_selectable = mapper.mapped_table
            # 如果项目中指明了特定数据库，就获取到bind_key指明的数据库，进行数据库绑定
            info = getattr(persist_selectable,'info',{})
            bind_key = info.get('bind_key')
            if bind_key is not None:
                return state.db.get_engine(self.app, bind=bind_key)

        if self._flushing:
            return state.db.get_engine(self.app, bind="master")
        else:
            slave_key = random.choice(["slave1", "slave2"])
            return state.db.get_engine(self.app, bind=slave_key)

# 自定义RoutingSQLAlchemy，继承于SQLAlchemy，重写写create_session，替换底层的SignallingSession
class RoutingSQLAlchemy(SQLAlchemy):
    def create_session(self, options):
        # 使用自定义实现了读写分离的RoutingSession
        return orm.sessionmaker(class_=RoutingSession, db=self, **options)

# 根据RoutingSQLAlchemy创建数据库对象
db = RoutingSQLAlchemy(app)

if __name__ == '__main__':
    app.run()