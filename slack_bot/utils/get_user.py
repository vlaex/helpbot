from slack_bot import bot

def get_user_nick(user_id: str):
  user = bot.client.users_info(user=user_id)

  return user['user']['profile']['display_name']
