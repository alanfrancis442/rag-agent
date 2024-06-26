import multiprocessing
import subprocess
import time

def run_server():
    print("Starting the server")
    subprocess.run(["python3",'server.py'])

def run_agent():
    time.sleep(10)
    print("Starting the agent and chat interface")
    subprocess.run(["chainlit",'run','agent.py'])

if __name__ == '__main__':
    server = multiprocessing.Process(target=run_server)
    agent = multiprocessing.Process(target=run_agent)

    server.start()
    agent.start()

    server.join()
    agent.join()