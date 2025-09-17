#!/usr/bin/env python
# -*- coding: utf-8 -*- 

# Adds the rule of thirds and symmetry. Instead of 1.85:1, adds 2.387:1 (2048x858).

#v1.0.0
#created by: Pushkarev Aleksandr

import foundry.ui
import guides, custom_guides

class RuleOfThirds(foundry.ui.Drawing):
    """ Draws rule of thirds lines
    """
    def __init__(self, name = "rule of thirds", aspect = 0.0):
        super().__init__(name)
        self.setCoordinateSystem(guides.kGuideSequence, 0.0, 0.0, 1.0, 1.0, aspect)
        self.setPen(1, 1, 1)
        third = 1.0 / 3.0
        self.drawLine(third, 0.0, third, 1.0) # first vertical line
        self.drawLine(third * 2.0, 0.0, third * 2.0, 1.0) # second vertical line
        self.drawLine(0.0, third, 1.0, third) # first horizontal line
        self.drawLine(0.0, third * 2.0, 1.0, third * 2.0) # second horizontal line
        self.aspect = aspect
        self.name = name

class Symmetry(foundry.ui.Drawing):
    """ Draws vertical, horizontal and 45 degree symmetry lines
    """
    def __init__(self, name = "symmetry", aspect = 0.0):
        super().__init__(name)
        self.setCoordinateSystem(guides.kGuideSequence, 0.0, 0.0, 1.0, 1.0, aspect)
        self.setPen(1, 1, 1)
        self.drawLine(0.5, 0.0, 0.5, 1.0)
        self.drawLine(0.0, 0.5, 1.0, 0.5)
        self.drawLine(0.0, 0.0, 1.0, 1.0)
        self.drawLine(0.0, 1.0, 1.0, 0.0)
        self.aspect = aspect
        self.name = name

custom_guides.viewer_guides.append(RuleOfThirds())
custom_guides.viewer_guides.append(Symmetry())

custom_guides.viewer_masks.pop(-2)
custom_guides.viewer_masks.append(guides.MaskGuide("2.387:1", 2048.0/858.0))
