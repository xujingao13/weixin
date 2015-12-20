/**
 * Created by littlepig on 2015/12/20.
 */
$(document).ready(function(){
    /*
    get_userinfo(function(data){
		openid = data.openid;
		nickname = data.nickname;
		headimgurl = data.headimgurl;
		headimgurl = data.headimgurl;
		$.getJSON("data/getTimeLineData?openid="+openid, function(data){
			renderByJson(data);
		})
	});*/
    data = getData();
    renderByJson(data);
});

function renderByJson(data){
    for(j = 0; j < 7; j++){
        for(i = 0; i < data.length; i++){
            if(!("none" in data[i])){
                addOneElement(getHTMLDict(data[i]), j);
            }
        }
        addItem(j);
    }
}

function addItem(j){
    $("#item"+j).append("<div class=\"carousel-caption\">"+ "title" + j + "</div>");
    $("#item"+j).append("<div style=\"height:20px;\"><div>");
}

function addOneElement(data, num){
    var newElement =  $("<div class=\"cd-timeline-block\">" +
            "<div class=\"cd-timeline-img cd-picture\"> " +
                data["imgString"] +
            "</div>" +
            "<div class=\"cd-timeline-content\">" +
                data["dataString"] +
            "</div>" +
            "</div>");
    $("#cd-timeline" + num).append(newElement);
}

function getHTMLDict(data){
    if("none" in data){
        return "";
    }
    else if(data["type"] == 1){
        return {
            imgString:getImgString("sleep.png"),
            dataString:getH2Element("Sleep") +
                getTime(data["startTime"])
        }
    }
    else if(data["type"] == 2){
        if(data["subType"] == 1){
            return {
                imgString:getImgString("warm_up.png"),
                dataString:getH2Element("Warm Up") +
                    getTime(data["startTime"])
            }
        }
        else if(data["subType"] == 2){
            return {
                imgString:getImgString("sport_walk.png"),
                dataString:getH2Element("Sport Walk") +
                    getTime(data["startTime"])
            }
        }
        else if(data["subType"] == 3){
            return {
                imgString:getImgString("ball.png"),
                dataString:getH2Element("Ball") +
                    getTime(data["startTime"])
            }
        }
        else if(data["subType"] == 4){
            return {
                imgString:getImgString("run.png"),
                dataString:getH2Element("Run") +
                    getTime(data["startTime"])
            }
        }
        else if(data["subType"] == 5){
            return {
                imgString:getImgString("swim.png"),
                dataString:getH2Element("Swim") +
                    getTime(data["startTime"])
            }
        }
    }
    else{
        if(data["subType"] == 1){
           return {
                imgString:getImgString("coffee.png"),
                dataString:getH2Element("Office") +
                    getTime(data["startTime"])
           }
        }
        else if(data["subType"] == 2){
            return {
                imgString:getImgString("walk.png"),
                dataString:getH2Element("Walk") +
                    getTime(data["startTime"])
            }
        }
        else if(data["subType"] == 3){
            return {
                imgString:getImgString("car.png"),
                dataString:getH2Element("Car") +
                    getTime(data["startTime"])
            }
        }
    }
}

function getImgString(data){
    return "<img src=\"images/TimeLine/" + data  + "\"alt=\"Picture\"> "
}

function getPElement(data){
    return "<p>" + data +"</p>"
}

function getH2Element(data){
    return "<h2>" + data +"</h2>"
}

function getTime(data){
    return "<span class=\"cd-date\">" + data + "</span>"
}

function getData(){
    data = []
    data[0] = {
        type:1,
        startTime:"12:50"
    }
    data[1] = {
        type:2,
        subType:1,
        startTime:"13:00"
    }
    data[2] = {
        type:2,
        subType:2,
        startTime:"13:10"
    }
    data[3] = {
        type:2,
        subType:3,
        startTime:"13:10"
    }
    data[4] = {
        type:2,
        subType:4,
        startTime:"13:20"
    }
    data[5] = {
        type:2,
        subType:5,
        startTime:"13:30"
    }
    data[6] = {
        type:3,
        subType:1,
        startTime:"13:00"
    }
    data[7] = {
        type:3,
        subType:2,
        startTime:"13:10"
    }
    data[8] = {
        type:3,
        subType:3,
        startTime:"13:10"
    }
    return data;
}