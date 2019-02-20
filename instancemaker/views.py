from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
import boto3
from .models import Room
import subprocess
import paramiko

def newRoom(request):
    room = Room()
    room.room_name = request.GET['room_name']
    room.room_code = request.GET['room_code']
    room.date_generated = timezone.now()
    ec2 = boto3.resource('ec2')
    instances = ec2.create_instances(
    ImageId='ami-06acfd07a72b7c26e',
    MinCount=1,
    MaxCount=1,
    InstanceType='t2.micro',
    KeyName='test',
    UserData='',
    SecurityGroupIds=[
        'sg-0f2a72eef89002c5d',
    ],
    )
    room.instance_id = instances[0].instance_id
    room.save()
    return HttpResponse("making new aws instance!!!")

def getRoom(request, room_code):
    try:
        room = Room.objects.get(room_code=room_code)
    except Post.DoesNotExist:
        raise Http404("room does not exist")
    ec2 = boto3.resource('ec2')
    ec2instance = ec2.Instance(room.instance_id)
    if ec2instance.public_ip_address is not None:
        room.server_ip = ec2instance.public_ip_address
        room.save()
    return HttpResponse(str(room.server_ip))

def closeRoom(request, room_code):
    try:
        room = Room.objects.get(room_code=room_code)
    except Post.DoesNotExist:
        raise Http404("room does not exist")
    ec2 = boto3.resource('ec2')
    ec2instance = ec2.Instance(room.instance_id)
    response = ec2instance.terminate(DryRun=False)
    return HttpResponse("successfully closed "+str(room.server_ip)+"\n"+str(response))

def runRoom(request, room_code):
    try:
        room = Room.objects.get(room_code=room_code)
    except Post.DoesNotExist:
        raise Http404("room does not exist")
    ec2 = boto3.resource('ec2')
    ec2instance = ec2.Instance(room.instance_id)
    if ec2instance.public_ip_address is not None:
        room.server_ip = ec2instance.public_ip_address
        room.save()
    # testCode = subprocess.call("ssh -i test.pem ubuntu@"+str(room.server_ip), shell=True)
    # if str(testCode) == "0":
    #     subprocess.call("yes")
    #     subprocess.call("cd moduflip-janus")
    #     subprocess.call("sudo DOCKER_IP="+str(room.server_ip)+" docker-compose up")
    #     subprocess.call("exit")
    #     return HttpResponse(str(room.server_ip)+" is running now!!!")
    # else:
    #     return HttpResponse("failed to run janus server")
    try:
        print("finding key...")
        cert = paramiko.RSAKey.from_private_key_file("/Users/hyeon/snatcherai/djangoPrac/awsmanager/instancemaker/test.pem")
        print("key is found!")
        c = paramiko.SSHClient()
        c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print("connecting...")
        c.connect( hostname = str(room.server_ip), username = "ubuntu", pkey = cert)
        print("connected!!!")
        stdin, stdout, stderr = c.exec_command('ls')
        print(stdout.readlines())
        print('going to run server with \n')
        print('sudo DOCKER_IP='+str(room.server_ip)+' docker-compose up')
        sstdin, sstdout, sstderr = c.exec_command('sudo')
        sstdin.write('DOCKER_IP='+str(room.server_ip)+' docker-compose up\n')
        sstdin.flush()
        print(sstdout.read())
        c.close()
        return HttpResponse(str(room.server_ip)+" is running now!!!")
    except Exception:
        print("Connection Failed!!!")
        print(Exception)
        return HttpResponse("failed to run janus server")
def getAllRoom(request):
    return HttpResponse('All room')
