$(document).ready(function()
{

    // when to do prefix search
    $("#searchbutton").click(do_prefix_search);
    $("#searchtext").keyup(do_prefix_search);


    function do_prefix_search()
    {
        var prefix = $("#searchtext").attr("value");
        $.get("http://localhost:3366/prefix_search?query=" + prefix,{},parse_xml);
    }

    function parse_xml(xml)
    {
        var items = $(xml).find("item");
        var html_result_string = "<table id='resulttable'>";
        html_result_string    += "<thead><tr><th>word</th><th>document #</th>";
        html_result_string    += "<th>percentage</th><th>%</th></tr></thead>";
        html_result_string    += "<tbody>";

        $(xml).find("item").each(function()
        {
            var visual_percentage = "|";
            html_result_string += '<tr>';
            html_result_string += '<td>' + $(this).find("completion").text() + '</td>';
            html_result_string += '<td>' + $(this).find("doclength").text() + '</td>';
            html_result_string += '<td>' + $(this).find("percentage").text() + '</td>';
            for (var i = 0; i < $(this).find("percentage").text(); i++)
            {
                visual_percentage += "|";
            }
            html_result_string += '<td>' + visual_percentage + '</td></tr>';
        });

        html_result_string += "</tbody></table>";
        $("#results").html(html_result_string);
        $("#resulttable").tablesorter();

    }


});
