from peewee import MySQLDatabase, Model, BigAutoField, CharField, \
    DateField, TimeField, FloatField, IntegerField, IPField
from config import DB_HOST, DB_NAME, DB_USER, DB_PASS


db = MySQLDatabase(DB_NAME, host=DB_HOST, user=DB_USER, password=DB_PASS, charset='utf8mb4')


class BaseModel(Model):
    class Meta:
        database = db


class CFLogs(BaseModel):
    # date,time,size,client_ip,host,endpoint,status,user_agent,response_time
    id = BigAutoField(primary_key=True)
    log_date = DateField(index=True)
    log_time = TimeField(index=True)
    size = IntegerField(default=0)
    client_ip = IPField()
    host = CharField(index=True, max_length=100)
    uri = CharField(index=True, max_length=250)
    status = IntegerField(default=0, index=True)
    user_agent = CharField(default="NotFound", index=True, max_length=500)
    response_time = FloatField(default=0.0, index=True)
