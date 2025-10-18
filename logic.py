from queue import Queue, PriorityQueue
from model import Client
import constants as c
import uuid
# Cola general
general_queue = Queue()

# Cola con proridad
priority_queue = PriorityQueue()

def add_client(name, type, n):
    # Id de 8 caracteres
    client_id = uuid.uuid4().hex[:8]
    client = Client(client_id, name, type, n)
    if (client.type == c.REGULAR):
        general_queue.put(client)
    elif (client.type == c.VIP):
        # Mas prioridad a los clients VIP
        priority_queue.put((1, n, client))
    else:
        # Menos proridad a los clientes online
        priority_queue.put((2, n, client))

def queue_to_list(queue):
    l = []
    while (not(queue.empty())):
        l.append(queue.get())
    return l

# IA
def copy_queue(q):
    """Devuelve una copia exacta de una PriorityQueue sin modificar la original."""
    temp_list = list(q.queue)  # Accede directamente al contenido interno
    new_q = Queue()
    for item in temp_list:
        new_q.put(item)
    return new_q
# /IA

def copy_priority_queue(q):
    """Devuelve una copia exacta de una PriorityQueue sin modificar la original."""
    temp_list = list(q.queue) # Accede directamente al contenido interno
    new_q = PriorityQueue()
    for item in temp_list:
        new_q.put(item)
    return new_q
