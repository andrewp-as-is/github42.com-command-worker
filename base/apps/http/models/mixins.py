from http.client import parse_headers
from io import BytesIO


class HeadersMixin:
    def get_headers(self):
        fp = BytesIO(self.headers.encode()) if self.headers else None
        return parse_headers(fp) if fp else {}
