from dishka import make_async_container, Provider, provide, Scope, AsyncContainer

from settings import get_settings, Settings

from storage.postgres import PostgresProvider


class SettingsProvider(Provider):
    @provide(scope=Scope.APP)
    def settings(self) -> Settings:
        return get_settings()


def create_container() -> AsyncContainer:
    return make_async_container(
        SettingsProvider(),
        PostgresProvider(),
    )
