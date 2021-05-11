# Build the docker image. Explicitly builds for amd64 in case this is run on Apple's M1 chip which is ARM.
echo "Building docker image..."
docker buildx build --platform linux/amd64 -f ./docker/workout_refresh.dockerfile -t us.gcr.io/pelotonmetrics/workout-refresh .

# Push the newly built image to Google's container registry.
echo "Pushing docker image..."
docker push us.gcr.io/pelotonmetrics/workout-refresh

# Make sure we're in the correct GCP project.
echo "Setting GCP project..."
gcloud config set project pelotonmetrics

# Make sure we're in the correct compute zone.
echo "Setting GCP compute zone..."
gcloud config set compute/zone us-east4-c

# Points kubectl to cluster-1 in our project and ensures we have creds to communicate with it.
echo "Getting K8s cluster credentials..."
gcloud container clusters get-credentials cluster-1

# Prints the current context, should be `gke_pelotonmetrics_us-east4-c_cluster-1`
echo "Current kubectl context is:"
kubectl config current-context

# Apply any changes made to the cron job configuration.
echo "Applying cron job configuration..."
kubectl apply -f docker/workout_refresh_cronjob.yaml
