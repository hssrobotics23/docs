def src_to_words(src):
    meta_words = src["words"]
    for meta in meta_words:
        for word in meta["word"].split('\n'):
            yield word


def src_to_box(src):
    meta_words = src["words"]
    for meta in meta_words:
        vecs = []
        for point in meta["points"]:
            vecs.append([point["x"], point["y"]])
        yield vecs


def gen_truth(sources):

    for (i, src) in enumerate(sources):
        real_box = list(src_to_box(src))
        real_words = list(src_to_words(src))
        real_text = ' '.join(real_words)

        yield {
            "text": real_text,
            "box": real_box
        }

def to_truth(sources):
    return list(gen_truth(sources))
