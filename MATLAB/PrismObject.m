classdef PrismObject < AnimationObject
% classdef PrismObject < AnimationObject
% Creates a 3D prism with its center at (x, y, z) and sizes given by width (w), length (l), and height (h)
    properties ( Access = protected )
        % Size variables
        p__length = 1;
        p__width = 1;
        p__height = 1;

        % Faces are stored in the graphics object
    end

    methods ( Access = private )
        function [X, Y, Z] = prismFaces(Obj)
            % Internal function: Copy class members for more readable code
            x = Obj.p__x;
            y = Obj.p__y;
            z = Obj.p__z;
            w = Obj.p__width;
            l = Obj.p__length;
            h = Obj.p__height;

            % Lists out the coordinates for the 8 vertices of a prism (cuboid)
            %       2---1
            %  If   |   |  is the size view of the prism (Y-Z axis), then the numbers alongside give the order of points
            %       3---4
            % In the figure above, horizontal direction is Y, vertical is Z and into the plane of the screen is X

            X = [   x + w/2, x + w/2, x + w/2, x + w/2, ...
                    x - w/2, x - w/2, x - w/2, x - w/2  ];
            Y = [   y + l/2, y - l/2, y - l/2, y + l/2, ...
                    y + l/2, y - l/2, y - l/2, y + l/2  ];
            Z = [   z + h/2, z + h/2, z - h/2, z - h/2, ...
                    z + h/2, z + h/2, z - h/2, z - h/2  ];
        end
    end

    methods ( Access = public )
        function Obj = PrismObject(fighandle, varargin)
        % function Obj = PrismObject(fighandle, position, wlh)
            Obj = Obj@AnimationObject(fighandle, varargin{:});
            if ( nargin > 2 )
                Obj.p__width  = varargin{2}(1); 
                Obj.p__length = varargin{2}(2);
                Obj.p__height = varargin{2}(3); 
            end

            [X, Y, Z] = Obj.prismFaces();
            faces = zeros(6, 4);    % Faces of the prism
            % Faces in the Y-Z plane
            faces(1, :) = [1 2 3 4];
            faces(2, :) = [1 2 3 4] + 4;

            % Faces in the X-Y plane
            faces(3, :) = [1 2 6 5];
            faces(4, :) = [1 2 6 5] + 2;

            % Faces in the X-Z plane
            faces(5, :) = [2 3 7 6];
            faces(6, :) = [1 4 8 5];

            Obj.graphics_obj = fill3( X(faces(1, :)), Y(faces(1, :)), Z(faces(1, :)), 'b' ); 
            hold on;
            for fi = 2 : size(faces, 1)
                Obj.graphics_obj(fi) = fill3( X(faces(fi, :)), Y(faces(fi, :)), Z(faces(fi, :)), 'b' ); 
                hold on;
            end
            grid on;
            Obj.copyToTFObj();
        end 
    end
end
