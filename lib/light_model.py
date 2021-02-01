from scipy.spatial import distance
from lib.prefix_tree import PrefixTree
from lib.GloVe.embedding_vector import get_embedding_vector


def light(source, target, dist_fun=distance.euclidean) -> float:
    """Evaluating additional light."""
    source_pos, source_size = source[0], source[1]
    target_pos, target_size = target[0], target[1]
    dist = dist_fun(source_pos, target_pos)

    return source_size * target_size / ((100 + target_size) * (1 + dist ** 2))


def get_dimensions(word: list):
    """Return position and size of light point."""
    words = word["word"].split("_")
    dim = get_embedding_vector(words[0])

    if dim is None:
        return (None, word["val"])

    for w in words[1:]:
        dim0 = get_embedding_vector(w)

        if dim0 is None:
            return (None, word["val"])

        dim = dim + dim0

    return dim / len(words), word["val"]


def light_model(dic, dict_fun=distance.euclidean):
    """Make ranking according to similarity from GloVe."""
    full_light = PrefixTree()

    for target in dic.list():
        total_light = target["val"]
        target_dimensions = get_dimensions(target)

        if target_dimensions[0] is not None:

            for source in dic.list():

                if source["word"] != target["word"]:
                    source_dimensions = get_dimensions(source)

                    if source_dimensions[0] is not None:
                        total_light += light(
                            target_dimensions, get_dimensions(source), dict_fun
                        )

        full_light.value(target["word"], total_light)

    return full_light
