var data_today = [
    {'user_rank': 1,'user_photo': "rank/1.jpg",'user_name': "Jingao",'user_lastTime': "15:00",'user_num':"20关",'user_color':"#00FF7F"},
    {'user_rank': 2,'user_photo': "rank/2.jpg",'user_name': "赵毅",'user_lastTime': "14:00",'user_num':"10关",'user_color':"#1E90FF"},
    {'user_rank': 3,'user_photo': "rank/3.jpg",'user_name': "朱子晨",'user_lastTime': "13:00",'user_num':"5关",'user_color':"#1E90FF"},
    {'user_rank': 4,'user_photo': "rank/4.jpg",'user_name': "学弟",'user_lastTime': "12:00",'user_num':"4关",'user_color':"#1E90FF"}
];
var data_all = [
    {'user_rank': 1,'user_photo': "rank/1.jpg",'user_name': "Jingao",'user_lastTime': "今天",'user_num':"80关",'user_color':"#00FF7F"},
    {'user_rank': 2,'user_photo': "rank/2.jpg",'user_name': "赵毅",'user_lastTime': "昨天",'user_num':"70关",'user_color':"#1E90FF"},
    {'user_rank': 3,'user_photo': "rank/3.jpg",'user_name': "朱子晨",'user_lastTime': "星期五",'user_num':"60关",'user_color':"#1E90FF"},
    {'user_rank': 4,'user_photo': "rank/4.jpg",'user_name': "学弟",'user_lastTime': "星期四",'user_num':"50关",'user_color':"#1E90FF"}
];
$(document).ready(function(){
    get_todayRank();
});
function get_rank(time){
    var data = [];
    if(time == 0){
        data = data_today;
        $('#today').attr({
            'class':'item active'
        });
        $('#all').attr({
            'class':'item'
        });
    }
    else{
        data = data_all;
        $('#today').attr({
            'class':'item'
        });
        $('#all').attr({
            'class':'item active'
        });
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
                       <span class="cinema">${data[i].user_lastTime}</span>
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
function get_todayRank(){
    get_rank(0);
}
function get_allRank(){
    get_rank(1);
}