/**
 *
 * You can write your JS code here, DO NOT touch the default style file
 * because it will make it harder for you to update.
 * 
 */
import Cookie from "js.cookie";


$.fn.editable.defaults.mode = 'inline';

$(function() {
  var toast = Cookie.get('toast');
  if (toast) {
    iziToast.success({
      title: toast,
      position: 'topRight',
      timeout: 3000
    });
    Cookie.remove('toast')
  }
});

function delete_key(url) {
  $.ajax({
    method: "delete",
    url: url,
    success: function(data) {
      if (data.code == 0) {
        Cookie.set("toast", "Delete Success!");
        window.location.assign(data.data);
      } else {
        iziToast.error({
          title: 'Error!',
          message: data.error,
          position: 'topRight'
        });
      }
    }
  });
  $('#fire-modal-1').modal('hide');
};













