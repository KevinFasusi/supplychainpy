import multiprocessing as mp


class CoreCount:
    """ Manage cpu core count for setting multiprocessing tasks.

    """
    def __init__(self):
        self._core_count = self._get_core_count()

    @property
    def core_count(self) ->int:
        """Returns system core count.
        """
        return self._core_count

    @staticmethod
    def _get_core_count()->int:
        return int(mp.cpu_count())

if __name__ =="__main__":
    c = CoreCount()
    print(c.core_count)