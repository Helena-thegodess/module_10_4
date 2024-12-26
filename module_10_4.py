from queue import Queue
import time
import threading
from random import randint


class Table:
    def __init__(self, number, guest=None):
        self.number = number
        self.guest = guest

class Guest(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        waiting_time = randint(3, 10)
        time.sleep(waiting_time)

class Cafe:
    def __init__(self, *tables):
        self.queue = Queue()
        self.tables = tables

    def guest_arrival(self, *guests):
        for guest in guests :
            for table in self.tables :
                if table.guest is None :
                    guest.start()
                    print(f'{guest.name} сел(-а) за стол номер {table.number}')
                    table.guest = guest
                    break
            else :
                self.queue.put(guest)
                print(f'{guest.name} в очереди')

    def discuss_guests(self):
        while not self.queue.empty() or any(table.guest is not None for table in self.tables):
            for table in self.tables:
                if table.guest is not None and not table.guest.is_alive():
                    print(f"{table.guest.name} покушал(-а) и ушёл(ушла)")
                    print(f"Стол номер {table.number} свободен")
                    table.guest = None
                if not self.queue.empty() and table.guest is None:
                    current_table = self.queue.get()
                    table.guest = current_table
                    current_table.start()
                    print(f"{current_table.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}")


tables = [Table(number) for number in range(1, 6)]
guests_names = [
'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]
guests = [Guest(name) for name in guests_names]
cafe = Cafe(*tables)
cafe.guest_arrival(*guests)
cafe.discuss_guests()




