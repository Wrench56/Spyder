from abc import ABC, abstractmethod


class Plugin(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def load(self) -> bool:
        pass

    @abstractmethod
    def unload(self) -> bool:
        pass

    @abstractmethod
    def health(self) -> bool:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    def __str__(self) -> str:
        return f'<Plugin "{self.name}">'
