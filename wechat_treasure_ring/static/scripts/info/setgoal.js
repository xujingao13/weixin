var STEP_METER = 0.6;
var openid;
var update_dis = function () {
	console.log(1);
	$('#goal_dis').val(Math.floor((Number($('#goal_step').val()) * STEP_METER).toString()));
};
var update_step = function () {
	$('#goal_step').val(Math.floor((Number($('#goal_dis').val()) / STEP_METER).toString()));
};
$(document).ready(function(){
	$('#goal_step').on('input', update_dis);
	$('#goal_dis').on('input', update_step);
	getopenid(function(data){
		$('#openid').val(data);
		openid = data;
		$.getJSON("data/ifregistered/"+openid, function(data){
			if (data.ifregistered == true) {
				$('#sex').val(data.sex);
				$('#age').val(data.age);
				$('#height').val(data.height);
				$('#weight').val(data.weight);
				$('#goal_step').val(data.goal_step);
				$('#goal_dis').val(Math.floor((data.goal_step * STEP_METER).toString()));
			}
		});
	});
});