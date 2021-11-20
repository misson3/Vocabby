# Oct31, 2021, ms
# vocabby_v1.py
# Oct.24, 2021
# vocabby.py

import myKeys as mk
import oxford_dict_handler as odh
import gspread_handler as gsh

# import logging
# logging.basicConfig(level=logging.DEBUG)

import os
import re
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# credentials
SLACK_BOT_TOKEN = mk.slack_bot_token
SLACK_APP_TOKEN = mk.slack_app_token

# Install the Slack app and get xoxb- token in advance
app = App(token=SLACK_BOT_TOKEN)


@app.event("app_mention")
def event_test(event, say):
    say(f"Hi there, <@{event['user']}>!")


# when msg started with 'v', 'vocab', 'V', 'Vocab'
@app.message(re.compile(r'^[vV](ocab)*\s+.+$'))
def vocab_msg_handler(message, say):
    # reply 1
    # print(message)
    user = f"{message['user']}"
    # print(user, type(user))
    rep = f"Hi, <@{message['user']}>!"
    words = [w for w in message['text'].strip().split(' ')[1:] if w != '']
    rep += '  I am going to look up: ' + ', '.join(words)
    say(rep)

    # look up words and reply first
    msg_lines, results = odh.makeMessageLines(words)
    # results is a list of (word, category, definition, example)
    for line in msg_lines:
        say(line)

    # register results to google sheets
    written_row_count = gsh.register_od_results(results, user)
    # reply 2
    if written_row_count == 0:
        rep = 'Oops! No word was registered.  Please check the spell :pencil:'
    elif written_row_count == 1:
        rep = 'One word is registered :dog:'
    else:
        rep = str(written_row_count) + ' words were registered :dodo:'
    say(rep)


if __name__ == "__main__":
    SocketModeHandler(app, SLACK_APP_TOKEN).start()
