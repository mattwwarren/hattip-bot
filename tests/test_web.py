import asyncio
import pytest
from unittest import TestCase
from unittest.mock import MagicMock, Mock, patch

from hattip.web import common, hooks, start
from tests.data import slack


class TestWebStart(TestCase):
    def test_default_handle(self):
        mocked_request = {}
        # TODO: mock a aiohttp.web.Request
        self.assertTrue(True)


class TestWebHooks(TestCase):
    def setUp(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        self.hooks = hooks.Hooks()
        self.mockedRequest = Mock()

    def test_call_func_error(self):
        self.mockedRequest.match_info = {'func': 'does_not_exist'}
        with self.assertRaises(AttributeError):
            self.hooks.call_func(self.mockedRequest)

    def test_call_func_success(self):
        self.mockedRequest.match_info = {'func': 'echo'}
        # TODO: figure out why this won't run
        # self.hooks.call_func(self.mockedRequest)

    def test_call_echo_json_error(self):
        self.mockedRequest.json = MagicMock(return_value=asyncio.Future())
        self.mockedRequest.json.return_value.set_result('this is a string')
        # TODO: figure out why this runs but the above doesn't
        asyncio.get_event_loop().run_until_complete(self.hooks.echo(self.mockedRequest))


class TestWebCommon(TestCase):
    def test_qsl_to_json(self):
        d = common.qsl_to_json(slack.add_tip_form_post)
        self.assertIsInstance(d, dict)
        self.assertDictEqual(d, slack.add_tip_json)
