import asyncio
import functools
import logging

import psycopg2

from core.config import settings

logger = logging.getLogger(__name__)

import pika, sys, os


def sync(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.get_event_loop().run_until_complete(f(*args, **kwargs))

    return wrapper


def main():
    connection = pika.BlockingConnection(pika.URLParameters('amqp://rabbitmq?connection_attempts=10&retry_delay=10'))
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    @sync
    async def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        db = psycopg2.connect(host=settings.DB_HOST,
                              database=settings.DB_NAME,
                              user=settings.DB_USER,
                              password=settings.DB_PASSWORD)
        cur = db.cursor()
        body = body.decode('utf-8')[::-1]
        cur.execute(f"insert into queue values (default, '{body}')")
        db.commit()

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
