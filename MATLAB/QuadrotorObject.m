classdef QuadrotorObject < AnimationObject
% classdef QuadrotorObject < AnimationObject
% Extends the abstract AnimationObject class to draw the various parts of a quadrotor: Two axis depicting the frame and
% 4 spheres representing the motors.
% Using code from GIBIANSKY/EXPERIMENTS on Github.com
% Shapes involved in the quadrotor object:
%   
    properties ( Access = protected, Constant ) % Dimensions
        frame_width = 1;
        frame_thickness = 0.2;
        motor_radius = 0.1;
    end

    methods ( Access = protected ) % Local functions

    end

    methods ( Access = public )
        function Obj = QuadrotorObject(fighandle, varargin)
            Obj = Obj@AnimationObject(fighandle, varargin{:});

            % Drawing the arms of the quadrotor
            center_pr1 = [0; 0; 0]; % Center for prism 1
            center_pr2 = [0; 0; 0]; % Center for prism 2
            wlh_pr1 = [Obj.frame_width; Obj.frame_thickness; Obj.frame_thickness];   % Dimensions for prism 1
            wlh_pr2 = [Obj.frame_thickness; Obj.frame_width; Obj.frame_thickness];   % Dimensions for prism 2

            Obj.children{1} = PrismObject(fighandle, center_pr1, wlh_pr1);
            Obj.children{2} = PrismObject(fighandle, center_pr2, wlh_pr2);

            % Drawing the 4 spheres (Depicting motors)
            c_m1 = [Obj.frame_width/2 + Obj.motor_radius; 0; 0];
            c_m2 = [0; Obj.frame_width/2 + Obj.motor_radius; 0];
            c_m3 = [-Obj.frame_width/2 - Obj.motor_radius; 0; 0];
            c_m4 = [0; -Obj.frame_width/2 - Obj.motor_radius; 0];

            Obj.children{3} = PointObject(fighandle, c_m1, Obj.motor_radius);
            Obj.children{4} = PointObject(fighandle, c_m2, Obj.motor_radius);
            Obj.children{5} = PointObject(fighandle, c_m3, Obj.motor_radius);
            Obj.children{6} = PointObject(fighandle, c_m4, Obj.motor_radius);
            
            % Merge all the graphics objects into a single transform object
            Obj.mergeChildren();
        end
    end
end
