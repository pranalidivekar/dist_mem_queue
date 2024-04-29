
python src/server/slave.py 6001 &
python src/server/slave.py 6002 &
python src/server/slave.py 6003 &


sleep 3

python src/server/language_model.py 6060 &

python src/server/master.py

