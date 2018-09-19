% Display the target shape from a particular block/trial
% response = the struct containing data from a session of the Drewes experiment

function showContour(response,blockNo,trialNo)

trialLines = response.Data.lineInfo{blockNo}{trialNo}; % struct with data from this block/trial
contour = trialLines.signalLines{1}; % target shape (first presentation)
noise = trialLines.distractorsLines{1}; % noise lines (on the frame with the target)
loc = trialLines.signalInfo.location; % target location
ori = trialLines.signalInfo.orientation; % target orientation
signalFrames = trialLines.intervalIndex; % which frames included target

% Draw the target shape
figure;
plot(real(contour),imag(contour),'k-','LineWidth',2);
axis image
title(['Target contour on block ' int2str(blockNo) ' trial ' int2str(trialNo)]);