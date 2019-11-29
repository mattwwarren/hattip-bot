import os
import logging
import asyncio
import ssl as ssl_lib
import certifi
import slack

from aiohttp import web
from concurrent.futures import ProcessPoolExecutor
from settings import SETTINGS
from web.start import build_webapp

# For simplicity we'll store our app data in-memory with the following data structure.
# onboarding_tutorials_sent = {"channel": {"user_id": OnboardingTutorial}}
onboarding_tutorials_sent = {}
hat_tips_received = {}


async def start_onboarding(web_client: slack.WebClient, user_id: str, channel_id: str):
    # Post the onboarding message in Slack
    response = await web_client.chat_postMessage(
            channel=channel_id,
            text='Hi there. We\'re so glad to be here.')

    # Capture the timestamp of the message we've just posted so
    # we can use it to update the message after a user
    # has completed an onboarding task.
    onboarding_tutorial = {'timestamp': response["ts"]}

    # Store the message sent in onboarding_tutorials_sent
    if channel_id not in onboarding_tutorials_sent:
        onboarding_tutorials_sent[channel_id] = {}
    onboarding_tutorials_sent[channel_id][user_id] = onboarding_tutorial


# ================ Team Join Event =============== #
# When the user first joins a team, the type of the event will be 'team_join'.
# Here we'll link the onboarding_message callback to the 'team_join' event.
@slack.RTMClient.run_on(event="team_join")
async def onboarding_message(**payload):
    """Create and send an onboarding welcome message to new users. Save the
    time stamp of this message so we can update this message in the future.
    """
    # Get WebClient so you can communicate back to Slack.
    web_client = payload["web_client"]

    # Get the id of the Slack user associated with the incoming event
    user_id = payload["data"]["user"]["id"]

    # Open a DM with the new user.
    response = web_client.im_open(user_id)
    channel = response["channel"]["id"]

    # Post the onboarding message.
    await start_onboarding(web_client, user_id, channel)


async def send_help(web_client, user_id, channel_id):
    response = await web_client.chat_postMessage(
            channel=channel_id,
            text="Hi there. We're not sure what you mean.")
    ts = response['ts']


# ============== Message Events ============= #
# When a user sends a DM, the event type will be 'message'.
# Here we'll link the message callback to the 'message' event.
@slack.RTMClient.run_on(event="message")
async def message(**payload):
    """Display the onboarding welcome message after receiving a message
    that contains "start".
    """
    data = payload["data"]
    web_client = payload["web_client"]
    channel_id = data.get("channel")
    user_id = data.get("user")
    text = data.get("text")

    # Only respond if the message was from a user
    if user_id:
        if text and text.lower() == "start":
            return await start_onboarding(web_client, user_id, channel_id)

        return await send_help(web_client, user_id, channel_id)


def build_slack_client():
    ssl_context = ssl_lib.create_default_context(cafile=certifi.where())
    slack_token = SETTINGS['SLACK_BOT_OAUTH_TOKEN']
    rtm_client = slack.RTMClient(
        token=slack_token, ssl=ssl_context, run_async=True, loop=loop
    )
    return rtm_client


async def start_background_tasks(app):
    slack_client = build_slack_client()
    app['slack_bot'] = slack_client
    asyncio.ensure_future(slack_client.start())


async def cleanup_background_tasks(app):
    app['slack_bot'].stop()


def main():
    loop = asyncio.get_event_loop()
    app = build_webapp()
    app.on_startup.append(start_background_tasks)
    app.on_cleanup.append(cleanup_background_tasks)
    web.run_app(app, port=os.environ.get('PORT', 8080))


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    main()
