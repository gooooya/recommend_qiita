@echo off
SET BASE_DIR=%cd%

echo Applying Kubernetes configurations in db folder...
cd /d %BASE_DIR%\db
kubectl delete -f .

echo Applying Kubernetes configurations in mlflow folder...
cd /d %BASE_DIR%\mlflow
kubectl delete -f .

echo Applying Kubernetes configurations in notebook folder...
cd /d %BASE_DIR%\notebook
kubectl delete -f .

cd /d %BASE_DIR%

echo All configurations have been deleted.
