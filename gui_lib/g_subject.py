from ast import Sub
from sort_lib.subject import Subject

class GSubject():

    def __init__(self, model: Subject):
        self._model = model
        # TODO:

    @property
    def model(self):
        return self._model