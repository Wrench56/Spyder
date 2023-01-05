from provider import base_com


class GroupCommunicator(base_com.BaseCommunicator):
    def login(self) -> bool:
        return True
