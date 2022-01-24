var getData = () => {
    $.ajax({
        url: '/data',
        success: function (data) {
            var body = "<tr>";
            $.each(data['table'], function (i, data) {
                console.log(data);
                if (data.status == 'open') {
                    body += "<td class='table-danger'>" + data.location + "</td>";
                    body += "<td class='table-danger'>" + data.status + "</td>";
                }
                else {
                    body += "<td class='table-info'>" + data.location + "</td>";
                    body += "<td class='table-info'>" + data.status + "</td>";
                }

                body += "</tr>";
            });
            $("#table tbody").html(body);
            $("#table").DataTable({
                retrieve: true,
                paging: false,
                searching: false,
            });
        }
    });
};
getData()
setInterval(getData, 100);