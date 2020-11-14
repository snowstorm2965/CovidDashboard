function request_province_plot() {
    $.ajax({
        url: "/plot_province",
        type: "GET",
        contentType: 'application/json;charset=UTF-8',
        data: {
            'selected': document.getElementById('selector_province').value
        },
        dataType: "json",

        success: function (data) {
            console.log(data);
            Plotly.newPlot('mygraph', data);
        }
    });
}
$('#selector_province').on('change', request_province_plot)
$(document).ready(request_province_plot)