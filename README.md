### Reproducing locally with Docker 

Run the following in your local shell terminal:

```
git clone git@github.com:hssrobotics23/model_training_pipeline.git
git clone git@github.com:hssrobotics23/app-deployment.git
git clone git@github.com:hssrobotics23/mlflow.git
git clone git@github.com:hssrobotics23/api.git
```

Now, Run `aws configure` if not already logged-in to AWS.

```
mkdir app-deployment/secrets
cp ~/.aws/credentials app-deployment/secrets/aws_credentials
cd app-deployment
docker-compose up -d
```

### Debugging docker-compose.yml
 
System differences (looking at you, Apple) may require small changes to `app-deployment/docker-compose.yml`. If port 5000 is used by your OS (MacOS Monterey), change the port mapping. 

```
ports:
    - "5001:5000"
```

For AMD processors (Apple Silicon), set platform for `services`, `ap`, `ml-flow`, and `model-pipeline`.

```
platform: linux/amd64
```

[rosetta]: https://collabnix.com/warning-the-requested-images-platform-linux-amd64-does-not-match-the-detected-host-platform-linux-arm64-v8/
