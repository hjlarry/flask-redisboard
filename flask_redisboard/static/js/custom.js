/**
 *
 * You can write your JS code here, DO NOT touch the default style file
 * because it will make it harder for you to update.
 * 
 */

$(function() {
  var toast = Cookies.get('toast');
  if (toast) {
    iziToast.success({
      title: toast,
      position: 'topRight',
      timeout: 3000
    });
    Cookies.remove('toast')
  }

});


function delete_key(keyname, db) {
  $.ajax({
    method: "delete",
    url: '/redisboard/db/' + db + '/key/' + keyname + '/del',
    success: function(data) {
      console.log(data)
      Cookies.set("toast", "Delete Success!");
      window.location.assign('/redisboard/db/' + db);
    },
    error: function(data) {
      console.log(data)
      iziToast.error({
        title: 'Error!',
        message: data,
        position: 'topRight'
      });
    }
  });
  $('#fire-modal-1').modal('hide');
};

$("#CmdTable").dataTable({
  "columnDefs": [
    { "sortable": true, "targets": '_all' }
  ],
  "paging": false,
  "searching": false,
  "info": false,
});

$("#SlowlogTable").dataTable({
  "columnDefs": [
    { "sortable": true, "targets": '_all' }
  ],
  "searching": false,
  "info": false,
});
$.fn.editable.defaults.mode = 'inline';
$('.myeditable').editable({
  pk: 1,
  url: '/redisboard/config',
  title: 'Enter username'
});
