// Dependencies
var d3 = require('d3');
var request = require('d3-request');
require("d3-geo-projection")(d3);
var topojson = require('topojson');
var _ = require('lodash');

var fm = require('./fm');
var throttle = require('./throttle');
var features = require('./detectFeatures')();

// Globals
var DEFAULT_WIDTH = 940;
var MOBILE_THRESHOLD = 600;
var PLAYBACK_SPEED = 200;

var bordersData = null;
var reactorsData = null;

var isMobile = false;

var playbackYear = 1955;

function init() {
  request.json('data/borders-topo.json', function(error, data) {
    bordersData = topojson.feature(data, data['objects']['ne_110m_admin_0_countries']);

    request.json('data/reactors.json', function(error, data) {
      reactorsData = data;

      render();
      $(window).resize(throttle(onResize, 250));
    });
  });
}

function onResize() {
  render()
}

function render() {
  var width = $('#interactive-content').width();

  if (width <= MOBILE_THRESHOLD) {
      isMobile = true;
  } else {
      isMobile = false;
  }

  playbackYear = playbackYear + 1;

  if (playbackYear > 2015) {
    playbackYear = 1955;
  }

  renderMap({
    container: '#map',
    width: width,
    borders: bordersData,
    sites: reactorsData['sites'],
    year: reactorsData['years'][playbackYear]
  });

  $('#year').text(playbackYear);

  // Resize
  fm.resize()

  _.delay(render, PLAYBACK_SPEED);
}

/*
 * Render a map.
 */
function renderMap(config) {
    /*
     * Setup
     */
    var aspectRatio = 5 / 2.5;
    var defaultScale = 180;

    var margins = {
      top: 0,
      right: 0,
      bottom: 0,
      left: 0
    };

    // Calculate actual chart dimensions
    var width = config['width'];
    var height = width / aspectRatio;

    var chartWidth = width - (margins['left'] + margins['right']);
    var chartHeight = height - (margins['top'] + margins['bottom']);

    var mapCenter = [10, 13];
    var scaleFactor = chartWidth / DEFAULT_WIDTH;
    var mapScale = scaleFactor * defaultScale;

    var projection = d3.geo.robinson()
      .center(mapCenter)
      .translate([width / 2, height / 2])
      .scale(mapScale);

    var geoPath = d3.geo.path()
      .projection(projection)

    // Clear existing graphic (for redraw)
    var containerElement = d3.select(config['container']);
    containerElement.html('');

    /*
     * Create the root SVG element.
     */
    var chartWrapper = containerElement.append('div')
      .attr('class', 'graphic-wrapper');

    var chartElement = chartWrapper.append('svg')
      .attr('width', chartWidth + margins['left'] + margins['right'])
      .attr('height', chartHeight + margins['top'] + margins['bottom'])
      .append('g')
      .attr('transform', 'translate(' + margins['left'] + ',' + margins['top'] + ')');

    /*
     * Create geographic elements.
     */
    var borders = chartElement.append('g')
      .attr('class', 'borders');

    borders.selectAll('path')
      .data(config['borders']['features'])
      .enter().append('path')
        .attr('id', function(d) {
          return d['id'];
        })
        .attr('d', geoPath);

    var reactors = chartElement.append('g')
      .attr('class', 'reactors');

    reactors.selectAll('circle')
      .data(config['year'])
      .enter().append('circle')
        .attr('r', 3)
        .attr('cx', function(d) {
          var coords = config['sites'][d[0]];

          if (_.isUndefined(coords)) {
            return 0;
          }

          return projection(coords)[0];
        })
        .attr('cy', function(d) {
          var coords = config['sites'][d[0]];

          if (_.isUndefined(coords)) {
            return 0;
          }

          return projection(coords)[1];
        })
        .attr('class', function(d) {
          return d[1];
        });

    // reactors.selectAll('text')
    //   .data(config['year'])
    //   .enter().append('text')
    //     .attr('x', function(d) {
    //       var coords = config['sites'][d[0]];
    //
    //       if (_.isUndefined(coords)) {
    //         return 0;
    //       }
    //
    //       return projection(coords)[0];
    //     })
    //     .attr('y', function(d) {
    //       var coords = config['sites'][d[0]];
    //
    //       if (_.isUndefined(coords)) {
    //         return 0;
    //       }
    //
    //       return projection(coords)[1];
    //     })
    //     .text(function(d) {
    //       return d[1];
    //     });
}

$(document).ready(function () {
  init();
});
