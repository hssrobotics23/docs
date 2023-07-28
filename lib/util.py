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
