#!/bin/bash

i="all"

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

fi

if [ $i = "volume" ]; then

ITEM=".items[0]"

elif [ $i = "image" ]; then

ITEM=".items[1]"

elif [ $i = "build" ]; then

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

else

  ITEM=""

fi

oc process -f $f \
-p BRANCH=$BRANCH \
-p HOST=$HOST \
-p MYSQL_PASSWORD=$MYSQL_PASSWORD \
-p MYSQL_USER=$MYSQL_USER \
-p MYSQL_DATABASE=$MYSQL_DATABASE \
-p FINBIF_API_TOKEN=$FINBIF_API_TOKEN \
-p FLASK_SECRET_KEY=$FLASK_SECRET_KEY \
| jq $ITEM

