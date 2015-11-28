The following AMI is prebuilt with Caffe: https://console.aws.amazon.com/ec2/v2/home?region=us-east-1#LaunchInstanceWizard:ami=ami-763a311e

Start it up with a G ec2 instance.

When SSHing into the instance, ensure you include the ```-X``` flag, or importing Caffe will fail (something about it can't find a display). E.g:
```
ssh -i ~/.ssh/LinuxMintThinkpadX1Carbon.pem ubuntu@52.23.233.61 -X
```

Add Caffe to the python path:
```
export PYTHONPATH="$PYTHONPATH:/home/ubuntu/caffe/python"
```

You should be able to import caffe now in python:
```
ubuntu@ip-172-31-55-68:~/caffe$ python
Python 2.7.6 (default, Mar 22 2014, 22:59:56) 
[GCC 4.8.2] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import caffe
libdc1394 error: Failed to initialize libdc1394

** (.:1933): WARNING **: Couldn't connect to accessibility bus: Failed to connect to socket /tmp/dbus-2Dj6DTa4Qp: Connection refused
>>> 
```

Get the images onto the node:
```
git clone https://github.com/kyledemeule/cmpt-726-ripeness-recognition.git
```

Then from here everything is the same.