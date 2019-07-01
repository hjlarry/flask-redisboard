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


var success_func = function(data) {
  if (data.code == 0) {
    iziToast.success({
      title: "Modify Success",
      position: 'topRight',
      timeout: 3000
    });
  } else {
    iziToast.error({
      title: "Error!",
      position: 'topRight',
      message: data.error,
    });
  }
};


$("#loglevel").editable({
  "send": "always",
  source: [
    { value: 'debug', text: 'Debug' },
    { value: 'verbose', text: 'Verbose' },
    { value: 'notice', text: 'Notice' },
    { value: 'warning', text: 'Warning' }
  ],
  success: success_func
});

$("#maxmemory-policy").editable({
  "send": "always",
  source: [
    { value: 'allkeys-lfu', text: 'allkeys-lfu' },
    { value: 'allkeys-lru', text: 'allkeys-lru' },
    { value: 'allkeys-random', text: 'allkeys-random' },
    { value: 'noeviction', text: 'noeviction' },
    { value: 'volatile-lfu', text: 'volatile-lfu' },
    { value: 'volatile-lru', text: 'volatile-lru' },
    { value: 'volatile-random', text: 'volatile-random' },
    { value: 'volatile-ttl', text: 'volatile-ttl' }
  ],
  success: success_func
});

var yes_or_no_option = "#protected-mode,#stop-writes-on-bgsave-error,#rdbcompression," +
  "#slave-serve-stale-data,#slave-read-only, #repl-disable-tcp-nodelay, #repl-diskless-sync," +
  "#lazyfree-lazy-eviction,#lazyfree-lazy-expire,#lazyfree-lazy-server-del,#slave-lazy-flush";

$(yes_or_no_option).editable({
  "send": "always",
  source: [
    { value: "yes", text: 'Yes' },
    { value: "no", text: 'No' },
  ],
  success: success_func
});

$('.myeditable').editable({
  "emptytext": "not set",
  "send": "always",
  "placement": "right",
  success: success_func
});