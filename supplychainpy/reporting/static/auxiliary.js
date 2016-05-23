/**
 * Created by Fasusi on 22/05/2016.
 */

$("document").ready(function () {



    //var myStyles = ['#708284','#708244', '#307444', '#898244', '#982344'];
    //var myStyles2 = [{  width: 200,
    //                    color: '#708284'},
    //                 {  width: 230,
    //                    color: '#708244'},
    //                 {  width: 240,
    //                    color: '#307444'},
    //                 {  width: 300,
    //                    color: '#898244'},
    //                 {  width: 200,
    //                    color: '#982344'}];
    //

    //var myStyles3 = [{
    //    width: 200,
    //    name: 'Augsto Pinochet',
    //    color: '#708284'
    //},
    //    {
    //        width: 230,
    //        name: 'Wacko Jacko',
    //        color: '#708244'
    //    },
    //    {
    //        width: 240,
    //        name: 'Notorious Big',
    //        color: '#307444'
    //    },
    //    {
    //        width: 300,
    //        name: 'Incredible Hulk',
    //        color: '#898244'
    //    },
    //    {
    //        width: 200,
    //        name: 'Iron Man',
    //        color: '#982344'
    //    }];


    //d3.selectAll('.item').text('select');
    //d3.select('.item:nth-child(3)').text('select');
    //d3.select('.item:nth-child(2n)').text('select');
    //d3.select('.item:nth-child(3)').remove();
    //d3.select('.item:nth-child(3)').attr('id', 'ia'); // replaces id
    //d3.select('.item:nth-child(3)').classed('highlight',true); // appends to class
    //d3.select('.item:nth-child(3)').classed({'highlight': true, item: false}); //use multiple classes
    //d3.select('.item:nth-child(3)').style({'background':'#708284','padding':'10px'}); //change style inline for selection

    //d3.selectAll('.item').data([true,true]).style({'background':'#708284'}); // adds selected item to data variable
    //d3.selectAll('.item').data(myStyles).style({'background':myStyles[0]}); // using data variable instead of selecting each point
    //d3.selectAll('.item').data(myStyles).style({'color': 'white',
    //    'background': function (d) {
    //    return d;
    //}
    //}); // use a function and you can do stuff to the value
    //d3.selectAll('.item').data(myStyles2).style({'color': 'white',
    //    'background': function (d) {
    //    return d.color;
    //}, width: function (d) {
    //    return d.width + 'px';
    //}
    //}); // you can use a lot of objects in the variable

    //d3.selectAll('#chart').selectAll('div')
    //    .data(myStyles3)
    //    .enter().append('div')
    //    .classed('item', true)
    //    .text(function (d) {
    //        return d.name;
    //    })
    //    .style({
    //        'color': 'white',
    //        'background': function (d) {
    //            return d.color;
    //        },
    //        width: function (d) {
    //            return d.width + 'px';
    //        }
    //    }); // you can use a lot of objects in the variabl

    //d3.select('#chart').append('svg')
    //    .attr('height', 300)
    //    .attr('width', 300)
    //    .style('background', '#939394')
    //    .append("rect")
    //    .attr('x',200)
    //    .attr('y',200)
    //    .attr('height',200)
    //    .attr('width',200)
    //    .style('fill','#349072'); //the append places the element inside the previous
    //d3.select('svg').append("circle")
    //    .attr('cx', 20)
    //    .attr('cy', 30)
    //    .attr('r', 30)
    //    .style('fill', '#893983'); // selecting the svg we just made, instead of appending again

    $.ajax({
        type: "GET",
        contentType: "application/json; charset=utf-8",
        url: 'http://127.0.0.1:5000/reporting/api/v1.0/revenue',
        dataType: 'json',
        async: true,
        data: "{}",
        success: function (data) {

            console.log(data);
            render_revenue_graph(data);

        },
        error: function (result) {


        }
    });


});


function unpack(data) {
    var barData = [];

    for (key in data) {
        tempData = data[key];
        //console.log(tempData);
        for (i in tempData) {
            //console.log(tempData[i].revenue);
            barData.push(tempData[i].revenue);
            //console.log(barData);
        }


    } return barData;
}

function unpack_bar(data){

}

function render_revenue_graph(data) {
    var barData = unpack(data);
    var tempData = [];

    //var height = 350,
    //   width = 300,
    var margin = {top: 30, right: 30, bottom: 40, left: 90};

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

    var myChart = d3.select('#chart').append('svg')
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

            tooltip.transition()
                .style('opacity', .9);

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


    d3.layout.pie

}
