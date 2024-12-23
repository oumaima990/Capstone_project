
import numpy as np
import random
from datetime import datetime
from search_gloss import search_gloss
#The class taht defines the baysian model nodes attributes as follow:
class BayesianKnowledgeTracing:
    def __init__(self, p_L0, p_T, p_G, p_S, baseline):
       
        self.p_L0 = p_L0     # Initial probability the student knows the KC
        self.p_T = p_T       # Transition probability
        self.p_G = p_G       # Guessing probability
        self.p_S = p_S       # Slipping probability
        self.p_know = p_L0   # Current probability the student knows the KC : Changes overtime to indicate the student knwoledge
        self.baseline = baseline  # Baseline threshold that is set once reached the update is either slower or stopped 
    def update(self, correct):
        """
          Update the knowledge probability based on whether the answer was correct or not.
        """
        #if the answer is correct then the update is as follow :
        if correct:
            # Probability of observing a correct response
            p_correct = self.p_know * (1 - self.p_S) + (1 - self.p_know) * self.p_G

            # Posterior probability of mastery given a correct response
            posterior_mastery = (self.p_know * (1 - self.p_S)) / p_correct
            # Apply transition probability increment if below baseline
            if self.p_know < self.baseline: 
                self.p_know =  posterior_mastery + (1-posterior_mastery)*self.p_T
            else:
                # Slow down updates once baseline is reached 
                self.p_know =  posterior_mastery + 0.1 * self.p_T
        else:
            # Probability of qfter qn incorrect response
            p_incorrect = self.p_know * self.p_S + (1 - self.p_know) * (1 - self.p_G)
            # Posterior probability of mastery given an incorrect response
            posterior_mastery = (self.p_know * self.p_S) / p_incorrect
            #ensuring that the probability staus within bound of [0,1]
            self.p_know = posterior_mastery+((1-posterior_mastery))*self.p_T
         # Update last updated timestamp
        self.last_updated = datetime.now().isoformat()  # ISO 8601 timestamp
        print(f"Timestamp updated: {self.last_updated}")
        return self.p_know
            
#the knowledge coponents extracted from grade 1 and grade 2
knowledge_components = {
    "KC_Vocab_مدرسة": {
        "bkt": BayesianKnowledgeTracing(0.8, 0.6, 0.1, 0.1, baseline=0.9), #the node initialization
        "unit": 1, #teh unit it belongs to
        "grade": 1,#the grade it belongs to 
        "click_count":0, #how many clicks did the student click
        "last_updated":"None", #last seen and asked questions on
    },
    "KC_Feminine": {
        "bkt": BayesianKnowledgeTracing(0.8, 0.6, 0.1, 0.1, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count":0,
        "last_updated":"None",
    },
    "KC_Masculine": {
        "bkt": BayesianKnowledgeTracing( 0.75, 0.5, 0.2, 0.1, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count":0,
        "last_updated":"None",
    },
    
    "KC_Vocab_على": {
        "bkt": BayesianKnowledgeTracing(0.8, 0.6, 0.1, 0.1, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count":0,
        "last_updated":"None",
    },
    # ... Other Unit 1, Grade 1 entries ...
    "KC_Vocab_احتفل": {
        "bkt": BayesianKnowledgeTracing(0.8, 0.6, 0.1, 0.1, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count":0,
        "last_updated":"None",
    }, 
    "KC_Vocab_عام": {
        "bkt": BayesianKnowledgeTracing(0.8, 0.6, 0.1, 0.1, baseline=0.9),
        "unit": 2,
        "grade": 1,
        "click_count":0,
        "last_updated":"None",
    },
    
    # Unit 2, Grade 2
    "KC_Vocab_سما": {
        "bkt": BayesianKnowledgeTracing(0.2, 0.1, 0.4, 0.3, baseline=0.9),
        "unit": 2,
        "grade": 2,
        "click_count":0,
        "last_updated":"None",
    },
    "KC_Vocab_بيت": {
        "bkt": BayesianKnowledgeTracing(0.2, 0.1, 0.4, 0.3, baseline=0.9),
        "unit": 2,
        "grade": 2,
        "click_count":0,
        "last_updated":"None",
    },
    # ... Other Unit 2, Grade 2 entries ...
    "KC_Vocab_ولا": {
        "bkt": BayesianKnowledgeTracing(0.2, 0.1, 0.4, 0.3, baseline=0.9),
        "unit": 2,
        "grade": 2,
        "click_count":0,
        "last_updated":"None",
    },
    
    #grade 1 Unit 1:
    "KC_Vocab_كل": {
        "bkt": BayesianKnowledgeTracing(0.75, 0.5, 0.2, 0.1, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_بعيد": {
        "bkt": BayesianKnowledgeTracing(0.75, 0.5, 0.2, 0.1, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_ميلاد": {
        "bkt": BayesianKnowledgeTracing(0.75, 0.5, 0.2, 0.1, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_علق": {
        "bkt": BayesianKnowledgeTracing(0.75, 0.5, 0.2, 0.1, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_تمنى": {
        "bkt": BayesianKnowledgeTracing(0.75, 0.5, 0.2, 0.1, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_ما": {
        "bkt": BayesianKnowledgeTracing(0.75, 0.5, 0.2, 0.1, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_حل": {
        "bkt": BayesianKnowledgeTracing(0.75, 0.5, 0.2, 0.1, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_جديد": {
        "bkt": BayesianKnowledgeTracing(0.75, 0.5, 0.2, 0.1, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_حمل": {
        "bkt": BayesianKnowledgeTracing(0.75, 0.5, 0.2, 0.1, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_قال": {
        "bkt": BayesianKnowledgeTracing(0.75, 0.5, 0.2, 0.1, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_كان": {
        "bkt": BayesianKnowledgeTracing(0.75, 0.5, 0.2, 0.1, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_عذر": {
        "bkt": BayesianKnowledgeTracing(0.75, 0.5, 0.2, 0.1, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_ظرف": {
        "bkt": BayesianKnowledgeTracing(0.75, 0.5, 0.2, 0.1, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_زيارة": {
        "bkt": BayesianKnowledgeTracing(0.75, 0.5, 0.2, 0.1, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_جدة": {
        "bkt": BayesianKnowledgeTracing(0.75, 0.5, 0.2, 0.1, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_عمة": {
        "bkt": BayesianKnowledgeTracing(0.75, 0.5, 0.2, 0.1, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_مريض": {
        "bkt": BayesianKnowledgeTracing(0.75, 0.5, 0.2, 0.1, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_حديقة": {
        "bkt": BayesianKnowledgeTracing(0.75, 0.5, 0.2, 0.1, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_شجرة": {
        "bkt": BayesianKnowledgeTracing(0.75, 0.5, 0.2, 0.1, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_غرس": {
        "bkt": BayesianKnowledgeTracing(0.75, 0.5, 0.2, 0.1, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_شتلة": {
        "bkt": BayesianKnowledgeTracing(0.75, 0.5, 0.2, 0.1, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_نظم": {
        "bkt": BayesianKnowledgeTracing(0.75, 0.5, 0.2, 0.1, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_مسابقة": {
        "bkt": BayesianKnowledgeTracing(0.75, 0.5, 0.2, 0.1, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_كافأ": {
        "bkt": BayesianKnowledgeTracing(0.75, 0.5, 0.2, 0.1, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_هواية": {
        "bkt": BayesianKnowledgeTracing(0.75, 0.5, 0.2, 0.1, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_رسم": {
        "bkt": BayesianKnowledgeTracing(0.75, 0.5, 0.2, 0.1, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_لعب": {
        "bkt": BayesianKnowledgeTracing(0.75, 0.5, 0.2, 0.1, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_خصص": {
        "bkt": BayesianKnowledgeTracing(0.75, 0.5, 0.2, 0.1, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_عناية": {
        "bkt": BayesianKnowledgeTracing(0.75, 0.5, 0.2, 0.1, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_متعة": {
        "bkt": BayesianKnowledgeTracing(0.75, 0.5, 0.2, 0.1, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_ٱحتفل": {
        "bkt": BayesianKnowledgeTracing(0.5, 0.3, 0.4, 0.3, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_تصنع": {
        "bkt": BayesianKnowledgeTracing(0.5, 0.3, 0.4, 0.3, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_زينة": {
        "bkt": BayesianKnowledgeTracing(0.5, 0.3, 0.4, 0.3, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_هذا": {
        "bkt": BayesianKnowledgeTracing(0.5, 0.3, 0.4, 0.3, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_ل": {
        "bkt": BayesianKnowledgeTracing(0.5, 0.3, 0.4, 0.3, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_معلوم": {
        "bkt": BayesianKnowledgeTracing(0.5, 0.3, 0.4, 0.3, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_أهدى": {
        "bkt": BayesianKnowledgeTracing(0.5, 0.3, 0.4, 0.3, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_تقبل": {
        "bkt": BayesianKnowledgeTracing(0.5, 0.3, 0.4, 0.3, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_شاكر": {
        "bkt": BayesianKnowledgeTracing(0.5, 0.3, 0.4, 0.3, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_أخذ": {
        "bkt": BayesianKnowledgeTracing(0.5, 0.3, 0.4, 0.3, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_شكر": {
        "bkt": BayesianKnowledgeTracing(0.5, 0.3, 0.4, 0.3, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_لكن": {
        "bkt": BayesianKnowledgeTracing(0.5, 0.3, 0.4, 0.3, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_قرأ": {
        "bkt": BayesianKnowledgeTracing(0.5, 0.3, 0.4, 0.3, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_مشي": {
        "bkt": BayesianKnowledgeTracing(0.5, 0.3, 0.4, 0.3, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_ركبة": {
        "bkt": BayesianKnowledgeTracing(0.5, 0.3, 0.4, 0.3, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_أم": {
        "bkt": BayesianKnowledgeTracing(0.15, 0.2, 0.5, 0.4, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_فطيرة": {
        "bkt": BayesianKnowledgeTracing(0.15, 0.2, 0.5, 0.4, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_لذيذ": {
        "bkt": BayesianKnowledgeTracing(0.15, 0.2, 0.5, 0.4, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_أب": {
        "bkt": BayesianKnowledgeTracing(0.15, 0.2, 0.5, 0.4, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_في": {
        "bkt": BayesianKnowledgeTracing(0.15, 0.2, 0.5, 0.4, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_نحو": {
        "bkt": BayesianKnowledgeTracing(0.15, 0.2, 0.5, 0.4, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_بيت": {
        "bkt": BayesianKnowledgeTracing(0.15, 0.2, 0.5, 0.4, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_أن": {
        "bkt": BayesianKnowledgeTracing(0.15, 0.2, 0.5, 0.4, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_ٱشترى": {
        "bkt": BayesianKnowledgeTracing(0.15, 0.2, 0.5, 0.4, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_والد": {
        "bkt": BayesianKnowledgeTracing(0.15, 0.2, 0.5, 0.4, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_دراجة": {
        "bkt": BayesianKnowledgeTracing(0.15, 0.2, 0.5, 0.4, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_يوم": {
        "bkt": BayesianKnowledgeTracing(0.15, 0.2, 0.5, 0.4, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_ثوب": {
        "bkt": BayesianKnowledgeTracing(0.15, 0.2, 0.5, 0.4, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_أقبل": {
        "bkt": BayesianKnowledgeTracing(0.15, 0.2, 0.5, 0.4, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_أبي": {
        "bkt": BayesianKnowledgeTracing(0.15, 0.2, 0.5, 0.4, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_مسجل": {
        "bkt": BayesianKnowledgeTracing(0.15, 0.2, 0.5, 0.4, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_فتور": {
        "bkt": BayesianKnowledgeTracing(0.15, 0.2, 0.5, 0.4, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_أراد": {
        "bkt": BayesianKnowledgeTracing(0.15, 0.2, 0.5, 0.4, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_لدى": {
        "bkt": BayesianKnowledgeTracing(0.15, 0.2, 0.5, 0.4, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_إزاء": {
        "bkt": BayesianKnowledgeTracing(0.15, 0.2, 0.5, 0.4, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_عاد": {
        "bkt": BayesianKnowledgeTracing(0.15, 0.2, 0.5, 0.4, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_مساء": {
        "bkt": BayesianKnowledgeTracing(0.15, 0.2, 0.5, 0.4, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_وجد": {
        "bkt": BayesianKnowledgeTracing(0.15, 0.2, 0.5, 0.4, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_شذب": {
        "bkt": BayesianKnowledgeTracing(0.15, 0.2, 0.5, 0.4, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_تنزه": {
        "bkt": BayesianKnowledgeTracing(0.15, 0.2, 0.5, 0.4, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_متاعب": {
        "bkt": BayesianKnowledgeTracing(0.15, 0.2, 0.5, 0.4, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_أمن": {
        "bkt": BayesianKnowledgeTracing(0.15, 0.2, 0.5, 0.4, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
    "KC_Vocab_سلم": {
        "bkt": BayesianKnowledgeTracing(0.15, 0.2, 0.5, 0.4, baseline=0.9),
        "unit": 1,
        "grade": 1,
        "click_count": 0,
        "last_updated": "None",
    },
}
#Possible dependencies in wich each node effects skightlt the other 
dependencies = {
#these dependencies will remain thorught any text
    # vocabulary Components
    "KC_Vocabulary_Object": {"KC_Grammar_Case_Nominative": 0.15, "KC_Morphology_SoundPlural": 0.05},
    "KC_Vocabulary_Verb": {"KC_Grammar_SentenceType_Verbal": 0.2, "KC_Grammar_Mood_Indicative": 0.1},
    "KC_Vocabulary_Adjective": {"KC_Grammar_gender_Agreement": 0.2, "KC_Morphology_BrokenPlural": 0.05},
    "KC_Vocabulary_Adverb": {"KC_Grammar_SentenceType_Verbal": 0.1},
    "KC_Vocabulary_Preposition": {"KC_Grammar_Preposition": 0.1},
    "KC_Vocabulary_Conjunction": {"KC_Grammar_SentenceType_Nominal": 0.05},
    #example but is not the rule
    "KC_Vocabulary_Pronouns": {"KC_Grammar_Pronoun_Personal": 0.15, "KC_Grammar_Pronoun_Object": 0.1},
    #again some but not all inderect
    "KC_Vocabulary_Proper_Noun": {"KC_Grammar_Case_Nominative": 0.2, "KC_Definiteness_Definite": 0.1},
    # grammar Components
    "KC_Grammar_Case_Nominative": {"KC_Vocabulary_Object": 0.1, "KC_Vocabulary_Proper_Noun": 0.1},
    "KC_Grammar_Case_Accusative": {"KC_Vocabulary_Object": 0.1, "KC_Definiteness_Indefinite": 0.05},
    "KC_Grammar_Case_Genitive": {"KC_Vocabulary_Preposition": 0.1},
    "KC_Grammar_SentenceType_Nominal": {"KC_Vocabulary_Adjective": 0.1},
    "KC_Grammar_SentenceType_Verbal": {"KC_Vocabulary_Verb": 0.2},
    "KC_Grammar_Pronoun_Personal": {"KC_Vocabulary_Pronouns": 0.15},
    "KC_Grammar_Pronoun_Possessive": {"KC_Vocabulary_Adjective": 0.1},
    "KC_Grammar_Pronoun_Object": {"KC_Vocabulary_Pronouns": 0.1},
    "KC_Grammar_Preposition": {"KC_Vocabulary_Preposition": 0.1},
    "KC_Grammar_gender_Agreement": {"KC_Vocabulary_Adjective": 0.2, "KC_Masculine": 0.1, "KC_Feminine": 0.1},
    "KC_Grammar_Number_Agreement": {"KC_Vocabulary_Object": 0.05, "KC_Morph_Plurality_Plural": 0.1},
    "KC_Grammar_Mood_Indicative": {"KC_Vocabulary_Verb": 0.2},
    "KC_Grammar_Mood_Subjunctive": {"KC_Vocabulary_Verb": 0.15},
    "KC_Grammar_Mood_Jussive": {"KC_Vocabulary_Verb": 0.15},
    # morphology Components
    "KC_Masculine": { "KC_Feminine": 0.05},
    "KC_Feminine": { "KC_Masculine": 0.05},
    "KC_Tense_Past": {"KC_Grammar_SentenceType_Verbal": 0.1},
    "KC_Tense_Present": {"KC_Grammar_SentenceType_Verbal": 0.1},
    "KC_Tense_Future": {"KC_Grammar_SentenceType_Verbal": 0.1},
    "KC_Definiteness_Definite": {"KC_Vocabulary_Proper_Noun": 0.1},
    "KC_Definiteness_Indefinite": {"KC_Grammar_Case_Accusative": 0.05},
    "KC_Morph_Plurality_Singular": {"KC_Morphology_SoundPlural": 0.1},
    "KC_Morph_Plurality_Dual": {"KC_Morphology_SoundPlural": 0.1},
    "KC_Morph_Plurality_Plural": {"KC_Grammar_Number_Agreement": 0.1},
    "KC_Morphology_SoundPlural": {"KC_Vocabulary_Object": 0.05},
    #some but not alll some are sepecific vocab
    "KC_Morphology_BrokenPlural": {"KC_Vocabulary_Object": 0.05},
    #these dependencies change per text
    #vocab :
    "KC_Vocab_عام":{"KC_Definiteness_Definite":0.1},
    "KC_Vocab_احتفل": {"KC_Grammar_Case_Nominative": 0.1, "KC_Morphology_SoundPlural": 0.05},

    "KC_Vocab_عام": {'KC_Grammar_SentenceType_Nominal': 0.01, 'KC_Masculine': 0.01} 

}
 
 

def update_related_kcs(kc_dict, dependencies, kc, correct):
    """
    Update dependencies based on influence from the main knowledge component.
    Args:
    - kc_dict (dict): The dictionary containing knowledge components.
    - dependencies (dict): The dependency relationships between knowledge components.
    - kc (str): The main knowledge component being updated.
    - correct (bool): Whether the student's response was correct.
    """
    if kc in dependencies:
        related_kcs = dependencies[kc]
        for related_kc, influence_prob in related_kcs.items():
            if related_kc in kc_dict:  # Ensure the related KC exists
                bkt_instance = kc_dict[related_kc]["bkt"]  # Access the BKT instance
                print(f"    Dependency '{related_kc}' before update: P(Know) = {bkt_instance.p_know:.4f}")
                # Positive update: Only if correct and below baseline
                if correct and bkt_instance.p_know < bkt_instance.baseline:
                    bkt_instance.p_know += influence_prob * (1 - bkt_instance.p_know)
                elif not correct:
                    # Negative update for an incorrect response
                    bkt_instance.p_know -= influence_prob * bkt_instance.p_know
                print(f"Dependency '{related_kc}' after update: P(Know) = {bkt_instance.p_know:.4f}")
            else:
                print(f"Dependency '{related_kc}' not found in knowledge components.")


def handle_clicks(word, current_testing_grade, current_testing_unit, knowledge_components):
    """
    Handles clicks on a word and determines its relation to the current, past, or future testing scope.
    
    Args:
    - word (str): The word the user clicked on.
    - current_testing_grade (int): The grade currently being tested.
    - current_testing_unit (int): The unit currently being tested.
    - knowledge_components (dict): Knowledge base containing knowledge components.
    """
    word_found = False
    # Step 1: Search for the word in the knowledge base
    for knowledge_component, kc_data in knowledge_components.items():
        if word in knowledge_component:
            word_found = True
            # Found the word in the knowledge base
            print(f"Found word '{word}' in knowledge base.")

            # Step 2: Determine if it's being tested now, later, or in the past based on the current_testing_grade and current_testing_unit
            is_tested_now = (
                kc_data["unit"] == current_testing_unit and
                kc_data["grade"] == current_testing_grade
            )
            is_tested_later = (
                kc_data["grade"] > current_testing_grade or 
               (kc_data["unit"] > current_testing_unit and kc_data["grade"] == current_testing_grade)
            )
            is_tested_past = (
                kc_data["unit"] < current_testing_unit or
                (kc_data["unit"] < current_testing_unit and kc_data["grade"] == current_testing_grade)
            )

            # Increment click count for that spêcific word
            kc_data["click_count"] += 1
            print(f"Click count for '{word}': {kc_data['click_count']}")
            # Rule 1: First 2 clicks -> Present glossary
            if kc_data["click_count"] <= 2:
             # General Rule: First 2 clicks on the same word
                print("Glossary entry presented for this word.")
                search_gloss(word)
           # Rule: 1 click on a word in an upcoming unit
            if is_tested_later and kc_data["click_count"] == 1:
                kc_data["bkt"].p_know = min(1.0, kc_data["bkt"].p_know + 0.10)
                print("Glossary presented and positive update applied for a future word.")
                search_gloss(word)
            # Rule: 1 click on a word in a past unit
            elif is_tested_past and kc_data["click_count"] == 1:
                kc_data["bkt"].p_know = max(0.0, kc_data["bkt"].p_know - 0.05)
                print("Decay applied for a past word (1st click).")
            # Rule: 2nd and 3rd click on a word in a past unit
            elif is_tested_past and 2 <= kc_data["click_count"] <= 3:
                kc_data["bkt"].p_know = max(0.0, kc_data["bkt"].p_know - 0.05)
                print(f"Additional decay applied for past word. Click count: {kc_data['click_count']}")
            # Rule: Clicks > 3
            elif kc_data["click_count"] > 3:
                if is_tested_now:
                    # Rule: More than 3 clicks on a target word in the current unit
                    print("Presenting a question from the question bank.")
                    result = ask_question(knowledge_component, question_bank)
                    for kc_name, is_correct in result.items():
                        general_update_function(kc_name, is_correct)
                    kc_data["click_count"] = 0
                    print(f"Click count for '{word}' reset after question.")
                elif is_tested_later:
                    # Rule: More than 3 clicks on a word in an upcoming unit
                    print("Negative update applied for excessive clicks on a future word.")
                    kc_data["bkt"].p_know = max(0.0, kc_data["bkt"].p_know - 0.10)
                elif is_tested_past:
                    # Rule: More than 3 clicks on a word in a past unit
                    print("Presenting question for past word.")
                    result = ask_question(knowledge_component, question_bank)
                    for kc_name, is_correct in result.items():
                        general_update_function(kc_name, is_correct)
                    kc_data["click_count"] = 0
                    print(f"Click count for '{word}' reset after question.")
    if not word_found:
        # Rule: Word not in the current testing curriculum
        print(f"Word '{word}' not found in the current testing curriculum. Presenting glossary repeatedly.")
        search_gloss(word)
#Question bank containing multiple choice and fill in blank:
question_bank = {
    "KC_Vocab_احتفل": [
        {
            "type": "multiple_choice",
            "question": "ما معنى كلمة 'احتفل'؟",
            "options": ["أقام احتفالاً", "لعب مع أصدقائه", "ذهب إلى المدرسة"],
            "answer": "أقام احتفالاً",
        },
        {
            "type": "fill_in_blank",
            "question": "احتفل أحمد ____ ميلاده.",
            "answer": "بعيد",
        },
        {
            "type": "multiple_choice",
            "question": "في أي من المناسبات يمكن أن نستخدم كلمة 'احتفل'؟",
            "options": ["عيد ميلاد", "الذهاب للعمل", "إصلاح سيارة"],
            "answer": "عيد ميلاد",
        },
        {
            "type": "fill_in_blank",
            "question": "____ احتفلنا بمناسبة خاصة.",
            "answer": "أمس",
        },
    ],
    "KC_Vocab_عام": [
        {
            "type": "multiple_choice",
            "question": "ما معنى كلمة 'عام' في اللغة العربية؟",
            "options": ["دورة زمنية", "حدث تاريخي", "شيء مجهول"],
            "answer": "دورة زمنية",
        },
        {
            "type": "fill_in_blank",
            "question": "يستمر العام ____ شهراً.",
            "answer": "اثني عشر",
        },
        {
            "type": "multiple_choice",
            "question": "ما الفرق بين 'عام' و'سنة'؟",
            "options": ["عام يدل على الإيجابية", "عام يدل على التعب", "عام ليس له علاقة بالسنة"],
            "answer": "عام يدل على الإيجابية",
        },
        {
            "type": "fill_in_blank",
            "question": "كان ____ مليئاً بالتحديات.",
            "answer": "عام",
        },
    ],
}

def ask_question(kc_name, question_bank):
    """
    Fetch a question from the question bank, present it to the user, and check if the answer is correct.
    
    Args:
    - kc_name (str): The name of the knowledge component (e.g., "KC_Vocab_عام").
    - question_bank (dict): A dictionary containing questions for each knowledge component.

    Returns:
    - dict: {kc_name: True/False}, indicating whether the answer was correct.
    """
    # Check if the knowledge component exists in the question bank
    if kc_name not in question_bank:
        print(f"No questions available for {kc_name}.")
        return {kc_name: False}

    # Fetch a random question
    question = random.choice(question_bank[kc_name])

    # Present the question based on its type
    if question["type"] == "multiple_choice":
        print(f"Question: {question['question']}")
        for i, option in enumerate(question["options"], 1):
            print(f"{i}. {option}")
        user_choice = int(input("Choose the correct option (1/2/3): ")) - 1
        if user_choice < 0 or user_choice >= len(question["options"]):
                print("Invalid choice. Answer marked as incorrect.")
                return {kc_name: False}
        user_answer = question["options"][user_choice]
    elif question["type"] == "fill_in_blank":
        print(f"Fill in the blank: {question['question']}")
        user_answer = input("Your Answer: ").strip()
    else:
        print("Unknown question type.")
        return {kc_name: False}

    # Check the answer
    is_correct = user_answer == question["answer"]

    # Feedback to the user
    if is_correct:
        print("Correct!")
    else:
        print(f"Incorrect! The correct answer is: {question['answer']}")

    # Return result
    return {kc_name: is_correct} 
    
def general_update_function(kc,is_correct):
    if kc in knowledge_components:
        bkt_instance = knowledge_components[kc]["bkt"]
                # Print before response
        print(f"\nKnowledge Component: {kc}")
        print(f"  Before response: P(Know) = {bkt_instance.p_know:.4f}")
                # Update main KC based on response
        updated_prob = bkt_instance.update(is_correct)
        print(f"  After response (correct={is_correct}): P(Know) = {updated_prob:.4f}")
                # Update related KCs based on dependencies
        update_related_kcs(knowledge_components, dependencies, kc, is_correct)
    else:
        print(f"Knowledge Component '{kc}' not found in the knowledge base.")

def simulate_student_responses():
    #example input:
    responses = [
        {"type": "response", "kc": "KC_Masculine", "correct": True},
        {"type": "response", "kc": "KC_Feminine", "correct": False},
         # 1. Current unit and grade : grade 1 unit 2
        {"type": "click_event", "word": "عام"},  # First click, glossary
        {"type": "click_event", "word": "عام"},  # Second click, glossary
        {"type": "click_event", "word": "عام"},  # Third click, glossary
        {"type": "click_event", "word": "عام"},  # ask question

        # 2. Future unit/grade
        {"type": "click_event", "word": "بيت"},  # First click, glossary and positive update
        {"type": "click_event", "word": "بيت"},  # Second click, decay
        {"type": "click_event", "word": "بيت"},  # Third click, decay
        {"type": "click_event", "word": "بيت"},  # Fourth click, negative update

        # 3. Past unit/grade
        {"type": "click_event", "word": "احتفل"},  # First click, decay
        {"type": "click_event", "word": "احتفل"},  # Second click, additional decay
        {"type": "click_event", "word": "احتفل"},  # Third click, additional decay
        {"type": "click_event", "word": "احتفل"},  # Fourth click, question triggered
        {"type": "click_event", "word": "احتفل"}, #fifth reset clicks 
        # 4. Word not in the knowledge base
        {"type": "click_event", "word": "مليار"},  # Glossary repeatedly

    ]

    for response in responses:
        if response["type"] == "click_event":
            # Handle click events
            word = response["word"]
            print(f"Processing click event for '{word}'")
            handle_clicks(word, current_testing_grade=1, current_testing_unit=2, knowledge_components=knowledge_components)

        elif response["type"] == "response":
            # Handle knowledge component responses
            kc = response["kc"]
            correct = response["correct"]

            if kc in knowledge_components:
                bkt_instance = knowledge_components[kc]["bkt"]
                # Print before response
                print(f"\nKnowledge Component: {kc}")
                print(f"  Before response: P(Know) = {bkt_instance.p_know:.4f}")
                # Update main KC based on response
                updated_prob = bkt_instance.update(correct)
                print(f"  After response (correct={correct}): P(Know) = {updated_prob:.4f}")
                # Update related KCs based on dependencies
                update_related_kcs(knowledge_components, dependencies, kc, correct)
            else:
                print(f"Knowledge Component '{kc}' not found in the knowledge base.")

if __name__ == "__main__":
    simulate_student_responses()
