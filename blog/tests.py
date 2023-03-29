from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


from .models import Post

class BlogTsets(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='heema', email='herawiibrahim@gmail.com', password='1234'
        )

        cls.post = Post.objects.create(
            title = 'A good title',
            body = 'Nice body content',
            author = cls.user
        )

    def test_post_model(self):
        self.assertEqual(self.post.title, 'A good title')
        self.assertEqual(self.post.body, 'Nice body content')
        self.assertEqual(self.post.author.username, 'heema')
        self.assertEqual(str(self.post), 'A good title')
        self.assertEqual(self.post.get_absolute_url(), '/post/1/')

    def test_correct_location_listview(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_correct_location_detailview(self):
        response = self.client.get('/post/1/')
        self.assertEqual(response.status_code, 200)

    def test_post_listview(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertContains(response, 'Nice body content')

    def test_post_detailview(self):
        response = self.client.get(reverse('post_detail', kwargs={'pk': self.post.pk}))
        no_response = self.client.get("/post/10000/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertTemplateUsed(response, 'post_detail.html')
        self.assertContains(response, 'A good title')

    def test_post_createview(self):
        response = self.client.post(
            reverse('post_new'),
            {
                "title": "New title",
                "body": "New text",
                "author": self.user.id,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, 'New title')
        self.assertEqual(Post.objects.last().body, 'New text')
    
    def test_post_updateview(self):
        response = self.client.post(
            reverse('post_edit', args="1"),
            {
                "title": "Updated title",
                "body": "Updated text",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, 'Updated title')
        self.assertEqual(Post.objects.last().body, 'Updated text')

    def test_post_deleteview(self):
        response = self.client.post(reverse('post_delete', kwargs={'pk':"1"}))
        self.assertEqual(response.status_code, 302)