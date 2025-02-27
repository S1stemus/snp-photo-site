from django.db import models
from viewflow import fsm


class State(models.TextChoices):
    WAITING = "waiting", "Ожидание"
    APPROVED = "approved", "Одобрено"
    REJECTED = "rejected", "Отклонено"
    ON_DELETE = "on_delete", "Ожидает Удаления"


class Flow:
    state = fsm.State(State, default=State.WAITING)

    def __init__(self, object):
        self.object = object

    @state.setter()
    def _set_object_state(self, value):
        self.object.state = value

    @state.getter()
    def _get_object_state(self):
        return self.object.state

    @state.on_success()
    def _on_transition_success(self, descriptor, source, target):
        self.object.save()

    @state.transition(source=(State.WAITING, State.ON_DELETE), target=State.APPROVED)
    def approve(self):
        pass

    @state.transition(source=(State.WAITING, State.ON_DELETE), target=State.REJECTED)
    def reject(self):
        pass

    @state.transition(
        source=(State.APPROVED, State.REJECTED, State.ON_DELETE, State.WAITING),
        target=State.WAITING,
    )
    def update_to_waiting(self):
        pass

    @state.transition(
        source=(State.APPROVED, State.REJECTED, State.WAITING,State.ON_DELETE), target=State.ON_DELETE
    )
    def update_to_on_delete(self):
        pass
