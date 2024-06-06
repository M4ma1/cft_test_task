import pika, sys, os, json, subprocess, semgrep
from git import Repo
import logging, socket
import time

def run_scan(path):
    command = [
        "semgrep",
        "--config=auto",
        "--output", 
        f"/reports/{path}",
        "--json",
        f"{path}"
    ]    
    subprocess.run(command, capture_output=True, text=True)

def main():
    time.sleep(60)
    logging.warning(socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("rabbit", 5672)))
    connection = pika.BlockingConnection(pika.ConnectionParameters(host= "rabbit", port=5672))
    channel = connection.channel()

    channel.queue_declare(queue='test')

    def callback(ch, method, properties, body):
        git_url = json.loads(body)['url']
        name = git_url.split('/')[-1]
        Repo.clone_from(git_url, f"/repos/{name}")
        run_scan(f"/repos/{name}")

    channel.basic_consume(queue='test', 
                        on_message_callback=callback,
                        auto_ack=True)
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