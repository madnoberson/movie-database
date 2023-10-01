from typing import Type, Callable, get_args

from aiogram import Dispatcher

from src.presentation.common.interfaces.gateway_factory import GatewayFactory
from .handler_factory import HandlerFactoryImpl


Handler = Type[Callable[[object], object]]
Dependency = object | GatewayFactory


def setup_handler_factories(
    dispatcher: Dispatcher, handlers: list[Handler], dependencies: list[Dependency]
) -> None:
    """
    Adds `handlers` factories injected with `dependencies` to `dispatcher`.
    Raises `ValueError` If required dependency cannot be found in `dependencies`.
    For Example `SomeHandler` can be used in aiogram update handler function like this:

    .. code-block::python
    from path_to_some_handler import SomeHandler
    from path_to_some_handler_dto import SomeHandlerDTO

    async def aiogram_function(
        message: Message,
        some_handler_factory: HandlerFactory[SomeHandler]
        # Note: `SomeHandler` has become `some_handler_factory`
    ) -> None:
        async with some_handler_factory.create_handler() as handle:
            await handle(SomeHandlerDTO())
    """

    def create_handler_factory_name(_handler: Handler) -> str:
        """
        Converts pascal case `_handler` name into snake case with '_factory' at the end.
        For example `SomeHandler` will become `some_handler_factory`
        """
        handler_name = _handler.__name__[0].lower() + _handler.__name__[1:]
        handler_factory_name = ""
        for letter in handler_name:
            if letter.isupper():
                handler_factory_name += f"_{letter.lower()}"
                continue
            handler_factory_name += letter
        return handler_factory_name + "_factory"
    
    for handler in handlers:
        name = create_handler_factory_name(handler)
        dispatcher[name] = create_handler_factory(handler, dependencies)
        
            
def create_handler_factory(handler: Handler, dependecies: list[Dependency]) -> HandlerFactoryImpl:
    """
    Returns `handler` factory injected with `dependencies`.
    Raises `ValueError` If required dependency cannot be found in `dependencies`
    """

    def check_gateway_factory(rd: object, d: Dependency) -> bool:
        if not issubclass(type(d), GatewayFactory):
            return False
        _type = get_args(d.create_gateway.__annotations__["return"])[0]
        return True if _type.__name__.endswith(rd.__name__) else False
    
    def check_simple_dependency(rd: object, d: Dependency) -> bool:
        return True if type(d).__name__.endswith(rd.__name__) else False

    simple_dependencies, gateway_factories = {}, {}
    for rdependency_name, rdependency in handler.__annotations__.items():
        for dependency in dependecies:
            if check_gateway_factory(rdependency, dependency):
                gateway_factories.update({rdependency_name: dependency})
            elif check_simple_dependency(rdependency, dependency):
                simple_dependencies.update({rdependency_name: dependency})

    return HandlerFactoryImpl(handler, simple_dependencies, gateway_factories)
                    

