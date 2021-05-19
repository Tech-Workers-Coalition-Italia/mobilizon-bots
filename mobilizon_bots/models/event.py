from tortoise import fields
from tortoise.models import Model


class Event(Model):
    id = fields.UUIDField(pk=True)
    name = fields.TextField()
    description = fields.TextField()

    mobilizon_id = fields.TextField()
    mobilizon_link = fields.TextField()
    thumbnail_link = fields.TextField(null=True)

    location = fields.TextField(null=True)

    begin_datetime = fields.DatetimeField()
    end_datetime = fields.DatetimeField()
    # UTC offset in seconds
    utcoffset = fields.IntField()
    last_accessed = fields.DatetimeField()

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"{self.id} - {self.name}"

    class Meta:
        table = "event"
