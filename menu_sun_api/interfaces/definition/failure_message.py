import graphene


class FailureMessageCategory(graphene.Enum):
    ERROR = 'ERROR'
    INFO = 'INFO'
    VALIDATION = 'VALIDATION'
    WARNING = 'WARNING'


class FailureMessage(graphene.ObjectType):
    category = FailureMessageCategory()
    target = graphene.String()
    key = graphene.String()
    args = graphene.List(graphene.String)
    message = graphene.String()

    @classmethod
    def to_definition(cls, messages):
        messages = messages if isinstance(messages, list) else [messages]
        msgs = []
        for message in messages:
            msg = FailureMessage(category=FailureMessageCategory.get(message.category.name),
                                 target=_to_camel_case(message.target),
                                 key=message.key,
                                 args=message.args,
                                 message=message.message())

            msgs.append(msg)
        return msgs


def _to_camel_case(cls, snake_str):
    if snake_str:
        components = snake_str.split('_')
        first_letter_of_component_capitalized = "".join(
            x.title() for x in components[1:])
        return components[0] + first_letter_of_component_capitalized
    else:
        return ""
