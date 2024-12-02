from rest_framework.routers import DefaultRouter
from .views import     KnowledgeNodeViewSet, KnowledgeComponentViewSet,GlossaryViewSet,QuestionViewSet,DependencyViewSet, TextViewSet, UnitViewSet,UnitProgressViewSet,GradeViewSet, QuizViewSet,QuizAttemptViewSet


router = DefaultRouter()

# Register all ViewSets
router.register(r'nodes', KnowledgeNodeViewSet, basename='node')
router.register(r'text', TextViewSet, basename='text')
router.register(r'questions', QuestionViewSet, basename='question')
router.register(r'knowledge-components', KnowledgeComponentViewSet)
router.register(r'Dependency',DependencyViewSet)
router.register(r'glossary', GlossaryViewSet, basename='glossary')
router.register(r'grade', GradeViewSet, basename='grade')
router.register(r'unit', UnitViewSet, basename='unit')
router.register(r'unitprogress', UnitProgressViewSet, basename='unitprogress')
router.register(r'quiz', QuizViewSet, basename='quiz')
router.register(r'quizattempt', QuizAttemptViewSet, basename='quizattempt')

urlpatterns = router.urls
