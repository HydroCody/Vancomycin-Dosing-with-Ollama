import math
import numpy as np 
import matplotlib.pyplot as plt 


class Kinetics:
    def __init__(self, age, weight, gender, height, SCr, doses =[500, 750, 1000, 1250, 1500, 1750, 2000], intervals =[8, 12, 18, 24, 36], goal_trough = [10,20]):
        self.age = age
        self.weight = weight
        self.gender = gender
        self.height = height
        self.SCr = SCr
        self.doses = doses
        self.intervals = intervals
        self.goal_trough_lower = goal_trough[0]
        self.goal_trough_upper = goal_trough[1]
        self.crcl = self.crcl_calculate()

        kinetics_values = self.calculate_kinetics()

        self.volume_distribution = kinetics_values["Vanc VD"]
        self.vancomycin_clearance = kinetics_values["Vanc Cl"]
        self.ke = kinetics_values["ke"]
        self.half_life = kinetics_values["t1/2"]

    def crcl_calculate(self):
        if self.gender == "female":
            adjustment_gender = 0.85
        else:
            adjustment_gender = 1.0


        crcl = ((140-self.age)*(self.weight*2.2)/(72 * self.SCr)) * adjustment_gender

        if crcl >120:
            crcl = 120

        return crcl
 #Creates a dictionary with key value pairs for Vancomycin volume of distribution 'Vanc VD', Vancomycin clearance 'Vanc Cl', ke coefficient 'ke', and calculated half life 't1/2' and their associated calculations   
    def calculate_kinetics(self):
        vanc_vd = self.weight * 0.7
        vanc_cl = self.crcl *0.06 * 0.65
        vanc_ke = vanc_cl/vanc_vd
        half_life = 0.693/vanc_ke

        return {
        "Vanc VD": vanc_vd,
        "Vanc Cl": vanc_cl,
        "ke": vanc_ke,
        "t1/2": half_life}
    
    def infusion_time(self, dose):
        if dose < 1000:
            return 1
        elif dose <1500:
            return 2
        else:
            return 3
        
    def predicted_peak_steady_state(self, dose, interval):
        peak = ((dose/self.infusion_time(dose))/(self.volume_distribution*self.ke))*((1-math.exp(-self.ke*self.infusion_time(dose)))/(1-math.exp(-self.ke*interval)))
        return peak
    
    def level_at_time(self, dose, interval, hour, peak_level="flag"):
        if peak_level == "flag":
            peak_level = self.predicted_peak_steady_state(dose, interval)
        
        level = peak_level*math.exp(-self.ke*hour)
        return level

    def steady_state_trough(self, dose, interval):
        trough = self.predicted_peak_steady_state(dose, interval)*math.exp(-self.ke*(interval-self.infusion_time(dose)))
        return trough
    
    def change_in_concentration_after_dose(self, dose):
        ti = self.infusion_time(dose)

        delta_c = ((dose*(1-math.exp(-self.ke*ti)))/(ti*self.ke*self.volume_distribution))
        return delta_c
    
    def all_regimens(self):
        list_of_regimens = []
        for dose in self.doses:
            for interval in self.intervals:
                predicted_peak = round(self.predicted_peak_steady_state(dose, interval), 2)
                trough = round(self.steady_state_trough(dose, interval), 2)
                list_of_regimens.append((dose, interval, predicted_peak, trough))
        
        return list_of_regimens
    
    def therapeutic_regimens(self):
        list_of_regimens = self.all_regimens()
        list_of_therapeutic_regimens =[]
        for regimen in list_of_regimens:
            dose, interval, predicted_peak, trough = regimen
            if trough > self.goal_trough_lower and trough < self.goal_trough_upper:
                list_of_therapeutic_regimens.append((dose, interval, predicted_peak, trough))
        
        return list_of_therapeutic_regimens

    def generate_plots_to_graph(self, dose, interval, hours_to_graph):
        time_hours = []
        concentrations = []

        for i in range(hours_to_graph):
            time_hours.append(i)
    
        sorted_hours = sorted(time_hours)

        counter = 0

        final_hours = sorted_hours.copy()
        infusion_time = self.infusion_time(dose)
        additive_level = self.change_in_concentration_after_dose(dose)
        for hour in sorted_hours:
            if hour == 0:
                concentrations.append(0)
            elif (hour - counter*interval) < infusion_time:
                final_hours.remove(hour)
            elif (hour - counter*interval) == infusion_time:
                if counter == 0:
                    concentrations.append(additive_level)
                    continue

                additive_level = concentrations[-1] + self.change_in_concentration_after_dose(dose)
                concentrations.append(self.level_at_time(dose, interval, (hour - counter*interval), additive_level))

            else:
                if hour % interval  == 0:
                    concentrations.append(self.level_at_time(dose, interval, (hour - counter*interval), additive_level))
                    counter +=1
                    continue

                concentrations.append(self.level_at_time(dose, interval, (hour - counter*interval), additive_level))
    

        
            
        print(f"final hours is {final_hours} and concentrations is {concentrations}")
        return {"times":final_hours, "concentrations": concentrations}
    
    def generate_graph(self, times_concentrations, dose, interval):
        times = times_concentrations["times"]
        concentrations = times_concentrations["concentrations"]

        hours = np.array(times)
        levels = np.array(concentrations)

        plt.plot(hours, levels, marker='o', linestyle='-')
        plt.xlabel("Time (hours)")
        plt.ylabel("Vancomycin Concentration (mg/L)")
        plt.title(f"Vancomycin kinetics for {dose}mg every {interval} hours")
        plt.grid(True)
        plt.show()

"""
kinetics = Kinetics(55, 70, "male", 70, 1.0)

print(f"Patients weight is {kinetics.weight} and SCr is {kinetics.SCr}")
print(f"The all regimens is {kinetics.all_regimens()}")
print(f"The viable regimens are {kinetics.therapeutic_regimens()}")

regimens = kinetics.therapeutic_regimens()

for option in regimens:
    plot_points = kinetics.generate_plots_to_graph(option[0], option[1], 160)
    kinetics.generate_graph(plot_points, option[0], option[1])
"""