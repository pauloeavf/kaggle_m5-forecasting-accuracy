#!/bin/bash
export K_M5_HOME=$PWD
export K_M5_DATA=$K_M5_HOME/data
export K_M5_SCRIPTS=$K_M5_HOME/scripts

mkdir -p $K_M5_DATA

filepath="$K_M5_DATA/m5-forecasting-accuracy.zip"

if [ ! -f $filepath ]; then
	echo "Downloading Kaggle M5 Forecasting - Accuracy competition files..."
	kaggle competitions download -c m5-forecasting-accuracy -p $K_M5_DATA
	unzip -o $filepath -d $K_M5_DATA > /dev/null 2>&1
else
	echo "Kaggle M5 Forecasting - Accuracy files already exist..."
fi
