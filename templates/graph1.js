window.onload = function () {

    var data;
    var requestOptions = {
        method: 'GET',
        redirect: 'follow'
      };
      
      fetch("158.108.182.10:3000/get_data", requestOptions)
        .then(response => {data=response.json})
        .then(result => console.log(result))
        .catch(error => console.log('error', error));

    var dps = []; // dataPoints
    var chart = new CanvasJS.Chart("chartContainer", {
        title :{
            text: "Total Money VS Time-Interval Park.1"
        },
        data: [{
              lineColor : "darkblue",
            type: "line",
            dataPoints: dps
        }],
         axisX:{
              title: "Time"
         },
          axisY:{
              title: "Total Money"
        }
    });
    
    var xVal = 0;
    var yVal = 0; //half part of y
    var updateInterval = 1000; // run time of graph
    var dataLength = 20; // number of dataPoints visible at any point // ความยาวแกน x
    
    var updateChart = function (count) {
    
        count = count || 1;
    
        for (var j = 0; j < count; j++) {
            dps.push({
                x: xVal,
                y: yVal
            });
            //change x y from here
            xVal = data["P1"]["this_park_time"];
            yVal = data["P1"]["charge"];
        }
    
        if (dps.length > dataLength) {
            dps.shift();
        }
    
        chart.render();
    };
    
    updateChart(dataLength);
    setInterval(function(){updateChart()}, updateInterval);
    
    }