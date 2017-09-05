classdef Animator < handle
% classdef Animator < handle
% Base class for doing animation inside a MATLAB figure
    properties ( Access = protected )
        fig = [];
        anim_obj = [];  % Animation object to be displayed
        neg_axis_scale = 1;
        pos_axis_scale = 1;
        min_axis_width = 2;
    end

    methods ( Access = protected )
        function updateAxis(Obj, translate)
            % oom = Obj.min_axis_width + abs(translate);  % Get the order of magnitude
            oom = Obj.min_axis_width * ones(size(translate)); % Keeping the correct size for potential future use

            %{
            % X Axis limits
            xmin = translate(1) - Obj.neg_axis_scale * oom(1);
            xmax = translate(1) + Obj.pos_axis_scale * oom(1);

            % Y Axis limits
            ymin = translate(2) - Obj.neg_axis_scale * oom(2);
            ymax = translate(2) + Obj.pos_axis_scale * oom(2);

            % Z Axis limits
            zmin = translate(3) - Obj.neg_axis_scale * oom(3);
            zmax = translate(3) + Obj.pos_axis_scale * oom(3);
            %}
            axis_size = 4;

            % X Axis limits
            xmin = -axis_size;
            xmax = axis_size;

            % Y Axis limits
            ymin = -axis_size;
            ymax = axis_size;

            % Z Axis limits
            zmin = -axis_size;
            zmax = axis_size;

            %{
            % X Axis limits
            xmin = - Obj.neg_axis_scale * oom(1);
            xmax = + Obj.pos_axis_scale * oom(1);

            % Y Axis limits
            ymin = - Obj.neg_axis_scale * oom(2);
            ymax = + Obj.pos_axis_scale * oom(2);

            % Z Axis limits
            zmin = - Obj.neg_axis_scale * oom(3);
            zmax = + Obj.pos_axis_scale * oom(3);
            %}
            axis([xmin xmax ymin ymax zmin zmax]);
            drawnow;
        end
    end

    methods ( Access = public )
        function Obj = Animator(ao, ao_parms)
            % Initialize a new figure object
            Obj.fig = figure();

            % AO should be a function handle to the object that you want to
            % instantiate
            Obj.anim_obj = ao(Obj.fig, ao_parms{:}); 
        end

        function animate(Obj, data)
            figure(Obj.fig);    % bring the object's figure into focus 

            % Wait for a keystroke to continue the animation
            disp('Click or Press Any key to continue');
            key_press = waitforbuttonpress;

            % The code here is based on Github source gibiansky/experiments
            for t = 1:length(data.tpts)
                dx = data.position(:, t);
                dtheta = data.angles(:, t);
                move = makehgtform('translate', dx);

                rotation_mat = [rotationMatrix(dtheta), zeros(3, 1); ...
                    zeros(1, 3), 1];

                % Update the animation object's matrix
                Obj.anim_obj.setMatrix(move * rotation_mat);

                % Update the axis
                Obj.updateAxis(dx);
            end
        end

        function initialize()
        % Initialize the axes and other 1-time initializations in this function. It is not clear if this
        % function should be accessible as a public function.

        end
    end
end
