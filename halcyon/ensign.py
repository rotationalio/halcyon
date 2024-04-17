import json
import base64
import pickle

from pyensign.ensign import Ensign


class Model:
    """
    Model is an object loaded from Ensign that's prepared for inference.
    """

    def __init__(self, **kwargs):
        self.ensign = Ensign(**kwargs)

    async def load(self, topic: str):
        """
        Load the latest model from an Ensign topic.
        """

        cursor = await self.ensign.query(f"SELECT * FROM {topic}")
        events = await cursor.fetchall()
        model = json.loads(events[-1].data.decode("utf-8"))
        self.model = pickle.loads(base64.b64decode(model["model"]))
        if "classes" in model:
            self.classes = model["classes"]

    def predict(self, X):
        """
        Predict samples using the loaded model.
        """

        preds = self.model.predict(X)
        if hasattr(self, "classes"):
            preds = [self.classes[p] for p in preds]

        return preds
