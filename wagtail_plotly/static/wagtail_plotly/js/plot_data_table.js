'use strict';

function initPlotDataTable(id, tableOptions) {
    var containerId = id + '-handsontable-container';
    var hiddenStreamInput = $('#' + id);
    var hot;
    var defaultOptions;
    var finalOptions = {};
    var persist;
    var cellEvent;
    var initEvent;
    var firstRowRenderer;
    var firstColRenderer;
    var data = null;
    var isInitialized = false;
    var foo;

    var plotType = tableOptions['plotType'];
    var colHeaders = tableOptions['colHeaders'];

    try {
        data = JSON.parse(hiddenStreamInput.val());
    } catch (e) {
        // do nothing
    }

    var scatterDataRowHeader = function(row, th) {
        if (row == 0) {
          th.textContent = 'Name';
        } else if (row > 0) {
          th.textContent = 'D' + (row - 1);
        } else {
          th.textContent = '';
        }
    };

    var lineDataColHeader = function(col, th) {
        if (col == 0) {
          th.textContent = 'X';
        } else if (col > 0) {
          th.textContent = 'Y' + (col - 1);
        } else {
          th.textContent = '';
        }
    };

    var scatterDataColHeader = function(col, th) {
        if (col >= 0) {
          th.textContent = ((col % 2 === 0) ? 'X' : 'Y') + Math.floor(col / 2);
        } else {
          th.textContent = '';
        }
    };

    persist = function() {
        hiddenStreamInput.val(
            JSON.stringify(hot.getData())
        );
    };

    cellEvent = function(change, source) {
        if (source === 'loadData') {
            return; //don't save this change
        }
        persist();
    };

    initEvent = function() {
        isInitialized = true;
    };

    firstRowRenderer = function(instance, td, row, col, prop, value, cellProperties) {
      Handsontable.renderers.TextRenderer.apply(this, arguments);
      td.style.fontWeight = 'bold';
      td.style.textAlign = "center";
      td.style.background = '#FEEEEE';
    }

    firstColRenderer  = function(instance, td, row, col, prop, value, cellProperties) {
      Handsontable.renderers.TextRenderer.apply(this, arguments);
      td.style.fontWeight = 'bold';
      td.style.background = '#F4F4F4';
    }

    var scatterXColRenderer  = function(instance, td, row, col, prop, value, cellProperties) {
      cellProperties.type = 'numeric';
      Handsontable.renderers.TextRenderer.apply(this, arguments);
      td.style.background = '#F4F4F4';
      td.style.textAlign = 'right';
    }

    defaultOptions = {
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
        finalOptions[key] = defaultOptions[key];
    });
    Object.keys(tableOptions).forEach(function (key) {
        finalOptions[key] = tableOptions[key];
    });

    finalOptions['cells'] = function(row, col, prop) {
      var cellProperties = {};

      if (plotType === 'scatter') {

        if (row === 0) {
          cellProperties.renderer = firstRowRenderer;
        }
        else if (col % 2 === 0) {
          cellProperties.renderer = scatterXColRenderer;
        }
        else {
          cellProperties.type = 'numeric';
        }

      } else {

        if ((row === 0) && (plotType !== 'pie')) {
          cellProperties.renderer = firstRowRenderer;
        }
        else if ((col === 0) && (plotType !== 'scatter')) {
          cellProperties.renderer = firstColRenderer;
        }
        else {
          cellProperties.type = 'numeric';
        }

      }
      return cellProperties;
    }

    hot = new Handsontable(document.getElementById(containerId), finalOptions);

    switch (plotType) {
      case 'bar':
      case 'line':
        hot.addHook('afterGetColHeader', lineDataColHeader);
        hot.addHook('afterGetRowHeader', scatterDataRowHeader);
        break;
      case 'scatter':
        hot.addHook('afterGetColHeader', scatterDataColHeader);
        hot.addHook('afterGetRowHeader', scatterDataRowHeader);
        break;

    }
    hot.render();
}
