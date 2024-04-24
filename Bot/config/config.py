from dataclasses import dataclass, field


@dataclass
class Database:
    data: field(default=dict)


@dataclass
class RedisConfig:
    data: field(default=dict)


@dataclass
class TgBot:
    data: field(default=dict)


@dataclass
class Email:
    data: field(default=dict)
