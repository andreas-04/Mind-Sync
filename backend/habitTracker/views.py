# This file defines the views for the Habit Tracker application. Views in Django are responsible for processing incoming HTTP requests and returning HTTP responses.
# They are essentially Python functions that take a Web request and return a Web response.

# Import necessary modules from the Django REST framework
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from .habitTrackerProcessor import promptify_serialized_habitTracker
# Import the models and serializers for this app
from .models import Task, HabitTracker, Goal, MentorConfig
from .serializers import TaskSerializer, HabitTrackerSerializer, GoalSerializer, MentorConfigSerializer
from openai import OpenAI
import time

# Define the viewset for the Goal model
class GoalViewSet(viewsets.ModelViewSet):
   # Specify the queryset to be all Goal objects
   queryset = Goal.objects.all()
   # Specify the serializer class to be the GoalSerializer
   serializer_class = GoalSerializer



# Define the viewset for the Task model
class TaskViewSet(viewsets.ModelViewSet):
   # Specify the queryset to be all Task objects
   queryset = Task.objects.all()
   # Specify the serializer class to be the TaskSerializer
   serializer_class = TaskSerializer

# Define the viewset for the HabitTracker model
class HabitTrackerViewSet(viewsets.ModelViewSet):
   # Specify the queryset to be all HabitTracker objects
   queryset = HabitTracker.objects.all() 
   # Specify the serializer class to be the HabitTrackerSerializer
   serializer_class = HabitTrackerSerializer

   # Define an additional action for this viewset
   @action(detail=True, methods=['get'])
   def tasks(self, request, pk=None):
      # Get the HabitTracker object for the given primary key
      habit_tracker = self.get_object()

      # Fetch all goals associated with this HabitTracker
      goals = Goal.objects.filter(habit_tracker=habit_tracker)

      # Initialize an empty list to hold all tasks
      all_tasks = []

      # Iterate over each goal and fetch its tasks
      for goal in goals:
         tasks = Task.objects.filter(goal=goal)
         # Append the tasks to the all_tasks list
         all_tasks.extend(tasks)

      # Serialize the tasks
      serializer = TaskSerializer(all_tasks, many=True)
      # Return the serialized data
      return Response(serializer.data)
   @action(detail=True, methods=['get'])
   def goals(self, request, pk=None):
      # Get the HabitTracker object for the given primary key
      habit_tracker = self.get_object()
      # Filter the Goal objects to get those associated with this HabitTracker
      goals = Goal.objects.filter(habit_tracker=habit_tracker)
      # Serialize the goals
      serializer = GoalSerializer(goals, many=True)
      # Return the serialized data
      return Response(serializer.data)
   
   @action(detail=True, methods=['post'])
   def submit(self, request, pk=None):
       habit_tracker = self.get_object()
       habit_tracker.submit()
       return Response({"status": "success"})
   
class SendMessage(APIView):
   def post(self, request, habitId ):
      if (request.data.get('message')):
         habit_tracker = HabitTracker.objects.get(pk=habitId)
         config = MentorConfig.objects.get(habit_tracker = habitId)
         configSerializer = MentorConfigSerializer(config)
         habitSerializer = HabitTrackerSerializer(habit_tracker)
         msg = request.data.get('message')
         prompt = promptify_serialized_habitTracker(habitSerializer.data, msg, configSerializer.data )
         message = client.beta.threads.messages.create(
            thread_id=habit_tracker.user.thread_id,
            role="user",
            content=prompt
         )
         run = client.beta.threads.runs.create(
            thread_id=habit_tracker.user.thread_id,
            assistant_id="asst_Sy64Dch7BiGm7Q54v14m3eyo",
         )
         max_wait = 60
         poll_interval = 1
         elapsed = 0
         while run.status in ['queued', 'in_progress', 'cancelling'] and elapsed < max_wait:
            time.sleep(poll_interval)
            elapsed += poll_interval
            run = client.beta.threads.runs.retrieve(
               thread_id=habit_tracker.user.thread_id,
               run_id=run.id
            )
         if run.status == 'completed':
            messages = client.beta.threads.messages.list(
               thread_id=habit_tracker.user.thread_id
            )
            assistant_messages = [msg for msg in messages.data if msg.assistant_id is not None]
            if assistant_messages:
               latest_message_content = assistant_messages[0].content[0].text.value
               return Response(latest_message_content, status=status.HTTP_200_OK)
         if elapsed >= max_wait:
            return Response({"error": "Assistant response timed out after 60 seconds"}, status=status.HTTP_504_GATEWAY_TIMEOUT)
         return Response({"error": f"Assistant run failed with status: {run.status}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
      
      return Response(status=status.HTTP_400_BAD_REQUEST)
   
class MentorConfigViewSet(viewsets.ModelViewSet):
   queryset = MentorConfig.objects.all()
   serializer_class = MentorConfigSerializer
