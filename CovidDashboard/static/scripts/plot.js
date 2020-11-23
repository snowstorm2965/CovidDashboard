function request_province_plot() {
    $.ajax({
        url: "/plot_province",
        type: "GET",
        contentType: 'application/json;charset=UTF-8',
        data: {
            'selected_region_code': Number(document.getElementById('selector_region').value),
            'selected_province_code': Number(document.getElementById('selector_province').value)
        },
        dataType: "json",

        success: function (data) {
            $('#province_latest_total_loader,#province_latest_increm_loader,#province_chart_loader').delay(1500).fadeOut(300).promise().done(function () {
                document.getElementById("province_latest_total_val").innerHTML = data.latest.total_cases;
                document.getElementById("province_latest_increm_val").innerHTML = data.latest.new_cases + (data.latest.increasing ? "<span class=\"fa fa-arrow-up\"/>" : "<span class=\"fa fa-arrow-down\"/>")
                var config = { responsive: true };
                Plotly.newPlot('province_chart', data.data_plot, data.layout, config);
            });
            //console.log(data)
        }
    });
}

//function request_region_list() {
//    $.ajax({
//        url: "/list_regions",
//        type: "GET",
//        contentType: "application/json;charset=UTF-8",
//        dataType: "json",
//        success: function (data) {
//            var $selector = $('#selector_region')
//            $selector.empty();
//            $.each(data, function (key, value) {
//                var $el = $("<option></option>").attr("value", value.codice_regione).text(value.denominazione_regione)
//                $selector.append($el)
//            })
//        }
//    })
//}

function request_province_list() {
    $.ajax({
        url: "/list_provinces",
        type: "GET",
        contentType: "application/json;charset=UTF-8",
        dataType: "json",
        data: {
            'selected_region_code': document.getElementById('selector_region').value
        },
        success: function (data) {
            var $selector = $('#selector_province')
            var capoluogo;
            $selector.empty();
            $.each(data, function (key, value) {
                if (value.codice_provincia < 200) {
                    var $opt = $("<option></option>").attr("value", value.codice_provincia).text(value.denominazione_provincia + " (" + value.sigla_provincia + ")")
                    $selector.append($opt)
                    if (value.capoluogo == true) {
                        capoluogo = value.codice_provincia;
                    }
                }
            });
            $selector.val(capoluogo).change();
        }
    })
}

$('#selector_region').on('change', request_province_list);
$('#selector_province').on('change', function () {
    $('#province_latest_total_val,#province_latest_increm_val,#province_chart').empty();
    $('#province_latest_total_loader,#province_latest_increm_loader,#province_chart_loader').fadeIn(300).promise().done(request_province_plot);
});
$(document).ready(function () {
    request_province_plot()
})
