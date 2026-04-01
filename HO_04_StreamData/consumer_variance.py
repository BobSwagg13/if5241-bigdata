from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'variance',
     bootstrap_servers=['127.0.0.1:9092'],
     auto_offset_reset='earliest',
     enable_auto_commit=True,
     group_id='my-group',
     value_deserializer=lambda x: x.decode('utf-8'))

# consumer = KafkaConsumer(
#     'variance',
#      bootstrap_servers=['127.0.0.1:9092'],
#      # ... sisa kodenya sama

for message in consumer:
    message = message.value
    print("message:", message)

