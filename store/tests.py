from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory
from store.models import Product, Review
from store.forms import ReviewForm

from store.views import all_reviews


class AddReviewTestCase(TestCase):
    def setUp(self):
        # Set up a test user
        self.user = User.objects.create_user(username='testuser', password='password123')

        # Set up a test product
        self.product = Product.objects.create(name='Test Product', price=10.0, description='Test Description', slug='test-product')

        # Set up a request factory and session middleware
        self.factory = RequestFactory()
        self.middleware = SessionMiddleware(get_response=lambda req: None)
        self.middleware.process_request(self.factory.get('/'))

    def test_add_review(self):
        # Create a request with a logged-in user
        request = self.factory.post(reverse('add_review', kwargs={'slug': self.product.slug}), {'review_subject': 'Test Subject', 'review_message': 'Test Message', 'rating': 5})
        request.user = self.user
        self.client = Client()
        self.client.login(username='testuser', password='password123')

        # Process the request
        response = self.client.post(reverse('add_review', kwargs={'slug': self.product.slug}), {'review_subject': 'Test Subject', 'review_message': 'Test Message', 'rating': 5})

        # Check if the review is added successfully
        self.assertEqual(response.status_code, 302)  # Check if the response is a redirect
        self.assertEqual(Review.objects.count(), 1)  # Check if the review is added to the database

        # Check if the review details are correct
        review = Review.objects.first()
        self.assertEqual(review.product, self.product)  # Check if the review is associated with the correct product
        self.assertEqual(review.user, self.user)  # Check if the review is associated with the correct user
        self.assertEqual(review.review_subject, 'Test Subject')  # Check if the review subject is correct
        self.assertEqual(review.review_message, 'Test Message')  # Check if the review message is correct
        self.assertEqual(review.rating, 5)  # Check if the review rating is correct

    def tearDown(self):
        # Clean up the test data
        User.objects.all().delete()
        Product.objects.all().delete()
        Review.objects.all().delete()

