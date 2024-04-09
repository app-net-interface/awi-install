LOCALBIN ?= $(shell pwd)/bin
$(LOCALBIN):
	mkdir -p $(LOCALBIN)

KUBEBIN ?= $(shell pwd)/kube-awi/bin
HELMIFY ?= $(LOCALBIN)/helmify
KUSTOMIZE ?= $(KUBEBIN)/kustomize

.PHONY: init-submodules
init-submodules:
	git submodule update --init --recursive

.PHONY: helmify
helmify: $(HELMIFY) ## Download helmify locally if necessary.
$(HELMIFY): $(LOCALBIN)
	test -s $(LOCALBIN)/helmify || GOBIN=$(LOCALBIN) go install github.com/arttor/helmify/cmd/helmify@v0.4.11

.PHONY: build-operator-chart
build-operator-chart: helmify
	$(MAKE) -C kube-awi manifests kustomize
	$(KUSTOMIZE) build kube-awi/config/default | $(HELMIFY) awi-operator
