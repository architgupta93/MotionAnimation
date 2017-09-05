clc; close all;
% Initializing object to descibe the animation data (trajectory for the object
% in this case)
tpts = [0:5e-3:2];    % A total time of 2 seconds being stepped by 10ms

position = [sin(2*pi*tpts); cos(2*pi*tpts); zeros(size(tpts))];   % Moving in a planar
                                                        % circle
ad = AnimationData(3, tpts, position);  % Angles remain constant (Not supplied)

% Supplying a function handle for the constructor of the animation object
pt_object = @QuadrotorObject;
pt_args = {[]};    % Only one argument has to be passed into the constructor,
                    % this is the radius of the sphere in this example

% Initializing the animator and calling the animate function on it
ao = Animator(pt_object, pt_args);
ao.animate(ad);
