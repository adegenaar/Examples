from abc import ABC, abstractmethod
import  random 



class TicketStrategy(ABC):
    @abstractmethod
    def create_ordering(self, TicketList)-> list:
        pass

class FIFOOrderingStrategy(TicketStrategy):
    def create_ordering(self, TicketList)-> list:
        return TicketList.copy()

class FILOOrderingStrategy(TicketStrategy):
    def create_ordering(self, TicketList)-> list:
        list_copy = TicketList.copy()
        list_copy.reverse
        return list_copy

class RandomOrderingStrategy(TicketStrategy):
    def create_ordering(self, TicketList)-> list:
        list_copy = TicketList.copy()
        random.shuffle(list_copy)
        return list_copy