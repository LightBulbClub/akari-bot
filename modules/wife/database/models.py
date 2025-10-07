from datetime import datetime, timedelta

from tortoise import fields

from core.database.base import DBModel

table_prefix = "module_wife_"


class TodayWifeInfo(DBModel):
    """
    用户随机到的老婆

    :param sender_id: 用户 ID。
    :param wife_name: 随机的老婆名。
    :param count: 换老婆次数。
    :param timestamp: 时间戳。
    """
    sender_id = fields.CharField(max_length=512, pk=True)
    wife_name = fields.CharField(max_length=512)
    count = fields.IntField()
    timestamp = fields.DatetimeField(null=True, auto_now_add=True)

    class Meta:
        table = f"{table_prefix}info"

    @classmethod
    async def get_wife(cls, sender_id: str, name: str):
        exist_info = await cls.get_or_none(sender_id=sender_id)
        if exist_info and exist_info.timestamp.date() != datetime.now().date():
            await exist_info.delete()
        elif exist_info and exist_info.count < 5:
            exist_info.count += 1
            await exist_info.save()
            return True
        elif exist_info and exist_info.count == 5:
            return False
        new_info = (await cls.get_or_create(sender_id=sender_id, name=name, count=0))[0]
        await new_info.save()
        return True

