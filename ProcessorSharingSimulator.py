class Job:
    """
    Represents a job in the processor-sharing queue.
    
    Attributes:
        id (int): Unique job identifier.
        arrival_time (float): Time the job arrives to the system.
        service_time (float): Total required processing time.
        abandonment_time (float): Time after which the job abandons the system if not completed.
        initial_infection_status (int): 1 if infected at arrival, 0 otherwise.
        infectious_start_time (float): Time the job becomes infectious if infected.
        time_of_infection (float or None): Time the job was infected.
        remaining_size (float): Remaining processing time needed.
        departure_time (float or None): Time job leaves the system.
        queue_length_at_arrival (int or None): Number of jobs in the system at arrival.
        work_in_system (float): Total work in system upon arrival.
        abandon_tag (str or None): Indicates if the job abandoned ("ABAND") or completed.
        cumulative_overlap (float): Total overlap time with infectious jobs.
    """
    def __init__(self, id, arrival_time, service_time, abandonment_time, initial_infection_status, infectious_start_time):
        self.id = id
        self.infection_status = initial_infection_status
        self.arrival_time = arrival_time
        self.initial_infection_status = initial_infection_status
        self.time_of_infection = arrival_time if initial_infection_status == 1 else None 
        self.infectious_start_time = arrival_time if initial_infection_status == 1 else infectious_start_time
        self.service_time = service_time
        self.abandonment_time = abandonment_time
        self.remaining_size = service_time
        self.departure_time = None
        self.queue_length_at_arrival = None
        self.work_in_system = 0
        self.abandon_tag = None
        self.cumulative_overlap = 0


class DiscreteEventSimulator:
    """
    A discrete event simulation of a processor-sharing queue with infection spread and abandonment.

    Attributes:
        num_jobs (int): Total number of jobs to simulate.
        inter_arrival_time (list of float): Time gaps between job arrivals.
        service_time_array (list of float): Required service times for each job.
        infectious_start_time_array (list of float): Times each job becomes infectious if infected.
        initial_infection_status_array (list of int): 1 if job is infected at arrival, 0 otherwise.
        inter_abandon (int): Constant time before any job abandons if not finished.
    """
    def __init__(self, num_jobs, inter_arrival_time, service_time_array, inter_abandon, infectious_start_time_array, initial_infection_status_array):
        self.num_jobs = num_jobs
        self.inter_arrival_time = inter_arrival_time
        self.service_time_array = service_time_array
        self.infectious_start_time_array = infectious_start_time_array
        self.initial_infection_status_array = initial_infection_status_array
        self.inter_abandon = inter_abandon
        self.arrivals = []
        self.departures = []
        self.queue = []

    def generate_arrivals(self):
        """
        Initializes and stores all job objects with calculated arrival and abandonment times.
        """
        current_time = 0
        for i in range(self.num_jobs):
            arrival_time = current_time + self.inter_arrival_time[i]
            service_time = self.service_time_array[i]
            abandonment_time = arrival_time + self.inter_abandon
            infectious_start_time = self.infectious_start_time_array[i]
            initial_infection_status = self.initial_infection_status_array[i]

            job = Job(i, arrival_time, service_time, abandonment_time, initial_infection_status, infectious_start_time)
            self.arrivals.append(job)
            current_time = arrival_time

    def run(self):
        """
        Runs the simulation: processes arrivals, shared processing, abandonments, and infection overlaps.
        """
        current_time = 0

        # Process job arrivals and simulate shared processing
        for job in self.arrivals:
            if len(self.queue) == 0:
                # If queue is empty, add job immediately
                self.queue.append(job)
                current_time = job.arrival_time
            else:
                if job.arrival_time == current_time:
                    self.queue.append(job)
                    current_time = job.arrival_time
                else:
                    next_arrival_time = job.arrival_time

                    # Process jobs in queue until next job arrives
                    while current_time < next_arrival_time:
                        # If queue is empty, add job immediately
                        if len(self.queue) == 0:
                            current_time = next_arrival_time
                            break

                        time_delta = next_arrival_time - current_time
                        num_jobs_in_system = len(self.queue)

                        # Calculate how much work can be done before next departure
                        work_done = min(time_delta / num_jobs_in_system, min(j.remaining_size for j in self.queue))
                        
                        # Check if any job must abandon before next departure, if so update work done to abandon on time
                        if current_time + work_done * num_jobs_in_system > min(j.abandonment_time for j in self.queue):
                            work_done = (min(j.abandonment_time for j in self.queue) - current_time) / num_jobs_in_system
                        
                        current_time += work_done * num_jobs_in_system

                        completed_jobs = []
                        for j in self.queue:
                            # Apply processor sharing logic to do work in queue
                            j.remaining_size -= work_done
                            if j.abandonment_time <= current_time and j.remaining_size > 0:
                                j.departure_time = current_time
                                j.abandon_tag = 'ABAND'
                                completed_jobs.append(j)
                            elif j.remaining_size <= 0:
                                j.departure_time = current_time
                                completed_jobs.append(j)

                        for j in completed_jobs:
                            self.queue.remove(j)
                            self.departures.append(j)

                    # Update job state on arrival
                    job.work_in_system = sum(j.remaining_size for j in self.queue)
                    self.queue.append(job)

        # Finish processing any remaining jobs after all arrivals
        while self.queue:
            num_jobs_in_system = len(self.queue)
            work_done = min(time_delta / num_jobs_in_system, min(j.remaining_size for j in self.queue))
            if current_time + work_done * num_jobs_in_system > min(j.abandonment_time for j in self.queue):
                work_done = (min(j.abandonment_time for j in self.queue) - current_time) / num_jobs_in_system
            current_time += work_done * num_jobs_in_system

            completed_jobs = []
            for j in self.queue:
                j.remaining_size -= work_done
                if j.abandonment_time <= current_time and j.remaining_size > 0:
                    j.departure_time = current_time
                    j.abandon_tag = 'ABAND'
                    completed_jobs.append(j)
                elif j.remaining_size <= 0:
                    j.departure_time = current_time
                    completed_jobs.append(j)

            for j in completed_jobs:
                self.queue.remove(j)
                self.departures.append(j)

        # Compute queue length at arrival time for each job
        for job in self.departures:
            jobs_arrived = sum(1 for j in self.departures if j.arrival_time <= job.arrival_time) - 1
            jobs_departed = sum(1 for j in self.departures if j.departure_time < job.arrival_time)
            job.queue_length_at_arrival = jobs_arrived - jobs_departed

        # Calculate infectious overlaps
        infectious_jobs = [job for job in self.arrivals if job.infection_status == 1]
        infectious_jobs.sort(key=lambda job: job.infectious_start_time)

        while infectious_jobs:
            current_infectious_job = infectious_jobs.pop(0)
            for j in self.arrivals:
                # Calculate time overlap with infectious window
                overlap = max(0, min(j.departure_time, current_infectious_job.departure_time) -
                                 max(j.arrival_time, current_infectious_job.infectious_start_time))
                if overlap > 0:
                    j.cumulative_overlap += overlap

        # Print summary statistics for each job
        for job in self.departures:
            results = {
                'arrival_time': round(job.arrival_time, 3),
                'service_time': round(job.service_time, 3),
                'departure_time': round(job.departure_time, 3),
                'response_time': job.abandon_tag if job.abandon_tag == 'ABAND' else round(job.departure_time - job.arrival_time, 3),
                'queue_length': job.queue_length_at_arrival,
                'work_in_system': round(job.work_in_system, 3),
                'initial_infection_status': job.initial_infection_status,
                'time_of_infection': round(job.time_of_infection, 3) if job.time_of_infection is not None else None,
                'infectious_start_time': round(job.infectious_start_time, 3) if job.infectious_start_time is not None else None,
                'infected': False if job.time_of_infection is None else True,
                'abandon_tag': job.abandon_tag if job.abandon_tag == 'ABAND' else 'Complete',
                'overlap': job.cumulative_overlap
            }
            print(results)
