# Adds buttons for enabling and disabling PerformanceTimers

# v1.0.0
# created by: Pushkarev Aleksandr

import nuke

nuke.menu("Nuke").addCommand("GreenFX/Utilities/PerformanceTimers/Start", "nuke.startPerformanceTimers()")
nuke.menu("Nuke").addCommand("GreenFX/Utilities/PerformanceTimers/Stop", "nuke.stopPerformanceTimers()")
nuke.menu("Nuke").addCommand("GreenFX/Utilities/PerformanceTimers/Reset", "nuke.resetPerformanceTimers()")
