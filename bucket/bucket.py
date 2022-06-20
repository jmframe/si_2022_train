import time
import numpy as np
import pandas as pd

class BUCKET():
    def __init__(self):
        super(BUCKET, self).__init__()
        
    # __________________________________________________________________________________________________________
    # MAIN MODEL FUNCTION
    def run_bucket(self, bucket_state):
        
        # ________________________________________________
        bucket_state.volin += bucket_state.timestep_input_m
        
        # ________________________________________________
        bucket_state.potential_et_m_per_timestep = bucket_state.potential_et_m_per_s * bucket_state.time_step_size
        

        # Add the input mass to the bucket
        bucket_state.h_water_level = bucket_state.h_water_level + bucket_state.volin

        # Lose mass out of the bucket. Some periodic type loss, evaporation, and some infiltration...
        # ________________________________________________
        # SUBROUTINE
        # timestep_rainfall_input_m = f(timestep_rainfall_input_m, potential_et_m_per_timestep)
        self.et_from_bucket(bucket_state)
        


        # Overflow if the bucket is too full
        if h_water_level[ibuc] > h_max[ibuc]:
            mass_overflow[ibuc] = h_water_level[ibuc] - h_max[ibuc]
            h_water_level[ibuc] = h_max[ibuc] - np.random.uniform(0, noise['h2'])

        # Calculate head on the spigot
        h_head_over_spigot = (h_water_level[ibuc] - h_spigot[ibuc] ) * np.random.normal(1, noise['head'])

        # Calculate water leaving bucket through spigot
        if h_head_over_spigot > 0:
            velocity_out = np.sqrt(2 * g * h_head_over_spigot)
            spigot_out = velocity_out *  spigot_area[ibuc] * time_step
            h_water_level[ibuc] = h_water_level[ibuc] - spigot_out
        else:
            spigot_out = 0



        # ________________________________________________
        cfe_state.current_time_step += 1
        cfe_state.current_time      += pd.Timedelta(value=cfe_state.time_step_size, unit='s')

        return
    

    # __________________________________________________________________________________________________________
    def et_from_bucket(self,bucket_state):
        
        """
            open water loses to the atmosphere.

        """
        
        if bucket_state.input_m >0.0:

            if bucket_state.timestep_input_m > bucket_state.potential_et_m_per_timestep:
        
                bucket_state.actual_et_m_per_timestep = bucket_state.potential_et_m_per_timestep
                bucket_state.timestep_rainfall_input_m -= bucket_state.actual_et_m_per_timestep

            else: 

                bucket_state.potential_et_m_per_timestep -= cfe_state.timestep_rainfall_input_m
                cfe_state.timestep_rainfall_input_m=0.0
        return
                
