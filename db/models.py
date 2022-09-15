import peewee
from config import pg_database

class News(peewee.Model):
    class Meta:
        database = pg_database
    
    title = peewee.CharField(max_length=255)
    image = peewee.CharField(max_length=255)
    desc = peewee.TextField()
    location = peewee.CharField(max_length=100)
    beds = peewee.IntegerField()
    price = peewee.DecimalField(max_digits=10, decimal_places=2)
    date = peewee.DateTimeField()