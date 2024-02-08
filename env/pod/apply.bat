@echo off
SET BASE_DIR=%cd%

echo Applying Kubernetes configurations in db folder...
cd /d %BASE_DIR%\db
kubectl apply -f .

echo Applying Kubernetes configurations in mlflow folder...
cd /d %BASE_DIR%\mlflow
kubectl apply -f .

echo Applying Kubernetes configurations in notebook folder...
cd /d %BASE_DIR%\notebook
kubectl apply -f .

cd /d %BASE_DIR%