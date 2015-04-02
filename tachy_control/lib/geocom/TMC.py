__author__ = 'jurgen'

# Inclination Sensor Measurement Program

TMC_MEA_INC = 0         # Use sensor (apriori sigma)
TMC_AUTO_INC = 1        # Automatic mode (sensor/plane)
TMC_PLANE_INC = 2       # Use plane (apriori sigma)


# TMC Measurement Mode

TMC_STOP = 0            # Stop measurement program
TMC_DEF_DIST = 1        # Default DIST-measurement program
TMC_CLEAR = 3           # TMC_STOP and clear data
TMC_SIGNAL = 4          # Signal measurement test function
TMC_DO_MEASURE = 6      # (Re)start measurement task
TMC_RTRK_DIST = 8       # Distance-TRK measurement program
TMC_RED_TRK_DIST = 10   # Reflectorless tracking
TMC_FREQUENCY = 11      # Frequency measurement (test)