import fastapi as fa
import pika

router = fa.APIRouter()


@router.post('/')
def celery_tasks_queue_reverse_text(
        text: str = fa.Body(...),
):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='hello')
    channel.basic_publish(exchange='', routing_key='hello', body=text)
    connection.close()
