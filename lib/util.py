from matplotlib import pyplot as plt

AWS_AI_URL="http://34.192.30.136/"
LOCAL_AI_PORT = "80"

def to_ai_url(use_aws_ai):
    return (
        AWS_AI_URL if use_aws_ai else f'http://localhost:{LOCAL_AI_PORT}/'
    )

def setup_plt(keep_ticks=False):
    plt.clf()
    plt.close()
    ax = plt.gca()
    if keep_ticks == False:
        ax.xaxis.set_tick_params(labelbottom=False)
        ax.yaxis.set_tick_params(labelleft=False)
        ax.set_xticks([])
        ax.set_yticks([])

def setup_viz_box(result_text, real_text):
    correct = result_text == real_text
    sep = "==" if correct else "≠"
    font = { "fontsize": 30 }
    title = (
        f'{result_text} {sep} {real_text}'
    )
    plt.title(title, **font)

    predicted = ({
        "linewidth": 10, "fmt": "w"
    }, {
        "linewidth": 5, "fmt": "k"
    })
    actual = ({
        "mew": 8, "ms": 35, "fmt": "w+"
    }, {
        "mew": 5, "ms": 30, "fmt": "g+"
    })

    return { "predicted": predicted, "actual": actual }


def draw_viz_box(label,boxes,props):

    for (bi, box) in enumerate(boxes):
        xs, ys = zip(*box)
        xs += (xs[0],)
        ys += (ys[0],)
        max_k = len(props) - 1
        for (ki, kw) in enumerate(props):
            kw["label"] = (
                label if bi == 0 and ki == max_k else f'_{bi}_{ki}'
            )
            fmt = kw.pop("fmt", None)
            plt.plot(xs,ys, fmt, **kw)
