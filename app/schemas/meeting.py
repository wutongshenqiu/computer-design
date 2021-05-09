from __future__ import annotations

from typing import Optional, Dict, Set
from enum import IntEnum
from datetime import datetime

from pydantic import BaseModel


class MeetingType(IntEnum):
    NOT_AVAILABLE: int = -1
    SECURE: int = 0
    NORMAL: int = 1
    SHARE: int = 2


class MeetingBase(BaseModel):
    meeting_id: Optional[str]
    meeting_password: Optional[str]
    name: Optional[str]
    meeting_tag: Optional[str]
    meeting_type: Optional[MeetingType]
    owner_id: Optional[int]
    participants: Optional[Set[int]]
    designated_participants: Optional[Set[int]]
    creation_time: Optional[datetime]
    end_time: Optional[datetime]

    @staticmethod
    def _optional_str_to_str(s: Optional[str]) -> str:
        if s is None:
            return ""
        return s

    @staticmethod
    def _optional_set_int_to_str(l: Optional[Set[int]]) -> str:
        if l is None:
            return ""
        return " ".join(map(str, l))

    @staticmethod
    def _optional_datetime_to_str(t: Optional[datetime]) -> str:
        if t is None:
            return ""
        return str(t.timestamp())

    def to_redis_dict(self) -> Dict:
        return {
            "meeting_id": self._optional_str_to_str(self.meeting_id),
            "meeting_password": self._optional_str_to_str(self.meeting_password),
            "name": self._optional_str_to_str(self.name),
            "meeting_tag": self._optional_str_to_str(self.meeting_tag),
            "meeting_type": int(MeetingType.NOT_AVAILABLE) if self.meeting_type is None else int(self.meeting_type),
            "owner_id": -1 if self.owner_id is None else self.owner_id,
            "participants": self._optional_set_int_to_str(self.participants),
            "designated_participants": self._optional_set_int_to_str(self.designated_participants),
            "creation_time": self._optional_datetime_to_str(self.creation_time),
            "end_time": self._optional_datetime_to_str(self.end_time)
        }

    @staticmethod
    def _str_to_optional_str(s: str) -> Optional[str]:
        if s == "":
            return None
        return s

    @staticmethod
    def _str_to_optional_set_int(s: str) -> Optional[Set[int]]:
        if s == "":
            return set()
        return set(map(int, s.split()))

    @staticmethod
    def _str_to_optional_datetime(s: str) -> Optional[datetime]:
        if s == "":
            return None
        return datetime.fromtimestamp(float(s))

    @staticmethod
    def from_redis_dict(redis_dict: Dict) -> MeetingBase:
        return MeetingBase(
            meeting_id=MeetingBase._str_to_optional_str(redis_dict["meeting_id"]),
            meeting_password=MeetingBase._str_to_optional_str(redis_dict["meeting_password"]),
            name=MeetingBase._str_to_optional_str(redis_dict["name"]),
            meeting_tag=MeetingBase._str_to_optional_str(redis_dict["meeting_tag"]),
            meeting_type=MeetingType(int(redis_dict["meeting_type"])),
            owner_id=None if redis_dict["owner_id"] == -1 else redis_dict["owner_id"],
            participants=MeetingBase._str_to_optional_set_int(redis_dict["participants"]),
            designated_participants=MeetingBase._str_to_optional_set_int(redis_dict["designated_participants"]),
            creation_time=MeetingBase._str_to_optional_datetime(redis_dict["creation_time"]),
            end_time=MeetingBase._str_to_optional_datetime(redis_dict["end_time"])
        )


class MeetingCreate(MeetingBase):
    meeting_id: str
    name: str
    meeting_type: MeetingType
    owner_id: int


class MeetingInDBBase(BaseModel):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class Meeting(MeetingInDBBase):
    pass


class MeetingInDB(MeetingInDBBase):
    pass
