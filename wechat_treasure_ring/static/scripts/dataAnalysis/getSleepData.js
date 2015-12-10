/**
 * Created by littlepig on 2015/11/29.
 */
 var openid;
$(document).ready(function(){
	$(function () {
		$('#collapseOne').collapse('show');
		$('#collapseTwo').collapse('show');
		$('#collapseThree').collapse('show');
		$('#collapseFour').collapse('show');
	});
	draw();
	getopenid(function(data){
		openid = data;
		alert(openid);
		$.getJSON("data/sleepData?openid="+data, function(sleepData){
			renderByJson(sleepData);
		})
	});
});

//test drawing
function draw(){
	var weekChartId = "week_sleep_chart";
	var weekChartSleepTime = [6,7,5,7,6,7,6];
	var weekChartDeepSleepTime = [5,6,4,6,5,6,5];
	var monthChartId = "month_sleep_chart";
	var monthChartSleepTime = [6,7,5,7,6,7,6];
	var monthChartDeepSleepTime = [5,6,4,6,5,6,5];

	sleepChart(weekChartSleepTime, weekChartDeepSleepTime, 7, weekChartId);
	sleepChart(monthChartSleepTime, monthChartDeepSleepTime, 7, monthChartId);
	setDataText("7-days-avg", Math.floor(Math.random()*24)+1, "h");
	setDataText("30-days-avg", Math.floor(Math.random()*24)+1, "h");
	setDataText("7-days-deep-avg", Math.floor(Math.random()*24)+1, "h");
	setDataText("30-days-deep-avg", Math.floor(Math.random()*24)+1, "h");
	setSleepFluctuate("7-days-flac", 1);
	setSleepFluctuate("30-days-flac", 0);
	setSleepDeepRate("7-deep-avg", 1);
	setSleepDeepRate("30-deep-avg", 2);
}

//draw the charts and change the data according to the json
function renderByJson(json){
	if(json == []){
		draw();
		return;
	}
	sleepChart(json["7-days-sleep"], json["7-days-deep-sleep"], 7, "week_sleep_chart");
	sleepChart(json["30-days-sleep"], json["30-days-deep-sleep"], 30, "month_sleep_chart");
	setDataText("7-days-avg", json["7-days-avg"], "h");
	setDataText("30-days-avg",json["30-days-avg"], "h");
	setDataText("7-days-deep-avg", json["7-days-deep-avg"], "h");
	setDataText("30-days-deep-avg",json["30-days-deep-avg"], "h");
	setSleepFluctuate("7-days-flac", json["7-days-flac"]);
	setSleepFluctuate("30-days-flac", json["30-days-flac"]);
	setSleepDeepRate("7-deep-avg", json["7-days-avg"]);
	setSleepDeepRate("30-deep-avg", json["30-deep-avg"]);
}

//draw the sleep chart(including sleep time and deep sleep time)
function sleepChart(chartSleepTime,chartDeepSleepTime, days, chartId){
	var sleepTime = [], deepSleepTime = [];
    for (var i = 0; i < 7; i += 1) {
        sleepTime.push([i,chartSleepTime[i]]);
        deepSleepTime.push([i, chartDeepSleepTime[i]]);
    }
	$.plot($("#" + chartId),
		[ { data: sleepTime, label: "sleep time"}, { data: deepSleepTime, label: "deep sleep time" } ], {
			series: {
				lines: { show: true },
				points: { show: true }
			},

			grid: { hoverable: true, clickable: true },
			xaxis: { min: 1, max: 7 },
			yaxis: { min: 1, max: 15 },
			colors: ["#F90", "#3C4049"]
		});
}

//set data according to the data, "suffix" is the unit
function setDataText(idString, data, suffix){
	$("#" + idString).text(String(data) + suffix);
}
//judge whether the fluctuation is normal
function setSleepFluctuate(idString, data){
	var result = "";
	if(data == 0){
		result = "Normal";
	}
	else{
		result = "Greatly";
	}
	$("#" + idString).text(result);
}
//judge whether the deep sleep rate is normal
function setSleepDeepRate(idString, data){
	var result = "";
	if(data == 0){
		result = "Low";
	}
	else{
		result = "Normal";
	}
	$("#" + idString).text(result);
}