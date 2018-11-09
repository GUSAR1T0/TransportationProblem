$('.add-node-btn.enabled').click(function () {
    if ($(this).is('.enabled')) {
        addColumn('consumption', 100);

        var nodes = $('.consumption-each-header').get();
        var factories = $('.productivity-each-header').get();
        var width = 72 / ($('.empty-line').get().length + 1);
        var id = parseInt(nodes[nodes.length - 1].innerHTML);
        var row = '';
        for (var i = 0; i < factories.length; i++) {
            row += '<td class="node editable text-centered" ' +
                'width="' + width + '%" contenteditable>0</td>';
        }

        $('.data-table').find('tr:last').prev().prev().after('<tr class="node-values">' +
            '<th scope="row" width="28%">- к узлу "' + id + '"</th>' + row + '</tr>');
    }
});

$('.add-factory-btn.enabled').click(function () {
    if ($(this).is('.enabled')) {
        addColumn('productivity', 100);
        addColumn('factory', 72);

        var width = 72 / ($('.empty-line').get().length + 1);
        $('.empty-lines').append('<td class="empty-line" width="' + width + '"></td>');
        $('.empty-line').attr('width', width + '%');

        $('.node').attr('width', width + '%');
        $('.node-values').append('<td class="node editable text-centered" width="' +
            width + '%" contenteditable>' + 0 + '</td>');

        $('.cost-one-ton').attr('width', width + '%');
        $('.cost-one-ton-values').append('<td class="cost-one-ton editable text-centered" width="' +
            width + '%" contenteditable>' + 0 + '</td>');

        $('.daily-cost-loading').attr('width', width + '%');
        $('.daily-cost-loading-values').append('<td class="daily-cost-loading editable text-centered" width="' +
            width + '%" contenteditable>' + 0 + '</td>');
    }
});

function addColumn(selectorGroup, maxWidth) {
    var elements = $('.' + selectorGroup + '-each-header').get();
    var width = maxWidth / (elements.length + 1);
    var id = parseInt(elements[elements.length - 1].innerHTML) + 1;

    $('.' + selectorGroup + '-header').attr('colspan', elements.length + 1);
    $('.' + selectorGroup + '-each-header').attr('width', width + '%');
    $('.' + selectorGroup).attr('width', width + '%');
    $('.' + selectorGroup + '-headers').append('<th scope="colgroup" class="' + selectorGroup +
        '-each-header text-centered" width="' + width + '%">' + id + '</th>');
    $('.' + selectorGroup + '-values').append('<td class="' + selectorGroup + ' editable text-centered" width="' +
        width + '%" contenteditable>' + 0 + '</td>');
}

$('.remove-node-btn.enabled').click(function () {
    setSelectOptions('consumption-each-header', 'node-select-form', 'Узел');
});

$('.remove-factory-btn.enabled').click(function () {
    setSelectOptions('productivity-each-header', 'factory-select-form', 'Фабрика');
});

function setSelectOptions(header, select, keyword) {
    var elements = $('.' + header).get();
    var html = '';

    for (var i = 0; i < elements.length; i++) {
        html += '<option value="' + elements[i].innerHTML + '">' + keyword + ' "' + elements[i].innerHTML + '"</option>';
    }

    $('.' + select).html(html);
}

$('.apply-remove-node-btn').click(function () {
    var nodes = $('.node-select-form').val();
    var elements = $('.consumption-each-header').get();

    if (elements.length - nodes.length >= 2) {
        removeColumns('consumption', nodes, 100);

        for (var i = nodes.length - 1; i >= 0; i--) {
            $('.node-values')[nodes[i] - 1].remove();
        }

        var headers = $('.node-values th').get();
        for (var j = 0; j < headers.length; j++) {
            headers[j].innerHTML = '- к узлу "' + (j + 1) + '"';
        }
    }

    $('.remove-node-modal').modal('hide');
});

$('.apply-remove-factory-btn').click(function () {
    var factories = $('.factory-select-form').val();
    var elements = $('.productivity-each-header').get();

    if (elements.length - factories.length >= 2) {
        removeColumns('productivity', factories, 100);

        var width = 72 / ($('.empty-line').get().length - factories.length);
        $('.empty-line').attr('width', width + '%');
        $('.node').attr('width', width + '%');
        $('.cost-one-ton').attr('width', width + '%');
        $('.daily-cost-loading').attr('width', width + '%');

        for (var i = factories.length - 1; i >= 0; i--) {
            $('.factory-headers').each(function () {
                $(this).find('th:eq(' + (factories[i] - 1) + ')').remove();
            });
            $('.empty-lines').each(function () {
                $(this).find('td:eq(' + (factories[i] - 1) + ')').remove();
            });
            $('.node-values').each(function () {
                $(this).find('td:eq(' + (factories[i] - 1) + ')').remove();
            });
            $('.cost-one-ton-values').each(function () {
                $(this).find('td:eq(' + (factories[i] - 1) + ')').remove();
            });
            $('.daily-cost-loading-values').each(function () {
                $(this).find('td:eq(' + (factories[i] - 1) + ')').remove();
            });
        }

        var headers = $('.factory-each-header').get();
        for (var j = 0; j < headers.length; j++) {
            headers[j].innerHTML = j + 1;
        }
    }

    $('.remove-factory-modal').modal('hide');
});

function removeColumns(selectorGroup, removingElements, maxWidth) {
    var elements = $('.' + selectorGroup + '-each-header').get();
    var width = maxWidth / (elements.length - removingElements.length);

    $('.' + selectorGroup + '-header').attr('colspan', elements.length - 1);
    $('.' + selectorGroup + '-each-header').attr('width', width + '%');
    $('.' + selectorGroup).attr('width', width + '%');
    for (var i = removingElements.length - 1; i >= 0; i--) {
        $('.' + selectorGroup + '-headers').each(function () {
            $(this).find('th:eq(' + (removingElements[i] - 1) + ')').remove();
        });
        $('.' + selectorGroup + '-values').each(function () {
            $(this).find('td:eq(' + (removingElements[i] - 1) + ')').remove();
        });
    }

    var headers = $('.' + selectorGroup + '-each-header').get();
    for (var j = 0; j < headers.length; j++) {
        headers[j].innerHTML = j + 1;
    }
}

$('.apply-settings-btn').click(function () {
    if ($('.cost-one-ton-checkbox').is(':checked')) {
        $('.cost-one-ton-values').removeClass('fade');
    } else {
        $('.cost-one-ton-values').addClass('fade');
        $('.cost-one-ton').each(function (index, value) {
            value.innerHTML = 0;
        })
    }

    if ($('.daily-cost-loading-checkbox').is(':checked')) {
        $('.daily-cost-loading-values').removeClass('fade');
    } else {
        $('.daily-cost-loading-values').addClass('fade');
        $('.daily-cost-loading').each(function (index, value) {
            value.innerHTML = 0;
        })
    }

    $('.settings-modal').modal('hide');
});
