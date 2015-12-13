var data_todaybird = [];
var data_allbird = [];
$(document).ready(function(){
    alert('1');
    get_userinfo(function(data){
		openid = data.openid;
		nickname = data.nickname;
		headimgurl = data.headimgurl;
        $.getJSON("data/gamerank?game=bird&start=0&end=100",function(data){
            alert(JSON.stringify(data));
            handle_data(data_todaybird, data.today);
            handle_data(data_allbird, data.total);
            get_todayBird();
        });
	});
});

function handle_data(data,data_list){
    for(var i = 0; i < data_list.length; i++){
        var color;
        if(data_list[i].openid == openid){
            color = "#00FF7F";
        }
        else{
            color = "#1E90FF";
        }
        var data_object = {
            user_rank: i+1,
            user_photo: data_list[i].headimgurl,
            user_name: data_list[i].nickname,
            user_num: data_list[i].score,
            user_title: get_title(i),
            user_color: color
        };
        data.push(data_object);
    }
}

function get_rank(type){
    var data = [];
    $('a').attr({'class':'item'});
    if(type == 0){
        $('#todaybird').attr({'class':'item active'});
        data = data_todaybird;
    }
    else if(type == 1){
        $('#todaysquare').attr({'class':'item active'});
        data = data_today;
    }
    else if(type == 2){
        $('#allbird').attr({'class':'item active'});
        data = data_allbird;
    }
    else if(type == 3){
        $('#allsquare').attr({'class':'item active'});
        data = data_all;
    }
    $('#rank_content').html("");
    for(var i = 0; i < 4; i++){
        var dom_template = `
        <div class="item" style="background-color:${data[i].user_color}">
               <div class="ui big teal label">${data[i].user_rank}</div>
               <img class="ui avatar image" src=${data[i].user_photo}>
               <div class="content">
                   <div class="header">${data[i].user_name}</div>
                   <div class="meta">
                       <span class="cinema">${data[i].user_title}</span>
                   </div>
               </div>
               <div class="right floated content">
                   <span class="left floated content">${data[i].user_num}</span>
                   <i class="smile icon"></i>
               </div>
        </div>`
        $('#rank_content').append(dom_template);
    }
}
function get_todayBird(){
    get_rank(0);
}
function get_todaySquare(){
    get_rank(1);
}
function get_allBird(){
    get_rank(2);
}
function get_allSquare(){
    get_rank(3);
}
function get_title(i){
    if(i == 0)
        return "王牌战斗鸡";
    if(i == 1)
        return "王牌飞行鸡";
    if(i == 2)
        return "王牌僚鸡";
    else{
        return "菜鸡";
    }
}