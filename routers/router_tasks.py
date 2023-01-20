import fastapi as fa
import pika

from core.config import settings

router = fa.APIRouter()


@router.post('/')
def celery_tasks_queue_reverse_text(
        text: str = fa.Body(...),
):
    connection = pika.BlockingConnection(
        pika.URLParameters(f'{settings.BROKER_URL}?connection_attempts=10&retry_delay=10'))
    channel = connection.channel()
    channel.queue_declare(queue='hello')
    channel.basic_publish(exchange='', routing_key='hello', body=text)
    connection.close()
