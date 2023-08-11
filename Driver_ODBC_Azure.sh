#!/bin/bash

# Installer odbcinst
apt-get update && apt-get install -y odbcinst

# Ajouter la clé Microsoft GPG
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -

# Ajouter le référentiel Microsoft pour Ubuntu 21.10
echo "deb [arch=amd64] https://packages.microsoft.com/ubuntu/21.10/prod impish main" > /etc/apt/sources.list.d/mssql-release.list

# Mettre à jour la liste des paquets
apt-get update

# Pré-configurer l'acceptation de la licence pour msodbcsql18
export ACCEPT_EULA=Y

# Installer msodbcsql18
apt-get install -y msodbcsql18