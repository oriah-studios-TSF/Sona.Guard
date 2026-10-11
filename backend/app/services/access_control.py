from datetime import datetime, timezone

from app.extensions import db
from app.models import Property, Entrance, Resident, AccessAttempt


# Helper function to persist physical access verification outcomes to the database.
# In security systems, recording both successful and denied attempts is essential for accountability.
def record_attempt(property_id, entrance, resident, user_id, result, reason):
    # Construct an AccessAttempt record linking the physical gate, estate, resident,
    # and the security officer (`user_id`) who processed the checkpoint check.
    access_attempt = AccessAttempt(
        property_id=property_id,
        entrance_id=entrance.id,
        resident_id=resident.id if resident else None,
        visitor_authorization_id=None,
        user_id=user_id,
        result=result,
        reason=reason,
    )

    # Save and commit the log immediately to guarantee that access events cannot be lost
    # even if subsequent network or application steps encounter problems.
    db.session.add(access_attempt)
    db.session.commit()

    # Return a structured dictionary summarizing the verification result and the saved log ID.
    return {
        'result': result,
        'reason': reason,
        'access_attempt_id': access_attempt.id,
    }


# Core Access Verification Engine:
# This function encapsulates the core business rules for validating whether a resident is
# permitted through a specific entrance gate.
#
# Business Rules & Reasoning:
# 1. Entrance must exist in the system.
# 2. Entrance must be active (gates under maintenance or closed at night reject all traffic).
# 3. Resident record must exist.
# 4. Resident must be active (suspended or evicted residents cannot enter).
# 5. Property must exist and be active (allows estate-wide security lockdowns).
# 6. Resident must belong to the exact property that owns the entrance (multi-tenant boundary check).
def verify_access(resident_id, entrance_id, user_id=None):
    # Step 1: Query the Entrance from the database using its primary key.
    entrance = db.session.get(Entrance, entrance_id)

    # If the entrance does not exist, fail-safe by denying entry immediately.
    # Note: We cannot record an AccessAttempt with a non-existent entrance_id due to foreign key constraints.
    if not entrance:
        return {
            'result': 'DENIED',
            'reason': 'Entrance not found.',
            'access_attempt_id': None,
        }

    # Extract the estate (property_id) associated with this specific entrance gate.
    property_id = entrance.property_id
    resident = db.session.get(Resident, resident_id)

    # Step 2: Check entrance operational status.
    # If the gate is deactivated (e.g. maintenance, emergency closure), deny access and log the attempt.
    if not entrance.is_active:
        return record_attempt(
            property_id, entrance, resident, user_id,
            'DENIED', 'Entrance is inactive.'
        )

    # Step 3: Check resident existence.
    # If no matching resident was found in the database, deny access.
    if not resident:
        return {
            'result': 'DENIED',
            'reason': 'Resident not found.',
            'access_attempt_id': None,
        }

    # Step 4: Check resident account status.
    # If the resident has been soft-deactivated (e.g. moved out, unpaid security levy), deny and log.
    if not resident.is_active:
        return record_attempt(
            property_id, entrance, resident, user_id,
            'DENIED', 'Resident is inactive.'
        )

    # Step 5: Check property status.
    property_record = db.session.get(Property, property_id)

    # If the parent estate is disabled or missing, deny entry. This enables facility-wide lockdown.
    if not property_record or not property_record.is_active:
        return record_attempt(
            property_id, entrance, resident, user_id,
            'DENIED', 'Property is inactive or unavailable.'
        )

    # Step 6: Multi-tenant boundary check.
    # Ensure that the resident actually lives in the property that owns this gate.
    # This prevents a resident with valid credentials at Estate A from opening gates at Estate B.
    if resident.property_id != property_id:
        return record_attempt(
            property_id, entrance, resident, user_id,
            'DENIED', 'Resident belongs to a different property.'
        )

    # Step 7: All business criteria satisfied.
    # Grant access and persist the successful verification record.
    return record_attempt(
        property_id, entrance, resident, user_id,
        'GRANTED', 'Resident verified. Access permitted.'
    )