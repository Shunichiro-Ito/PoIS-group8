from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import sys
from sqlalchemy.orm import (sessionmaker, relationship, scoped_session)
import sshtunnel as sshtun

SSH_PKEY = '~/.ssh/Group08.Admin.pem'

# SSHトンネル接続情報の設定
ssh_forwarder = sshtun.SSHTunnelForwarder(
    ssh_address_or_host='ec2-54-196-139-143.compute-1.amazonaws.com',
    ssh_username='ec2-user',
    ssh_password='Shakai.Group08',
    remote_bind_address=('ip-172-31-21-16.ec2.internal', 3306),
    ssh_pkey=SSH_PKEY,
    
)
db_name = 'group8_db'

#create session
class SQLSession:

    def __init__(self):
        try:
            # SSHトンネルを開始
            ssh_forwarder.start()

            engine = create_engine(
                f'mysql+pymysql://user1:PoIS-group8@{ssh_forwarder.local_bind_address}:{ssh_forwarder.local_bind_port}',#/{db_name}?charset=utf8', 
                echo=False, 
                pool_recycle=10
            )

            self.SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=True, expire_on_commit=False, bind=engine))
            self.Base = declarative_base()

        finally:
            # SSHトンネルを停止
            ssh_forwarder.close()
            sys.dont_write_bytecode = True

    def close(self):
        self.SessionLocal.remove()
        # SSHトンネルを停止
        ssh_forwarder.close()
        sys.dont_write_bytecode = True
    

    # MySQLサーバーからデータを取得
    #with engine.connect() as conn:
    #    rows = conn.execute(
    #        'データ取得SQL')
    #    for row in rows:
    #        print(row)


    #url = f"mysql+pymysql://{user}:{password}@{host}/{db_name}?charset=utf8"
    #url = f'mysql+mysqlconnector://{user}:{password}@{host}/{db_name}?charset=utf8'
    #url = "mysql+pymysql://root:group_8@localhost:3306/failure_story_db?charset=utf8"