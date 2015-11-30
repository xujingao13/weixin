var STEP_METER = 0.6;
var update_dis = function () {
	$('#goal_dis').val(Math.floor((Number($('#goal_step').val()) * STEP_METER).toString()));
};
var update_step = function () {
	$('#goal_step').val(Math.floor((Number($('#goal_dis').val()) / STEP_METER).toString()));
};
$('#goal_step').on('input', update_dis);
$('#goal_dis').on('input', update_step);

