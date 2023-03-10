from typing import List

from sqlalchemy import BigInteger, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Protocol(Base):
    __tablename__ = "protocol"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    tokens: Mapped[List["ProtocolToken"]] = relationship(back_populates="protocol")


class Token(Base):
    __tablename__ = "token"

    id: Mapped[int] = mapped_column(primary_key=True)
    address: Mapped[str] = mapped_column(String(30))
    name: Mapped[str] = mapped_column(String(30))
    symbol: Mapped[str] = mapped_column(String(30))
    decimals: Mapped[int] = mapped_column(Integer)

    protocols: Mapped[List["ProtocolToken"]] = relationship(back_populates="token")


class ProtocolToken(Base):
    __tablename__ = "protocol_token"

    id: Mapped[int] = mapped_column(primary_key=True)
    token_id: Mapped[int] = mapped_column(ForeignKey("token.id"), index=True)
    protocol_id: Mapped[int] = mapped_column(ForeignKey("protocol.id"), index=True)

    protocol: Mapped[Protocol] = relationship(back_populates="tokens")
    token: Mapped[Token] = relationship(back_populates="protocols")

    account_balances: Mapped[List["AccountBalance"]] = relationship(back_populates="protocol_tokens")
    token_prices: Mapped[List["TokenPrice"]] = relationship(back_populates="protocol_token")
    tvls: Mapped[List["Tvl"]] = relationship(back_populates="protocol_token")


class Account(Base):
    __tablename__ = "account"

    id: Mapped[int] = mapped_column(primary_key=True)
    wallet_address: Mapped[str] = mapped_column(String(30), index=True)

    account_balances: Mapped[List["AccountBalance"]] = relationship(back_populates="accounts")


class AccountBalance(Base):
    __tablename__ = "account_balance"

    id: Mapped[int] = mapped_column(primary_key=True)
    protocol_token_id: Mapped[int] = mapped_column(ForeignKey("protocol_token.id"), index=True)
    protocol_tokens: Mapped[List[ProtocolToken]] = relationship(back_populates="account_balances")
    amount: Mapped[int] = mapped_column(BigInteger)
    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"), index=True)
    accounts: Mapped[List[Account]] = relationship(back_populates="account_balances")
    created_at_block: Mapped[int]


class TokenPrice(Base):
    __tablename__ = "token_price"

    id: Mapped[int] = mapped_column(primary_key=True)
    protocol_token_id: Mapped[int] = mapped_column(ForeignKey("protocol_token.id"), index=True)
    usd_price: Mapped[int] = mapped_column(Numeric)
    created_at: Mapped[int]

    protocol_token: Mapped[ProtocolToken] = relationship(back_populates="token_prices")


class Tvl(Base):
    __tablename__ = "tvl"

    id: Mapped[int] = mapped_column(primary_key=True)
    protocol_token_id: Mapped[int] = mapped_column(ForeignKey("protocol_token.id"))
    amount: Mapped[int] = mapped_column(Numeric)
    amount_usd: Mapped[int] = mapped_column(Numeric)
    created_at: Mapped[int]
    created_at_block: Mapped[int]

    protocol_token: Mapped[ProtocolToken] = relationship(back_populates="tvls")
