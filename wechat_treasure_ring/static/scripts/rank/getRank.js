$(document).ready(function(){
    get_todayRank();
});
function get_todayRank(){
    $('#today').attr({
        'class':'item active'
    });
    $('#all').attr({
        'class':'item'
    });
    $('#rank_content').html("");
    for(var i = 0; i < 4; i++){
        if(i == 0){
            var data = {
                'user_rank': 1,
                'user_photo': "rank/1.jpg",
                'user_name': "Jingao",
                'user_lastTime': "今天",
                'user_num': "20关",
                'user_color': "#00FF7F"
            };
        }
        if(i == 1){
            var data = {
                'user_rank': 2,
                'user_photo': "rank/2.jpg",
                'user_name': "赵毅",
                'user_lastTime': "昨天",
                'user_num': "15关",
                'user_color': "#1E90FF"
            };
        }
        if(i == 2){
            var data = {
                'user_rank': 3,
                'user_photo': "rank/3.jpg",
                'user_name': "朱子晨",
                'user_lastTime': "星期五",
                'user_num': "9关",
                'user_color': "#1E90FF"
            };
        }
        if(i == 3){
            var data = {
                'user_rank': 4,
                'user_photo': "rank/4.jpg",
                'user_name': "学弟",
                'user_lastTime': "星期四",
                'user_num': "5关",
                'user_color': "#1E90FF"
            };
        }
        var dom_template = `
        <div class="item" style="background-color:${data.user_color}">
               <div class="ui big teal label">${data.user_rank}</div>
               <img class="ui avatar image" src=${data.user_photo}>
               <div class="content">
                   <div class="header">${data.user_name}</div>
                   <div class="meta">
                       <span class="cinema">${data.user_lastTime}</span>
                   </div>
               </div>
               <div class="right floated content">
                   <span class="left floated content">${data.user_num}</span>
                   <i class="smile icon"></i>
               </div>
        </div>`
        $('#rank_content').append(dom_template);
    }
}
function get_allRank(){
    $('#today').attr({
        'class':'item'
    });
    $('#all').attr({
        'class':'item active'
    });
    $('#rank_content').html("");
    for(var i = 0; i < 4; i++){
        if(i == 0){
            var data = {
                'user_rank': 1,
                'user_photo': "rank/1.jpg",
                'user_name': "Jingao",
                'user_lastTime': "今天",
                'user_num': "80关",
                'user_color': "#00FF7F"
            };
        }
        if(i == 1){
            var data = {
                'user_rank': 2,
                'user_photo': "rank/2.jpg",
                'user_name': "赵毅",
                'user_lastTime': "昨天",
                'user_num': "70关",
                'user_color': "#1E90FF"
            };
        }
        if(i == 2){
            var data = {
                'user_rank': 3,
                'user_photo': "rank/3.jpg",
                'user_name': "朱子晨",
                'user_lastTime': "星期五",
                'user_num': "60关",
                'user_color': "#1E90FF"
            };
        }
        if(i == 3){
            var data = {
                'user_rank': 4,
                'user_photo': "rank/4.jpg",
                'user_name': "学弟",
                'user_lastTime': "星期四",
                'user_num': "50关",
                'user_color': "#1E90FF"
            };
        }
        var dom_template = `
        <div class="item" style="background-color:${data.user_color}">
               <div class="ui big teal label">${data.user_rank}</div>
               <img class="ui avatar image" src=${data.user_photo}>
               <div class="content">
                   <div class="header">${data.user_name}</div>
                   <div class="meta">
                       <span class="cinema">${data.user_lastTime}</span>
                   </div>
               </div>
               <div class="right floated content">
                   <span class="left floated content">${data.user_num}</span>
                   <i class="smile icon"></i>
               </div>
        </div>`
        $('#rank_content').append(dom_template);
    }
}