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
        var html_result_string = "Search results: ";
        for (var i = 0; i < items.length; i++)
        {
            html_result_string += (i > 0 ? ", " : "") + items.eq(i).text();
        }
        $("#results").html(html_result_string);

    }


});
