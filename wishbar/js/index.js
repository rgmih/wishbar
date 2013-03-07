(function() {
	$(document).ready(function() {
		// custom checkbox support
		$('input[type="checkbox"]').change(function() {
			if ($(this).is(":checked")) {
				$(this).parent().children(".checkbox").addClass('checked');
			} else {
				$(this).parent().children(".checkbox").removeClass('checked');
			}
		}).attr("checked",null);
		
		$('#submit').click(function() {
			$("#bar").submit();
			return false;
		});
		$('#submit-now').click(function() {
			$('#bequick').attr('value','true');
			$("#bar").submit();
			return false;
		});
	});
})();
