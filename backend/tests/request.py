import json
from json import JSONDecodeError

from aivivn_backend.app import app
from tests.utils import get_user_header

USERS = [
    dict(username='user1', password='password'),
    dict(username='user2', password='password'),
    dict(username='user3', password='password'),
    dict(username='user4', password='password'),
    dict(username='user5', password='password'),
    dict(username='user6', password='password')
]


class Base:
    def __init__(self,
                 endpoint,
                 data=None,
                 user=None,
                 user_id=None,
                 expected_status_code=None,
                 **kwargs):
        """
        send api request
        :param endpoint:
        :param data:
        :param user: dict with username, password
        :param expected_status_code: check if request returns this status code
        :param kwargs:
        """
        self._endpoint = endpoint
        self._user = user or (USERS[user_id - 1] if user_id else None)
        self._header = get_user_header(app.test_client(), self._user)
        self._data = data
        self._kwargs = kwargs
        self._status_code = expected_status_code
        self._request_fn = kwargs['request_fn']

        endpoint = self._endpoint

        params = []
        if 'limit' in self._kwargs:
            params.append('limit=%d' % self._kwargs['limit'])
        if 'offset' in self._kwargs:
            params.append('offset=%d' % self._kwargs['offset'])
        endpoint += "?%s" % ('&'.join(params))

        with self._request_fn(endpoint, headers=self._header, data=self._data) as res:
            self.res = {
                'data': res.data,
                'status_code': res.status_code
            }
            print('----------------------------')
            print("endpoint:", endpoint, "(%s)" % self._request_fn)
            print("status code:", res.status_code)
            print("response:", res.data)
        if self._status_code is not None:
            assert self.res['status_code'] == self._status_code

    def __enter__(self):
        try:
            return json.loads(self.res['data'])
        except JSONDecodeError:
            return self.res['data']

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class get(Base):
    def __init__(self, endpoint, **kwargs):
        kwargs['request_fn'] = app.test_client().get
        super().__init__(endpoint, **kwargs)


class post(Base):
    def __init__(self, endpoint, **kwargs):
        kwargs['request_fn'] = app.test_client().post
        super().__init__(endpoint, **kwargs)


class patch(Base):
    def __init__(self, endpoint, **kwargs):
        kwargs['request_fn'] = app.test_client().patch
        super().__init__(endpoint, **kwargs)


class delete(Base):
    def __init__(self, endpoint, **kwargs):
        kwargs['request_fn'] = app.test_client().delete
        super().__init__(endpoint, **kwargs)


class put(Base):
    def __init__(self, endpoint, **kwargs):
        kwargs['request_fn'] = app.test_client().put
        super().__init__(endpoint, **kwargs)
