from apps.notifier.handlers.main_menu import register_module_notifier
from apps.notifier.handlers.make_message import register_make_messages
from apps.notifier.handlers.send_message import register_send_messages
from apps.notifier.handlers.show_messages import register_show_messages


def register_notifier(dp):
    register_module_notifier(dp)
    register_make_messages(dp)
    register_send_messages(dp)
    register_show_messages(dp)
