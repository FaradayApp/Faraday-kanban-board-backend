from .dev import Container


container = Container()


def get_di_container() -> Container:
    return container
