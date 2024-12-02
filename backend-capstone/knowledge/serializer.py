from rest_framework import serializers
from .models import KnowledgeNode, KnowledgeComponent, Glossary, Question,Dependency,Text,UnitProgress,Unit,Grade,QuizAttempt,QuizResponse

class KnowledgeNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = KnowledgeNode
        fields = '__all__'


class KnowledgeComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = KnowledgeComponent
        fields = '__all__'


class GlossarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Glossary
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

        
class DependencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Dependency
        fields = '__all__'


        
class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = '__all__'

class WordMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dependency
        fields = '__all__'

class UnitProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitProgress
        fields = '__all__'

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = '__all__'
class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'

from rest_framework import serializers

class QuizAttemptSerializer(serializers.ModelSerializer):
    grade = serializers.CharField(source='unit.grade.name')  # Fetch the grade name from the related Unit model

    class Meta:
        model = QuizAttempt
        fields = ['id', 'unit', 'grade', 'score', 'passed', 'attempt_date']