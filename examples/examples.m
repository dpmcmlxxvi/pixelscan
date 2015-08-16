function examples

    drawscan('circlescan.csv', 'circlescan.png', @chebyshevmap);
    drawscan('gridscan.csv', 'gridscan.png', @gridymap);
    drawscan('chebyshev.csv', 'chebyshev.png', @chebyshevmap);
    drawscan('manhattan.csv', 'manhattan.png', @manhattanmap);
    drawscan('snakescan.csv', 'snakescan.png', @gridymap);
    drawscan('walkscan.csv', 'walkscan.png', @gridxmap);

end

function drawscan(filepoints, fileimage, scanmap)

    % ==================================================
    % READ POINTS
    % --------------------------------------------------
    points = csvread(filepoints);
    
    % Flip from pixel to image coordinates
    points(:,2) = -points(:,2);

    % ==================================================
    % CREATE POINT LABELS
    % --------------------------------------------------
    npoints = size(points,1);
    minxy = min(points);
    maxxy = max(points);
    labels = mat2cell(num2str((1:npoints)'), ones(npoints,1));

    % ==================================================
    % CREATE GRID LINES
    % --------------------------------------------------
    gridx = (floor(minxy(1)) - 0.5 : ceil(maxxy(1)) + 0.5);
    gridxi = [gridx; gridx];
    gridxj = repmat([minxy(2) - 0.5; maxxy(2) + 0.5], 1, length(gridx));

    gridy = (floor(minxy(2)) - 0.5 : ceil(maxxy(2)) + 0.5);
    gridyi = repmat([minxy(1) - 0.5; maxxy(1) + 0.5], 1, length(gridy));
    gridyj = [gridy; gridy];

    % ==================================================
    % CREATE MAP COLORS
    % --------------------------------------------------
    nx = length(gridx);
    ny = length(gridy);
    [map] = scanmap(nx, ny);

    % ==================================================
    % PLOT MAP COLORS
    % --------------------------------------------------
    figure('Visible','off');

    imagesc(gridx(1:end-1)+0.5, gridy(1:end-1)+0.5, map(1:end-1, 1:end-1));
    colormap prism;
    hold on;

    % ==================================================
    % PLOT POINT LABELS
    % --------------------------------------------------
    text(points(:,1), points(:,2), labels, 'FontSize', 5, ...
        'FontWeight', 'bold', 'HorizontalAlignment', 'center');

    % ==================================================
    % PLOT GRID LINES
    % --------------------------------------------------
    plot(gridxi, gridxj, 'k', 'LineWidth', 1.0);
    plot(gridyi, gridyj, 'k', 'LineWidth', 1.0);
    
    axis equal;
    axis off;
    
    % ==================================================
    % SAVE FIGURE
    % --------------------------------------------------
    [~, ~, extension] = fileparts(fileimage);

    fig = gcf;
    fig.InvertHardcopy = 'off';
    fig.PaperUnits = 'inches';
    fig.PaperPosition = [0 0 1.5 1.5];
    fig.PaperSize = [1.5 1.5];
    fig.PaperPositionMode = 'manual';
    fig.Renderer = 'painters';
    set(gca,'position', [0.02, 0.02, 0.96, 0.96], 'units', 'normalized');
    set(gca,'color','none');

    saveas(gcf, fileimage, extension(2:end));
    close all hidden;

end

function [map] = chebyshevmap(nx, ny)

    [x, y] = meshgrid(1:nx, 1:ny);
    map = max(abs(x - nx/2), abs(y - ny/2));

end

function [map] = circlemap(nx, ny)

    [x, y] = meshgrid(1:nx, 1:ny);
    map = (sqrt((x - nx/2).^2 + (y - ny/2).^2));

end

function [map] = gridxmap(nx, ny)

    [x, ~] = meshgrid(1:nx, 1:ny);
    map = x;

end

function [map] = gridymap(nx, ny)

    [~, y] = meshgrid(1:nx, 1:ny);
    map = y;

end

function [map] = manhattanmap(nx, ny)

    [x, y] = meshgrid(1:nx, 1:ny);
    map = (abs(x - nx/2) + abs(y - ny/2));

end
