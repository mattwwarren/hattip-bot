from unittest import Mock, TestCase
from hattip.web import common, hooks, start
from tests.data import slack


class TestWebStart(TestCase):
    def test_default_handle(self):
        mocked_request = {}

    def test_qsl_to_json(self):
        d = common.qsl_to_json(slack.add_tip_form_post)
        self.assertIsInstance(d, dict)
        self.assertDictEqual(d, slack.add_tip_json)
