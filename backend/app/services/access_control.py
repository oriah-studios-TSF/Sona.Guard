from datetime import datetime, timezone

from app.extensions import db
from app.models import Person, Entrance, Permission, AccessAttempt

def record_attempt(person, entrance, permission, user_id, result, reason):
    access_attempt = AccessAttempt(
        person_id=person.id,
        entrance_id=entrance.id,
        user_id=user_id,
        permission_id=permission.id if permission else None,
        result=result,
        reason=reason
    )

    db.session.add(access_attempt)
    db.session.commit()

    return {
        'result': result,
        'reason': reason,
        'access_attempt_id': access_attempt.id
    }

def verify_access(person_id, entrance_id, user_id=None):
    person = Person.query.get(person_id)
    entrance = Entrance.query.get(entrance_id)

    if not person:
        return {
            'result': 'DENIED',
            'reason': 'Person not found.',
            'access_attempt_id': None
        }

    if not person.is_active:
        return record_attempt(
            person,
            entrance,
            None,
            user_id,
            'DENIED',
            'Person is inactive.'
        )

    if not entrance:
        return {
            'result': 'DENIED',
            'reason': 'Entrance not found.',
            'access_attempt_id': None
        }

    if not entrance.is_active:
        return record_attempt(
            person,
            entrance,
            None,
            user_id,
            'DENIED',
            'Entrance is inactive.'
        )

    permission = Permission.query.filter_by(
        person_id=person.id,
        entrance_id=entrance.id,
        is_active=True
    ).first()

    if not permission:
        return record_attempt(
            person,
            entrance,
            None,
            user_id,
            'DENIED',
            'No active permission found.'
        )

    now = datetime.now(timezone.utc)

    if permission.valid_from and now < permission.valid_from:
        return record_attempt(
            person,
            entrance,
            permission,
            user_id,
            'DENIED',
            'Permission is not yet valid.'
        )

    if permission.valid_until and now > permission.valid_until:
        return record_attempt(
            person,
            entrance,
            permission,
            user_id,
            'DENIED',
            'Permission has expired.'
        )

   
    return record_attempt(
        person,
        entrance,
        permission,
        user_id,
        'GRANTED',
        'Access permitted.'
    )
    

    