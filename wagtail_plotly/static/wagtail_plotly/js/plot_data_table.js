'use strict';

function barPlotTable(containerId, options) {

    var firstRowRenderer = function(instance, td, row, col, prop, value, cellProperties) {
        Handsontable.renderers.TextRenderer.apply(this, arguments);
        td.style.fontWeight = 'bold';
        td.style.textAlign = "center";
        td.style.background = '#FEEEEE';
    }

    var firstColRenderer  = function(instance, td, row, col, prop, value, cellProperties) {
        Handsontable.renderers.TextRenderer.apply(this, arguments);
        td.style.fontWeight = 'bold';
        td.style.background = '#F4F4F4';
    }

    var colHeader = function(col, th) {
        if (col == 0) {
            th.textContent = 'X';
        } else if (col > 0) {
            th.textContent = 'Y' + (col - 1);
        } else {
            th.textContent = '';
        }
    };

    var rowHeader = function(row, th) {
        if (row == 0) {
            th.textContent = 'Name';
        } else if (row > 0) {
            th.textContent = 'D' + (row - 1);
        } else {
            th.textContent = '';
        }
    };

    options['cells'] = function(row, col, prop) {
        var cellProperties = {};

        if (row === 0) {
            cellProperties.renderer = firstRowRenderer;
        } else if (col === 0) {
            cellProperties.renderer = firstColRenderer;
        } else {
            cellProperties.type = 'numeric';
        }
        return cellProperties;
    }

    var hot = new Handsontable(document.getElementById(containerId), options);

    hot.addHook('afterGetColHeader', colHeader);
    hot.addHook('afterGetRowHeader', rowHeader);

    return hot;
}


function contourPlotTable(containerId, options) {

    var axisRenderer = function(instance, td, row, col, prop, value, cellProperties) {
        Handsontable.renderers.TextRenderer.apply(this, arguments);

        td.style.fontWeight = 'bold';

        if ((row === 0) && (col === 0)) {
            cellProperties.readOnly = 'true';
            td.textContent = 'Axis (x/y)';
            td.style.background = '#F4F4F4';
            td.style.textAlign = 'center';
        } else {
            td.style.background = '#FEEEEE';
            td.style.textAlign = 'center';
        }
    }

    var rowHeader = function(row, th) {
        if (row > 0) {
            th.textContent = 'Y' + (row - 1);
        } else {
            th.textContent = '';
        }
    };

    var colHeader = function(col, th) {
        if (col > 0) {
            th.textContent = 'X' + (col - 1);
        } else {
            th.textContent = '';
        }
    };

    // Setup cell properties
    options['cells'] = function(row, col, prop) {
        var cellProperties = {};

        if ((row === 0) || (col === 0)) {
            cellProperties.renderer = axisRenderer;
        } else {
            cellProperties.type = 'numeric';
        }
        return cellProperties;
    }

    var hot = new Handsontable(document.getElementById(containerId), options);

    hot.addHook('afterGetColHeader', colHeader);
    hot.addHook('afterGetRowHeader', rowHeader);

    return hot;
}


function linePlotTable(containerId, options) {

    var firstRowRenderer = function(instance, td, row, col, prop, value, cellProperties) {
        Handsontable.renderers.TextRenderer.apply(this, arguments);
        td.style.fontWeight = 'bold';
        td.style.textAlign = "center";
        td.style.background = '#FEEEEE';
    }

    var firstColRenderer  = function(instance, td, row, col, prop, value, cellProperties) {
        Handsontable.renderers.TextRenderer.apply(this, arguments);
        td.style.fontWeight = 'bold';
        td.style.background = '#F4F4F4';
    }

    var colHeader = function(col, th) {
        if (col == 0) {
            th.textContent = 'X';
        } else if (col > 0) {
            th.textContent = 'Y' + (col - 1);
        } else {
            th.textContent = '';
        }
    };

    var rowHeader = function(row, th) {
        if (row == 0) {
            th.textContent = 'Name';
        } else if (row > 0) {
            th.textContent = 'D' + (row - 1);
        } else {
            th.textContent = '';
        }
    };

    options['cells'] = function(row, col, prop) {
        var cellProperties = {};

        if (row === 0) {
            cellProperties.renderer = firstRowRenderer;
        } else if (col === 0) {
            cellProperties.renderer = firstColRenderer;
        } else {
            cellProperties.type = 'numeric';
        }
        return cellProperties;
    }

    var hot = new Handsontable(document.getElementById(containerId), options);

    hot.addHook('afterGetColHeader', colHeader);
    hot.addHook('afterGetRowHeader', rowHeader);

    return hot;
}


function piePlotTable(containerId, options) {

    var firstColRenderer  = function(instance, td, row, col, prop, value, cellProperties) {
        Handsontable.renderers.TextRenderer.apply(this, arguments);
        td.style.fontWeight = 'bold';
        td.style.background = '#F4F4F4';
    }

    options['cells'] = function(row, col, prop) {
        var cellProperties = {};

        if (col === 0) {
            cellProperties.renderer = firstColRenderer;
        } else {
            cellProperties.type = 'numeric';
        }
        return cellProperties;
    }

    var hot = new Handsontable(document.getElementById(containerId), options);

    return hot;
}


function scatterPlotTable(containerId, options) {

    var nameRowRenderer = function(instance, td, row, col, prop, value, cellProperties) {
        Handsontable.renderers.TextRenderer.apply(this, arguments);
        td.style.fontWeight = 'bold';
        td.style.textAlign = "center";
        td.style.background = '#FEEEEE';
    }

    var xColRenderer = function(instance, td, row, col, prop, value, cellProperties) {
        cellProperties.type = 'numeric';
        Handsontable.renderers.TextRenderer.apply(this, arguments);
        td.style.background = '#F4F4F4';
        td.style.textAlign = 'right';
    }

    var rowHeader = function(row, th) {
        if (row == 0) {
            th.textContent = 'Name';
        } else if (row > 0) {
            th.textContent = 'D' + (row - 1);
        } else {
            th.textContent = '';
        }
    };

    var colHeader = function(col, th) {
        if (col >= 0) {
            th.textContent = ((col % 2 === 0) ? 'X' : 'Y') + Math.floor(col / 2);
        } else {
            th.textContent = '';
        }
    };

    // Setup cell properties
    options['cells'] = function(row, col, prop) {
        var cellProperties = {};

        if (row === 0) {
            cellProperties.renderer = nameRowRenderer;
        } else if (col % 2 === 0) {
            cellProperties.renderer = xColRenderer;
        } else {
            cellProperties.type = 'numeric';
        }
        return cellProperties;
    }

    var hot = new Handsontable(document.getElementById(containerId), options);

    hot.addHook('afterGetColHeader', colHeader);
    hot.addHook('afterGetRowHeader', rowHeader);

    return hot;
}


function initPlotDataTable(id, tableOptions) {
    var containerId = id + '-handsontable-container';
    var hiddenStreamInput = $('#' + id);
    var hot;
    var options = {};
    var data = null;
    var isInitialized = false;
    var plotType = tableOptions['plotType'];

    try {
        data = JSON.parse(hiddenStreamInput.val());
    } catch (e) {
        // do nothing
    }

    var persist = function() {
        hiddenStreamInput.val(
            JSON.stringify(hot.getData())
        );
    };

    var cellEvent = function(change, source) {
        if (source === 'loadData') {
            return; //don't save this change
        }
        persist();
    };

    var initEvent = function() {
        isInitialized = true;
    };

    // Setup the table options
    var defaultOptions = {
        afterChange: cellEvent,
        afterCreateCol: persist,
        afterCreateRow: persist,
        afterRemoveCol: persist,
        afterRemoveRow: persist,
        afterColumnMove: persist,
        afterRowMove: persist,
        afterInit: initEvent,
    };

    if (data !== null) {
        defaultOptions.data = data;
    }

    Object.keys(defaultOptions).forEach(function (key) {
        options[key] = defaultOptions[key];
    });
    Object.keys(tableOptions).forEach(function (key) {
        options[key] = tableOptions[key];
    });

    // Create a table based on the plot type
    switch (plotType) {
        case 'bar':
            hot = barPlotTable(containerId, options);
            break;

        case 'contour':
            hot = contourPlotTable(containerId, options);
            break;

        case 'line':
            hot = linePlotTable(containerId, options);
            break;

        case 'pie':
            hot = piePlotTable(containerId, options);
            break;

        case 'scatter':
            hot = scatterPlotTable(containerId, options);
            break;
    }

    if (hot) {
        hot.render();
    }
}
