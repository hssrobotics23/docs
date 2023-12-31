# HSS Robotics 2023

### Project Repositories

- [The OCR + classifier API implementaion](https://github.com/hssrobotics23/api)
- [Training pipeline for classifier](https://github.com/hssrobotics23/model_training_pipeline)
- [Generation of Synthetic images](https://github.com/hssrobotics23/to-spice-images)
- [Scraping real spice images](https://github.com/hssrobotics23/image_dl)
- [Deployment of FastAPI](https://github.com/hssrobotics23/app-deployment)
- [ML flow container](https://github.com/hssrobotics23/mlflow)
  
### This Repository

Both syntehtic and scraped data are hosted publicly on AWS, [for jupyter notebook demos](#included-notebooks). The notebooks use the API to run our classifier model and EasyOCR on the images. The `example_usage` notebook gives the most succinct API usage, with no dependencies. The `performance` notebook measures precision and recall on the scraped image dataset. The `visualize` notebook measures bounding box accuracy on synthetic images. Both the `visualize` and `example_usage` notebooks conclude with demonstrations of recipe geneation by passing the recognized spices to OpenAI. They connect to a local or cloud backend depending on the `USE_AWS_AI` flag at the top of each file. View the [image generation documentation](https://github.com/hssrobotics23/to-spice-images)

This page provides two types of documentation:

1) [Run Jupyter notebooks](#included-notebooks) with access to our public API
2) For `USE_AWS_AI=False`, run the API [locally with Docker](#reproducing-locally-with-docker)

## Included notebooks

- In `example_usage.ipynb`, view the [core api usage](#core-api-usage)
- In `visualize.ipynb`, view a [general visualization demo](#visualize-in-jupyter-notebook)
- In `performance.ipynb`, view a [performance demo](#performance-in-jupyter-notebook)


For all but `example_usage.ipynb`, create a `conada` environment and install `pip` dependencies.

```
git clone https://github.com/hssrobotics23/docs.git
cd docs
conda create -n visualize python=3.9
conda activate visualize
conda install nb_conda_kernels
pip install -r requirements.txt
python3 -m jupyterlab
```

## Core API usage

Run `python3 -m jupyterlab`, and navigate to `example_usage.ipynb`. This runs the API pipeline on `example_image.jpeg`.

## Visualize in Jupyter notebook

Run `python3 -m jupyterlab`, and navigate to `visualize.ipynb`. This runs on the synthetic images hosted on AWS, indexed in `merged.json`.

## Performance in Jupyter notebook

Run `python3 -m jupyterlab`, and navigate to `performance.ipynb`. This runs on the scraped images hostod on AWS, indexed in `images.json`.

## Reproducing Data used

The synthetic data is indexed in `merged.json`, following [this documentation](https://github.com/thejohnhoffer/to-spice-images#text-generation). The real-world data is indexed in `images.json`, which is generated by this command:

```
aws --output json s3api list-objects --bucket dgmd-s17-assets --prefix 'train/downloaded-images/' | jq '[.Contents[].Key]' > images.json
```

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

The Docker image repositories automatically update the docker images when pushed to the `main` branch on GitHub. Once the image has been built (check GitHub Actions for the status), run `docker image list` to see the relevant image ID, then remove the existing image with `docker image rm [ID]`. Next, run `docker-compose up -d` to relaunch the updated docker image. This is only required when changing dependencies in the `requirements.txt`. All other changes to the code itself are watched continously and updtated live at runtime.

### Opening the API client

Now, make post requests to the local prediction API, or run the notebooks with `USE_AWS_AI = False`.

```
http://localhost:80/predict
```

[rosetta]: https://collabnix.com/warning-the-requested-images-platform-linux-amd64-does-not-match-the-detected-host-platform-linux-arm64-v8/
