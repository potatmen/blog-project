from django.http import response
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Post

class BlogTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username = 'testuser',
            email = 'test@email.com',
            password = 'secret'
        )
        
        self.post = Post.objects.create(
            title = 'Title',
            body = 'Body',
            author = self.user,
        )
    def test_string_repr(self):
        post = Post(title ='A sample title')
        self.assertEqual(str(post),post.title)
    def test_post_content(self):
        self.assertEqual(f'{self.post.title}','Title')
        self.assertEqual(f'{self.post.author}','testuser')
        self.assertEqual(f'{self.post.body}','Body')
    def test_post_list_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,'Body')
        self.assertTemplateUsed(response,'home.html')
    def test_post_detail_view(self):
        response = self.client.get('/post/1/')
        no_response = self.client.get('/post/10000/')
        self.assertEqual(response.status_code,200)
        self.assertEqual(no_response.status_code,404)
        self.assertContains(response,'Title')
        self.assertTemplateUsed(response,'post_detail.html')
    def test_post_create_view(self):
        response = self.client.post(reverse('post_new'),{
         'title' : 'New Title',
         'author' : self.user.id,
         'body' : 'New Text',
        })
        self.assertEqual(response.status_code,302)
        self.assertEqual(Post.objects.last().title,'New Title')
        self.assertEqual(Post.objects.last().body,'New Text')
    def test_post_update(self):
        response = self.client.post(reverse('post_edit',args ='1'),{
            'title': 'Update title',
            'body' : 'Update bodty',
        })
        self.assertEqual(response.status_code,302)
    def test_post_delete_view(self):
        response = self.client.post(reverse('post_delete',args = '1'))
        self.assertEqual(response.status_code,302)
    