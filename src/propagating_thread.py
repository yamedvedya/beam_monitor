import threading
import sys
import traceback

class ExcThread(threading.Thread):


    def __init__(self, target, threadname, errorBucket,  *args):
        threading.Thread.__init__(self, target=target, name=threadname, args=args)
        self.bucket = errorBucket
        self._stop_event = threading.Event()

    def run(self):
        try:
            if hasattr(self, '_Thread__target'):
                self.ret = self._Thread__target(*self._Thread__args, **self._Thread__kwargs)
            else:
                self.ret = self._target(*self._args, **self._kwargs)
        except Exception as exp:
            print ('exception in caught propagating thread:')
            print (exp)
            traceback.print_tb(sys.exc_info()[2])
            self.bucket.put(sys.exc_info())

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.isSet()