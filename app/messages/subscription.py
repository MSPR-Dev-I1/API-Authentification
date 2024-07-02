import os
import time
import json
import threading
from contextlib import asynccontextmanager
from google.cloud import pubsub_v1
from google.cloud.pubsub_v1.subscriber.message import Message
from app.compute.compute import create_deactivated_token
from app.database.connexion import get_db

google_project = os.getenv('GOOGLE_PROJECT')


def create_subscriber_client(): # pragma: no cover
    """
        Create a new subscriber
    """
    return pubsub_v1.SubscriberClient()

def deconnexion_subscription(): # pragma: no cover
    """
        Subscribe to the revoke-access-token-message-topic-sub subscriber
    """
    subscriber = create_subscriber_client()
    subscription_path = subscriber.subscription_path(
                                    google_project, 'revoke-access-token-message-topic-sub')
    while True:
        try:
            streaming_pull_future = subscriber.subscribe(subscription_path, deconnexion)
            streaming_pull_future.result()
        except Exception as e: # pylint: disable=broad-except
            print(f"The deconnexion subscription threw an exception: {e}. Retrying...")
            streaming_pull_future.cancel()
            streaming_pull_future.result()
            time.sleep(2)

def deconnexion(message: Message): # pragma: no cover
    """
        Revoke access token from message
    """
    try :
        print("Message Received: " + message.data.decode('utf-8'))
        data = json.loads(message.data.decode('utf-8'))
        db = get_db()
        create_deactivated_token(db,token=data["token"])
        db.close()
        message.ack()
    except Exception as e: # pylint: disable=broad-except
        print(f"The deconnexion threw an exception: {e}.")
        message.nack()

@asynccontextmanager
async def lifespan(): # pragma: no cover
    """
        Add subscription to new thread on startup
    """
    subscription_thread = threading.Thread(target=deconnexion_subscription)
    subscription_thread.start()

    yield

    subscription_thread.join()
