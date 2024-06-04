import os
import sys

import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "root.settings")
django.setup()


if __name__ == "__main__":
    from query.models import BackFillStatus, Thread

    threads = Thread.objects.all()
    for thread in threads:
        if thread.label is None:
            BackFillStatus.objects.create(thread=thread)
