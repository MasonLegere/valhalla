import pulumi
from dynaconf import Dynaconf
import logging


def stack_config() -> Dynaconf:
    conf = Dynaconf(
        settings_files=["config.yaml"],
        environments=True,
        force_env=pulumi.get_stack(),
        lowercase_read=False,
    )

    logging.warn(f"Config: {conf.as_dict()}")
    return conf
