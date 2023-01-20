import asyncio
import functools
import logging

from core.config import settings
from database import SessionLocal
from database.models.text import TextModel

logger = logging.getLogger(__name__)

import pika, sys, os


def sync(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.get_event_loop().run_until_complete(f(*args, **kwargs))

    return wrapper


def main():
    connection = pika.BlockingConnection(
        pika.URLParameters(f'{settings.BROKER_URL}?connection_attempts=10&retry_delay=10'))
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    @sync
    async def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        session = SessionLocal()
        body = body.decode('utf-8')[::-1]
        new_text = TextModel(text=body)
        session.add(new_text)
        session.commit()
        session.close()

    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
