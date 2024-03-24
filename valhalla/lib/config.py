from dynaconf import Dynaconfig
import pulumi


def stack_config() -> Dynaconfig:
    return Dynaconfig(
        settings_files=["config.yaml"],
        environments=True,
        force_env=pulumi.get_stack(),
    )
