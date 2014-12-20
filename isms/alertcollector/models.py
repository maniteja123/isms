from django.db import models

# Create your models here.

class Alertgenerator(models.Model):
    alert_gen_id = models.AutoField(primary_key=True)
    alert_gen_name = models.CharField(max_length=100, blank=True)
    alert_gen_author = models.CharField(max_length=100, blank=True, null=True)
    deleted = models.NullBooleanField()
    alert_gen_ip = models.IPAddressField()
    alert_gen_key = models.IntegerField()

    class Meta:
	db_table = 'alertgenerator'

    def __unicode__(self):
	return self.alert_gen_name


class Alertgroup(models.Model):
    alert_group_id = models.AutoField(primary_key=True)
    alert_group_name = models.CharField(max_length=100,blank=True)
    alert_group_description = models.CharField(max_length=500, blank=True)
    alert_gen = models.ForeignKey('Alertgenerator',blank=True, null=True)
    deleted = models.NullBooleanField()

    class Meta:
        db_table = 'alertgroup'

    def __unicode__(self):
	return self.alert_group_name

class Alertclass(models.Model):
    alert_class_id = models.AutoField(primary_key=True)
    alert_class_reg_time = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    alert_class_name = models.CharField(max_length=500, blank=True)
    alert_class_description = models.CharField(max_length=500, blank=True)
    alert_class_help = models.CharField(max_length=500, blank=True)
    alert_class_syntax = models.CharField(max_length=500, blank=True)
    alert_class_filter_syntax = models.CharField(max_length=500, blank=True)
    alert_class_parent = models.CharField(max_length=500, blank=True)
    alert_group = models.ForeignKey('Alertgroup', blank=True, null=True)
    is_operator = models.NullBooleanField()
    is_filter = models.NullBooleanField()
    deleted = models.NullBooleanField()

    class Meta:
        db_table = 'alertclass'
   
    def __unicode__(self):
	return self.alert_class_name
