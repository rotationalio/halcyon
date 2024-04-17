class TextScorer:
    """
    TextScorer is a base class for scoring small text samples.
    """

    def __init__(self, model: object):
        self.model = model

    def _check_loaded(self):
        """
        Ensure that the model has been loaded.
        """

        if not hasattr(self, "model"):
            raise ValueError("Model has not been loaded.")

    def score(self, text: str) -> dict:
        """
        Score a text sample using a loaded model.
        """

        self._check_loaded()
        return self.model.predict(text)
