from datetime import datetime, timedelta, timezone
from uuid import UUID

import arrow
import pytest

from mobilizon_reshare.event.event import MobilizonEvent
from mobilizon_reshare.publishers.platforms.platform_mapping import get_formatter_class

begin_date = arrow.get(
    datetime(
        year=2021,
        month=1,
        day=1,
        hour=11,
        minute=30,
        tzinfo=timezone(timedelta(hours=1)),
    )
).to("local")

end_date = begin_date.shift(hours=1)


@pytest.fixture()
def event() -> MobilizonEvent:
    return MobilizonEvent(
        name="test event",
        description="<p><h1>description of the event</h1></p>",
        begin_datetime=begin_date,
        end_datetime=end_date,
        mobilizon_link="http://some_link.com/123",
        mobilizon_id=UUID(int=12345),
        thumbnail_link="http://some_link.com/123.jpg",
        location="location",
        last_update_time=begin_date,
    )


@pytest.mark.parametrize(
    "publisher_name,expected_output",
    [
        [
            "facebook",
            f"""# test event

🕒 01 January, {begin_date.format('HH:mm')} - 01 January, {end_date.format('HH:mm')}


📍 location


description of the event

Link: http://some_link.com/123
""",
        ],
        [
            "telegram",
            f"""<strong>test event</strong>

🕒 01 January, {begin_date.format('HH:mm')} - 01 January, {end_date.format('HH:mm')}
📍 location

<b>description of the event</b>

<a href="http://some_link.com/123">Link</a>""",
        ],
    ],
)
def test_output_format(event, publisher_name, expected_output):
    assert (
        get_formatter_class(publisher_name)().get_message_from_event(event).strip()
        == expected_output.strip()
    )
