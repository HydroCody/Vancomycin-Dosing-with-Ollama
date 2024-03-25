Dosing_model

This model accepts an age, weight, gender, height, and serum creatinine and creates an object that generates patient specific kinetics for this information. Accepted doses, Intervals, and goal trough can be 
edited but will default to doses of doses =[500, 750, 1000, 1250, 1500, 1750, 2000], intervals =[8, 12, 18, 24, 36], goal_trough = [10,20]. The object can create peaks and troughs for all dosing combinations and then selects those with troughs
within the goal troughs listed. Generate_graph will graph the first X hours of the kinetics plot out.

Practicevanc

This randomly generates a patient that is passed to the ollama llama2 model to generate a patient case. After the case is printed the user is prompted for an acceptable dose and then interval for the practice patient. The answer is passed to the language model
with the correct choices to explain to the user.


Known issues:
This is the initial push for proof of concept. Currently there is no error checking for user inputs. The second pass of the information to the language model needs improved verbiage to optimize the output. The language model llama2 likely is not the ideal model
for using and will be tested with alternative models. 

Future plans:
Improvement of the dosing model to allow testing of the users input to pass a graph of their choice back, this information will also be passed to the language model for better critiques for the users choices.
