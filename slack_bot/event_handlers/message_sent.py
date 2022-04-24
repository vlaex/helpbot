import re
import base64
from slack_bot import bot
from slack_bot.config import TASK_ID_REGEX, channels
from slack_bot.utils.slack_messages import delete_message
from slack_bot.utils.graphql import client

@bot.message(re.compile(r"снять\s(отметку|нарушение)|:blue_approve:", re.IGNORECASE))
def send_to_antispamers(message):
  task_id = re.search(TASK_ID_REGEX, message['text'])
  if task_id is None:
    return

  task_id = int(task_id.group())

  encoded_task_id = base64.b64encode(
    bytes(f"question:{task_id}", 'utf-8')
  ).decode('utf-8')

  question_data = client.execute(query="""
    query GetQuestion($questionId: ID!) {
      question(id: $questionId) {
        subject {name}
        content
        answers { nodes {content} }
      }
    }
  """, variables={'questionId': encoded_task_id})

  if 'errors' in question_data:
    raise ValueError(f"An error has occured while trying to fetch Brainly: {question_data}")

  question = question_data['data']['question']

  if question is None:
    raise ValueError(f"The question #{task_id} does not exist")

  question_content = re.sub(r"<\w+\s?\/?>", '', question['content'])
  subject = question['subject']['name']
  answers_count = len(question['answers']['nodes'])

  message_blocks = [{
    'type': 'section',
    'text': {
      'type': 'mrkdwn',
      'text': f":blue_approve: [*{subject}*, ответы: *{answers_count}*] *<https://znanija.com/task/{task_id}>*"
    }
  }, {
    'type': 'section',
    'text': {
      'type': 'mrkdwn',
      'text': f"{question_content[:300]}..." if len(question_content) > 300 else question_content
    }
  }, {
		'type': 'context',
		'elements': [{
			'type': 'mrkdwn',
			'text': f"Отправлено <@{message['user']}>\n{message['text']}"
		}]
  }]

  bot.client.chat_postMessage(
    channel=channels['ANTISPAMERS'],
    blocks=message_blocks,
    text='Снятие отметки нарушения'
  )

  delete_message(channel_id=message['channel'], ts=message['ts'])
