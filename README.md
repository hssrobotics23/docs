# HSS Robotics 2023

This repository describes the steps to:

1) [Run a Jupyter notebook](#visualize-in-jupyter-notebook) with access to our public API
2) Reproduce that public API [locally with Docker](#reproducing-locally-with-docker)

A pre-generated dataset is publicly hosted on AWS, [for a demo in the jupyter notebook](#visualize-in-jupyter-notebook). This notebook uses EasyOCR on the synthetic images, measuring text prediction accuracy and the precision of the bounding boxes. The Jupyter notebook concludes with a demo of recipe geneation by passing the recognized spices to OpenAI. When contributing to this repository, please run `Restart Kernel and Clear Outputs of All Cells…` before commiting in order to avoid needless merge conflicts.


## Visualize in Jupyter notebook

Please write your `OPENAI_KEY` to `docs/.env`. Using [conda](https://docs.anaconda.com/anaconda/install/windows/) is easier!

```
git clone https://github.com/hssrobotics23/docs.git
cd docs
conda create -n visualize python=3.9
conda activate visualize
pip install requests
pip install python-dotenv
pip install matplotlib numpy openai
pip install jupyterlab opencv-python
pip install git+https://github.com/JaidedAI/EasyOCR.git@f947eaa36a55adb306feac58966378e01cc67f85
python3 -m pip install --force-reinstall -v "Pillow==9.5.0"
conda install nb_conda_kernels
python3 -m jupyterlab
```

Here are the `pyenv` instructions:

```
pyenv install 3.9.17
pyenv local 3.9.17
python3 -m pip install jupyterlab numpy
python3 -m pip install opencv-python
python3 -m pip install matplotlib openai
python3 -m pip install git+https://github.com/JaidedAI/EasyOCR.git@f947eaa36a55adb306feac58966378e01cc67f85
python3 -m pip install --force-reinstall -v "Pillow==9.5.0"
python3 -m jupyterlab
```

### Running the full notebook

To run the notebook to completion, you'll need:

- the included `merged.json`, with an index to the `s3` demo images
- an openai API key, [available when logged in here](https://platform.openai.com/account/api-keys)

Note, you may follow [these steps](https://albertauyeung.github.io/2020/08/17/pyenv-jupyter.html/) to enable `pyenv` within `jupyterlab`. Note, the git install of EasyOCR is needed until the resolution of [this EasyOCR Issue](https://github.com/JaidedAI/EasyOCR/issues/1077)

## Reproducing locally with Docker 

Run the following in your local shell terminal:

```
git clone git@github.com:hssrobotics23/model_training_pipeline.git
git clone git@github.com:hssrobotics23/app-deployment.git
git clone git@github.com:hssrobotics23/mlflow.git
git clone git@github.com:hssrobotics23/api.git
```

Now, Run `aws configure` if not already logged-in to AWS. If running on Unix/Linux/MacOS, run `lsof -i :80` and then `kill` any existing process running on port `80`.

```
mkdir app-deployment/secrets
cp ~/.aws/credentials app-deployment/secrets/aws_credentials
cd app-deployment
docker-compose up -d
```

Now running `lsof -i :80` should show the one API server running on port 80.

When you're done testing locally, stop all docker containers:

```
docker ps -aq | xargs docker stop | xargs docker rm
```

### Debugging docker-compose.yml

`25GiB` storage is needed. If a `POST` request to `https://localhost:80` results in `HTTP 500`, then your may need to use the live `dgmd` service: search and replace in `docker-compose.yml`, replacing each `http://dgmd_mlflow` reference with the live URL `http://34.192.30.136`. Further, system differences (looking at you, Apple) may cause issues. If port 5000 is used by your OS (MacOS Monterey), [disable Airplay in System Preferences / Sharing](https://developer.apple.com/forums/thread/682332). For AMD v8 processors (ie, Apple M1), the following issue has not been resolved:

`The requested image's platform (linux/amd64) does not match the detected host platform (linux/arm64/v8)`

It is also possible to run the docker container on a remote server, then test privately with `sudo ssh -L 80:localhost:80 root@example.com` to access the server at `localhost`. Ensure that port `80` is open for http, such as `sudo ufw allow from any to any port 80` on Ubuntu.

### Development

The Docker image repositories automatically update the docker images when pushed to the `main` branch on GitHub. Once the image has been built (check GitHub Actions for the status), run `docker images -q dgmd_apis`, for example, and `docker-compose up -d` to relaunch the updated docker image. This is only required when changing dependencies in the `requirements.txt`. All other changes to the code itself are watched continously and updtated live at runtime.

### Opening the API client

Now, make post requests to the local prediction API

```
http://localhost:80/predict
```

[rosetta]: https://collabnix.com/warning-the-requested-images-platform-linux-amd64-does-not-match-the-detected-host-platform-linux-arm64-v8/
