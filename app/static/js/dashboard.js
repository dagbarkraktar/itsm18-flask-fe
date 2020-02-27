//
// JS helper functions
//
function drawSensorGraph(container_id) {

    // initialize echarts instance
    var myChart = echarts.init(document.getElementById(container_id), 'dark');

    $.get("./sensors").done(function(response){

        //var data32 = jQuery.parseJSON(response);
        var data32 = JSON.parse(response);

        var dateList = data32.map(function (item) { return item[0]; });
        var valueList = data32.map(function (item) { return item[1]; });

        // last value in dataset (current temperature to show over the graph)
        var lastValue = valueList[valueList.length-1];

        option = {
            backgroundColor: 'transparent',
            title: {
                text: lastValue+'°C', // last value in data
                textAlign: 'left',
                left: '65',
                top: '25',
                textStyle: {
                    fontSize: 50,
                    color: 'rgba(255, 255, 255, 0.7)'
                }
            },

            tooltip: {
                trigger: 'axis'
            },
            xAxis: {
                data: dateList,
                splitLine: {
                    show: true,
                    lineStyle: {
                        color: 'rgba(255, 255, 255, 0.3)'
                    }
                },
                axisLabel: {
                    textStyle: {
                        color: 'rgba(255, 255, 255, 0.7)'
                    },
                    // format data to DD/MM HH:MM
                    formatter: function(value){
                        var date = new Date(value);

                        var hours = date.getUTCHours()
                        if (hours < 10)
                            hours = "0" + hours;

                        var minutes = date.getUTCMinutes()
                        if (minutes < 10)
                            minutes = "0" + minutes;

                        // DD/MM HH:MM
                        return date.getDate() + "/" + (date.getMonth()+1) + " " + hours + ":" + minutes;
                    }
                },
                axisLine: {
                    lineStyle: {
                        color: 'rgba(255, 255, 255, 0.7)'
                    }
                }
            },
            yAxis: {
                min: 15,
                max: 30,
                splitLine: {
                    show: true,
                    lineStyle: {
                        color: 'rgba(255, 255, 255, 0.3)'
                    }
                },
                axisLabel: {
                    formatter: '{value} °C',
                    textStyle: {
                        color: 'rgba(255, 255, 255, 0.7)'
                    }
                },
                axisLine: {
                    lineStyle: {
                        color: 'rgba(255, 255, 255, 0.7)'
                    }
                }
            },

            grid: { // margins: x,y = left,top x2,y2 = right,bottom
                x: 60, // default 80
                y: 20, // default 60
                x2: 40, // default 80
                show: true,
                borderColor: 'rgba(255, 255, 255, 0.3)'
            },

            dataZoom: [{
                //startValue: '2019-03-30'
                startValue: dateList[dateList.length-48],
                //backgroundColor: 'rgba(221,160,221,0.5)',
                //fillerColor: 'rgba(38,143,26,0.6)',
                //handleColor: 'rgba(128,43,16,0.8)',
                height: 25,
                y: 180,
                y2: 0,
                dataBackgroundColor: 'rgba(255,255,255,0.4)'
            }, {
                type: 'inside'
            }],
            visualMap: {
                show: false, // don't show visual map legend
                top: 10,
                right: 10,
                pieces: [{
                    gt: 15,
                    lte: 18,
                    color: '#0000cd'
                },{
                    gt: 18,
                    lte: 21,
                    color: '#096'
                }, {
                    gt: 21,
                    lte: 22,
                    color: '#ffde33'
                }, {
                    gt: 22,
                    lte: 24,
                    color: '#ff9933'
                }, {
                    gt: 24,
                    lte: 33,
                    color: '#cc0033'
                }, {
                    gt: 33,
                    color: '#660099'
                }],
                outOfRange: {
                    color: '#999'
                }
            },
            series: {
                name: 'Temp °C',
                type: 'line',
                data: valueList,
                smooth: true
                /*,
                tooltip:{
                    trigger: 'item',
                    formatter: "{c}°C<br>{b}" // {c}=temperature value {b}=datetime
                }
                markLine: {
                    silent: true,
                    data: [{
                        yAxis: 50
                    }, {
                        yAxis: 100
                    }, {
                        yAxis: 150
                    }, {
                        yAxis: 200
                    }, {
                        yAxis: 300
                    }]
                }*/
            }
        }

        // use configuration item and data specified to show chart
        myChart.setOption(option);
    });
}


// Fill table and draw bar chart for backups
function drawBackupsData(data_table_id) {

    data_table = document.getElementById(data_table_id)

    $.get("./backups_data").done(function(response){
        var data = JSON.parse(response);

        var cnt = 0;
        var backup_title = ["Backup: BUHSRV", "Backup: ORACLE", "Backup: SDP", "Backup: SUDIMOST"];
        var backup_norm_val = [1500, 10000, 800, 12];

        for (data_name in data) {
            // Dataset for each backup
            b_data = data[data_name]
            // last file size in MBytes
            var last_val = (b_data[9][1]/1024/1024).toFixed(2);
            // (today - yesterday) in bytes
            var delta = b_data[9][1] - b_data[8][1]

            var trow = ""
            // OK or NOT OK
            if (last_val > backup_norm_val[cnt]) trow = trow + "<td><span class='badge badge-success'>OK</span></td>"
            else trow = trow + "<td><span class='badge badge-danger'>???</span></td>"
            // Title and last backup filesize
            trow = trow + "<td>" + backup_title[cnt] + "</td>"
            trow = trow + "<td style='text-align:right;'>" + last_val + " MB</td>"
            // Trend for filesize
            if (delta > 0) trow = trow + "<td><span data-feather='trending-up'></span></td>"
            else if (delta < 0) trow = trow + "<td><span data-feather='trending-down'></span></td>"
            else trow = trow + "<td><span data-feather='activity'></span></td>"
            // add div for barchart
            trow = trow + "<td><div id='stat_0" + cnt + "_chart' style='width:100px; height:25px;'></div></td>"
            // add row to table
            // $("#backups_chart_table").append("<tr>" + trow + "</tr>");
            $(data_table).append("<tr>" + trow + "</tr>");
            // draw barchart with b_data dataset in specified div
            drawBarStat("stat_0" + cnt + "_chart", b_data);
            // iterate cnt
            cnt++;
        }
        // replace feather icons
        feather.replace()
    });
}

// Draw piechart for hdd drive (used/free space)
function drawDrivePie(used, free, drive_name, container_id) {

    // initialize echarts instance
    var myChart = echarts.init(document.getElementById(container_id));

    var spaceUsed = used;
    var spaceFree = free;
    var pieColor = '#00CC76';
    var percentFree = (spaceFree/(spaceUsed+spaceFree)*100)
    // set pie color depending on free drive space
    if (percentFree < 10) pieColor = '#cc0033' // red (danger)
    else
        if(percentFree < 20) pieColor = '#ff9933' // orange (warning)
        else pieColor = '#00CC76' // green (good)

    // specify chart configuration item and data
    option = {
        //backgroundColor: '#031f2d',
        tooltip: {},

    series: [{
        name: 'PIE01',
        type: 'pie',
        radius: ['60%', '85%'], // donut size
        //center:['10%','50%'], // position
        color: pieColor,
        label: {
            normal: {
                position: 'center'
            }
        },
        data: [{
            value: spaceFree,
            name: 'Free space',

            label: {
                normal: {
                    //formatter: '{d} %',
                    //formatter: '{c} Gb',
                    formatter: function(param){
                        return Math.round(param.value)+" Gb"
                    },
                    textStyle: {
                        fontSize: 18
                    }
                }
            },
            tooltip:{
                    trigger: 'item',
                    formatter: "{b}: {c} Gb ({d}%)"
            }
        }, {
            value: spaceUsed,
            name: 'Used space',
            label: {
                normal: {
                    //formatter: '\nDrive D:',
                    formatter: '\n'+drive_name,
                    textStyle: {
                        color: '#ccc',
                        fontSize: 14
                    }
                }
            },
            tooltip:{
                    trigger: 'item',
                    formatter: "{b}: {c} Gb ({d}%)"
            },
            itemStyle: {
                normal: {
                    color: '#aaa'
                },
                emphasis: {
                    color: '#aaa'
                }
            },
        }]
    }]
    };

    // use configuration item and data specified to show chart
    myChart.setOption(option);
}

function drawBarStat(container_id, data) {

    // map date and value rows from data
    var dateList = data.map(function (item) { return item[0]; });
    var valueList = data.map(function (item) { return (item[1]/1024/1024).toFixed(2); });

    // initialize echarts instance
    var myChart = echarts.init(document.getElementById(container_id));

    // specify chart configuration item and data
    var option = {
        //backgroundColor: '#031f2d',
        grid: {x: '0%', y: '0%', width: '100%', height: '100%'},
        tooltip: {},
        // set bar color depending on value levels
        color: function(params){
            if (params.value < 10)
                return "#cc0033"; // red
            else return "#00CC76"; // green
        },
//        xAxis: {data: [1,2,3,4,5,6,7,8,9,10], show:false},
        xAxis: {data: dateList, show:false},
        yAxis: {show:false},
        series: [{
            name: 'Backup file size, MB',
            type: 'bar',
//            data: [5,12,11,10,7,11,13,10,8,6]
            data: valueList
        }]
    };

    // use configuration item and data specified to show chart
    myChart.setOption(option);
}
