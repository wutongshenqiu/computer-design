from typing import Set, Any, Optional, Dict, List
from datetime import datetime, timedelta
import uuid
import secrets

from fastapi import APIRouter, Depends, Body, HTTPException

from aioredis import Redis

from app import schemas
from app.api import deps
from app.core.config import settings

router = APIRouter()


async def _generate_meeting_id(redis_db: Redis) -> str:
    meeting_id = str(uuid.uuid4())
    while await redis_db.hlen(meeting_id):
        meeting_id = str(uuid.uuid4())

    return meeting_id


async def _generate_meeting_password(meeting_type: schemas.MeetingType) -> Optional[str]:
    if meeting_type != schemas.MeetingType.SECURE:
        return None

    return secrets.token_urlsafe(16)


async def _hset_with_expires(
    redis_db: Redis,
    *,
    name: str,
    mapping: Dict,
    expires_duration: timedelta
) -> None:
    await redis_db.hset(name=name, mapping=mapping)
    await redis_db.expire(name, expires_duration)


@router.post("/create", response_model=schemas.MeetingCreate)
async def create_meeting(
    redis_db: Redis = Depends(deps.get_redis_db),
    *,
    name: str = Body(...),
    meeting_type: schemas.MeetingType = Body(...),
    owner_id: int = Body(...),
    designated_participants: Optional[Set[int]] = Body(...),
    creation_time: datetime = Body(...),
    duration: float = Body(...),
    _current_user: schemas.User = Depends(deps.get_current_user)
) -> Any:
    if duration > settings.MAX_MEETING_DURATION:
        raise HTTPException(
            status_code=403,
            detail={
                "type": "duration",
                "msg": "Meeting duration should not exceed 6 hours"
            }
        )

    meeting_id = await _generate_meeting_id(redis_db)
    meeting_obj = schemas.MeetingCreate(
        meeting_id=meeting_id,
        meeting_password=await _generate_meeting_password(meeting_type),
        name=name,
        meeting_type=meeting_type,
        owner_id=owner_id,
        designated_participants=designated_participants,
        creation_time=creation_time,
        end_time=creation_time + timedelta(hours=duration)
    )

    await _hset_with_expires(
        redis_db=redis_db,
        name=meeting_id,
        mapping=meeting_obj.to_redis_dict(),
        expires_duration=timedelta(hours=duration)
    )

    return meeting_obj


@router.post("/join", response_model=schemas.MeetingCreate)
async def join_meeting(
    redis_db: Redis = Depends(deps.get_redis_db),
    *,
    meeting_id: str = Depends(deps.check_meeting_exists),
    current_user: schemas.User = Depends(deps.get_current_user)
) -> Any:
    meeting_obj = schemas.MeetingCreate.from_redis_dict(await redis_db.hgetall(meeting_id))

    if meeting_obj.meeting_type == schemas.MeetingType.SECURE:
        if current_user.id != meeting_obj.owner_id and current_user.id not in meeting_obj.designated_participants:
            raise HTTPException(
                status_code=403,
                detail={
                    "type": "current_user",
                    "msg": "Current user are not allowed to join the meeting"
                }
            )

    meeting_obj.participants.add(current_user.id)
    redis_db.hset(meeting_id, "participants", meeting_obj._optional_set_int_to_str(meeting_obj.participants))

    return meeting_obj


# TODO
# reduce return value
@router.get("/share", response_model=List[schemas.MeetingCreate])
async def get_share_meetings(
    redis_db: Redis = Depends(deps.get_redis_db),
    *,
    _current_user: schemas.User = Depends(deps.get_current_user)
) -> Any:
    shared_meetings = []

    async def _is_share_meeting(name: str) -> bool:
        if int(await redis_db.hget(name, "meeting_type")) == schemas.MeetingType.SHARE:
            return True
        return False

    async for name in redis_db.scan_iter("*"):
        if await _is_share_meeting(name):
            shared_meetings.append(schemas.MeetingCreate.from_redis_dict(await redis_db.hgetall(name)))

    return shared_meetings
    