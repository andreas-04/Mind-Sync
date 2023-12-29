"""
This file, tests.py, contains the unit tests for the HabitTracker application of the project.

The tests are divided into two main classes: HabitTrackerModelTest and HabitTrackerAPITest.

HabitTrackerModelTest is responsible for testing the models of the application, specifically 
the Task and HabitTracker models. It checks the verbose names of the 'name' field of the 
Task model and the 'completed' field of the HabitTracker model. The setUpTestData method
is used to create a test user, a test habit tracker, and a test task that are used in the tests.

HabitTrackerAPITest is responsible for testing the API endpoints of the application. 
It tests the GET methods for the habit trackers and tasks. The setUp method is used to 
create a test client, a test user, a test habit tracker, and a test task that are used in the tests.

Both classes inherit from the TestCase class from the django.test module, which is a 
subclass of the unittest.TestCase from the Python standard library. This provides a set of 
tools for constructing tests, such as assertion methods and a setup and teardown framework.
"""
# Importing necessary modules for testing
from django.test import TestCase
from rest_framework.test import APIClient
# Importing the models to be tested
from .models import Task, HabitTracker, DailyEntry
from users.models import CustomUser

# Testing the HabitTracker model
class HabitTrackerModelTest(TestCase):
    # Setting up test data to be used in the tests
    @classmethod
    def setUpTestData(cls):
        # Creating a test user
        user = CustomUser.objects.create(username='testuser', password='testpassword')
        # Creating a test habit tracker
        habit_tracker = HabitTracker.objects.create(daily_completed_percentage=0.0, longterm_completed_percentage=0.0, user=user)
        # Creating a test task
        Task.objects.create(name='testtask', completed=False, habit_tracker=habit_tracker)
        # Creating a test daily entry
        DailyEntry.objects.create(habit_tracker=habit_tracker, journal_entry='Test journal entry')
    # Testing the 'name' field of the Task model
    def test_task_name_label(self):
        # Getting the test task
        task = Task.objects.get(id=1)
        # Getting the verbose name of the 'name' field
        field_label = task._meta.get_field('name').verbose_name
        # Asserting that the verbose name is 'name'
        self.assertEqual(field_label, 'name')

    # Testing the 'daily_completed_percentage' field of the HabitTracker model
    def test_habit_tracker_daily_completed_percentage_label(self):
        # Getting the test habit tracker
        habit_tracker = HabitTracker.objects.get(id=1)
        # Getting the verbose name of the 'daily_completed_percentage' field
        field_label = habit_tracker._meta.get_field('daily_completed_percentage').verbose_name
        # Asserting that the verbose name is 'daily completed percentage'
        self.assertEqual(field_label, 'daily completed percentage')

    # Testing the 'longterm_completed_percentage' field of the HabitTracker model
    def test_habit_tracker_longterm_completed_percentage_label(self):
        # Getting the test habit tracker
        habit_tracker = HabitTracker.objects.get(id=1)
        # Getting the verbose name of the 'longterm_completed_percentage' field
        field_label = habit_tracker._meta.get_field('longterm_completed_percentage').verbose_name
        # Asserting that the verbose name is 'longterm completed percentage'
        self.assertEqual(field_label, 'longterm completed percentage')

# Testing the HabitTracker API
class HabitTrackerAPITest(TestCase):
    # Setting up test data to be used in the tests
    def setUp(self):
        # Creating a test client
        self.client = APIClient()
        # Creating a test user
        self.user = CustomUser.objects.create(username='testuser', password='testpassword')
        # Creating a test habit tracker
        self.habit_tracker = HabitTracker.objects.create(daily_completed_percentage=0.0, longterm_completed_percentage=0.0, user=self.user)
        # Creating a test task
        self.task = Task.objects.create(name='testtask', habit_tracker=self.habit_tracker)
    # Testing the GET method for the habit trackers
    def test_get_habit_trackers(self):
        # Sending a GET request to the habit trackers API
        response = self.client.get('/api/habitTrackers/')
        # Asserting that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

    # Testing the GET method for the tasks
    def test_get_tasks(self):
        # Sending a GET request to the tasks API
        response = self.client.get('/api/tasks/')
        # Asserting that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
# Adding a test for the DailyEntry model
class DailyEntryModelTest(TestCase):
    # Setting up test data to be used in the tests
    @classmethod
    def setUpTestData(cls):
        # Creating a test user
        user = CustomUser.objects.create(username='testuser', password='testpassword')
        # Creating a test habit tracker
        habit_tracker = HabitTracker.objects.create(user=user)
        # Creating a test task
        Task.objects.create(name='testtask', completed=False, habit_tracker=habit_tracker)
        # Creating a test daily entry
        DailyEntry.objects.create(habit_tracker=habit_tracker, journal_entry='Test journal entry')

    # Testing the 'journal_entry' field of the DailyEntry model
    def test_daily_entry_journal_entry_label(self):
        # Getting the test daily entry
        daily_entry = DailyEntry.objects.get(id=1)
        # Getting the verbose name of the 'journal_entry' field
        field_label = daily_entry._meta.get_field('journal_entry').verbose_name
        # Asserting that the verbose name is 'journal entry'
        self.assertEqual(field_label, 'journal entry')