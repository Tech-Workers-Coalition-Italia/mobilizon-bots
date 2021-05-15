from abc import ABC, abstractmethod
from typing import List, Optional
import arrow

from mobilizon_bots.event.event import MobilizonEvent


class EventSelectionStrategy(ABC):
    @abstractmethod
    def select(
        self,
        published_events: List[MobilizonEvent],
        unpublished_events: List[MobilizonEvent],
    ) -> Optional[MobilizonEvent]:
        pass


class SelectNextEventStrategy(EventSelectionStrategy):
    def __init__(self, minimum_break_between_events_in_minutes: int):
        self.minimum_break_between_events_in_minutes = (
            minimum_break_between_events_in_minutes
        )

    def select(
        self,
        published_events: List[MobilizonEvent],
        unpublished_events: List[MobilizonEvent],
    ) -> Optional[MobilizonEvent]:

        last_published_event = published_events[-1]
        first_unpublished_event = unpublished_events[0]
        now = arrow.now()
        assert last_published_event.publication_time < now, (
            f"Last published event has been published in the future\n"
            f"{last_published_event.publication_time}\n"
            f"{now}"
        )
        if (
            last_published_event.publication_time.shift(
                minutes=self.minimum_break_between_events_in_minutes
            )
            > now
        ):
            return None

        return first_unpublished_event


class EventSelector:
    def __init__(
        self,
        published_events: List[MobilizonEvent],
        unpublished_events: List[MobilizonEvent],
    ):
        self.published_events = published_events.sort(key=lambda x: x.begin_datetime)
        self.unpublished_events = unpublished_events.sort(
            key=lambda x: x.begin_datetime
        )

    def select_event_to_publish(
        self, strategy: EventSelectionStrategy
    ) -> Optional[MobilizonEvent]:
        return strategy.select(self.published_events, self.unpublished_events)
