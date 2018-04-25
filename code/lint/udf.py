

from pyspark.sql import types as T
from pyspark.sql.functions import udf

from lint.utils import get_spark, zip_bin


BIN_COUNT_SCHEMA = T.MapType(
    T.StringType(),
    T.ArrayType(T.IntegerType()),
)

def _ext_bin_counts(vocab, bin_count=20):
    """Count binned tokens.
    """
    vocab = set(vocab)

    @udf(BIN_COUNT_SCHEMA)
    def worker(tokens):

        # Downcase tokens.
        tokens = [t.lower() for t in tokens]

        counts = {
            token: [0] * bin_count
            for token in vocab
        }

        for token, bin in zip_bin(tokens, bin_count):
            if token in vocab:
                counts[token][bin] += 1

        return counts

    return worker
