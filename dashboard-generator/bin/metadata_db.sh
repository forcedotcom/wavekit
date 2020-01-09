#!/bin/bash

if [[ $# -lt 2 ]]; then
    echo "No arguments supplied: Please specify staging or prod and config file"
    exit 1
else
    ENV=$1
    CFG=$2
fi

TMP_FOLDER='./tmp'

if [[ ! -e $TMPFOLDER ]]; then
  mkdir $TMP_FOLDER
fi

if [[ $ENV == "staging" ]]; then
    sed s/dashboard_ui/dashboard_ui_staging/ < sql/metadata_model.sql > $TMP_FOLDER/metadata_model_by_env.sql
    sed s/dashboard_ui/dashboard_ui_staging/ < sql/dashboard_data.sql > $TMP_FOLDER/dashboard_data_by_env.sql
elif [[ $ENV == "prod" ]]; then
    sed s/dashboard_ui/dashboard_ui_prod/ < sql/metadata_model.sql > $TMP_FOLDER/metadata_model_by_env.sql
    sed s/dashboard_ui/dashboard_ui_prod/ < sql/dashboard_data.sql > $TMP_FOLDER/dashboard_data_by_env.sql
else
    echo "Incorrect argument: Please specify staging or prod"
    exit 1
fi

validate_variable() {
  if [[ -z "$1" ]]; then
    print "Variable is empty"
    exit 1
  else
    print "Variable is NOT empty"
  fi
}

echo $CFG

source $CFG

echo "Refresh ${ENV} database"

#validate_variable $DATABASE
#validate_variable $DB_USER
#validate_variable $DB_HOST
#validate_variable $DB_PASSWORD

export PGPASSWORD=$DB_PASSWORD

echo "update database model "

psql -X -U $DB_USER -h $DB_HOST -f $TMP_FOLDER/metadata_model_by_env.sql \
    --echo-all  --single-transaction --set AUTOCOMMIT=off --set ON_ERROR_STOP=on $DATABASE

echo "insert data into database "

psql -X  -U $DB_USER -h $DB_HOST -f $TMP_FOLDER/dashboard_data_by_env.sql \
    --echo-all --single-transaction --set AUTOCOMMIT=off --set ON_ERROR_STOP=on $DATABASE

echo "${ENV} database has been updated!"
