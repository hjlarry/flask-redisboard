var submit_cmd_func = function() {
  $.ajax({
    method: "post",
    data: { 'command': $('#cmd_val').val() },
    success: function(data) {
      if (data.code == 0) {
        var element = '<div class="alert alert-light"><div class="alert-title">' +
          $('#cmd_val').val() + '</div>' + data.data + '</div>';
      } else {
        var element = '<div class="alert alert-warning"><div class="alert-title">' +
          $('#cmd_val').val() + '</div>' + data.error + '</div>';
      }
      $('.chat-content').append(element);
      $('#cmd_val').val('');

      var target_height = 0;
      $('#cmd_box').find('.chat-content .alert').each(function() {
        target_height += $(this).outerHeight();
      });
      setTimeout(function() {
        $('#cmd_box').find('.chat-content').scrollTop(target_height, -1);
      }, 100);
    }
  });
}


$('#cmd_val').bind('keypress', function(event) {
  if (event.keyCode == "13") {
    submit_cmd_func();
  }
});

$('#send_cmd_btn').click(submit_cmd_func)