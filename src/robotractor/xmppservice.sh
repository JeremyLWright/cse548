#description "Robotractor XMPP <-> Django adapter"
#author "jeremy@codestrokes.com"

#env PYTHON_HOME=/home/ubuntu/robotenv/bin/activate
. /home/ubuntu/robotenv/bin/activate

#start on runlevel [2345]
#stop on runlevel [!2345]

#exec $PYTHON_HOME/bin/python /home/ubuntu/robo/xmppservice/xmppservice.py
python /home/ubuntu/robot/src/robotractor/xmppservice.py


