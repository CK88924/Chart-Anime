import pika
import json

# RabbitMQ 配置
RABBITMQ_HOST = 'localhost'
QUEUE_NAME = 'chart_updates'

def publish_message(message):
    """
    發布消息到 RabbitMQ 隊列，確保數據可序列化為 JSON。
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME)
    try:
        # 確保消息中的所有字段都可被 JSON 序列化
        serialized_message = json.dumps(message)
        channel.basic_publish(exchange='', routing_key=QUEUE_NAME, body=serialized_message)
        print(f"Debug: Message published: {serialized_message}")
    finally:
        connection.close()

def consume_messages(callback):
    """
    訂閱 RabbitMQ 隊列並處理消息
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME)

    def on_message(ch, method, properties, body):
        data = json.loads(body)
        print(f"Debug: Message consumed: {data}")
        callback(data)

    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=on_message, auto_ack=True)
    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()
