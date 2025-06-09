kubectl apply -f namespace.yaml

kubectl config set-context --current --namespace=peloton-metrics

kubectl create secret generic app-secrets  --from-file=../docker/secrets/postgres_root_pw --from-file=../docker/secrets/postgres_user --from-file=../docker/secrets/peloton_api_auth.json
kubectl create secret generic grafana-secrets --from-file=../docker/secrets/grafana_admin --from-file=../docker/secrets/postgres_grafana_pw 

kubectl apply -f ./db/persistent_volume.yaml
kubectl apply -f ./db/persistent_volume_claim.yaml
kubectl apply -f ./db/postgres_deployment.yaml
kubectl apply -f ./db/postgres_service.yaml

# To connect to this locally from Azure data studio, use the following command
# and connect on post 5433
#  kubectl port-forward service/postgres 5433:5432 > /dev/null &

kubectl apply -f ./app/workout_refresh.yaml

