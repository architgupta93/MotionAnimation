classdef PointObject < AnimationObject
% classdef PointObject < AnimationObject
% This class descibes a point object, which is displayed as a sphere of a given
% radius.
    properties ( Access = private )
        radius = 1;
    end
    
    methods ( Access = protected )

    end

    methods ( Access = public )
        function Obj = PointObject(fighandle, varargin)
        % function Obj = PointObject(fighandle, position, radius)
            Obj = Obj@AnimationObject(fighandle, varargin{:});
            if ( nargin > 2 )
               Obj.radius = varargin{2};
            end 
            [x, y, z] = sphere;
            x = Obj.radius * x + Obj.p__x;
            y = Obj.radius * y + Obj.p__y;
            z = Obj.radius * z + Obj.p__z;

            % Resizing the x, y, and z coordinates according to the given radius
            % of the sphere
            Obj.graphics_obj = surf(x, y, z, Obj.graphics_opts{:});
            Obj.copyToTFObj();
        end
    end
end
