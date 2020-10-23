$('#new_password, #confirm_new_password').on('keyup', function () {
  if ($('#new_password').val() === $('#confirm_new_password').val()) {
    $('#message').html('Matching').css('color', 'green');
  } else
    $('#message').html('Not Matching').css('color', 'red');
});