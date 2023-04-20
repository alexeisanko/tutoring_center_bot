from .handlers import write_to_exam, begin_registration
from .admin import handlers_admin

bps = [write_to_exam.bp, begin_registration.bp, handlers_admin.bp]
