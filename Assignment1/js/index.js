var ctx = document.getElementById('myChart').getContext('2d');

var dataset = {};
data.forEach(d => {
  Object.keys(d).forEach(key => {
    if (dataset[key]) {
      dataset[key].push(d[key])
    } else {
      dataset[key] = [d[key]]
    }
  })
})

var labels = dataset.Year;
var years = [...dataset.Year];
delete dataset.Year;


//backgroung color =  white, black, red, yellow, green, and blue.

var colors = ['#3366ff', '#ff0000', '#cc3300', '#cccc00', '#000066', '#666699', '#339966', '#003300', '#999966', '#003399', '#339933', '#006666', '#ff9933', '#00cc99'];


dataset = Object.keys(dataset).map((key, i) => {
  return {
    label: key,
    data: dataset[key],
    borderColor: colors[i],
    borderWidth: 1,
    fill: false
  }
})


var myChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: labels,
    datasets: dataset,
    options: {
      title: {
        display: true,
        text: 'Global, hemespheric and zonal average tempartures.',
        // position: 'top'
      }
    }
  }
});


$(".js-range-slider").ionRangeSlider({
  type: "double",
  min: Math.min(...years),
  max: Math.max(...years),
  onFinish: onFinish,
});


function updateChartData(to, from) {

  var dataset = {};
  data.forEach(d => {
    if (d.Year >= from && d.Year <= to) {
      Object.keys(d).forEach(key => {
        if (dataset[key]) {
          dataset[key].push(d[key])
        } else {
          dataset[key] = [d[key]]
        }
      })
    }
  })
  delete dataset.Year;
  dataset = Object.keys(dataset).map((key, i) => {
    return {
      label: key,
      data: dataset[key],
      borderColor: colors[i],
      borderWidth: 1,
      fill: false
    }
  })
  return dataset;

}

function onFinish(data) {
  let labels = years.filter(year => (year >= data.from && year <= data.to));
  myChart.data.labels = labels;
  myChart.data.datasets = updateChartData(data.to, data.from);
  myChart.update();
}
