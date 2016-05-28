/**
 * Created by Fasusi on 22/05/2016.
 */

$("document").ready(function () {
    // ajax request for json containing sku related. Is used to: builds revenue chart (#chart).
    $.ajax({
        type: "GET",
        contentType: "application/json; charset=utf-8",
        url: 'http://127.0.0.1:5000/reporting/api/v1.0/sku_detail',
        dataType: 'json',
        async: true,
        data: "{}",
        success: function (data) {

            //console.log(data);
            render_revenue_graph(data, '#chart');

        },
        error: function (result) {


        }
    });

    //ajax request for json containing all costs summarised by product class (abcxyz), builds pie chart (#chart2)
    $.ajax({
        type: "GET",
        contentType: "application/json; charset=utf-8",
        url: 'http://127.0.0.1:5000/reporting/api/v1.0/abc_summary',
        dataType: 'json',
        async: true,
        data: "{}",
        success: function (data) {
            //console.log(data);
            render_pie_chart(data);
            //render_pie_chart_test(data);
        },
        error: function (result) {
            //console.log(result);// make 404.html page
        }
    });

    //ajax request for json containing all costs summarised by product class (abcxyz), builds pie chart (#chart2)
    $.ajax({
        type: "GET",
        contentType: "application/json; charset=utf-8",
        url: 'http://127.0.0.1:5000/reporting/api/v1.0/top_shortages',
        dataType: 'json',
        async: true,
        data: "{}",
        success: function (data) {
            //console.log(data);
            create_shortages_table(data);
            render_shortages_chart(data, '#chart4')

        },
        error: function (result) {
            //console.log(result);// make 404.html page
        }
    });


    $.ajax({
        type: "GET",
        contentType: "application/json; charset=utf-8",
        url: 'http://127.0.0.1:5000/reporting/api/v1.0/top_excess',
        dataType: 'json',
        async: true,
        data: "{}",
        success: function (data) {
            //console.log(data);
            create_excess_table(data);


        },
        error: function (result) {
            //console.log(result);// make 404.html page
        }
    });

});


// helper functions for unpacking data from ajax requests
var unpack = {
    attribute_enum: {
        revenue: 'revenue',
        shortage_cost: 'shortage_cost',
        shortages: 'shortages'

    },

    sku_detail: function (data, value) {
        var barData = [];

        for (key in data) {
            tempData = data[key];
            //console.log(tempData);
            for (i in tempData) {
                //console.log(tempData[i].revenue);
                switch (value) {
                    case unpack.attribute_enum.revenue:
                        barData.push(tempData[i].revenue);
                        //console.log(barData);
                        break;
                    case upack.attribute_enum.shoratge_cost:
                        barData.push(tempData[i].shoratge_cost);
                }

            }

        }
        return barData;
    },

    excess: function (data, target) {
        var excess_data = [];

        for (key in data) {
            tempData = data[key];
            //console.log(tempData);
            for (i in tempData) {
                //console.log(tempData[i]);
                switch (target) {

                    case 'chart':
                        excess_data.push([tempData[i].sku_id, tempData[i].excess_cost]);
                        console.log(excess_data);
                        break;

                    case 'table':
                        excess_data.push(tempData[i]);
                        console.log(excess_data);
                        break;
                }

            }

        }
        return excess_data;
    },

    pie: function (data) {
        var pieData = [];

        for (key in data) {
            tempData = data[key];
            //console.log(tempData);
            for (i in tempData) {
                //console.log(tempData[i]);
                pieData.push([tempData[i].abc_xyz_classification, tempData[i].total_shortages]);
                //onsole.log(pieData);
            }


        }
        return pieData;
    },

    shortages: function (data, target) {
        var shortages_data = [];

        for (key in data) {
            tempData = data[key];
            //console.log(tempData);
            for (i in tempData) {
                //console.log(tempData[i]);
                switch (target) {

                    case 'chart':
                        shortages_data.push([tempData[i].sku_id, tempData[i].shortage_cost]);
                        console.log(shortages_data);
                        break;

                    case 'table':
                        shortages_data.push(tempData[i]);
                        console.log(shortages_data);
                        break;
                }

            }

        }
        return shortages_data;
    }
};

function create_shortages_table(data) {
    var shortages_data = new unpack.shortages(data, 'table');
    var total_shortage = 0;

    $("#shortage-table").append().html("<tr id='first'><th>SKU</th><th>Quantity on Hand</th><th>Average Orders</th>" +
        "<th>Shortage</th><th>Shortage Cost</th><th>Safety Stock</th><th>Reorder Level</th><th>Classification</th></tr>");
    //console.log(shortages_data[0].sku_id);

    for (obj in shortages_data) {
        //console.log(shortages_data[obj].sku_id);
        total_shortage += shortages_data[obj].shortage_cost;
        console.log(total_shortage);

        $("<tr><td><a href=\"sku_detail/" + shortages_data[obj].sku_id + "\">" + shortages_data[obj].sku_id + "</a></td>" +
            "<td>" + shortages_data[obj].quantity_on_hand + "</td>" +
            "<td>" + shortages_data[obj].average_orders + "</td>" +
            "<td>" + shortages_data[obj].shortages + "</td>" +
            "<td>" + shortages_data[obj].shortage_cost + "</td>" +
            "<td>" + shortages_data[obj].safety_stock + "</td>" +
            "<td>" + shortages_data[obj].reorder_level + "</td>" +
            "<td>" + shortages_data[obj].abc_xyz_classification + "</td></tr>").insertAfter("#shortage-table tr:last");

    }

    $("#lg-shortage-sku").append().html("<h1><strong>" + shortages_data[0].sku_id + "</strong></h1>")
        .find("> h1").css("color", "#2176C7");
    $("#lg-shortage-cost").append().html("<h1><strong>" + "$" + shortages_data[0].shortage_cost + "</strong></h1>")
        .find("> h1").css("color", "#D11C29");
    $("#lg-shortage-units").append().html("<h1><strong>" + shortages_data[0].shortages + " units" + "</strong></h1>")
        .find("> h1").css("color", "#819090");
    $("#total-shortage").append().html("<h1><strong>" + total_shortage + "</strong></h1>")
        .find("> h1").css("color", "#D11C29");
}


function create_excess_table(data) {
    var excess_data = new unpack.excess(data, 'table');
    $("#excess-table").append().html("<tr id='first'><th>SKU</th><th>Quantity on Hand</th><th>Average Orders</th>" +
        "<th>Excess</th><th>Excess Cost</th><th>Classification</th></tr>");
    //console.log(excess_data);

    for (obj in excess_data) {
        //console.log(excess_data[obj].sku_id);
        $("<tr><td><a href=\"sku_detail/" + excess_data[obj].sku_id + "\">" + excess_data[obj].sku_id + "</td>" +
            "<td>" + excess_data[obj].quantity_on_hand + "</td>" +
            "<td>" + excess_data[obj].average_orders + "</td>" +
            "<td>" + excess_data[obj].excess_stock + "</td>" +
            "<td>" + excess_data[obj].excess_cost + "</td>" +
            "<td>" + excess_data[obj].abc_xyz_classification + "</td></tr>").insertAfter("#excess-table tr:last");
    }

}

// change functions to graph rendering class
function render_revenue_graph(data, id) {
    var barData = unpack.sku_detail(data, "revenue");//change to enums
    var tempData = [];

    //var height = 350,
    //   width = 300,
    var margin = {top: 30, right: 20, bottom: 40, left: 90};

    var height = 350 - margin.top - margin.bottom;
    var width = 400 - margin.left - margin.right;
    var barWidth = 10;
    var barOffset = 5;

    var tempColor;


    var yScale = d3.scale.linear()
        .domain([0, d3.max(barData)]) //  calculates the max range of the chart area
        .range([0, height]); // the range of the chart area

    var xScale = d3.scale.ordinal()
        .domain(d3.range(0, barData.length))
        .rangeBands([0, width]);

    var colors = d3.scale.linear()
        .domain([0, barData.length * .33, barData.length * .88, barData.length])
        .range(['#FFB832', '#C61C6F', '#C31C6F', '#382982']); //the number of values in the domain must match the number of values in the range

    var myChart = d3.select(id).append('svg')
        .style('background', 'transparent')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append('g')
        .attr('transform', 'translate(' + margin.left + ', ' + margin.top + ')')
        .selectAll('rect').data(barData)
        .enter().append('rect') //the data command reads the bar data and the appends the selectall rect for each piece of data
        .style('fill', colors)
        .attr('width', xScale.rangeBand())
        .attr('height', 0)
        .attr('x', function (d, i) {
            return xScale(i);
        })
        .attr('y', height)
        .on('mouseover', function (d) {

            tooltip.transaction()
                .style('opacity', 0.5);
            tooltip.html(d)
                .style('left', (d3.event.pageX - 35) + 'px')
                .style('top', (d3.event.pageY - 30) + 'px');

            tempColor = this.style.fill;

            d3.select(this)
                .style('opacity', .5)
                .style('fill', '#389334')

        }).on('mouseout', function (d) {
            d3.select(this)
                .style('opacity', 1)
                .style('fill', tempColor)
        });

    myChart.transition()
        .attr('height', function (d) {
            return yScale(d);
        })
        .attr('y', function (d) {
            return height - yScale(d);
        })
        .delay(function (d, i) {
            return i * 20;
        })
        .duration(1000)
        .ease('elastic');


    var tooltip = d3.select('body')
        .append('div')
        .style('position', 'absolute')
        .style('background', 'white')
        .style('padding', '0 10px')
        .style('opacity', 0);

    var vGuideScale = d3.scale.linear()
        .domain([0, d3.max(barData)]).range([height, 0]); //reversing the order of the scale on the y axis
    var vAxis = d3.svg.axis()
        .scale(vGuideScale)
        .orient('left')
        .ticks(10);

    var vGuide = d3.select('svg').append('g');
    vAxis(vGuide);
    vGuide.attr('transform', 'translate(' + margin.left + ', ' + margin.top + ')');
    vGuide.selectAll('path')
        .style({fill: 'none', stroke: "#000"});
    vGuide.selectAll('line')
        .style({stroke: "#000"});

    var hAxis = d3.svg.axis()
        .scale(xScale)
        .orient('bottom')
        .tickValues(xScale.domain().filter(function (d, i) {
            return !(i % (barData.length / 10));
        }));

    var hGuide = d3.select('svg').append('g');
    hAxis(hGuide);
    hGuide.attr('transform', 'translate(' + margin.left + ', ' + (height + margin.top) + ')');
    hGuide.selectAll('path')
        .style({fill: 'none', stroke: "#000"});
    hGuide.selectAll('line')
        .style({stroke: "#000"});


}


function render_pie_chart(data) {
    //console.log(data);

    var width = 200;
    var height = 200;
    var radius = 100;
    var colors = d3.scale.ordinal()
        .range(['#259286', '#2176C7', '#FCF4DC', 'white', '#819090', '#A57706', '#EAE3CB', '#2e004d']);

    var pieData = unpack.pie(data);
    //console.log(pieData);

    var pie = d3.layout.pie()
        .value(function (d) {
            //console.log(d[1]);
            return d[1];
        });

    var arc = d3.svg.arc()
        .outerRadius(radius);

    var myChart = d3.select('#chart2').append('svg')
        .attr('width', width)
        .attr('height', height)
        .append('g')
        .attr('transform', 'translate(' + (width - radius) + ',' + (height - radius) + ')')
        .selectAll('path').data(pie(pieData))
        .enter().append('g')
        .attr('class', 'slice');

    var slices = d3.selectAll('g.slice')
        .append('path')
        .attr('fill', function (d, i) {
            return colors(i);
        })
        .attr('opacity', .6)
        .attr('d', arc);

    var text = d3.selectAll('g.slice')
        .append('text')
        .text(function (d, i) {
            //console.log(d.data[0]);

            return d.data[0];

        })
        .attr('text-anchor', 'middle')
        .attr('fill', 'white')
        .attr('transform', function (d) {
            d.innerRadius = 0;
            d.outerRadius = radius;
            return 'translate(' + arc.centroid(d) + ')'
        });


}


function render_shortages_chart(data, id) {
    var bardata = unpack.shortages(data, 'chart');
    var nums = [];
    var switchColor;

    for (i in bardata) {
        nums.push(bardata[i][1]);
    }

    var tooltip = d3.select('body')
        .append('div')
        .style('position', 'absolute')
        .style('background', 'white')
        .style('padding', '0 10px')
        .style('opacity', 0);

    console.log(nums);

    var margin = {top: 10, right: 300, bottom: 40, left: 0.1};

    var height = 250 - margin.top - margin.bottom;
    var width = 650 - margin.left - margin.right;

    var colors = d3.scale.linear()
        .domain([0, nums.length * .33, nums.length * .66, nums.length])
        .range(['white', '#259286', '#738A05', '#2176C7']);

    var yScale = d3.scale.linear()
        .domain([0, d3.max(nums)])
        .range([0, height]);

    var xScale = d3.scale.ordinal()
        .domain(d3.range(0, nums.length))
        .rangeBands([0, width]);

    var shortage_chart = d3.select(id).append('svg')
        .attr('width', width)
        .attr('height', height)
        .append('g')
        .style('background', 'white')
        .selectAll('rect').data(nums)
        .enter().append('rect')
        .style('fill', function (d, i) {
            return colors(i);
        })
        .attr('width', xScale.rangeBand() * .5)
        .attr('height', 0)
        .attr('x', function (d, i) {
            return xScale(i);
        })
        .attr('y', height).on('mouseover', function (d) {
            console.log(d);
            tooltip.transition()
                .style('opacity', 0.5);
            tooltip.html(d)
                .style('left', (d3.event.pageX - 35) + 'px')
                .style('top', (d3.event.pageY - 30) + 'px');

            switchColor = this.style.fill;
            d3.select(this)
                .style('opacity', .5);
            d3.select(this)
                .style('fill', '#D11C24')

        }).on('mouseout', function (d) {
            d3.select(this)
                .transition()
                .delay(300)
                .duration(300)
                .style('fill', switchColor);
            d3.select(this)
                .style('opacity', 1)
        });
    //transitions graph in
    shortage_chart.transition()
        .attr('height', function (d, i) {
            return yScale(d);
        })
        .attr('y', function (d) {
            return height - yScale(d);
        }).delay(function (d, i) {
        return i * 70;

    }).ease('elastic');

    var vGuideScale = d3.scale.linear()
        .domain([0, d3.max(nums)]).range([height, 0.5]); //reversing the order of the scale on the y axi

    var vAxis = d3.svg.axis()
        .scale(vGuideScale)
        .orient('left')
        .ticks(10);

    var vGuide = d3.select('#chart4 > svg').append('g');
    vAxis(vGuide);
    vGuide.attr('transform', 'translate(' + margin.left + ', ' + margin.top + ')');
    vGuide.selectAll('path')
        .style({fill: 'none', stroke: "#000"});
    vGuide.selectAll('line')
        .style({stroke: "#000"});


}

function render_pie_chart_test(data) {
    //console.log(data);

    var width = 150;
    var height = 150;
    var radius = 75;
    var colors = d3.scale.ordinal()
        .range(['#259286', '#2176C7', '#FCF4DC', 'white', '#819090', '#A57706', '#EAE3CB', '#2e004d']);

    var pieData = unpack.pie(data);
    //console.log(pieData);

    var pie = d3.layout.pie()
        .value(function (d) {
            //console.log(d[1]);
            return d[1];
        });

    var arc = d3.svg.arc()
        .outerRadius(radius);

    var myChart = d3.select('#chart5').append('svg')
        .attr('width', width)
        .attr('height', height)
        .append('g')
        .attr('transform', 'translate(' + (width - radius) + ',' + (height - radius) + ')')
        .selectAll('path').data(pie(pieData))
        .enter().append('g')
        .attr('class', 'slice');

    var slices = d3.selectAll('g.slice')
        .append('path')
        .attr('fill', function (d, i) {
            return colors(i);
        })
        .attr('opacity', .6)
        .attr('d', arc);

    var text = d3.selectAll('g.slice')
        .append('text')
        .text(function (d, i) {
            //console.log(d.data[0]);

            return d.data[0];

        })
        .attr('text-anchor', 'middle')
        .attr('fill', 'white')
        .attr('transform', function (d) {
            d.innerRadius = 0;
            d.outerRadius = radius;
            return 'translate(' + arc.centroid(d) + ')'
        });


}
