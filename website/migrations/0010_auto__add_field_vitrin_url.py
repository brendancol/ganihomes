# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Vitrin.url'
        db.add_column('website_vitrin', 'url', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Vitrin.url'
        db.delete_column('website_vitrin', 'url')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'places.photo': {
            'Meta': {'ordering': "['timestamp']", 'object_name': 'Photo'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['places.Place']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'places.place': {
            'Meta': {'ordering': "['timestamp']", 'object_name': 'Place'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'bathrooms': ('django.db.models.fields.SmallIntegerField', [], {}),
            'bed_type': ('django.db.models.fields.SmallIntegerField', [], {}),
            'bedroom': ('django.db.models.fields.SmallIntegerField', [], {}),
            'cancellation': ('django.db.models.fields.SmallIntegerField', [], {}),
            'capacity': ('django.db.models.fields.SmallIntegerField', [], {}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'clean_rating': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'cleaning_fee': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            'comfort_rating': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'district': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'emergency_phone': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'extra_limit': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'extra_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '2', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'location_rating': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'manual': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'max_stay': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'min_stay': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'monthly_discount': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'overall_rating': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'pets': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'rules': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'size': ('django.db.models.fields.IntegerField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'space': ('django.db.models.fields.SmallIntegerField', [], {}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'street_view': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['places.Tag']", 'null': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'type': ('django.db.models.fields.SmallIntegerField', [], {}),
            'value_money_rating': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'weekly_discount': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'places.tag': {
            'Meta': {'ordering': "['timestamp']", 'object_name': 'Tag'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['places.TagCategory']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'places.tagcategory': {
            'Meta': {'ordering': "['timestamp']", 'object_name': 'TagCategory'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'website.ceviriler': {
            'Meta': {'ordering': "['timestamp']", 'object_name': 'Ceviriler'},
            'asil': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'ceviri': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kelime': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Kelime']"}),
            'kod': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'website.haber': {
            'Meta': {'ordering': "['-sabit', '-pul']", 'object_name': 'Haber'},
            'anahtar_kelime': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'baslik': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'dil_kodu': ('django.db.models.fields.CharField', [], {'max_length': '5', 'db_index': 'True'}),
            'etkin': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'icerik': ('tinymce.models.HTMLField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'medya': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['website.Medya']", 'null': 'True', 'blank': 'True'}),
            'pul': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'sabit': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'son_guncelleme': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'tanim': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'website.icerik': {
            'Meta': {'unique_together': "(('dil_kodu', 'sayfa'),)", 'object_name': 'Icerik'},
            'anahtar': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'baslik': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'dil_kodu': ('django.db.models.fields.CharField', [], {'max_length': '5', 'db_index': 'True'}),
            'guncelleme': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'html_baslik': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'menu_baslik': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'metin': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'olusturma': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'sayfa': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Sayfa']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'db_index': 'True'}),
            'tanim': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'website.kelime': {
            'Meta': {'ordering': "['timestamp']", 'object_name': 'Kelime'},
            'durum': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kelime': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'website.medya': {
            'Meta': {'object_name': 'Medya'},
            'ad': ('django.db.models.fields.CharField', [], {'max_length': '185'}),
            'dil_kodu': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'dosya': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'etkin': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pul': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'sablon': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'tip': ('django.db.models.fields.SmallIntegerField', [], {'db_index': 'True'})
        },
        'website.sayfa': {
            'Meta': {'object_name': 'Sayfa'},
            'etkin': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'medya': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['website.Medya']", 'null': 'True', 'blank': 'True'}),
            'menude': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['website.Sayfa']"}),
            'pul': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'sablon': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'sadece_uyeler': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'website.vitrin': {
            'Meta': {'ordering': "['sira']", 'object_name': 'Vitrin'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'dil_kodu': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'gorsel': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['places.Place']", 'null': 'True', 'blank': 'True'}),
            'place_photo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['places.Photo']", 'null': 'True', 'blank': 'True'}),
            'pul': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'sira': ('django.db.models.fields.SmallIntegerField', [], {'db_index': 'True'}),
            'tops': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'type': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['website']
