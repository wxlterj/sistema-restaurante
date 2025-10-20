# El código generado con IA va desde las lineas que empienzan con el comentario "# IA" hasta el siguiente comentario "# /IA"

from queue import Queue, PriorityQueue
from model import Client, Product
import constants as c
import uuid

# El cliente que se está atendiendo
current_client = None
# Cola general
general_queue = Queue()
# Cola con proridad
priority_queue = PriorityQueue()
# Stack para poder deshacer las ultimas acciones
actions_stack = []
products = [Product("P001", "Hamburguesa", 12000), Product("P002", "Papas Fritas", 4000), Product("P003", "Refresco", 3500)]

def add_client(name, type, n, order, id=None):
    ''' Agrega un nuevo cliente a la cola correspondiente según su tipo '''
    # Id de 8 caracteres
    client_id = id if (id is not None) else uuid.uuid4().hex[:8]
    client = Client(client_id, name, type, n, order)
    if (client.type == c.REGULAR):
        general_queue.put(client)
        add_action(c.ADD_REGULAR, client)
    elif (client.type == c.VIP):
        # Mas prioridad a los clients VIP
        priority_queue.put((1, n, client))
        add_action(c.ADD_PRIORITY, client)
    else:
        # Menos proridad a los clientes online
        priority_queue.put((2, n, client))
        add_action(c.ADD_PRIORITY, client)

def queue_to_list(queue):
    l = []
    while (not(queue.empty())):
        l.append(queue.get())
    return l

def list_to_queue(list, queue, priority=False):
    for element in list:
        queue.put(element)
    return queue
# IA
def copy_queue(q):
    """Devuelve una copia exacta de una PriorityQueue sin modificar la original."""
    temp_list = list(q.queue)  # Accede directamente al contenido interno
    new_q = Queue()
    for item in temp_list:
        new_q.put(item)
    return new_q

def copy_priority_queue(q):
    """Devuelve una copia exacta de una PriorityQueue sin modificar la original."""
    temp_list = list(q.queue) # Accede directamente al contenido interno
    new_q = PriorityQueue()
    for item in temp_list:
        new_q.put(item)
    return new_q
# /IA

def add_action(type, client):
    ''' Agrega una acción al stack de acciones para poder deshacerla luego '''
    MAX_ACTIONS = 5
    actions_stack.append((type, client))
    if len(actions_stack) > MAX_ACTIONS:
        del actions_stack[0: len(actions_stack) - MAX_ACTIONS]


def undo():
    ''' Deshace la última acción realizada que se encuentra en el stack de acciones '''
    global current_client, general_queue, priority_queue

    if not actions_stack:
        return False

    action, client = actions_stack.pop()

    if action == c.ADD_REGULAR:
        queue_list = queue_to_list(general_queue)
        queue_list.pop()
        list_to_queue(queue_list, general_queue)

    elif action == c.ADD_PRIORITY:
        priority_list = queue_to_list(priority_queue)
        priority_list = [c for c in priority_list if c[2].id != client.id]
        list_to_queue(priority_list, priority_queue, priority=True)

    elif action == c.CALL:
        if client.type == c.REGULAR:
            queue_list = queue_to_list(general_queue)
            queue_list.insert(0, client)
            list_to_queue(queue_list, general_queue)
        else:
            priority_value = 1 if client.type == c.VIP else 2
            priority_list = queue_to_list(priority_queue)
            priority_list.insert(0, (priority_value, client.n_order, client))
            list_to_queue(priority_list, priority_queue, priority=True)
        current_client = None

    elif action == c.SERVICE_COMPLETED:
        current_client = client

    else:
        return False

    return True

