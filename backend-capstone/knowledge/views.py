from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render
from .models import KnowledgeComponent, KnowledgeNode,Glossary,Question, Student, Dependency,Glossary, Text, WordMapping,Grade,Unit,UnitProgress,QuizResponse,QuizAttempt
from .serializer import GlossarySerializer,QuestionSerializer, KnowledgeComponentSerializer, KnowledgeNodeSerializer, DependencySerializer, WordMappingSerializer, TextSerializer,UnitProgressSerializer,UnitSerializer,GradeSerializer
from rest_framework import viewsets
from rest_framework import status, viewsets
from knowledge.models import KnowledgeComponent
from django.utils.timezone import now
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import F
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
import random

# nodes views
class KnowledgeNodeViewSet(viewsets.ModelViewSet):
    queryset = KnowledgeNode.objects.all()
    serializer_class = KnowledgeNodeSerializer

#knowledge views
class KnowledgeComponentViewSet(viewsets.ModelViewSet):
    queryset = KnowledgeComponent.objects.all()
    serializer_class = KnowledgeComponentSerializer
    def update_dependencies_for_knowledge_component(self, main_kc, is_correct):
        
        dependencies = Dependency.objects.filter(main_node=main_kc.node)
        updated_dependencies = []

        for dependency in dependencies:
            # Fetch the dependent KnowledgeComponent for the same student
            dependent_kc = KnowledgeComponent.objects.filter(
                student=main_kc.student,
                node=dependency.dependent_node
            ).first()

            if dependent_kc:
                influence_prob = dependency.influence_probability
                old_p_know = dependent_kc.p_know

                # Apply positive or negative influence
                if is_correct and dependent_kc.p_know < dependent_kc.node.baseline:

                    dependent_kc.p_know += influence_prob * (1 - dependent_kc.p_know)

                elif not is_correct:
                    
                    dependent_kc.p_know -= influence_prob * dependent_kc.p_know

                # Ensure `p_know` remains within bounds [0, 1]
                dependent_kc.p_know = max(0.0, min(dependent_kc.p_know, 1.0))
                dependent_kc.save()

                # Append updated dependency details to the response list
                updated_dependencies.append({
                    "dependent_node": dependent_kc.node.name,
                    "old_p_know": round(old_p_know, 4),
                    "updated_p_know": round(dependent_kc.p_know, 4),
                })
            else:
                updated_dependencies.append({
                    "dependent_node": dependency.dependent_node.name,
                    "error": f"Dependent KnowledgeComponent not found for student ID {main_kc.student.id}."
                })

        return updated_dependencies

    def calculate_probability(self, knowledge_component, node, is_correct):
        if is_correct:
            p_correct = (
                knowledge_component.p_know * (1 - node.p_S) +
                (1 - knowledge_component.p_know) * node.p_G
            )
            posterior_mastery = (
                (knowledge_component.p_know * (1 - node.p_S)) / p_correct
            )
            if knowledge_component.p_know >= 0.9:#if the knowledge proability is beyond or equals 0.8
                knowledge_component.p_know = (
                posterior_mastery + 0.05 * node.p_T  # Slower update
            ) 
            else:
                knowledge_component.p_know = (posterior_mastery + (1 - posterior_mastery) * node.p_T)
        else:
            p_incorrect = (knowledge_component.p_know * node.p_S +(1 - knowledge_component.p_know) * (1 - node.p_G))
            posterior_mastery = ((knowledge_component.p_know * node.p_S) / p_incorrect)

            if knowledge_component.p_know <= 0.2: #if the knowledge proability os bellow or equals 0.2
                knowledge_component.p_know = (posterior_mastery + 0.05 * node.p_T ) # Slower update
            else:
                knowledge_component.p_know = (posterior_mastery + (1 - posterior_mastery) * node.p_T)
        knowledge_component.p_know = max(0.0, min(knowledge_component.p_know, 1.0))
        return knowledge_component.p_know    
    
    @action(detail=False, methods=['post'])
    def update_probability(self, request):
        """
        Validate the user's answer and update the knowledge component.
        """
        try:
            # Extract required data from the request
            question_id = request.data.get("question_id")
            student_id = request.data.get("student_id")
            user_answer = request.data.get("answer")

            # Ensure required fields are provided
            if not all([question_id, student_id, user_answer]):
                return Response(
                    {"error": "Missing required fields (question_id, student_id, answer)."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Fetch the question
            question = get_object_or_404(Question, id=question_id)

            # Fetch the related KnowledgeNode dynamically by name
            node = KnowledgeNode.objects.filter(name=question.node).first()
            if not node:
                return Response(
                    {"error": f"KnowledgeNode with name '{question.node}' not found."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Validate the answer
            is_correct = question.answer.strip().lower() == user_answer.strip().lower()

            # Fetch the KnowledgeComponent for the node and student
            student = get_object_or_404(Student, user__id=student_id)
            knowledge_component = KnowledgeComponent.objects.filter(node=node, student=student).first()

            if not knowledge_component:
                return Response(
                    {"error": "KnowledgeComponent not found for the specified node and student."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Update the main KnowledgeComponent probability
            knowledge_component.p_know = self.calculate_probability(knowledge_component, node, is_correct)
            knowledge_component.last_updated = timezone.now()
            knowledge_component.save()

            # Update dependencies of the main KnowledgeComponent
            updated_dependencies = self.update_dependencies_for_knowledge_component(knowledge_component, is_correct)

            # Return response
            return Response({
                "is_correct": is_correct,
                "main_knowledge_component": {
                    "node_name": node.name,
                    "student_name": student.user.username,
                    "p_know": knowledge_component.p_know,
                    "last_updated": knowledge_component.last_updated,
                },
                "updated_dependencies": updated_dependencies
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def search_gloss(self,word):
        try:
            # Find the KnowledgeNode associated with the word
            node = KnowledgeNode.objects.filter(name__icontains=word).first()
            if not node:
                return {
                    "error": f"The word '{word}' is not found in any KnowledgeNode."
                }

            # Check if a Glossary entry exists for the node
            glossary = Glossary.objects.filter(node=node).first()
            if glossary:
                return {
                    "gloss": glossary.gloss,
                    "definition": glossary.definition,                   
                    "Sentence":glossary.Sentence,
                    "node":glossary.node,                    
                }
            else:
                return {
                    "error": f"No glossary available for the word '{word}' associated with node '{node.name}'."
                }

        except Exception as e:
            return {"error": str(e)}
    #handle clicks:

    @action(detail=False, methods=['post'])
    def handle_click(self, request):
        """
        Handle a click event for a specific word with rules based on the unit context.
        """
        try:
            # Parse input data
            text_id = request.data.get("text_id")
            surface_form = request.data.get("word")
            student_id = request.data.get("student_id")

            # Validate input data
            if not all([text_id, surface_form, student_id]):
                return Response({"error": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)

            # Retrieve the relevant text, unit, and grade
            text = Text.objects.get(id=text_id)
            current_testing_grade = text.grade
            current_testing_unit = text.unit

            # Retrieve word mapping and lemma
            word_mapping = WordMapping.objects.get(surface_form=surface_form)
            lemma = word_mapping.lemma

            # Fetch the knowledge components linked to the student
            knowledge_components = KnowledgeComponent.objects.select_related('node').filter(student__user__id=student_id)
            word_found = False

            for kc in knowledge_components:
                if lemma in kc.node.name:  # Match lemma with node name
                    word_found = True

                    # Increment click count and update last modified timestamp
                    kc.click_count = F('click_count') + 1
                    kc.last_updated = now()
                    kc.save()
                    kc.refresh_from_db()

                    # Determine the context of the click (current, future, or past unit)
                    is_tested_now = kc.node.grade == current_testing_grade and kc.node.unit == current_testing_unit
                    is_tested_future = kc.node.grade > current_testing_grade or (
                        kc.node.unit > current_testing_unit and kc.node.grade == current_testing_grade)
                    is_tested_past = kc.node.grade < current_testing_grade or (
                        kc.node.unit < current_testing_unit and kc.node.grade == current_testing_grade)

                    # General Rule: Show glossary for the first three clicks
                    if kc.click_count <= 3:
                        gloss_data = self.search_gloss(lemma)  # Retrieve glossary details
                        if gloss_data:
                            return Response({
                                "action": "show_glossary",
                                "word": lemma,
                                "glossary": {
                                    "node": gloss_data.get("node"),
                                    "sentence": gloss_data.get("sentence"),
                                    "gloss": gloss_data.get("gloss"),
                                    "definition": gloss_data.get("definition"),
                                }
                            }, status=status.HTTP_200_OK)

                    # Future Unit: Apply a positive update and show glossary
                    if is_tested_future:
                        kc.p_know = min(1.0, kc.p_know + 0.10)  # Positive knowledge update
                        kc.save()
                        return Response({
                            "action": "show_glossary",
                            "message": "Positive update applied for future unit.",
                            "word": lemma
                        }, status=status.HTTP_200_OK)

                    # Past Unit: Apply decay or present a question based on click count
                    if is_tested_past:
                        if kc.click_count > 3:
                            kc.click_count = 0  # Reset click count
                            kc.save()
                            question = Question.objects.filter(node=kc.node.name).order_by('?').first()
                            if question:
                                return Response({
                                    "action": "ask_question",
                                    "question_id": question.id,
                                    "question_text": question.question,
                                    "type": question.type,
                                    "options": question.options if question.type == "multiple_choice" else None,
                                    "answer": question.answer  # Include answer if needed f
                                }, status=status.HTTP_200_OK)
                        else:
                            kc.p_know = max(0.0, kc.p_know - 0.05)  # Apply decay
                            kc.save()
                            return Response({
                                "action": "apply_decay",
                                "message": "Decay applied for past unit.",
                                "word": lemma
                            }, status=status.HTTP_200_OK)

                    # Current Unit: Ask a question if clicks exceed 3
                    if is_tested_now and kc.click_count > 3:
                        kc.click_count = 0  # Reset click count
                        kc.save()
                        question = Question.objects.filter(node=kc.node.name).order_by('?').first()
                        if question:
                            return Response({
                                "action": "ask_question",
                                "question_id": question.id,
                                "question_text": question.question,
                                "type": question.type,
                                "options": question.options if question.type == "multiple_choice" else None,
                                "answer": question.answer  # Include answer if needed f
                            }, status=status.HTTP_200_OK)

            # If the word is not found in the current knowledge components, show glossary
            if not word_found:
                gloss_data = self.search_gloss(lemma)
                if gloss_data:
                    return Response({
                        "action": "show_glossary",
                        "word": lemma,
                        "message": "Word not found in the current curriculum."
                    }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=["post"], url_path="submit-quiz")
    def submit_quiz(self, request):
        student_id = request.data.get("student_id")
        grade_order = request.data.get("grade_order")
        unit_order = request.data.get("unit_order")
        responses = request.data.get("responses", [])

        if not all([student_id, grade_order, unit_order, responses]):
            return Response(
                {"error": "Student ID, Grade Order, Unit Order, and responses are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Fetch the student
            student = get_object_or_404(Student, user__id=student_id)
            print(student)
            print(student.user.id)
            # Fetch the grade and unit using the provided orders
            grade = get_object_or_404(Grade, order=grade_order)
            unit = get_object_or_404(Unit, grade=grade, order=unit_order)

            # Generate a unique identifier for the unit
            unique_unit_identifier = f"Grade-{grade.order}-Unit-{unit.order}"
            print(f"Unique Unit Identifier: {unique_unit_identifier}")

            correct_count = 0
            total_questions = len(responses)
            correct_answers = {}

            for response in responses:
                question_id = response.get("question_id")
                student_answer = response.get("student_answer")

                question = get_object_or_404(Question, id=question_id)
                is_correct = question.answer.strip().lower() == student_answer.strip().lower()

                if is_correct:
                    correct_count += 1

                correct_answers[question.id] = {
                    "correct_answer": question.answer,
                    "is_correct": is_correct,
                }

                # Call the function to update probabilities
                self.update_probability_logic(question, student, is_correct)

            # Calculate percentage score
            score = (correct_count / total_questions) * 100
            passed = score >= 70.0  # Set 70% as the passing score

            # Create QuizAttempt record
            quiz_attempt = QuizAttempt.objects.create(
                student=student,
                unit=unit,
                score=score,
                passed=passed,
            )

            # Create QuizResponse records
            for response in responses:
                question_id = response.get("question_id")
                student_answer = response.get("student_answer")
                question = get_object_or_404(Question, id=question_id)
                is_correct = question.answer.strip().lower() == student_answer.strip().lower()

                QuizResponse.objects.create(
                    quiz_attempt=quiz_attempt,
                    question=question,
                    student_answer=student_answer,
                    is_correct=is_correct,
                )

            # Unlock the next unit if the student passed the quiz
            if passed:
                next_unit_unlocked = False

                # Check if there is a next unit in the current grade
                next_unit = Unit.objects.filter(grade=grade, order=unit.order + 1).first()
                if next_unit:
                    # Unlock the next unit in the same grade
                    UnitProgress.objects.update_or_create(
                        student=student,
                        unit=next_unit,
                        defaults={"unlocked": True},
                    )
                    next_unit_unlocked = True
                    next_unit_identifier = f"Grade-{grade.order}-Unit-{next_unit.order}"

                # If no next unit in the current grade, unlock the first unit of the next grade
                if not next_unit_unlocked:
                    next_grade = Grade.objects.filter(order=grade.order + 1).first()
                    if next_grade:
                        first_unit_next_grade = Unit.objects.filter(grade=next_grade).order_by("order").first()
                        if first_unit_next_grade:
                            UnitProgress.objects.update_or_create(
                                student=student,
                                unit=first_unit_next_grade,
                                defaults={"unlocked": True},
                            )
                            next_unit_identifier = f"Grade-{next_grade.order}-Unit-{first_unit_next_grade.order}"
                        else:
                            next_unit_identifier = "None (No units in next grade)"
                    else:
                        next_unit_identifier = "None (No next grade available)"

                # Include next unit info in the response
                return Response(
                    {
                        "success": True,
                        "score": score,
                        "passed": passed,
                        "correct_answers": correct_answers,
                        "grade_order": grade_order,
                        "unit_order": unit_order,
                        "next_unit_unlocked": next_unit_identifier,
                    },
                    status=status.HTTP_200_OK,
                )

            # If quiz not passed, no unlocking happens
            return Response(
                {
                    "success": True,
                    "score": score,
                    "passed": passed,
                    "correct_answers": correct_answers,
                    "grade_order": grade_order,
                    "unit_order": unit_order,
                    "next_unit_unlocked": "None (Quiz not passed)",
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update_probability_logic(self, question, student, is_correct):
        """
        Logic for updating knowledge probabilities based on correctness of the answer.
        """
        try:
            # Fetch the related KnowledgeNode dynamically by name
            node = KnowledgeNode.objects.filter(name=question.node).first()
            if not node:
                raise Exception(f"KnowledgeNode with name '{question.node}' not found.")

            # Fetch the KnowledgeComponent for the node and student
            knowledge_component = KnowledgeComponent.objects.filter(node=node, student=student).first()

            if not knowledge_component:
                raise Exception("KnowledgeComponent not found for the specified node and student.")

            # Update the main KnowledgeComponent probability
            knowledge_component.p_know = self.calculate_probability(knowledge_component, node, is_correct)
            knowledge_component.last_updated = timezone.now()
            knowledge_component.save()

            # Update dependencies of the main KnowledgeComponent
            self.update_dependencies_for_knowledge_component(knowledge_component, is_correct)

        except Exception as e:
            print(f"Error in updating probabilities: {str(e)}")

        
class DependencyViewSet(viewsets.ModelViewSet):
    queryset = Dependency.objects.all()
    serializer_class = DependencySerializer
  
#question views 
class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    
#glossary views
class GlossaryViewSet(viewsets.ModelViewSet):
    queryset = Glossary.objects.all()
    serializer_class = GlossarySerializer

class WordMappingViewSet(viewsets.ModelViewSet):
    queryset = WordMapping.objects.all()
    serializer_class = WordMappingSerializer

class TextViewSet(viewsets.ModelViewSet):
    queryset = Text.objects.all()
    serializer_class = TextSerializer
    def get(self, request, unit,grade):
        texts = Text.objects.filter(unit=unit, grade= grade).values("id", "title", "grade", "unit")
        return Response(list(texts), status=status.HTTP_200_OK)
       
    @action(detail=False, methods=['get'], url_path='get-texts')
    def get_texts(self, request):
        # Retrieve query parameters from the request
        grade = request.query_params.get('grade')
        unit = request.query_params.get('unit')

        if not grade or not unit:
            return Response({"error": "Both 'grade' and 'unit' query parameters are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Filter texts based on grade and unit
        texts = Text.objects.filter(grade=grade, unit=unit).values("id", "title", "grade", "unit")

        return Response(list(texts), status=status.HTTP_200_OK)
    @action(detail=False, methods=['get'], url_path='get_text_by_id')
    def get_text_by_id(self, request):
        # Retrieve query parameters from the request
        id = request.query_params.get('id')
        if not id:
            return Response({"error": "Both 'grade' and 'unit' query parameters are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Filter texts based on grade and unit
        texts = Text.objects.filter(id=id).values("id", "title", "grade", "unit","content","image")

        return Response(list(texts), status=status.HTTP_200_OK)
    
    
    #gradeViewset
class UnitProgressViewSet(viewsets.ModelViewSet):
    queryset = UnitProgress.objects.all()
    serializer_class = UnitProgressSerializer

    #progressViewset
class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    
#unit viewset
@action(detail=False, methods=['post'])
class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer   
    @action(detail=False, methods=["get"])
    def get_units_by_grade(request, student_id, grade_id):
        try:
            units = Unit.objects.filter(grade_id=grade_id).order_by("order")
            progress = UnitProgress.objects.filter(student_id=student_id, unit__grade_id=grade_id)

            units_with_status = [
                {
                    "id": unit.id,
                    "title": unit.title,
                    "unlocked": progress.filter(unit=unit).first().unlocked if progress.filter(unit=unit).exists() else False,
                }
                for unit in units
            ]
            return Response(units_with_status, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    @action(detail=False, methods=["get"])
    def student_progress(self, request):
        # Get the student ID from query params or session
        student_id = request.query_params.get("student_id")
        if not student_id:
            return Response({"error": "Missing student_id parameter."}, status=400)

        student = get_object_or_404(Student, user__id=student_id)

        # Query the UnitProgress table for the student using the student object
        progress_records = UnitProgress.objects.filter(student=student).select_related("unit", "unit__grade")
        # Serialize the progress records
        data = [
            {
                "unit_name": progress.unit.title,
                "grade_name": progress.unit.grade.name,
                "grade":progress.unit.grade.order,
                "unit":progress.unit.order,
                "unlocked": progress.unlocked,
            }
            for progress in progress_records
        ]
        return Response(data, status=200)
    
from random import sample
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

class QuizViewSet(viewsets.ViewSet):
    @action(detail=False, methods=["get"], url_path="generate-quiz")
    def generate_quiz(self, request):
        grade = request.query_params.get("grade")
        unit = request.query_params.get("unit")
        num_questions = int(request.query_params.get("num_questions", 5))  # Default to 5 questions

        if not grade or not unit:
            return Response({"error": "Grade and Unit are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Fetch the KnowledgeNode names for the given grade and unit
            node_names = KnowledgeNode.objects.filter(grade=grade, unit=unit).values_list("name", flat=True)

            # Filter questions that match these nodes
            questions = Question.objects.filter(node__in=node_names)

            if questions.count() < num_questions:
                num_questions = questions.count()

            selected_questions = sample(list(questions), num_questions)

            # Prepare response data
            data = [
                {
                    "id": question.id,
                    "question": question.question,
                    "type": question.type,
                    "options": question.options if question.type == "multiple_choice" else None,
                    "answer": question.answer  # Include answer if needed for debugging or validation
                }
                for question in selected_questions
            ]

            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

   
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import QuizAttempt
from .serializer import QuizAttemptSerializer

from rest_framework.exceptions import PermissionDenied

class QuizAttemptViewSet(viewsets.ModelViewSet):
    queryset = QuizAttempt.objects.all()
    serializer_class = QuizAttemptSerializer

    @action(detail=False, methods=['get'])
    def past_attempts(self, request):
        # Retrieve student_id from query parameters
        student_id = request.query_params.get('student_id')
        
        if not student_id:
            return Response(
                {"error": "student_id query parameter is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Fetch attempts for the given student_id without authentication verification
        attempts = QuizAttempt.objects.filter(student__user__id=student_id).order_by('-attempt_date')
        serializer = self.get_serializer(attempts, many=True)
        return Response(serializer.data)
    @action(detail=False, methods=["get"], url_path="get_student_progress_info")
    def get_student_progress_info(self, request):
        # Get the student ID from the query parameters
        student_user_id = request.query_params.get("student_id")
        
        if not student_user_id:
            return Response({"error": "Missing student_id parameter."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Fetch the student object based on the student_user_id
        student = get_object_or_404(Student, user__id=student_user_id)

        # Fetch the quiz attempts and unit progress for the student
        quiz_attempts = QuizAttempt.objects.filter(student=student)
        unit_progress = UnitProgress.objects.filter(student=student)

        # Organize the data to send in the response
        progress_data = []
        
        for attempt in quiz_attempts:
            progress_data.append({
                "unit": attempt.unit.order,
                "grade": attempt.unit.grade.order,
                "score": attempt.score,
                "passed": attempt.passed,
                "attempt_date": attempt.attempt_date
            })

        for progress in unit_progress:
            progress_data.append({
                "unit": progress.unit.order,
                "unlocked": progress.unlocked,
            })

        return Response(progress_data, status=status.HTTP_200_OK)