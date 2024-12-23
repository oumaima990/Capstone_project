from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# Bayesian Knowledge Tracing Class
class BayesianKnowledgeTracing:
    def __init__(self, p_L0, p_T, p_G, p_S, lower_baseline=0.2, upper_baseline=0.9):
        self.p_know = p_L0  # Initial mastery probability
        self.p_T = p_T  # Learning rate
        self.p_G = p_G  # Guessing probability
        self.p_S = p_S  # Slipping probability
        self.lower_baseline = lower_baseline  # Lower threshold
        self.upper_baseline = upper_baseline  # Upper threshold
        self.last_updated = None  # Timestamp of the last update

    def update(self, correct):
      #Using the update function:
        if correct:
            p_correct = self.p_know * (1 - self.p_S) + (1 - self.p_know) * self.p_G
            posterior_mastery = (self.p_know * (1 - self.p_S)) / p_correct
            if self.p_know >= self.upper_baseline:
                self.p_know = posterior_mastery + 0.05 * self.p_T
            else:
                self.p_know = posterior_mastery + (1 - posterior_mastery) * self.p_T
        else:
            p_incorrect = self.p_know * self.p_S + (1 - self.p_know) * (1 - self.p_G)
            posterior_mastery = (self.p_know * self.p_S) / p_incorrect
            if self.p_know <= self.lower_baseline:
                self.p_know = posterior_mastery + 0.05 * self.p_T
            else:
                self.p_know = posterior_mastery + (1 - posterior_mastery) * self.p_T

        self.p_know = max(0, min(1, self.p_know))
        self.last_updated = datetime.now().isoformat()
        return self.p_know


# Defining the Student Class
class Student:
    def __init__(self, p_L0, learning_rate):
        self.bkt_model = BayesianKnowledgeTracing(
            p_L0=p_L0, p_T=learning_rate, p_G=0.2, p_S=0.1
        )

    def generate_response(self):

        return np.random.rand() < self.bkt_model.p_know 

    def adapt_and_update_knowledge(self, correct):
        return self.bkt_model.update(correct)


# Define synthetic students
students = {
    "Fast Learner": Student(p_L0=0.1, learning_rate=0.8),
    "Intermediate Learner": Student(p_L0=0.1, learning_rate=0.6),
    "Slow Learner": Student(p_L0=0.1, learning_rate=0.4),
}

# Simulate learning
num_interactions = 50

simulation_results = []
for student_name, student in students.items():
    for interaction in range(1, num_interactions + 1):
        correct_response = student.generate_response()
        updated_knowledge = student.adapt_and_update_knowledge(correct=correct_response)
        simulation_results.append({
            "Student": student_name,
            "Interaction": interaction,
            "Correct Response": int(correct_response),
            "Updated Knowledge Probability": updated_knowledge
        })

# Convert results into a DataFrame
simulation_df = pd.DataFrame(simulation_results)

# Save results to a CSV file
simulation_df.to_csv("student_simulation_results.csv", index=False)

# Preview the first few rows
print(simulation_df.head())

# Visualization
plt.figure(figsize=(10, 6))
for student_name in students.keys():
    student_data = simulation_df[simulation_df["Student"] == student_name]
    plt.plot(student_data["Interaction"], student_data["Updated Knowledge Probability"], label=student_name)

plt.xlabel("Interaction")
plt.ylabel("Knowledge Probability")
plt.title("Knowledge Progression Over Interactions (Based on Learning Rate)")
plt.legend()
plt.show()
