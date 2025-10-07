import random
import orjson
from datetime import datetime
from zoneinfo import ZoneInfo

from core.builtins.bot import Bot
from core.builtins.message.internal import Plain, Image
from core.component import module
from core.constants import assets_path

trt = module("tarot", desc="今日塔罗牌🥳")

assets = assets_path / "modules" / "tarot"

sum_file = assets_path / "modules" / "tarot" / "tarot_cards.json"

@trt.command("{幻星集塔罗}")
async def tarot(msg: Bot.MessageSession):
    cards:list[dict] = orjson.loads(sum_file.read_text())
    utc_8 = datetime.now(ZoneInfo("Asia/Shanghai"))
    date_str = utc_8.strftime("/%y/%m%d")
    user_name = msg.session_info.sender_name
    userseed = hash(date_str + user_name)
    random.seed(userseed)
    pn = random.randint(0,1)
    your_card:dict = random.sample(cards, 1)[0]
    send = await msg.send_message(
        [
            Plain(your_card.get('name')),
            Plain(your_card.get('positive' if pn == 1 else 'negative')),
            Image(assets / your_card.get('imageName')),
            Plain('[90秒后撤回]')
        ]
    )
    await msg.sleep(90)
    await send.delete()

