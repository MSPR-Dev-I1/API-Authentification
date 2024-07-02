from google.cloud import pubsub_v1
import os
import time
import json
from app.compute.compute import create_deactivated_token
from app.database.connexion import get_db

google_project = os.getenv('GOOGLE_PROJECT')

def deconnexion_subscription():
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(google_project, 'deconnexion-topic')
    while True:
        try:
            streaming_pull_future = subscriber.subscribe(subscription_path,deconnexion)
            streaming_pull_future.result()
        except Exception as e:
            print(f"The deconnexion subscription threw an exception: {e}. Retrying...")
            streaming_pull_future.cancel()
            streaming_pull_future.result()
            time.sleep(2)
                  
def deconnexion(message):
    try :
        data = json.loads(message.data.decode('utf-8'))
        db = get_db()
        create_deactivated_token(db,token=data["token"])
        db.close()
        message.ack()
    except Exception as e:
        print(f"The deconnexion threw an exception: {e}.")
        message.nack() 
