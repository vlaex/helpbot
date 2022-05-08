from slack_bot import bot
from slack_bot.core.users import SlackUser


@bot.use
def get_extra_info(context, payload, next):
  """ Load extra info about the event: `user` object, `user_nick`, `message` object """

  if 'user' in payload:
    slack_user = SlackUser(payload['user'])

    context['user_data'] = slack_user.get_user()
    context['user_nick'] = slack_user.get_nick()

  if payload['type'] == 'reaction_added':
    item_ts = payload['item']['ts']

    messages = bot.client.conversations_history(
      limit=1,
      channel=payload['item']['channel'],
      inclusive=True,
      latest=item_ts
    )

    for message in messages['messages']:
      if message['ts'] == item_ts:
        context['message'] = message

        author = SlackUser(message['user'])
        context['message_user'] = author.get_user()
        context['message_user_nick'] = author.get_nick()

  next()
