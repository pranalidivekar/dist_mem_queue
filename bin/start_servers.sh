
python3 src/server/slave.py 6001 &
python3 src/server/slave.py 6002 &
python3 src/server/slave.py 6003 &


sleep 3

python3 src/server/language_model.py 6060 &

python3 src/server/master.py

