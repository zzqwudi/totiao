class Config:
    """
    General configuration parent class
    """
    JWT_SECRET = 'TPmi4aLWRbyVq8zu9v82dWYW17/z+UvRnYTt4P6fAXA'
    JWT_EXPIRY_HOURS = 24  # 过期时间
    JWT_REFRESH_DAYS = 14  # 刷新时间

    DATACENTER_ID = 0  # 数据中心ID
    WORKER_ID = 0  # 工作机ID
    SEQUENCE = 0  # 序列号

    # flask-sqlalchemy使用的参数
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1/1909_db'  # 数据库
    SQLALCHEMY_BINDS = {
        'bj-m1': 'mysql+pymysql://root:root@127.0.0.1:3306/1909_db',
        'bj-s1': 'mysql+pymysql://root:root@127.0.0.1:3306/toutiao',
        # 'masters': ['bj-m1'],
        # 'slaves': ['bj-m1'],
        'default': 'bj-m1'
    }

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    All_CHANNELS_CACHE_TTL = 24 * 60 * 60
