from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.preprocessing import FunctionTransformer

from halcyon.scorer import TextScorer
from halcyon.utils import FreqDist, lexical_diversity, repetition_score


class AutoGeneratedScorer(TextScorer):
    """
    Score text that may have been produced by a generative model.
    """

    def __init__(self, model: object):
        self.model = model
        self.pipeline = self._make_pipeline()
        self.labels = ["human", "auto"]

    def _make_pipeline(self):
        """
        Create a new pipeline for scoring raw text samples, without the final
        estimator.
        """

        return Pipeline(
            [
                ("freq_dist", FreqDist()),
                (
                    "union",
                    FeatureUnion(
                        transformer_list=[
                            (
                                "lexical_diversity",
                                FunctionTransformer(
                                    lambda x: [
                                        lexical_diversity(freq_dist) for freq_dist in x
                                    ]
                                ),
                            ),
                            (
                                "repetition_score",
                                FunctionTransformer(
                                    lambda x: [
                                        repetition_score(freq_dist) for freq_dist in x
                                    ]
                                ),
                            ),
                        ]
                    ),
                ),
            ]
        )

    def score(self, text: str) -> dict:
        """
        Return a dict of scores that represents how likely the text was produced by a
        generative model.
        """

        # Run the text through the pipeline to get the scores
        lex_score, rep_score = self.pipeline.transform([text])

        # Call predict on the model to get the classification
        pred = self.model.predict([[lex_score, rep_score]])

        return {
            "lexical_diversity": lex_score,
            "repetition_score": rep_score,
            "classification": self.labels[pred[0]],
            "probs": self.model.predict_proba([[lex_score, rep_score]])[0],
        }
