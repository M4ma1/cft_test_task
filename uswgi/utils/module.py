import pika, json
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
 
def is_string_an_url(url_string: str) -> bool:
    validate_url = URLValidator()

    try:
        validate_url(url_string)
    except ValidationError:
        return False

    return True

def send_to_queue(url):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbit', port=5672)) # broker ip
    channel = connection.channel()

    data = json.dumps({"url": url})

    channel.queue_declare(queue='test') # define queue

    channel.basic_publish(exchange='',
                        routing_key='test', # queue name 
                        body=data)

    connection.close()