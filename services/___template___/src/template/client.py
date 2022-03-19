import requests

HTTP_SUCCESS_STATUS_CODES = [200, 201, 202, 203, 204]


class WebClientError(Exception):
    def __init__(self, message, status_code, content):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.content = content


class WebClient:
    def __init__(self, base):
        self._base = base

    def get(self, resource, raw=False):
        res = requests.get(self._base + resource)

        if res.status_code not in HTTP_SUCCESS_STATUS_CODES:
            raise WebClientError(
                f"Request GET: {self._base + resource} failed",
                res.status_code,
                res.json() if self._is_json(res) else res.text,
            )

        return res.json() if not raw else res.content

    def post(self, resource, data=None, file=None, raw=False):
        res = requests.post(
            self._base + resource,
            json=data,
            files={"file": (file.filename, file)} if file else None,
        )

        if res.status_code not in HTTP_SUCCESS_STATUS_CODES:
            raise WebClientError(
                f"Request POST: {self._base + resource} failed",
                res.status_code,
                res.json() if self._is_json(res) else res.text,
            )

        return res.json() if not raw else res.content

    def put(self, resource, data=None, raw=False):
        res = requests.put(self._base + resource, json=data)

        if res.status_code not in HTTP_SUCCESS_STATUS_CODES:
            raise WebClientError(
                f"Request PUT: {self._base + resource} failed",
                res.status_code,
                res.json() if self._is_json(res) else res.text,
            )

        return res.json() if not raw else res.content

    def _is_json(self, res):
        return "application/json" in res.headers.get("Content-Type")
