class Message(dict):
    def __init__(self, role: str, content: str):
        super().__init__({"role": role, "content": content})

    def __hash__(self) -> int:
        return hash(hash((key, value)) for key, value in self.items())

class UserMessage(Message):
    def __init__(self, content: str):
        super().__init__("user", content)


class TemplateUserMessage:
    def __init__(self, template: str):
        self.template = template

    def format(self, *args, **kwargs):
        return UserMessage(self.template.format(*args, **kwargs))


class AssistantMessage(Message):
    def __init__(self, content: str):
        super().__init__("assistant", content)


class SystemMessage(Message):
    def __init__(self, content: str):
        super().__init__("system", content)
