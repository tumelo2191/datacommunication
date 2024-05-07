from azure.storage.queue import QueueClient

# Azure Queue Storage credentials
connection_string = "DefaultEndpointsProtocol=https;AccountName=serialcomms;AccountKey=jLtYi6hcYE/+ObmLkOGs9SXaRSP/0wdNZWfkX82+BcoVVzBhKpgF4rPBSbtbmyP3rLWAHnQe/WDM+AStt2AWoA==;EndpointSuffix=core.windows.net"
queue_name = "serialcommqueue"

# Initialize Azure Queue client
queue_client = QueueClient.from_connection_string(connection_string, queue_name)

def put_message_in_queue(message):
    # Add message to Azure Queue
    queue_client.send_message(message)
    print("Message placed in Azure Queue successfully")

if __name__ == "__main__":
    # Test putting a message in the queue
    message_to_put = "Hello, Azure Queue!"
    put_message_in_queue(message_to_put)
