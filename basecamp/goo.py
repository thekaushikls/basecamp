from Grasshopper.Kernel.Types import GH_GeometricGoo
from Grasshopper.Kernel import IGH_BakeAwareData, IGH_PreviewData

import copy

from elements import Tent

class TentGoo(GH_GeometricGoo[Tent], IGH_BakeAwareData, IGH_PreviewData):

    def __init__(self, tent):
        self.m_value = tent
    
    def get_TypeName(self):
        return "TentGoo"
    
    def get_TypeDescription(self):
        return "TentGoo"
    
    def get_IsValid(self):
        return True

    def ToString(self):
        return "TentGoo"

    def get_BoundingBox(self):
        return self.m_value.GetBoundingBox()
    
    def get_ClippingBox(self):
        return self.m_value.GetBoundingBox()
    
    def GetBoundingBox(self, xform):
        return self.m_value.GetBoundingBox()
    
    def DuplicateGeometry(self):
        return TentGoo(copy.deepcopy(self.m_value))

    def Transform(self, xform): return
    
    def DrawViewportWires(self, args):
        self.m_value.DrawViewportWires(args)
    
    def DrawViewportMeshes(self, args):
        pass

    def BakeGeometry(self, doc, att, id):
        pass
    
