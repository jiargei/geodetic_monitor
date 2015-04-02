__author__ = 'jurgen'

# BAP Measurement Modes

BAP_NO_MEAS = 0         # no measurements, take last one
BAP_NO_DIST = 1         # no dist. measurement, angles only
BAP_DEF_DIST = 2        # default dist. measurments, pre-defined using BAP_SetMeasPrg
BAP_CLEAR_DIST = 5      # clear distances
BAP_STOP_TRK = 6        # stop tracking

# BAP Distance measurement Programs

BAP_SINGLE_REF_STANDARD = 0   # IR Standard
BAP_SINGLE_REF_FAST = 1       # IR Fast
BAP_SINGLE_REF_VISIBLE = 2    # LO Standard
BAP_SINGLE_RLESS_VISIBLE = 3  # RL Standard
BAP_CONT_REF_STANDARD = 4     # IR Tracking
BAP_CONT_REF_FAST = 5         # not supported by Viva TPS
BAP_AVG_REF_STANDARD = 7      # IR Average
BAP_AVG_REF_VISIBLE = 8       # LO Average
BAP_AVG_RLESS_VISIBILE = 9    # RL Average
BAP_CONT_REF_SYNCHRO = 10     # IR Synchro Tracking
BAP_SINGLE_REF_PRECISE = 11   # IR Precise (TS30, TM30)

# BAP Prism type Definition

BAP_PRISM_ROUND = 0      # Leica Circular Prism
BAP_PRISM_MINI = 1       # Leica Mini Prism
BAP_PRISM_TAPE = 2       # Leica Reflector Tape
BAP_PRISM_360 = 3        # Leica 360 degree Prism
BAP_PRISM_USER1 = 4      # not supported by TPS1200
BAP_PRISM_USER2 = 5      # not supported by TPS1200
BAP_PRISM_USER3 = 6      # not supported by TPS1200
BAP_PRISM_360_MINI = 7   # Leica Mini 360 degree Prism
BAP_PRISM_MINI_ZERO = 8  # Leica Mini Zero Prism
BAP_PRISM_USER = 9       # User Defined Prism
BAP_PRISM_NDS_TAPE = 10  # Leica HDS Target