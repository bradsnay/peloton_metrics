# Builds the images and deploys them to the local k8s cluster.
docker compose build liquibase
docker compose build workout-refresh

kubectl apply -f namespace.yaml

kubectl config set-context --current --namespace=peloton-metrics

kubectl delete secret app-secrets
kubectl delete secret grafana-secrets

kubectl create secret generic app-secrets  --from-file=../docker/secrets/postgres_root_pw --from-file=../docker/secrets/postgres_user --from-file=../docker/secrets/peloton_api_auth.json
kubectl create secret generic grafana-secrets --from-file=../docker/secrets/grafana_admin --from-file=../docker/secrets/postgres_grafana_pw 

# Create/update the DB resources.
kubectl apply -f ./db/persistent_volume.yaml
kubectl apply -f ./db/persistent_volume_claim.yaml
kubectl apply -f ./db/postgres_deployment.yaml
kubectl apply -f ./db/postgres_service.yaml

# To connect to the K8s DB locally from Azure data studio, 
# use the following command and connect on port 5433
#  kubectl port-forward service/postgres 5433:5432 > /dev/null &

# Create/update the workout refresh cron job.
kubectl apply -f ./app/workout_refresh.yaml

