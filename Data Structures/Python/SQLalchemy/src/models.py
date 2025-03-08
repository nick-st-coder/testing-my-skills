from sqlalchemy import Table, Column, String, Integer, MetaData, ForeignKey, text, TIMESTAMP, Enum, CheckConstraint, Index
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base, str_256, sync_engine
from typing import Optional, Annotated
import enum

intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('UTC', NOW())"))]
updated_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('UTC', NOW())"),
                                               onupdate=datetime.utcnow())]

metadata_obj = MetaData()

class WorkersOrm(Base):
    __tablename__ = "workers"

    id: Mapped[intpk]
    username: Mapped[str] = mapped_column()

    resumes:Mapped[list["ResumesOrm"]] = relationship(
        back_populates="worker",
    )

    resumes_parttime:Mapped[list["ResumesOrm"]] = relationship(
        back_populates="worker",
        primaryjoin="and_(WorkersOrm.id == ResumesOrm.worker_id, ResumesOrm.workload == 'part_time')",
        viewonly=True
    )

class Workload(enum.Enum):
    full_time = "full_time"
    part_time = "part_time"

class ResumesOrm(Base):
    __tablename__ = "resumes"

    id: Mapped[intpk]
    
    title: Mapped[str_256] = mapped_column()
    compensation: Mapped[Optional[int]]
    workload: Mapped[Workload]
    worker_id: Mapped[int] = mapped_column(ForeignKey("workers.id"))
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    worker: Mapped["WorkersOrm"] = relationship(
        back_populates="resumes",
    )

    vacancies_replied:Mapped[list["VacanciesOrm"]] = relationship(
        back_populates="resumes_replied",
        secondary="vacancies_replies",
    )

    __table_args__ = (
        Index("title_index","title"),
        CheckConstraint("compensation>=0", name="compensation_check_positive"),
    )

class VacanciesOrm(Base):
    __tablename__ = "vacancies"

    id:Mapped[intpk]
    title:Mapped[str_256]
    compensation:Mapped[Optional[int]]  

    resumes_replied:Mapped[list["ResumesOrm"]] = relationship(
        back_populates="vacancies_replied",
        secondary="vacancies_replies",
    )

class VacanciesRepliesOrm(Base):
    __tablename__ = "vacancies_replies"

    resume_id: Mapped[int] = mapped_column(
        ForeignKey("resumes.id", ondelete="CASCADE"),
        primary_key=True,
    )
    vacancy_id: Mapped[int] = mapped_column(
        ForeignKey("vacancies.id", ondelete="CASCADE"),
        primary_key=True,
    )

    cover_letter:Mapped[Optional[str]]    








metadata_obj = MetaData()

workers_table = Table(
    "workers",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("username", String),
)

resumes_table = Table(
    "resumes",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("title", String(256)),
    Column("compensation", Integer, nullable=True),
    Column("workload", Enum(Workload)),
    Column("worker_id", ForeignKey("workers.id", ondelete="CASCADE")),
    Column("created_at", TIMESTAMP,server_default=text("TIMEZONE('utc', now())")),
    Column("updated_at", TIMESTAMP,server_default=text("TIMEZONE('utc', now())"), onupdate=datetime.utcnow()),
)