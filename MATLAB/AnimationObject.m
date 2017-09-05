classdef AnimationObject < handle
% classdef AnimationObject < handle
% This class creates an animation object using the HGTRANSFORM class. The object
% can be used later for animations.
    properties ( Access = protected )
        graphics_obj = [];
        tf_obj = [];    % A transform object instantiated in the constructed
                        % using a figure handle (using its axes)
        % Other animation objects that might have to be added
        children = {};

        % Arguments to be passed into the plot functions 
        graphics_opts = {};

        % Position Variables
        p__x = 0;
        p__y = 0;
        p__z = 0;

        % Angular Position Variables
        p__roll = 0;
        p__pitch = 0;
        p__yaw = 0;
    end

    methods ( Access = protected )
        function copyToTFObj(Obj)
            Obj.tf_obj.Parent = Obj.graphics_obj.Parent;

            % Assigning the parent for this object to be Obj.tf_obj. This modifies the Object on the RHS to contain the
            % graphics object, which in this case is a surf
            set(Obj.graphics_obj, 'Parent', Obj.tf_obj);
        end

        function mergeChildren(Obj)
        % Instead of taking elementary graphics objects and merging them together, we have several children, each of
        % which is an Animation Object and we merge them together
            h(1) = Obj.children{1}.tf_obj;
            Obj.tf_obj.Parent = h(1).Parent;
            for i = 2 : length(Obj.children)
                h(i) = Obj.children{i}.tf_obj;
            end
            set(h, 'Parent', Obj.tf_obj);
        end
    end

    methods ( Access = public )
        function Obj = AnimationObject(fighandle, varargin)
            figure(fighandle);  % Bringing the figure into focus

            % Create a new Transform Object which contains a placeholder for the graphics object we will be putting in
            % later on.
            Obj.tf_obj = copy(hgtransform);

            % Since the Parent Axis is not copied by the copy function, we have to do that manually

            % This object has a field 'Children', which is initialized as a 0x0 GraphicsPlaceholder and can be
            % substituted with a graphics object like a plot/surf/mesh etc.
            if ( nargin > 1 )
                position = varargin{1};
                if ( ~isempty(position) )
                    Obj.p__x = position(1);
                    Obj.p__y = position(2);
                    Obj.p__z = position(3);
                end
            end
        end
        
        function setMatrix(Obj, mat)
            Obj.tf_obj.Matrix = mat;
            drawnow;
        end

        function setGraphicsOpts(Obj, opts)
            Obj.graphics_opts = opts;
        end
    end
end
