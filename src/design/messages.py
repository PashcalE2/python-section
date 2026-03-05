import enum
from dataclasses import dataclass
from typing import Type, Self


class MessageType(enum.Enum):
    TELEGRAM = enum.auto()
    MATTERMOST = enum.auto()
    SLACK = enum.auto()


@dataclass
class JsonMessage:
    message_type: MessageType
    payload: str


@dataclass
class ParsedMessage:
    """There is no need to describe anything here."""


class Parser:
    def parse(self, message: str) -> ParsedMessage:
        raise NotImplementedError()


class TelegramParser(Parser):
    def parse(self, message: str) -> ParsedMessage:
        print(f"Parse telegram message: {message=}")
        return ParsedMessage()


class MettermostParser(Parser):
    def parse(self, message: str) -> ParsedMessage:
        print(f"Parse mettermost message: {message=}")
        return ParsedMessage()


class SlackParser(Parser):
    def parse(self, message: str) -> ParsedMessage:
        print(f"Parse slack message: {message=}")
        return ParsedMessage()


class ParserFabric:
    __parsers: dict[MessageType, Type[Parser]] = {}

    def add(self, message_type: MessageType, parser_cls: Type[Parser]) -> Self:
        if message_type in self.__parsers:
            raise ValueError(f"Parser for `{message_type}` is already present")
        self.__parsers[message_type] = parser_cls
        return self

    def create(self, message_type: MessageType) -> Parser:
        return self.__parsers[message_type]()


fabric = ParserFabric()
fabric.add(MessageType.TELEGRAM, TelegramParser).add(
    MessageType.MATTERMOST, MettermostParser).add(MessageType.SLACK, SlackParser)

tg = fabric.create(MessageType.TELEGRAM)
tg.parse("message")

mat = fabric.create(MessageType.MATTERMOST)
mat.parse("message")

sl = fabric.create(MessageType.SLACK)
sl.parse("message")
