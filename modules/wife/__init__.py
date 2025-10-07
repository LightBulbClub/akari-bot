from core.builtins.bot import Bot
from core.builtins.message.internal import I18NContext, Image, Plain
from core.component import module
from core.constants.path import assets_path
from .database.models import TodayWifeInfo

from datetime import datetime
import os, random

wif = module('wife', ["waifu","jrlp"], "{{I18N:wife.help}}")

assets = assets_path / "modules" / "wife"

wife_names = os.listdir(assets)

@wif.command("{{I18N:wife.help}}")
async def _(msg: Bot.MessageSession):
    _id = msg.session_info.sender_id
    random.seed(_id+str(datetime.now()))
    chose = random.sample(wife_names, 1)[0]
    db = await TodayWifeInfo(sender_id=_id, name=chose, count=0).get_or_none()
    wife_now = "琪露诺.png"
    if db:
        wife_now = db.wife_name
    if await TodayWifeInfo.get_wife(sender_id=_id, name=chose):
        await msg.finish([I18NContext("wife.message.success"), Plain(chose), Image(assets / chose)])
    await msg.finish([I18NContext("wife.message.failure"), Plain(wife_now), Image(assets / wife_now)])
