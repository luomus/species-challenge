#!/bin/bash

TIMESTAMP=$(date '+%Y%m%d%H%M%S')

mariadb-dump --host=$MYSQL_HOST --user=$MYSQL_USER --password=$MYSQL_PASSWORD --databases $MYSQL_DATABASE | gzip > /usr/src/app/backup-$TIMESTAMP-$BRANCH.sql.gz

echo "Copying data to object store [$TIMESTAMP]\n"

rclone --config=/usr/src/app/rclone.conf copy "/usr/src/app/backup-$TIMESTAMP-$BRANCH.sql.gz" "default:hy-7088-species-challenge"

echo "Removing local archive [$TIMESTAMP]\n"

rm /usr/src/app/backup-$TIMESTAMP-$BRANCH.sql.gz
