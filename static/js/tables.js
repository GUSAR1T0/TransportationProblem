$('.solve-btn').click(function (event) {
    var consumption = getElements('consumption');
    var productivity = getElements('productivity');
    var nodes = getElements('node');
    var costOneTon = getElements('cost-one-ton');
    var dailyCostLoading;
    if (!$('.daily-cost-loading').is('.fade')) {
        dailyCostLoading = getElements('daily-cost-loading');
    } else {
        dailyCostLoading = [];
    }

    event.preventDefault();
    if ($('.solve-btn').length) {
        $.ajax({
            type: 'GET',
            url: '/solve/',
            dataType: 'json',
            data: {
                'consumption': consumption,
                'productivity': productivity,
                'nodes': nodes,
                'cost_one_ton': costOneTon,
                'daily_cost_loading': dailyCostLoading
            },
            success: function (data) {
                if (data.is_successful) {
                    $('.info').html(
                        '<div class="alert alert-success alert-dismissible fade show" role="alert">\n' +
                        '  <strong>Вычисления прошли успешно.</strong> Пожалуйста, нажмите на кнопку ниже, чтобы посмотреть результаты.' +
                        '  <button type="button" class="close" data-dismiss="alert" aria-label="Close">\n' +
                        '    <span aria-hidden="true">&times;</span>\n' +
                        '  </button>\n' +
                        '</div>'
                    );
                    $('.loading-btn').html('<i class="fa fa-tasks" aria-hidden="true"></i>')
                        .removeClass('btn-outline-warning')
                        .removeClass('btn-outline-danger')
                        .addClass('btn-outline-success')
                        .removeClass('disabled')
                        .attr('aria-disabled', false)
                        .attr('data-toggle', 'collapse')
                        .attr('href', '#collapse-results')
                        .attr('aria-expanded', 'false')
                        .attr('aria-controls', 'false');
                    katex.render(data.results['problem_statement'], ps);
                    katex.render(data.results['basic_diff'], basic_diff);
                    $('#mem').html(data.results['minimal_element_method']);
                    katex.render(data.results['non-degenerated_values'], non_degenerated_values);
                    $('#non_degenerated_status').html(data.results['non-degenerated']);
                    for (var i = 0; i < data.results['diffs'].length; i++) {
                        $('#pm').append('<br><h5>ИТЕРАЦИЯ №' + (i + 1) + '</h5>' + data.results['step_table'][i] +
                            '<p><span id="pseudos-' + i + '"></span></p>' +
                            '<p><span id="diffs-' + i + '"></span></p>');
                        katex.render(data.results['pseudos'][i], document.getElementById('pseudos-' + i));
                        katex.render(data.results['diffs'][i], document.getElementById('diffs-' + i));
                        if (i + 1 < data.results['diffs'].length) {
                            $('#pm').append(data.results['potential_method'][i] +
                                '<p><span id="theta-' + i + '"></span></p>' + data.results['table_after'][i]);
                            katex.render(data.results['theta'][i], document.getElementById('theta-' + i));
                        }
                    }
                    $('#final').html(data.results['final']);
                    katex.render(data.results['objective_function_value'], ofv);
                } else {
                    $('.info').html(
                        '<div class="alert alert-danger alert-dismissible fade show" role="alert">\n' +
                        '  <strong>Во время вычислений было получено исключение:</strong> ' + data.errmsg + '.\n' +
                        '  <button type="button" class="close" data-dismiss="alert" aria-label="Close">\n' +
                        '    <span aria-hidden="true">&times;</span>\n' +
                        '  </button>\n' +
                        '</div>'
                    );
                    $('.editable').attr('contenteditable', true);
                    $('.loading-btn').html('<i class="fa fa-magic" aria-hidden="true"></i>')
                        .removeClass('disabled')
                        .attr('aria-disabled', false)
                        .addClass('solve-btn')
                        .removeClass('loading-btn')
                        .removeClass('btn-outline-secondary')
                        .removeClass('btn-outline-warning')
                        .addClass('btn-outline-danger');
                    $('.add-node-btn').removeClass('disabled').addClass('enabled');
                    $('.add-factory-btn').removeClass('disabled').addClass('enabled');
                    $('.remove-node-btn').removeClass('disabled').addClass('enabled').attr('data-target', '.remove-node-modal');
                    $('.remove-factory-btn').removeClass('disabled').addClass('enabled').attr('data-target', '.remove-factory-modal');
                    $('.settings-btn').removeClass('disabled').addClass('enabled').attr('data-target', '.settings-modal');
                }
            },
            error: function (xhr, errmsg, err) {
                $('.info').html(
                    '<div class="alert alert-danger alert-dismissible fade show" role="alert">\n' +
                    '  <strong>Не удалось выполнить вычисления:</strong> ' + data.errmsg + '.\n' +
                    '  <button type="button" class="close" data-dismiss="alert" aria-label="Close">\n' +
                    '    <span aria-hidden="true">&times;</span>\n' +
                    '  </button>\n' +
                    '</div>'
                );
                $('.editable').attr('contenteditable', true);
                $('.loading-btn').html('<i class="fa fa-magic" aria-hidden="true"></i>')
                    .removeClass('disabled')
                    .attr('aria-disabled', false)
                    .addClass('solve-btn')
                    .removeClass('loading-btn')
                    .removeClass('btn-outline-secondary')
                    .removeClass('btn-outline-warning')
                    .addClass('btn-outline-danger');
                $('.add-node-btn').removeClass('disabled').addClass('enabled');
                $('.add-factory-btn').removeClass('disabled').addClass('enabled');
                $('.remove-node-btn').removeClass('disabled').addClass('enabled').attr('data-target', '.remove-node-modal');
                $('.remove-factory-btn').removeClass('disabled').addClass('enabled').attr('data-target', '.remove-factory-modal');
                $('.settings-btn').removeClass('disabled').addClass('enabled').attr('data-target', '.settings-modal');
            }
        });

        $('.info').html(
            '<div class="alert alert-warning alert-dismissible fade show" role="alert">\n' +
            '  <strong>Пожалуйста, подождите, идут вычисления.</strong>' +
            '</div>'
        );
        $('.editable').attr('contenteditable', false);
        $('.solve-btn').html('<i class="fa fa-cog fa-spin fa-fw"></i>')
            .addClass('disabled')
            .attr('aria-disabled', true)
            .addClass('loading-btn')
            .removeClass('solve-btn')
            .removeClass('btn-outline-secondary')
            .removeClass('btn-outline-danger')
            .addClass('btn-outline-warning');
        $('.add-node-btn').removeClass('enabled').addClass('disabled');
        $('.add-factory-btn').removeClass('enabled').addClass('disabled');
        $('.remove-node-btn').removeClass('enabled').addClass('disabled').attr('data-target', false);
        $('.remove-factory-btn').removeClass('enabled').addClass('disabled').attr('data-target', false);
        $('.settings-btn').removeClass('enabled').addClass('disabled').attr('data-target', false);
    }
});

function getElements(selector) {
    var values = [];

    var elements = $('.' + selector).get();
    for (var i = 0; i < elements.length; i++) {
        values.push(elements[i].innerHTML);
    }

    return values;
}
