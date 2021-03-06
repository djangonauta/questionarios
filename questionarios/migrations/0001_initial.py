# Generated by Django 2.2.1 on 2019-05-31 11:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AlternativaQuestao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('titulo', models.CharField(max_length=255)),
                ('descricao', models.TextField(blank=True)),
                ('tipo_alternativa', models.IntegerField(choices=[(1, 'Padrão'), (2, 'Texto'), (3, 'Múltipla Escolha')], default=1)),
                ('resposta', models.TextField(blank=True)),
                ('alternativa', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='alternativas', to='questionarios.AlternativaQuestao')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Questao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('tipo_questao', models.IntegerField(choices=[(1, 'Texto Livre'), (2, 'Única Escolha'), (3, 'Múltipla Escolha'), (4, 'Avaliação')])),
                ('titulo', models.CharField(max_length=255)),
                ('descricao', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Questionario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('titulo', models.CharField(max_length=255)),
                ('descricao', models.TextField()),
                ('inicio', models.DateTimeField()),
                ('fim', models.DateTimeField(null=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='UsuarioQuestionario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('submetido', models.BooleanField()),
                ('questionario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usuarios_questionarios', to='questionarios.Questionario')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usuarios_questionarios', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('usuario', 'questionario')},
            },
        ),
        migrations.CreateModel(
            name='RespostaQuestao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('resposta', models.TextField(blank=True)),
                ('alternativa_selecionada', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='resposta_questao_selecionada', to='questionarios.AlternativaQuestao')),
                ('alternativas_selecionadas', models.ManyToManyField(blank=True, related_name='respostas_questoes_selecionadas', to='questionarios.AlternativaQuestao')),
                ('questao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='respostas_questao', to='questionarios.Questao')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='respostas_questao', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('questao', 'usuario')},
            },
        ),
        migrations.AddField(
            model_name='questionario',
            name='usuarios',
            field=models.ManyToManyField(blank=True, related_name='questionarios', through='questionarios.UsuarioQuestionario', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='questao',
            name='questionario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questoes', to='questionarios.Questionario'),
        ),
        migrations.AddField(
            model_name='questao',
            name='usuarios',
            field=models.ManyToManyField(related_name='questoes', through='questionarios.RespostaQuestao', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='alternativaquestao',
            name='questao',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='alternativas', to='questionarios.Questao'),
        ),
    ]
