clc; close all;

% Initializing object to descibe the animation data (trajectory for the object
% in this case)
tpts = [0:1e-2:2];    % A total time of 2 seconds being stepped by 10ms

position = [sin(2*pi*tpts); cos(2*pi*tpts); zeros(size(tpts))];   % Moving in a planar
angles = [zeros(size(tpts)); zeros(size(tpts)); 2*pi*tpts];
                                                        % circle
ad = AnimationData(3, tpts, position, angles);

% Supplying a function handle for the constructor of the animation object
pt_object = @PrismObject;
pt_args = {};    % Only one argument has to be passed into the constructor,
                    % this is the radius of the sphere in this example

% Initializing the animator and calling the animate function on it
ao = Animator(pt_object, pt_args);
ao.animate(ad);
