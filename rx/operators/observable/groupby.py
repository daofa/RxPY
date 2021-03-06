from rx.core import ObservableBase, Observable


def group_by(source: ObservableBase, key_mapper, element_mapper=None) -> ObservableBase:
    """Groups the elements of an observable sequence according to a
    specified key mapper function and comparer and selects the resulting
    elements by using a specified function.

    1 - observable.group_by(lambda x: x.id)
    2 - observable.group_by(lambda x: x.id, lambda x: x.name)
    3 - observable.group_by(
        lambda x: x.id,
        lambda x: x.name,
        lambda x: str(x))

    Keyword arguments:
    key_mapper -- A function to extract the key for each element.
    element_mapper -- [Optional] A function to map each source element to
        an element in an observable group.

    Returns a sequence of observable groups, each of which corresponds to a
    unique key value, containing all elements that share that same key
    value.
    """

    def duration_mapper(_):
        return Observable.never()

    return source.group_by_until(key_mapper, element_mapper, duration_mapper)
