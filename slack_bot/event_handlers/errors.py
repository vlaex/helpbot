from slack_bot import bot

@bot.error
def error_handler(error, body, logger):
  logger.exception(f"An error occured: {error}")
  logger.info(f"Request body: {body}")
