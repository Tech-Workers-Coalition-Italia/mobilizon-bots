from typing import List

from dynaconf import Dynaconf, Validator

from mobilizon_bots.config import strategies, publishers, notifiers
from mobilizon_bots.config.notifiers import notifier_names
from mobilizon_bots.config.publishers import publisher_names


def build_settings(
    settings_files: List[str] = None, validators: List[Validator] = None
):

    SETTINGS_FILE = settings_files or [
        "mobilizon_bots/settings.toml",
        "mobilizon_bots/.secrets.toml",
        "/etc/mobilizon_bots.toml",
        "/etc/mobilizon_bots_secrets.toml",
    ]
    ENVVAR_PREFIX = "MOBILIZON_BOTS"

    return Dynaconf(
        environments=True,
        envvar_prefix=ENVVAR_PREFIX,
        settings_files=SETTINGS_FILE,
        validators=validators or [],
    )


def build_and_validate_settings(settings_files: List[str] = None):

    base_validators = (
        [
            Validator("selection.strategy", must_exist=True),
            Validator("source.mobilizon.url", must_exist=True),
        ]
        + [
            Validator(
                f"publisher.{publisher_name}.active", must_exist=True, is_type_of=bool
            )
            for publisher_name in publisher_names
        ]
        + [
            Validator(
                f"notifier.{notifier_name}.active", must_exist=True, is_type_of=bool
            )
            for notifier_name in notifier_names
        ]
    )
    raw_settings = build_settings(settings_files=settings_files)
    strategy_validators = strategies.get_validators(raw_settings)
    publisher_validators = publishers.get_validators(raw_settings)
    notifier_validators = notifiers.get_validators(raw_settings)
    settings = build_settings(
        settings_files,
        base_validators
        + strategy_validators
        + publisher_validators
        + notifier_validators,
    )
    # TODO use validation control in dynaconf 3.2.0 once released
    settings.validators.validate()
    return settings


settings = build_and_validate_settings()
