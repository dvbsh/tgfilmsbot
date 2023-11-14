from bot import bot

async def check_sub(userid):
	check_member = await bot.get_chat_member(-1001835115019, userid)
	return check_member.status in ["member", "creator", "administrator"]
