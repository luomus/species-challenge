#!/bin/bash

i="all"
f="template.yml"
e=".env"

while getopts ":f:e:i::" flag; do
  case $flag in
    f) f=${OPTARG} ;;
    e) e=${OPTARG} ;;
    i) i=${OPTARG} ;;
  esac
done

set -a

source ./$e

set +a

BRANCH=$(git symbolic-ref --short -q HEAD)

# If not in main, assume dev
if [ "$BRANCH" != "main" ]; then

  HOST=$HOST_DEV
  MYSQL_PASSWORD=$MYSQL_PASSWORD_DEV
  ITSYSTEM=$ITSYSTEM_DEV

fi

if [ $i = "volume" ]; then

  ITEM=".items[0]"

elif [ $i = "config" ]; then

  ITEM=".items[1]"

elif [ $i = "secrets" ]; then

  ITEM=".items[2]"

elif [ $i = "deploy-app" ]; then

  ITEM=".items[3]"

elif [ $i = "deploy-db" ]; then

  ITEM=".items[4]"

elif [ $i = "service-app" ]; then

  ITEM=".items[5]"

elif [ $i = "service-db" ]; then

  ITEM=".items[6]"

elif [ $i = "route" ]; then

  ITEM=".items[7]"

elif [ $i = "job" ]; then

  ITEM=".items[8]"

elif [ $i = "all" ]; then

  ITEM=""

else

  echo "Object not found"
  exit 1

fi

FINBIF_API_TOKEN=$(echo -n $FINBIF_API_TOKEN | base64)
MYSQL_PASSWORD=$(echo -n $MYSQL_PASSWORD | base64)
FLASK_SECRET_KEY=$(echo -n $FLASK_SECRET_KEY | base64)
RCLONE_ACCESS_KEY_ID=$(echo -n $RCLONE_ACCESS_KEY_ID | base64)
RCLONE_SECRET_ACCESS_KEY=$(echo -n $RCLONE_SECRET_ACCESS_KEY | base64)

echo "# $(oc project species-challenge)"

oc process -f $f \
-p BRANCH="$BRANCH" \
-p HOST="$HOST" \
-p MYSQL_PASSWORD="$MYSQL_PASSWORD" \
-p MYSQL_USER="$MYSQL_USER" \
-p MYSQL_DATABASE="$MYSQL_DATABASE" \
-p FINBIF_API_TOKEN="$FINBIF_API_TOKEN" \
-p FLASK_SECRET_KEY="$FLASK_SECRET_KEY" \
-p ITSYSTEM="$ITSYSTEM" \
-p RCLONE_ACCESS_KEY_ID="$RCLONE_ACCESS_KEY_ID" \
-p RCLONE_SECRET_ACCESS_KEY="$RCLONE_SECRET_ACCESS_KEY" \
| jq $ITEM
