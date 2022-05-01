from random import randint
import Rhino, System

# GLOBALS
TENT_ENTRY_MIN_WIDTH_FACTOR     = 0.3
TENT_ENTRY_MAX_WIDTH_FACTOR     = 0.8
TENT_ENTRY_MIN_HEIGHT_FACTOR    = 0.5
TENT_ENTRY_MAX_HEIGHT_FACTOR    = 0.7
TENT_ENTRY_FLAP_WIDTH_RATIO     = 0.8
TENT_ENTRY_FLAP_HEIGHT_RATIO    = 0.1
TENT_CAP_SCALE_FACTOR           = 0.3
TENT_APEX_EXTENSION_RATIO       = 0.15

class Tent(object):
    
    _primary_material = None
    _secondary_material = None

    #region PROPERTIES
    @property
    def has_entry(self):
        return self._is_open
    
    @has_entry.setter
    def has_entry(self, value):
        self._is_open = bool(value)
    
    @property
    def has_cap(self):
        return self._has_cap
    
    @has_cap.setter
    def has_cap(self, value):
        self._has_cap = bool(value)
    
    @property
    def entry_height_factor(self):
        return self._opening_height_factor
    
    @entry_height_factor.setter
    def entry_height_factor(self, value):
        if TENT_ENTRY_MIN_HEIGHT_FACTOR <= value <= TENT_ENTRY_MAX_HEIGHT_FACTOR:
            self._opening_height_factor = value
        else:
            raise ValueError("Input out of bounds.")
    
    @property
    def entry_width_factor(self):
        return self._opening_width_factor
    
    @entry_width_factor.setter
    def entry_width_factor(self, value):
        if TENT_ENTRY_MIN_WIDTH_FACTOR <= value <= TENT_ENTRY_MAX_WIDTH_FACTOR:
            self._opening_width_factor = value
        else:
            raise ValueError("Input out of bounds.")
    
    @property
    def origin(self):
        return self._origin
    
    @origin.setter
    def origin(self, value):
        if isinstance(value, Rhino.Geometry.Point3d):
            self._origin = Rhino.Geometry.Point3d(value.X - self.width/2, value.Y, value.Z)
        else:
            self._origin = Rhino.Geometry.Point3d(self.width/2, 0, 0)
    
    @property
    def geometry(self):
        return self._geometry
    
    @property
    def primary_color(self):
        return self._primary_material.Diffuse
    
    @primary_color.setter
    def primary_color(self, value):
        self._primary_material = Rhino.Display.DisplayMaterial(value)
    
    @property
    def secondary_color(self):
        return self._secondary_material.Diffuse
    
    @secondary_color.setter
    def secondary_color(self, value):
        self._secondary_material = Rhino.Display.DisplayMaterial(value)
    #endregion PROPERTIES

    #region CONSTRUCTOR
    def __init__(self, origin, width = 150, height=200):
        self._is_open = bool(randint(0,10)//3)
        self._has_cap = bool(randint(0,10)//3)
        self._opening_height_factor = 0.55
        self._opening_width_factor = 0.35
        self._geometry = None
        self.primary_color = System.Drawing.Color.White
        self.secondary_color = System.Drawing.Color.Black

        self.height = height
        self.width = width
        self.origin = origin
        

        self.generate_geometry()
    #endregion CONSTRUCTOR

    #region PRIVATE METHODS
    def __apply_gravity(self, triangle): # WIP
        width = triangle.Point(1).X/2
        height = triangle.Point(2).Y
        
        curves = []
        curves.append(Rhino.Geometry.LineCurve(triangle.Point(0), triangle.Point(1)))

        pta = triangle.Point(1)
        ptb = Rhino.Geometry.Point3d(width * 1.8, height * 0.1, 0)
        ptc = triangle.Point(2)
        right_slope = Rhino.Geometry.NurbsCurve.Create(False, 2, [pta, ptb, ptc])
        curves.append(right_slope)
        
        pta = triangle.Point(2)
        ptb = Rhino.Geometry.Point3d(width * 0.2, height * 0.1, 0)
        ptc = triangle.Point(0)
        left_slope = Rhino.Geometry.NurbsCurve.Create(False, 2, [pta, ptb, ptc])
        curves.append(left_slope)
        
        return Rhino.Geometry.Curve.JoinCurves(curves, 0.01)
        
    def _generate_base_triangle(self):
        point_a = self.origin
        point_b = self.origin + Rhino.Geometry.Point3d(self.width,0,0)
        point_c = self.origin + Rhino.Geometry.Point3d(self.width/2,self.height,0)

        self._base_triangle = Rhino.Geometry.PolylineCurve([point_a, point_b, point_c, point_a])
        return self._base_triangle
    
    def _generate_cap_triangle(self):
        if self.has_cap and self._base_triangle:
            self._cap_triangle = Rhino.Geometry.PolylineCurve(self._base_triangle)
            center = self._cap_triangle.Point(2)
            xform = Rhino.Geometry.Transform.Scale(center, TENT_CAP_SCALE_FACTOR)
            self._cap_triangle.Transform(xform)
            return True
        self._cap_triangle = None
        return False
    
    def _generate_entry_triangle(self):
        if self.has_entry and self._base_triangle:
            self._entry_triangle = Rhino.Geometry.PolylineCurve(self._base_triangle)
            plane = Rhino.Geometry.Plane.WorldXY

            
            plane.Origin = self.origin + Rhino.Geometry.Point3d(self.width/2, 0, 0)
            
            xform = Rhino.Geometry.Transform.Scale(plane, self._opening_width_factor, self._opening_height_factor, 1)

            self._entry_triangle.Transform(xform)
            return True
        self._entry_triangle = None
        return False

    def _generate_entry_flap_triangle(self):
        if self.has_entry and self._entry_triangle:
            point_a = self._entry_triangle.Point(1)
            point_b = self.origin + Rhino.Geometry.Point3d(self.width * TENT_ENTRY_FLAP_WIDTH_RATIO, self.height * TENT_ENTRY_FLAP_HEIGHT_RATIO, 0)
            point_c = self._entry_triangle.Point(2)
            self._flap_triangle = Rhino.Geometry.PolylineCurve([point_a, point_b, point_c, point_a])
            return True
        self._flap_triangle = None
        return False

    def _generate_apex_pole(self):

        if self._base_triangle:
            dir_a = (self._base_triangle.Point(2) - self._base_triangle.Point(0))
            dir_a *= TENT_APEX_EXTENSION_RATIO

            dir_c = (self._base_triangle.Point(2) - self._base_triangle.Point(1))
            dir_c *= TENT_APEX_EXTENSION_RATIO

            point_a = self._base_triangle.Point(2) + dir_a
            point_c = self._base_triangle.Point(2) + dir_c

            line_a = Rhino.Geometry.Line(self._base_triangle.Point(0), point_a)
            line_b = Rhino.Geometry.Line(self._base_triangle.Point(1), point_c)

            #self._apex_pole_extension = Rhino.Geometry.PolylineCurve([point_a, self._base_triangle.Point(2), point_c])
            self._apex_pole_extension = [line_a, line_b]
            return True

        self._apex_pole_extension = []
        return False
    
    def _generate_surfaces(self):

        self._geometry = [] + self._apex_pole_extension
        
        negative = []
        if self.has_cap:
            self._cap_geometry = Rhino.Geometry.Brep.CreatePlanarBreps(self._cap_triangle)[0]
            self._geometry.append(self._cap_geometry)
            negative.append(self._cap_triangle)
        if self.has_entry:
            self._entry_geometry = Rhino.Geometry.Brep.CreatePlanarBreps(self._entry_triangle)[0]
            self._geometry.append(self._entry_geometry)
            negative.append(self._entry_triangle)
            negative.append(self._flap_triangle)
        if negative:
            self._base_geometry = Rhino.Geometry.Brep.CreatePlanarBreps(Rhino.Geometry.Curve.CreateBooleanDifference(self._base_triangle, negative))[0]
        else:
            self._base_geometry = Rhino.Geometry.Brep.CreatePlanarBreps(self._base_triangle)[0]
        self._geometry.append(self._base_geometry)

        return self._geometry
    #endregion PRIVATE METHODS
    
    def generate_geometry(self):
        self._generate_base_triangle()
        self._generate_cap_triangle()
        self._generate_entry_triangle()
        self._generate_entry_flap_triangle()
        self._generate_apex_pole()
        self._generate_surfaces()

        return self._geometry

    def DrawViewportWires(self, args):
        # Draw Tent Base
        args.Pipeline.DrawBrepShaded(self._base_geometry, self._primary_material)
        # Draw Pole Extension
        for line in self._apex_pole_extension:
            args.Pipeline.DrawLine(line, self._primary_material.Diffuse, 5)
        # Draw Cap
        if self.has_cap:
            args.Pipeline.DrawBrepShaded(self._cap_geometry, self._secondary_material)
        # Draw Entry
        if self.has_entry:
            args.Pipeline.DrawBrepShaded(self._entry_geometry, self._secondary_material)
    
    def GetBoundingBox(self):
        if self._base_triangle:
            return self._base_triangle.GetBoundingBox(False)
        else:
            return Rhino.Geometry.BoundingBox.Empty
    
    def __str__(self):
        return self.__class__.__name__
    
    def __repr__(self):
        return self.__str__()
    
    def ToString(self):
        return self.__str__()
