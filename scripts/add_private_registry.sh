kubectl get secret -n $NAMESPACE ausm-private-registry > /dev/null 2>&1 && \
	{ \
		echo "Secret already exists. Removing it."; \
		kubectl delete secret  -n $NAMESPACE ausm-private-registry; \
	}

kubectl create secret docker-registry ausm-private-registry \
    -n $NAMESPACE \
    --docker-server=229451923406.dkr.ecr.us-west-2.amazonaws.com \
    --docker-username=AWS \
    --docker-password="$(aws ecr get-login-password --region us-west-2)"
