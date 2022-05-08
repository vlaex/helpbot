from slack_bot import bot


class SlackUser:
  """ A class to represent a Slack user. """

  def __init__(self, user_id: str):
    self.id = user_id
    self.retrieve_slack_user()

  def retrieve_slack_user(self):
    """ Retrieve information about a Slack user """
    data = bot.client.users_info(user=self.id)
    self.user = data['user']

  def get_user(self):
    """ Get information about the user """
    return self.user

  def get_nick(self):
    """ Get nick of the user """
    return self.user['profile']['display_name'] or self.user['name']
