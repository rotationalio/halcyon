from sklearn.feature_extraction.text import CountVectorizer
from sklearn.base import BaseEstimator, TransformerMixin


class FreqDist(BaseEstimator, TransformerMixin):
    """
    Compute the token frequency distribution for text samples. This estimator is
    is compatible with scikit-learn pipelines, it takes a list of strings and outputs
    a list of dictionaries with the token names and frequencies.
    """

    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        arr = []
        for x in X:
            vec = CountVectorizer()
            freqs = vec.fit_transform([x]).toarray()
            arr.append(
                {"feature_names": vec.get_feature_names_out(), "frequencies": freqs}
            )
        return arr


def lexical_diversity(freq_dist: dict) -> float:
    """
    Lexical diversity is a measure of how many unique tokens are in a text sample.
    """
    return len(freq_dist["feature_names"]) / freq_dist["frequencies"].sum()


def repetition_score(freq_dist: dict) -> float:
    """
    Repetition score is a measure of how often tokens are repeated. It's computed from
    the approximate "steepness" of the frequency distribution. A higher score means
    certain tokens are repeated more often than others.
    """
    freqs = freq_dist["frequencies"]
    return (freqs.max() - freqs.min()) / freqs.mean()
