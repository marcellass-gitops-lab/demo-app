# 🚀 End-to-End GitOps Pipeline with FastAPI, GitHub Actions & ArgoCD

Implementação prática de um fluxo completo de GitOps e Integração/Entrega Contínua (CI/CD) para microsserviços em Kubernetes, utilizando **ArgoCD**, **GitHub Actions**, **Kustomize** e um cluster local multi-container provisionado com **Kind**.

---

## 🏗️ Arquitetura e Segregação de Responsabilidades

Para eliminar o risco de credenciais administrativas de cluster expostas na esteira de CI e prevenir ciclos de build recursivos, a arquitetura foi desenhada com estrita segregação de repositórios:

```text
[ Repositório: demo-app ]                  [ Repositório: demo-config ]
(Aplicação & CI)                           (Fonte da Verdade / GitOps)
  ├── app/ (FastAPI)                         └── overlays/dev/
  ├── tests/ (Pytest)                             ├── deployment.yaml
  ├── Dockerfile (Non-root user)                  ├── service.yaml
  └── .github/workflows/ci.yaml                   └── kustomization.yaml
           │                                                ▲
           │ (1. Test & Build)                              │ (3. Update Tag)
           ▼                                                │
   [ GitHub Container Registry ] ───────────────────────────┘
               ▲
               │ (4. Pull Declarativo & Reconciliação Contínua)
        [ ArgoCD Controller ]
               │
               ▼
     [ Kubernetes Cluster (Kind) ]
```

### 1. `demo-app` (Repositório de Código & CI)
* **Stack:** Python 3.11, FastAPI, Pytest, Docker (Buildx).
* **Pipeline de CI:** 
  1. *Shift-Left Testing:* Execução de testes unitários com Pytest como barreira de qualidade.
  2. *Build & Push:* Compilação de container seguro (usuário não-root) e publicação no GitHub Container Registry (`ghcr.io`).
  3. *Imutabilidade de Artefatos:* Tags geradas dinamicamente com o SHA curto do commit (`7-digit SHA`), garantindo rastreabilidade e auditoria.
  4. *GitOps Trigger:* Atualização declarativa do arquivo `kustomization.yaml` no repositório `demo-config` via automação de bot sem acoplamento de credenciais do cluster.

### 2. `demo-config` (Repositório GitOps - Single Source of Truth)
* **Stack:** Kubernetes Manifests (Deployment, Service NodePort), Kustomize.
* Contém o estado desejado da infraestrutura para o ambiente de desenvolvimento (`overlays/dev`).
* O cluster Kubernetes não expõe portas administrativas para a internet; o ArgoCD realiza o sync de dentro para fora (*Pull model*).

---

## 🛡️ Resiliência e Governança Comprovada em Testes

O ambiente foi validado sob três cenários de estresse e resiliência:

1. **Deploy Automatizado Zero-Downtime:**
   * Atualização de versão da API (`v1.0.0` para `v2.0.0`) propagada em menos de 2 minutos via *RollingUpdate* orquestrado pelo ArgoCD.
2. **Self-Healing (Neutralização de Drift):**
   * Tentativas de alteração imperativa direta no cluster (`kubectl scale --replicas=5`) foram detectadas e revertidas automaticamente pelo ArgoCD em milissegundos para manter o contrato declarado no Git (`replicas: 2`).
3. **Alta Disponibilidade e Auto-Recuperação de Pods:**
   * Exclusão forçada de pods em execução com recomposição automática imediata pelo ReplicaSet gerenciado.

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem & Framework:** Python 3.11, FastAPI, Uvicorn
* **Testes & Qualidade:** Pytest, HTTPX
* **Containerização:** Docker, Docker Buildx, GHCR (GitHub Container Registry)
* **Orquestração & Infra:** Kubernetes (Kind), Kustomize
* **GitOps & CI/CD:** ArgoCD, GitHub Actions, Personal Access Tokens (PAT) com escopos granulares
