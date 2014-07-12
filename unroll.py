import subprocess

class Unroll(object):

    def __init__(self):
        super(Unroll, self).__init__()
        self.unrolls = []
        self.unrolling = False

    def run(self, task, unroll=None, critical=True):
        try:
            self._run_task(task)
            if unroll is not None and not self.unrolling:
                self.unrolls.insert(0, unroll)
        except:
            print 'Task failed!'
            if critical and not self.unrolling:
                self.unroll()
                raise

    def unroll(self):
        for task in self.unrolls:
            try:
                self.unrolling = True
                self._run_task(task)
            except:
                print 'Failed to unroll task'
            finally:
                self.unrolling = False

    def _run_task(self, task):
        if task is None:
            pass
        elif isinstance(task, list):
            subprocess.check_call(task)
        elif isinstance(task, str):
            subprocess.check_call(task.split())
        elif callable(task):
            task()
        else:
            raise ValueError('Unknown task type: {:s}'.format(repr(task)))
