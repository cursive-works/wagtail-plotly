'use strict';

const greyColor = '#F4F4F4';
const pinkColor = '#FEEEEE';
const greenColor = '#F2FCFC';

function barPlotTable(containerId, options) {

    var firstRowRenderer = function(instance, td, row, col, prop, value, cellProperties) {
        Handsontable.renderers.TextRenderer.apply(this, arguments);
        td.style.fontWeight = 'bold';
        td.style.textAlign = 'center';
        td.style.background = pinkColor;
    }

    var firstColRenderer  = function(instance, td, row, col, prop, value, cellProperties) {
        Handsontable.renderers.TextRenderer.apply(this, arguments);
        td.style.fontWeight = 'bold';
        td.style.background = greyColor;
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


function bubblePlotTable(containerId, options) {

    var nameRowRenderer = function(instance, td, row, col, prop, value, cellProperties) {
        Handsontable.renderers.TextRenderer.apply(this, arguments);
        td.style.fontWeight = 'bold';
    }

    var rowHeader = function(row, th) {
        th.textContent = 'D' + row;
    };

    // Setup cell properties
    options['cells'] = function(row, col, prop) {
        var cellProperties = {};

        if (col === 0) {
            cellProperties.renderer = nameRowRenderer;
        } else {
            cellProperties.type = 'numeric';
        }
        return cellProperties;
    }

    var hot = new Handsontable(document.getElementById(containerId), options);

    return hot;
}


function contourPlotTable(containerId, options) {

    var axisRenderer = function(instance, td, row, col, prop, value, cellProperties) {
        Handsontable.renderers.TextRenderer.apply(this, arguments);

        td.style.fontWeight = 'bold';

        if ((row === 0) && (col === 0)) {
            cellProperties.readOnly = 'true';
            td.textContent = 'Axis (x/y)';
            td.style.background = greyColor;
            td.style.textAlign = 'center';
        } else {
            td.style.background = pinkColor;
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


function dotPlotTable(containerId, options) {

    var firstRowRenderer = function(instance, td, row, col, prop, value, cellProperties) {
        Handsontable.renderers.TextRenderer.apply(this, arguments);
        td.style.fontWeight = 'bold';
        td.style.textAlign = 'center';
        td.style.background = pinkColor;
    }

    var firstColRenderer  = function(instance, td, row, col, prop, value, cellProperties) {
        Handsontable.renderers.TextRenderer.apply(this, arguments);
        td.style.fontWeight = 'bold';
        td.style.background = greyColor;
    }

    var colHeader = function(col, th) {
        if (col == 0) {
            th.textContent = 'Y';
        } else if (col > 0) {
            th.textContent = 'X' + (col - 1);
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


function linePlotTable(containerId, options) {

    var firstRowRenderer = function(instance, td, row, col, prop, value, cellProperties) {
        Handsontable.renderers.TextRenderer.apply(this, arguments);
        td.style.fontWeight = 'bold';
        td.style.textAlign = 'center';
        td.style.background = pinkColor;
    }

    var firstColRenderer  = function(instance, td, row, col, prop, value, cellProperties) {
        Handsontable.renderers.TextRenderer.apply(this, arguments);
        td.style.fontWeight = 'bold';
        td.style.background = greyColor;
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
        td.style.background = pinkColor;
    }

    var rowHeader = function(row, th) {
        th.textContent = 'D' + row;
    };

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

    hot.addHook('afterGetRowHeader', rowHeader);

    return hot;
}


function scatterPlotTable(containerId, options) {

    var nameRowRenderer = function(instance, td, row, col, prop, value, cellProperties) {
        Handsontable.renderers.TextRenderer.apply(this, arguments);
        td.style.fontWeight = 'bold';
        td.style.textAlign = 'center';
        td.style.background = pinkColor;
    }

    var xColRenderer = function(instance, td, row, col, prop, value, cellProperties) {
        cellProperties.type = 'numeric';
        Handsontable.renderers.TextRenderer.apply(this, arguments);
        td.style.background = greyColor;
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

        case 'bubble':
            hot = bubblePlotTable(containerId, options);
            break;

        case 'contour':
            hot = contourPlotTable(containerId, options);
            break;

        case 'dot':
            hot = dotPlotTable(containerId, options);
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
window.initPlotDataTable = initPlotDataTable;

class PlotTableInput {
  constructor(options, strings) {
    this.options = options;
    this.strings = strings;
  }

  render(placeholder, name, id, initialState) {
    const container = document.createElement('div');
    container.innerHTML = `
      <div id="${id}-handsontable-container"></div>
      <input type="hidden" name="${name}" id="${id}" placeholder="${this.strings['Table']}">
    `;
    placeholder.replaceWith(container);

    const input = container.querySelector(`input[name="${name}"]`);
    const options = this.options;

    const widget = {
      getValue() {
        return JSON.parse(input.value);
      },
      getState() {
        return JSON.parse(input.value);
      },
      setState(state) {
        input.value = JSON.stringify(state);
        initPlotDataTable(id, options);
      },
      // eslint-disable-next-line @typescript-eslint/no-empty-function
      focus() {},
    };
    widget.setState(initialState);
    return widget;
  }
}
window.telepath.register('wagtail_plotly.widgets.PlotTableInput', PlotTableInput);
