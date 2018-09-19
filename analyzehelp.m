data = load('replicationDY16052012-1542.mat')
%% Collect data from files
c = 1;
trialData = [];
acc = [];
for n = 1:length(dataFile)
    data = load('replicationDY16052012-1542.mat');
    
    % Delays used in the experiment
    timeSeq = unique(data.response.fixationDisplayTimeSeq);
    
    % Make delay labels for figures
    delayLabel = {};
    for j = 1:(length(timeSeq)-1)
        delayLabel{j} = int2str(1000*timeSeq(j+1));
    end
    
    % Foh delay
    for j = 1:length(timeSeq)
        
		% Identify blocks with this delay
        blocks = find(data.response.fixationDisplayTimeSeq == timeSeq(j));
        for b = 1:length(blocks)
            gt = data.response.imageObjectFlagSeq{blocks(b)}; % ground truth
            resp = data.response.Data.Response{blocks(b)}; % subject's response
            
            % Accuracy
            correct = resp == gt;
            acc(j,c-1+b) = mean(correct)
   
            % Number of distractors - original (Drewes) code only saves the
			% rounded values, but braket code saves non-rounded values
            QUESTdist = data.response.Data.numDistractors{blocks(b)};
            try
                QUESTfinal = data.response.qSaved{blocks(b)};
                nDistFinal = 1./(10.^(QuestMean(QUESTfinal))); % not rounded (braket only)
            catch
                nDistFinal = QUESTdist(end) % rounded (Drewes replication)
            end
            nDist(j,c-1+b) = nDistFinal
            
            
			% Add block data to a matrix
            thisBlock = [n*ones(size(gt')) b*ones(size(gt')) 1000*timeSeq(j)*ones(size(gt')) (1:length(gt))' gt' resp' QUESTdist' nDistFinal*ones(size(gt'))];
            trialData = [trialData; thisBlock];
            
        end
        
    end
    c = c + length(blocks);
end

%% FIGURES
acc = rand(7,6)
nDist = rand(7,6)
% Average over block and session
mean_acc = mean(acc,2)
mean_nDist = mean(nDist,2)

% Accuracy
figure
plot(timeSeq(2:end),mean_acc(2:end),'k-','LineWidth',2); hold on
plot(timeSeq(2:end),repmat(mean_acc(1),size(timeSeq(2:end))),'k--','LineWidth',2);
for c = 1:size(acc,2)
    plot(timeSeq(2:end),acc(2:end,c),'k:','LineWidth',1); hold on
    plot(timeSeq(2:end),repmat(acc(1,c),size(timeSeq(2:end))),'k:','LineWidth',1);
end
set(gca, 'xtick', timeSeq(2:end)); set(gca, 'xticklabel', delayLabel); xlabel('Delay (msec)');
ylim([0.5 1]); ylabel('Proportion correct');
legend({'Dual presentation','Single presentation'},'Location','northeast');
%title([subID ' Accuracy (target: ket-bra, distractor: bra-ket, serifs = 50%)']);
title([titleTxt ' - Accuracy (' subID ')']);

% Number of distractors
figure
plot(timeSeq(2:end),mean_nDist(2:end),'k-','LineWidth',2); hold on
plot(timeSeq(2:end),repmat(mean_nDist(1),size(timeSeq(2:end))),'k--','LineWidth',2);
for c = 1:size(nDist,2)
    plot(timeSeq(2:end),nDist(2:end,c),'k:','LineWidth',1); hold on
    plot(timeSeq(2:end),repmat(nDist(1,c),size(timeSeq(2:end))),'k:','LineWidth',1);
end
set(gca, 'xtick', timeSeq(2:end)); set(gca, 'xticklabel', delayLabel); xlabel('Delay (msec)');
%ylim([0 6]);
ylabel('Number of distractors');
legend({'Dual presentation','Single presentation'},'Location','northeast');
%title([subID ' N distractors (target: ket-bra, distractor: bra-ket, serifs = 50%)']);
title([titleTxt ' - N distractors (' subID ')']);
