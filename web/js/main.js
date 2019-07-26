api_crawler = 'http://localhost:5000/crawler/';
api_dataset = 'http://localhost:5000/dataset/';
api_cluster = 'http://localhost:5000/cluster/';

var timerHandler;
var current_dataset = 'demo';
var current_cluster = 'kmeans';

$(document).ready(function () {
  crawler_status();
  loadDataSet(current_dataset)
});

function toggleDataViewer() {
  $('#data_viewer_table').slideToggle()
}

// crawler control
function crawler_start() {
  $.ajax(api_crawler + 'start').done(function (d) {
    update_crawler_status(d);
    timerHandler = setInterval(crawler_status, 1000);
  })
}

function crawler_status() {
  $.ajax(api_crawler + 'status').done(function (d) {
    update_crawler_status(d)
  })
}

function crawler_stop() {
  $.ajax(api_crawler + 'stop').done(function (d) {
    update_crawler_status(d)
  })
}

function update_crawler_status(d) {
  $('#crawler_status').text(d.status);
  $('#crawler_message').text(d.message);
  if (d.status === '0' && d.message === 'Stopped.') {
    clearInterval(timerHandler)
  }
}

// d3js table view
var tabulate = function (data,columns) {
  var table = d3.select('#data_viewer_table').append('table').attr('class', 'table table-striped table-sm');
  var thead = table.append('thead');
  var tbody = table.append('tbody');

  thead.append('tr')
    .selectAll('th')
    .data(columns)
    .enter()
    .append('th')
    .text(function (d) { return d });

  var rows = tbody.selectAll('tr')
    .data(data)
    .enter()
    .append('tr')
    .selectAll('td')
    .data(function (d) { return d })
    .enter()
    .append('td')
    .text(function (d) { return d });

  return table;
};

function loadDataSet(dataset) {

  current_dataset = dataset;

  // reset table
  d3.select('#data_viewer_table').html("");
  var table = d3.select('#data_viewer_table').append('table').attr('class', 'table table-striped table-sm');

  d3.json(api_dataset + dataset, function (d) {
    if (d.status === 0) {
      // success get data
      // first line is header
      var columns = d.data.shift();
      tabulate(d.data, columns)
    }
    else {
      // error
      table.text(d.data)
    }
  });


}function loadCluster(cluster) {

  current_cluster = cluster;

  // reset vis
  d3.select('#cluster_visualisation').html("");

// set the dimensions and margins of the graph
    var margin = {top: 10, right: 30, bottom: 30, left: 60},
      width = 1200 - margin.left - margin.right,
      height = 400 - margin.top - margin.bottom;

// append the svg object to the body of the page
    var svg = d3.select("#cluster_visualisation").append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform",
        "translate(" + margin.left + "," + margin.top + ")");

//Read the data
    d3.json(api_cluster + current_dataset + '/' + current_cluster, function (d) {

      data = d.data;

      color = ["#007FFF", '#DA1884', '#006B3C', '#9966CC', '#006B3C'];

      // Add X axis
      var x = d3.scaleLinear()
        .domain([0, 80])
        .range([ 0, width ]);
      svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x));

      // Add Y axis
      var y = d3.scaleLinear()
        .domain([0, 30])
        .range([ height, 0]);
      svg.append("g")
        .call(d3.axisLeft(y));

      // Add dots
      svg.append('g')
        .selectAll("dot")
        .data(data)
        .enter()
        .append("circle")
        .attr("cx", function (d) { return x(d.Location); } )
        .attr("cy", function (d) { return y(d.Connection); } )
        .attr("r", 5)
        .style("fill", function (d) { return color[d['group']]})

        })

}



