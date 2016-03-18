from expects import expect
import httpretty
from .fakes import with_fake_http
from .matchers import have_json


class when_adding_an_acl_to_an_existing_stream(with_fake_http):

    def given_an_existing_stream_with_no_metadata(self):
        self.start_mocking_http()
        self.fake_response('/streams/my-stream/metadata', status=200, body='{}')
        self.expect_call('/streams/my-stream/metadata', httpretty.POST)

    def because_we_set_the_acl(self):
        self.client.streams.set_acl('my-stream',
                                    write=['ops'],
                                    read=['devs', 'ops', 'qa'],
                                    eventid="foo"
                                    )

    def it_should_post_the_correct_acl(self):
        expect(httpretty.last_request()).to(have_json([{
            "eventId": "foo",
            "eventType": "$user-updated",
            "$acl": {
                "$r": ["devs", "ops", "qa"],
                "$w": ["ops"]
            }
        }]))


class when_updating_the_acl_of_a_stream(with_fake_http):
    pass


class when_updating_the_acl_of_a_nonexistent_stream(with_fake_http):
    pass
