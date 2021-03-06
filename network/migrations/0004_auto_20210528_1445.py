# Generated by Django 3.0.3 on 2021-05-28 14:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_post_n_likes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post_likes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('post_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='network.Post')),
            ],
        ),
        migrations.RenameModel(
            old_name='following',
            new_name='Follower',
        ),
        migrations.RenameField(
            model_name='follower',
            old_name='followed_id',
            new_name='follower_id',
        ),
        migrations.DeleteModel(
            name='Followers',
        ),
    ]
