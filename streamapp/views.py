from django.shortcuts import render,redirect
from django.http.response import StreamingHttpResponse
from streamapp.camera import VideoCamera, IPWebCam, MaskDetect, LiveWebCam
# Create your views here.

from .forms import UserRegistrationForm
from django.contrib.auth import login
import boto3

def index(request):
	return render(request, 'streamapp/home.html')


def gen(camera):
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def video_feed(request):
	return render(request, 'streamapp/video_feed.html')


def video_feed_output(request):
	return StreamingHttpResponse(gen(VideoCamera()),
					content_type='multipart/x-mixed-replace; boundary=frame')


def webcam_feed(request):
	return StreamingHttpResponse(gen(IPWebCam()),
					content_type='multipart/x-mixed-replace; boundary=frame')


def mask_feed(request):
	return StreamingHttpResponse(gen(MaskDetect()),
					content_type='multipart/x-mixed-replace; boundary=frame')
					
def livecam_feed(request):
	return StreamingHttpResponse(gen(LiveWebCam()),
					content_type='multipart/x-mixed-replace; boundary=frame')

queue_url = "https://sqs.ap-south-1.amazonaws.com/997165460744/IBM-project-sqs"

def getAuthenticateEmail(email):
	sqs = boto3.client('sqs',region_name='ap-south-1')
	
	# Send message to SQS queue
	response = sqs.send_message(
		QueueUrl=queue_url,
		DelaySeconds=10,
		MessageAttributes={
			'email': {
				'DataType': 'String',
				'StringValue': email
			},
			'is_secret': {
				'DataType': 'String',
				'StringValue': "no"
			}					
		},
		MessageBody=(
			'sgnons'
		)
	)
	print("\n\n\n\n\n")
	print(response['MessageId'])


def register(request):
	if request.method == "POST":
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			getAuthenticateEmail(request.POST['email'])
			user = form.save()
			login(request, user)
			
			return redirect("video_feed")
	form = UserRegistrationForm()
	return render (request=request, template_name="registration/register.html", context={"register_form":form})    
