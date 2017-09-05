classdef AnimationData < handle
% classdef AnimationData < handle
% Class responsible for deciding on the format in which simulation data should be provided to the Animator class
    properties ( Access = public )
        dof = 0;
        tpts = []; % Time points
        position = [];  % Position coordinates
        angles = [];    % Three Euler angles descibing the angular position
    end

    methods ( Access = protected )
        function checkDimensions(Dat, vec)
            if ( size(vec, 2) ~= length(Dat.tpts) )
                fprintf('TPTS = %d x %d, VEC = %d x %d\n', size(Dat.tpts, 1), ...
                    size(Dat.tpts, 2), size(vec, 1), size(vec, 2));
                error('Mismatch in TPTS and allocated vector''s size. Aborting.');
            elseif ( size(vec, 1) ~= Dat.dof )
                fprintf('DOF = %d, VEC = %d x %d\n', Dat.dof, size(vec, 1), ...
                    size(vec, 2));
                error('Mismatch in DOF and the allocated vector''s size. Aborting'); 
            end
        end
    end

    methods ( Access = public )
        function Dat = AnimationData(dof, tpts, position, angles)
            narginchk(1, 4);    % Providing NO arguments in NOT OK
            Dat.dof = dof;
            % Doing the default allocations (single time-point), based on the
            % dof provided here in the constructor
            Dat.position = zeros(Dat.dof, 1);
            Dat.angles = zeros(Dat.dof, 1);

            if (nargin > 1)
                Dat.setTPts(tpts);
                % Position assignment
                if (nargin > 2)
                    Dat.setPosition(position);
                else    % Assume that the position never changes over time
                    Dat.position = repmat(Dat.position, [1, length(Dat.tpts)]);
                end

                % Angle assignment
                if (nargin > 3)
                    Dat.setAngles(angles);
                else
                    Dat.angles = repmat(Dat.angles, [1, length(Dat.tpts)]);
                end
            end
        end

        function setTPts(Dat, tpts)
            if ( ~isvector(tpts) )
                error('Allocated TPTS is not a column vector. Please Check');
            end
            Dat.tpts = tpts; 
        end

        function setPosition(Dat, position)
            Dat.checkDimensions(position);
            Dat.position = position;
        end

        function setAngles(Dat, angles)
            Dat.checkDimensions(angles);
            Dat.angles = angles;
        end
    end
end
