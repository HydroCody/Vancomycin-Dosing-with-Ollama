import ollama
import random
from dosing_model import Kinetics

creatinine = round(random.uniform(0.4,1.8), 2)
age = random.randint(20,65)
weight = random.randint(60,100)
gender = random.choice(["male", "female"])
height = 50
infection = random.choice(["cellulitis", "abscess", "osteomyelitis", "meningitis", "pneumonia"])

patient = Kinetics(age, weight, gender, height, creatinine)

prompt = (f"Please generate a sample patient case using the following variables to be used as a student practice for dosing Vancomycin:\n"
          f"Patient age = {age} years, weight = {weight} kg, gender = {gender}, creatinine = {creatinine}.\n"
          f"Please do not include any guideline information or hints for how to dose vancomycin.\n"
          f"This prompt should only generate a fictitious patient with this data and an infection type of {infection}.\n"
          f"Example, begin with patient narrative: Patient presents to the emergency department with complaints of {infection}.\n"
          f"The patient is a {gender} aged {age} with a weight of {weight} kg.\n"
          f"Lab results reveal creatinine level of {creatinine}.\n"
          "Do not include list of medications, do not include a social history section, do not include an additional information. Review of symptoms section should only include the affected organ system. Allergy list should be very minimal. No acknowledgement of prompt needed, just begin with Patient Information.")

stream = ollama.chat(
    model='llama2',
    messages=[{'role': 'user', 'content': prompt}],
    stream=True,
)

for chunk in stream:
  print(chunk['message']['content'], end='', flush=True)

print("\n")

print("What is your recommended Vancomycin regimen?")

recommended_dose = int(input("Recommended dose in mg: "))
recommended_interval = int(input("Recommended interval in hours: "))
viable_regimens = patient.therapeutic_regimens()

response_prompt = (f"The student has selected a vancomycin regimen of {recommended_dose} every {recommended_interval} for the infection of {infection}. The list of correct possible answers are {viable_regimens}. Please provide them feedback on their answer")

stream = ollama.chat(
    model='llama2',
    messages=[{'role': 'user', 'content': response_prompt}],
    stream=True,
)

for chunk in stream:
  print(chunk['message']['content'], end='', flush=True)