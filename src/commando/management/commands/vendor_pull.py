import helper

from django.core.management.base import BaseCommand
from typing import Any

from saas_project.settings import STATICFILES_VENDOR_DIR



VENDOR_STATICFILES = {
    "saas-theme.min.css": "https://raw.githubusercontent.com/codingforentrepreneurs/SaaS-Foundations/main/src/staticfiles/theme/saas-theme.min.css",
    "flowbite.min.css": "https://cdn.jsdelivr.net/npm/flowbite@4.0.1/dist/flowbite.min.css",
    "flowbite.min.js": "https://cdn.jsdelivr.net/npm/flowbite@4.0.1/dist/flowbite.min.js",
    "flowbite.min.js.map": "https://cdn.jsdelivr.net/npm/flowbite@4.0.1/dist/flowbite.min.js.map"
}


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any):
        self.stdout.write('Downloading vendor static files...')
        
        for name, url in VENDOR_STATICFILES.items():
            out_path = STATICFILES_VENDOR_DIR / name
            dl_success = helper.download_to_local(url, out_path)
            if dl_success:
                self.stdout.write(self.style.SUCCESS(f'Downloading {name} from {url}'))
            else:
                self.stdout.write(self.style.ERROR(f'Failed to download {name} from {url}'))
