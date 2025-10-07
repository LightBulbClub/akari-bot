import random

from datetime import datetime
from zoneinfo import ZoneInfo

from core.builtins.bot import Bot
from core.component import module

luck = module("luck_today","jrrp", desc="今天人品怎么样？")

mapping = {
    (0,10): "……（是百分制哦）",
    (11,19): "？！不会吧……",
    (20,39): "！呜……",
    (40,49): "！勉强还行吧……？",
    (50,64): "！还行啦，还行啦。",
    (65,89): "！今天运气不错呢！",
    (90,97): "！好评如潮！",
    (98,100): "！差点就到 100 了呢……",
}

special = {
    0: "？！",
    50: "！五五开……",
    100: "！100！100！！！！！",
}

@luck.command('{今日人品}')
async def luck_today(msg: Bot.MessageSession):
    utc_8 = datetime.now(ZoneInfo("Asia/Shanghai"))
    date_str = utc_8.strftime("/%y/%m%d")
    user_name = msg.session_info.sender_name
    userseed = hash(date_str + user_name)
    random.seed(userseed)

    # 使用加权随机 - 高分概率更大
    weights = [1, 3, 3, 1]  # 越高分权重越大
    ranges = [(1, 20), (21, 50), (51, 80), (81, 100)]

    selected_range = random.choices(ranges, weights=weights, k=1)[0]
    rp = random.randint(selected_range[0], selected_range[1])
    for i, desc in special.items():
        if rp == i:
            await msg.finish(f"你今天的人品值是：{rp}{desc}")
    for (low, high), desc in mapping.items():
        if low <= rp <= high:
            await msg.finish(f"你今天的人品值是：{rp}{desc}")


