from django.http.response import HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView
from . models import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from . serializer import *
# Create your views here.
from torchvision import models
import torch
from torchvision import transforms
import json
from PIL import Image as Image2

class ReactView(APIView):
	
	serializer_class = ReactSerializer
    
	def get(self, request):
		detail = [ 
            {
                "title": detail.title,
                "content": detail.content, 
                "image_url": detail.image_url, 
                "pytorch_label": detail.pytorch_label,
            }
		for detail in Post.objects.all()]
		return Response(detail)

	def post(self, request):

		serializer = ReactSerializer(data=request.data)
		if serializer.is_valid(raise_exception=True):
			serializer.save()
			return Response(serializer.data)
class PostView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)

        # print(serializer.data)
        # return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        posts_serializer = PostSerializer(data=request.data)
        if posts_serializer.is_valid():
            posts_serializer.save()
            # print(posts_serializer.data)

            t = Post.objects.get(id=posts_serializer.data["id"])


            # pytorch implemenation
            alexnet = models.alexnet(pretrained=True)
            transform = transforms.Compose([            #[1]
            transforms.Resize(256),                    #[2]
            transforms.CenterCrop(224),                #[3]
            transforms.ToTensor(),                     #[4]
            transforms.Normalize(                      #[5]
            mean=[0.485, 0.456, 0.406],                #[6]
            std=[0.229, 0.224, 0.225]                  #[7]
            )])
            img2 = Image2.open(t.image)
            img_t = transform(img2)
            batch_t = torch.unsqueeze(img_t, 0)
            alexnet.eval()
            out = alexnet(batch_t)
            _, index = torch.max(out, 1)
            percentage = torch.nn.functional.softmax(out, dim=1)[0] * 100
            labels_data = open('media/imagenet-simple-labels.json')
            labels = json.load(labels_data)
            my_list = percentage.tolist()
            index = my_list.index(max(my_list))
            print(labels[index])

            t.pytorch_label = labels[index]  # change field
            t.title = labels[index] 
            t.image_url = "http://127.0.0.1:8000/media/"+str(t.image)
            t.save() # this will update only
            # return HttpResponse("<h1>data sent sussfully</h1>")
            return Response(posts_serializer.data, status=status.HTTP_201_CREATED)
    