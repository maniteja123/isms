from rest_framework import serializers
from alertcollector.models import Alertgenerator,Alertgroup,Alertclass

class GeneratorSerializer(serializers.ModelSerializer):
    
    class Meta:
	model = Alertgenerator
	fields = ("alert_gen_id","alert_gen_name","alert_gen_author","deleted","alert_gen_ip","alert_gen_key") 

class GroupSerializer(serializers.ModelSerializer):

    class Meta:
	model = Alertgroup
	fields = ("alert_group_id","alert_group_name","alert_group_description","alert_gen","deleted")

class ClassSerializer(serializers.ModelSerializer):
	
    class Meta:
	model = Alertclass
	fields= ("alert_class_id","alert_class_name","alert_class_description","alert_class_help","alert_class_syntax","alert_class_filter_syntax","alert_class_parent","alert_group","is_operator","is_filter","deleted")
