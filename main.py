from ProcessorSharingSimulator import DiscreteEventSimulator
import numpy as np
import random

num_jobs = 10
arrival_rate = .8
service_rate = 1.0
infectious_rate = .9

random_interarrivals_array = np.random.exponential(1/arrival_rate, num_jobs)
random_servicetimes_array =  np.random.exponential(1/service_rate, num_jobs) 
random_infectious_start_time_array = np.random.exponential(1/infectious_rate, num_jobs)
random_initial_infection_status = random.choices([0, 1], weights=[0.85, 0.15], k=num_jobs)


time_limit = 15

queue = DiscreteEventSimulator(num_jobs, random_interarrivals_array, random_servicetimes_array, time_limit, random_infectious_start_time_array, random_initial_infection_status)
queue.generate_arrivals()
queue.run()
