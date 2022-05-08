import re
import json
from slack_bot import bot
from slack_bot.config import PROFILE_LINK_REGEX
from slack_bot.utils.slack_messages import get_delete_reason
from slack_bot.core.graphql import client, to_base64
from slack_bot.core.redis_db import redis_client


@bot.message(re.compile(PROFILE_LINK_REGEX))
def save_message(message, context):
  profile_link = re.search(PROFILE_LINK_REGEX, message['text'])

  if profile_link is None:
    raise ValueError(f"Failed to find the profile link in the message: {message['text']}")

  profile_link = profile_link.group()
  user = context.get('user_data')

  user_id = profile_link.split('-')[-1]
  encoded_user_id = to_base64(user_id, 'user')

  # Fetch user data
  user_data = client.execute(query="""
    query GetUser($id: ID!) {
      user(id: $id) {
        nick rank {name} points answers {count} avatar {url} thanks {count} created helpedUsersCount
      }
    }
  """, variables={'id': encoded_user_id})

  if not user_data['data'] or not user_data['data']['user']:
    raise ValueError(f"Brainly error / User <{user_id}> ({profile_link}) is deleted")

  brainly_user = user_data['data']['user']

  data = {
    'sent_by': context.get('user_nick'),
    'reason': get_delete_reason(message['text']),
    'link': profile_link,
    'user': {
      'id': encoded_user_id,
      'database_id': int(user_id),
      'nick': brainly_user['nick'],
      'rank': brainly_user['rank']['name'] if brainly_user['rank'] else '',
      'points': brainly_user['points'],
      'answers_count': brainly_user['answers']['count'],
      'avatar': brainly_user['avatar']['url'] if brainly_user['avatar'] else '/img/avatars/100-ON.png',
      'thanks_count': brainly_user['thanks']['count'],
      'created': brainly_user['created'],
      'helped_users_count': brainly_user['helpedUsersCount']
    },
    'message': {
      'text': message['text'],
      'ts': message['ts']
    },
    'sender': {
      'id': user['id'],
      'team_id': user['team_id'],
      'nick': context.get('user_nick'),
      'avatar': user['profile']['image_192']
    },
    'note': ''
  }

  # Save data in the Redis storage
  redis_client.set(f"todelete:{message['ts']}:{message['user']}", json.dumps(data))
