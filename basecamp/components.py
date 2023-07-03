from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Rhino, Grasshopper
import System

from elements import Tent
from goo import TentGoo

class BaseCampComponent(component):
    
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "BaseCamp", "BaseCamp", """Generates a tent.""", "Display", "Camp")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("470ebf1e-61ff-4f4c-9ded-f3455077cfee")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_Point()
        self.SetUpParam(p, "Anchor", "A", "Anchor point for Tent.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        p.SetPersistentData(Grasshopper.Kernel.Types.GH_Point(Rhino.Geometry.Point3d(0,0,0)))
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Number()
        self.SetUpParam(p, "Width", "W", "Width of tent.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        p.SetPersistentData(Grasshopper.Kernel.Types.GH_Number(150.00))
        self.Params.Input.Add(p)

        p = Grasshopper.Kernel.Parameters.Param_Number()
        self.SetUpParam(p, "Height", "H", "Height of tent.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        p.SetPersistentData(Grasshopper.Kernel.Types.GH_Number(200.00))
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Colour()
        self.SetUpParam(p, "ColorA", "A", "Primary color for tent.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Colour()
        self.SetUpParam(p, "ColorB", "B", "Secondary color for tent.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "Tent", "T", "Generated Tent(s).")
        self.Params.Output.Add(p)
        
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        p1 = self.marshal.GetInput(DA, 1)
        p2 = self.marshal.GetInput(DA, 2)
        p3 = self.marshal.GetInput(DA, 3)
        p4 = self.marshal.GetInput(DA, 4)
        result = self.RunScript(p0, p1, p2, p3, p4)

        if result is not None:
            self.marshal.SetOutput(result, DA, 0, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAHYcAAB2HAY/l8WUAAAJ4SURBVEhLYxhZIDc3VxREFxcXi4EFqAwYnZycZnp6eubY2Nj0////nxEqTj1ga2sbb2pq+sHNzS0AKkRdUFBQoCQrK3uNJq4HAV9fXx9gMH1NTk62hgpRF3h4eCxbv379f2A8zIQKUQ8YGhrKFxYW/v758+f/+Pj4x1ZWVrxQKeoAExOTrEOHDgGD////DRs2/JeTk/OGSlEOgGYyGRgYnABG8v/6+vr/2dnZ/3V0dFZDpSkH4eHhytzc3H+AzP8wLCEh8WvBggXKIHmKgYaGRj0TExPccBBmY2P7D0xRZSB5isC7d+/4geH9EMgEGwxMSf9ZWFjAbCkpqRMgNRSBoKAgdx4eHrCBnJyc/48ePfpDW1v7O4jPz8//Pz8/3xyskFygpqa2FEiBLdDS0vr/48ePz+Xl5dsYGRn/g4LNzMxsKlghOWDWrFkyoqKiX4BMsAVRUVHgZPr8+fNyoK9ugMSAwfTs+vXr5OUJBweHdHZ2drDhIDxx4kSwBd++fZuvrq6eAfIBFxcXyOJYsAZSgaqq6mkgBTYcZNjBgwf///79+//jx49vAn3BDUyqz0BywDyxCaSeJFBVVWUmJCQEd728vDzI4P/AVPX/xYsX/4BAGlgvJAJT1F+guq/A4FQEayQWANN+K5CCWxAQEPAfVA69evUKTAMt8DUyMrIAWvALJO/j4wNSTxzo7u7m1tTUfCUuLg7Ksf+BEf1/0qRJ///8+fP/9evXYAuOHTt2Apg/PoDkQRhYlNyDaicMgOUNV2xsrP2ECRNsenp6bDo6OmwOHz5sc+bMGZvjx4+D6RUrVrgAk6sTSH7KlCk2Li4uJlDt9AQMDAD6Vxzg10WBlwAAAABJRU5ErkJggg=="
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    def RunScript(self, origin, width, height, ColorA=None, ColorB=None):
        
        tent = Tent(origin, width, height)
        
        if ColorA and ColorB:
            tent.primary_color = ColorA
            tent.secondary_color = ColorB
        
        return TentGoo(tent)

