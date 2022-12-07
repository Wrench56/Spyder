import threading
import logging

# From: https://stackoverflow.com/questions/323972/is-there-any-way-to-kill-a-thread
class DestroyableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self,  *args, **kwargs):
        super(DestroyableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def kill(self):
        logging.debug(f'Killing {self.getName()}...')
        self._stop_event.set()

    def killed(self):
        return self._stop_event.is_set()

class SocketThread(DestroyableThread):
    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def kill(self):
        super().kill()