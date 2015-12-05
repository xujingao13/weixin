var openid;
$(document).ready(function(){
	getopenid(function(data){
		openid = data;
		alert(openid);
	});
});