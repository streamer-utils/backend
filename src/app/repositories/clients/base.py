import abc


class BaseRepository(abc.ABC):
    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        ...
