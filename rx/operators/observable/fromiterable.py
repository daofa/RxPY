from typing import Iterable, Any

from rx.core import ObservableBase, AnonymousObservable
from rx.core.typing import Scheduler
from rx.concurrency import current_thread_scheduler
from rx.disposables import CompositeDisposable, AnonymousDisposable


def from_iterable(iterable: Iterable) -> ObservableBase:
    """Converts an iterable to an observable sequence.

    1 - res = from_iterable([1,2,3])

    Keyword arguments:
    iterable - A Python iterable

    Returns the observable sequence whose elements are pulled from the
    given iterable sequence.
    """

    def subscribe(observer, scheduler=None):
        scheduler = scheduler or current_thread_scheduler
        iterator = iter(iterable)
        disposed = False

        def action(_: Scheduler, __: Any = None):
            nonlocal disposed

            try:
                while not disposed:
                    value = next(iterator)
                    observer.on_next(value)
            except StopIteration:
                observer.on_completed()
            except Exception as error:  # pylint: disable=W0703
                observer.on_error(error)

        def dispose():
            nonlocal disposed
            disposed = True

        disposable = AnonymousDisposable(dispose)
        return CompositeDisposable(scheduler.schedule(action), disposable)
    return AnonymousObservable(subscribe)
