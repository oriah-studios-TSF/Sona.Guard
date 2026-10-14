# Models Package Initialization
#
# In Python, an `__init__.py` file turns a folder into a package.
# Re-exporting our domain models here provides two important architectural benefits:
# 1. Cleaner imports across the app: Other modules can write `from app.models import User, Resident`
#    instead of deep imports like `from app.models.user import User`.
# 2. Metadata discovery: When `app.models` is imported by `create_app()`, SQLAlchemy's declarative
#    base discovers all tables, columns, and foreign key relationships so that schema generation
#    (e.g. `db.create_all()`) and migration tools (Alembic) recognize all models.

from app.models.user import User
from app.models.audit_log import AuditLog
from app.models.resident import Resident
from app.models.entrance import Entrance
from app.models.access_attempt import AccessAttempt
from app.models.property import Property
from app.models.visitor import Visitor
from app.models.visitor_authorization import VisitorAuthorization
from app.models.unit import Unit
