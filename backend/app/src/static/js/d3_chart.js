function numberWithSpaces(x) {
    var parts = x.toString().split(".");
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, " ");
    return parts.join(".");
}
 function type(d) {
     return {
         date: parseDate(d.Date),
         price: +d.Close,
         average: +d.Average,
         volume: +d.Volume,
     }
 }
 
 var parseDate = d3.timeParse('%d/%m/%Y');


//stock_price_chart(data1.map(type),'chart',{width:700,height:400},margin,margin2,margin3);

function stock_price_chart(data,chart_id, fig_size, size_price, size_volume, size_low, 
	legend_format = '%b %d, %Y', 
	y_axis_margin = 12,
	focus_cirle={radius:3.5}
	) {	
	function trn_str(a,b) {return `translate(${a},${b})`;};
    // set the dimensions and margins of the graph
    const width = fig_size.width - fig_size.left - fig_size.right,
		  height = size_price.height ,
		  height2 = size_low.height ,
		  volume_h = size_volume.height ;	
		  
    var bisectDate = d3.bisector(function (d) {return d.date;}).left,
		legendFormat = d3.timeFormat(legend_format);



//alert (max_date.getFullYear()-min_date.getFullYear())


    var x = d3.scaleTime().range([0, width]),
		x2 = d3.scaleTime().range([0, width]),

		y = d3.scaleLinear().range([height, 0]),
		y1 = d3.scaleLinear().range([height, 0]),
		y2 = d3.scaleLinear().range([height2, 0]),
		y3 = d3.scaleLinear().range([volume_h, 0]);

    var xAxis = d3.axisBottom(x),
		xAxis2 = d3.axisBottom(x2),
		
		yAxis = d3.axisLeft(y);
//xAxis2.tickFormat(d3.timeFormat("%Y"));
xAxis2.ticks(10 ,"%Y");

    var priceLine = d3.line()
        .curve(d3.curveMonotoneX)
        .x(function (d) {return x(d.date);})
        .y(function (d) {return y(d.price);})
        /*		
		,
        avgLine = d3.line()
        .curve(d3.curveMonotoneX)
        .x(function (d) {return x(d.date);})
        .y(function (d) {return y(d.average);})
		*/
        volumeLine = d3.line()
        .curve(d3.curveMonotoneX)
        .x(function (d) {return x(d.date);})
        .y(function (d) {return y2(d.volume);})		
		;
    var area2 = d3.area()
        .curve(d3.curveMonotoneX)
        .x(function (d) {return x2(d.date);})
        .y0(height2)
        .y1(function (d) {return y3(d.price);})// 3rd graph
		;

    var svg = d3.select('#'+chart_id).append('svg')
        .attr('class', 'chart')
        .attr('width', fig_size.width )
        .attr('height', volume_h+height+height2+fig_size.top+fig_size.bottom + size_price.top + size_price.bottom+ size_low.top + size_low.bottom+ size_volume.top + size_volume.bottom);

    svg.append('defs').append('clipPath')
		.attr('id', 'clip')
		.append('rect')
		.attr('width', width)
		.attr('height', height);

    var make_y_axis = function () {return d3.axisLeft().scale(y).ticks(3);};
	
    var _margin=fig_size.top+size_price.top;
    var focus = svg.append('g')
        .attr('class', 'focus')
        .attr('transform', trn_str(fig_size.left,_margin));
	
    _margin=_margin+height+size_price.bottom+size_volume.top;
    var barsGroup = svg.append('g')
        .attr('class', 'barsGroup')
        .attr('clip-path', 'url(#clip)') 
        .attr('transform', trn_str(fig_size.left,_margin));
		
    _margin=_margin+volume_h+size_volume.bottom+size_low.top;
    var context = svg.append('g')
        .attr('class', 'context')
        .attr('transform', trn_str(fig_size.left,_margin));

    var legend = svg.append('g')
        .attr('class', 'chart__legend')
        .attr('width', width)
        .attr('height', fig_size.top)
        .attr('transform', trn_str(fig_size.left,size_price.top));
/*
    legend.append('text')
    .attr('class', 'chart__symbol')
    .text('NASDAQ: AAPL')
*/
    var rangeSelection = legend
        .append('g')
        .attr('class', 'chart__range-selection')
        .attr('transform', trn_str(0,0));

    var brush = d3.brushX()
        .extent([[0, 0], [width, height2]])
        .on('brush end', brushed);

    var xRange = d3.extent(data.map(function (d) {return d.date;}));
	
	x.domain(xRange);
    y.domain(d3.extent(data.map(function (d) {return d.price;})));
    y3.domain(d3.extent(data.map(function (d) {return d.price;})));
    x2.domain(x.domain());
   // y2.domain(y.domain());
y2.domain(d3.extent(data.map(function (d) {return d.volume;})));
    const min = d3.min(data.map(function (d) {return d.price;})),
          max = d3.max(data.map(function (d) {return d.price;}));

    var range = legend.append('text')
        .text(legendFormat(new Date(xRange[0])) + ' - ' + legendFormat(new Date(xRange[1])))
        .style('text-anchor', 'end')
        .attr('transform', trn_str(width,0));

    focus.append('g')
		.attr('class', 'y chart__grid')
		.call(make_y_axis()
			.tickSize(-width, 0, 0)
			.tickFormat(''));
			
    barsGroup.append('g')
		.attr('class', 'y chart__grid')
		.call(make_y_axis()
			.tickSize(-width, 0, 0)
			.tickFormat(''));			
			
/*
    var averageChart = focus.append('path')
        .datum(data)
        .attr('class', 'chart__line chart__average--focus line')
        .attr('d', avgLine);
*/
    var priceChart = focus.append('path')
        .datum(data)
        .attr('class', 'chart__line chart__price--focus line')
        .attr('d', priceLine);
		

		
    var barsGroupChart = barsGroup.selectAll('rect')
        .data(data)
      .enter().append('rect')
        .attr('class', 'chart__bars')
        .attr('x', function(d, i) { return x(d.date); })
        .attr('height', function(d) { return volume_h - y2(d.volume); })
        .attr('width',  1)
        .attr('y', function(d) { return y2(d.volume); });		
		
		
    focus.append('g')
		.attr('class', 'x axis')
		.attr('transform', trn_str(0,height) )
		.call(xAxis);

    focus.append('g')
		.attr('class', 'y axis')
		.attr('transform', trn_str(y_axis_margin,0))
		.call(yAxis);
		

///////////////
    var helper = focus.append('g')
        .attr('class', 'chart__helper')
        .style('text-anchor', 'start')
        .attr('transform', trn_str(0,-1));

    var helperText = helper.append('text'),
    	 priceTooltip = focus.append('g')
			.attr('class', 'chart__tooltip--price')
			.append('circle')
			.style('display', 'none')
			.attr('r', focus_cirle.radius);
/*
    var averageTooltip = focus.append('g')
        .attr('class', 'chart__tooltip--average')
        .append('circle')
        .style('display', 'none')
        .attr('r', 2.5);
*/
    var mouseArea = svg.append('g')
        .attr('class', 'chart__mouse')
        .append('rect')
        .attr('class', 'chart__overlay')
        .attr('width', width)
        .attr('height', height)
        .attr('transform', trn_str(fig_size.left,fig_size.top))
        .on('mouseover', function () {
            helper.style('display', null);
            priceTooltip.style('display', null);
           // averageTooltip.style('display', null);
        })
        .on('mouseout', function () {
            helper.style('display', 'none');
            priceTooltip.style('display', 'none');
           // averageTooltip.style('display', 'none');
        })
        .on('mousemove', mousemove);

    context.append('path')
		.datum(data)
		.attr('class', 'chart__area area')
		.attr('d', area2);

    context.append('g')
    .attr('class', 'x axis chart__axis--context')
    .attr('y', 0)
    .attr('transform', 'translate(0,' + (height2 - 22) + ')')
   .call(xAxis2)
	;

    context.append('g')
    .attr('class', 'x brush')
    .call(brush)
    .selectAll('rect')
    .attr('y', -6)
    .attr('height', height2 + 7);

    function mousemove() {
        var x0 = x.invert(d3.mouse(this)[0]);
        var i = bisectDate(data, x0, 1);
        var d0 = data[i - 1];
        var d1 = data[i];
        var d = x0 - d0.date > d1.date - x0 ? d1 : d0;
        helperText.text(legendFormat(new Date(d.date)) + ' - Price: ' + numberWithSpaces(d.price) + ' Volume: ' + numberWithSpaces(d.volume));
        priceTooltip.attr('transform', 'translate(' + x(d.date) + ',' + y(d.price) + ')');
        //averageTooltip.attr('transform', 'translate(' + x(d.date) + ',' + y(d.average) + ')');
    }

    function brushed() {

        const brush_event = d3.event.selection;

        const brush_empty = (brush_event === null);

        if (!brush_empty) {
            var ext = brush_event.map(x2.invert);
            x.domain(brush_empty ? x2.domain() : ext);

            y.domain([
                    d3.min(data.map(function (d) {
                            return (d.date >= ext[0] && d.date <= ext[1]) ? d.price : max;
                        })),
                    d3.max(data.map(function (d) {
                            return (d.date >= ext[0] && d.date <= ext[1]) ? d.price : min;
                        }))
                ]);

            range.text(legendFormat(new Date(ext[0])) + ' - ' + legendFormat(new Date(ext[1])))

            barsGroupChart.attr('x', function (d, i) {return x(d.date);});

            var days = Math.ceil((ext[1] - ext[0]) / (24 * 3600 * 1000))
                ///
                barsGroupChart.attr('width', (40 > days) ? (40 - days) * 5 / 6 : 5)

        }

        priceChart.attr('d', priceLine);
		//barsGroupChart.attr('d', priceLine);
        //averageChart.attr('d', avgLine);
        focus.select('.x.axis').call(xAxis);
        focus.select('.y.axis').call(yAxis);
		
	   // barsGroup.select('.x.axis').call(xAxis);
     //   barsGroup.select('.y.axis').call(yAxis);	

    }

    var dateRange = ['1w', '1m', '3m', '6m', '1y', '5y','x']
    for (var i = 0, l = dateRange.length; i < l; i++) {
        var v = dateRange[i];
        rangeSelection
        .append('text')
        .attr('class', 'chart__range-selection')
        .text(v)
        .attr('transform', 'translate(' + (18 * i) + ', 0)')
        .on('click', function (d) {
            focusOnRange(this.textContent);
        });
    }

    function focusOnRange(range) {

        var today = new Date(data[data.length - 1].date)
            var ext = new Date(data[data.length - 1].date),
			   first_date=new Date(data[0].date),
			 flg=1;

            if (range === '1m'){
			ext.setMonth(ext.getMonth() - 1)}

                else if (range === '1w'){
				ext.setDate(ext.getDate() - 7)}

                    else if (range === '3m'){
                        ext.setMonth(ext.getMonth() - 3)}

                        else if (range === '6m'){
							ext.setMonth(ext.getMonth() - 6)}

                            else if (range === '1y'){
								ext.setFullYear(ext.getFullYear() - 1)}

                                else if (range === '5y'){
								ext.setFullYear(ext.getFullYear() - 5)}
								else {
									flg=0;
								}
                                    if (flg === 1){
                                    context.select('g.x.brush').call(brush.move, [ext, today].map(x2))
									}	else {
									context.select('g.x.brush').call(brush.move, [first_date, today].map(x2));
									context.select('g.x.brush').call(brush.move, null);
									}
									
                                    //brushed();

                                    //context.select('g.x.brush').call(brush.move, [ext, today].map(x2))
    }

}










