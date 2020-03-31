for FILE in sales_train_validation.csv calendar.csv
do
  if ! [ -f "data/raw/m5/$FILE" ]; then
    echo "M5 comp file $FILE does not exist, please download them from: https://www.kaggle.com/c/m5-forecasting-accuracy/data
and place it in the data/raw directory" && exit
  fi
done
hts make-dataset --raw=data/raw --train=data/processed --name=m5
