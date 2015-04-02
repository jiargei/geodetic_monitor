__author__ = 'jurgen'

# AUT Position Precision

AUT_NORMAL = 0          # fast positioning mode
AUT_PRECISE = 1         # exact positioning mode - can distinctly claim more time for the positioning


# AUT Fine-adjust Position Mode

AUT_NORM_MODE = 0       # Angle tolerance
AUT_POINT_MODE = 1      # Point tolerance
AUT_DEFINE_MODE = 2     # System indiependet positioning tolerance. Set with AUT_SetTol


# AUT Automatic Target Recognition Mode

AUT_POSITION = 0        # Positioning to the hz- and v-angle
AUT_TARGET = 1          # Positioning to a target in the environment of the hz- and v-angle