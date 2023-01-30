# Automation Queue

[![Python 3.11.1](https://img.shields.io/badge/python-3.11.1-blue.svg)](https://www.python.org/downloads/release/python-3111/)

>Project still under development to simulate situations involving communication between threads using the python language. This algorithm handles **FIFO(First-In-First-Out)** operations for message management using mult-threadign. The consumer is responsible for receiving the message and executing the procedure, whether for operations involving database IO or triggering pre-scheduled processes.

The app module uses mocked locks simulating waiting processing with time.sleep, the functionality is given a float code to simulate waiting. This predictable behavior makes it possible to run programmed tests, making it possible to generate greater waiting loads whether for remote queries, integrations or automated searches based on human behavior.

Model for sending messages between different threads

![alt text](https://github.com/rodrigmars/Automationqueue/blob/main/images/teste_thread.drawio.png?raw=true)

2 BOTS workers operating in parallel writing to the queue and a worker consumer for IO write operations. The challenge involves managing the queues for simple inserts using a relational database, the strategy is to apply the use of queues without adopting explicit locks in the program.
