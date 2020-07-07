# Generated by Django 3.0.8 on 2020-07-07 14:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(blank=True, max_length=100, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Couser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=30, null=True)),
                ('email', models.CharField(blank=True, max_length=40, null=True)),
                ('mobile', models.CharField(blank=True, max_length=10, null=True)),
                ('password', models.CharField(blank=True, max_length=30, null=True)),
                ('fullname', models.CharField(blank=True, max_length=50, null=True)),
                ('avatar', models.ImageField(default='', upload_to='images/')),
                ('dob', models.DateField(blank=True, null=True)),
                ('about', models.CharField(blank=True, max_length=300, null=True)),
                ('place', models.CharField(blank=True, max_length=100, null=True)),
                ('followings_count', models.PositiveIntegerField(default=0)),
                ('followers_count', models.PositiveIntegerField(default=0)),
                ('bookmarks_count', models.PositiveIntegerField(default=0)),
                ('posts_count', models.PositiveIntegerField(default=0)),
                ('is_account_verified', models.BooleanField(default=True)),
                ('is_email_verified', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EntityType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('body', models.TextField(blank=True, null=True)),
                ('picture', models.ImageField(blank=True, default='', null=True, upload_to='images/')),
                ('likes_count', models.PositiveIntegerField(default=0)),
                ('comments_count', models.PositiveIntegerField(default=0)),
                ('bookmarks_count', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='masterapp.Category')),
                ('couser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='masterapp.Couser')),
            ],
        ),
        migrations.CreateModel(
            name='ReportType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detail', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entity_type', models.CharField(blank=True, max_length=40, null=True)),
                ('custome_report', models.CharField(blank=True, max_length=200, null=True)),
                ('comment', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='report_comments', to='masterapp.Comment')),
                ('couser', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='report_cousers', to='masterapp.Couser')),
                ('post', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='post_posts', to='masterapp.Post')),
                ('report_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='couser_report_types', to='masterapp.ReportType')),
                ('reporter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='couser_reporters', to='masterapp.Couser')),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('couser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='masterapp.Couser')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='masterapp.Post')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='couser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='masterapp.Couser'),
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='masterapp.Post'),
        ),
        migrations.CreateModel(
            name='Bookmark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('couser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookmarks', to='masterapp.Couser')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookmarks', to='masterapp.Post')),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followings', to='masterapp.Couser')),
                ('following', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to='masterapp.Couser')),
            ],
            options={
                'unique_together': {('follower', 'following')},
            },
        ),
    ]