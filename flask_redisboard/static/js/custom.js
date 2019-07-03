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


function delete_key(url) {
  $.ajax({
    method: "delete",
    url: url,
    success: function(data) {
      if (data.code == 0) {
        Cookies.set("toast", "Delete Success!");
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
  send: "always",
  source: [
    { value: 'debug', text: 'Debug' },
    { value: 'verbose', text: 'Verbose' },
    { value: 'notice', text: 'Notice' },
    { value: 'warning', text: 'Warning' }
  ],
  success: success_func
});

$("#maxmemory-policy").editable({
  send: "always",
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

$("#appendfsync").editable({
  send: "always",
  source: [
    { value: 'always', text: 'always' },
    { value: 'everysec', text: 'everysec' },
    { value: 'no', text: 'no' }
  ],
  success: success_func
});

$("#notify-keyspace-events").editable({
  send: "always",
  source: [
    { value: 'K', text: 'K-Keyspace events' },
    { value: 'E', text: 'E-Keyevent events' },
    { value: 'g', text: 'Generic commands' },
    { value: '$', text: '$-String commands' },
    { value: 'l', text: 'List commands' },
    { value: 's', text: 'Set commands' },
    { value: 'h', text: 'Hash commands' },
    { value: 'z', text: 'Sorted set commands' },
    { value: 'x', text: 'Expired events' },
    { value: 'e', text: 'Evicted commands' },
    { value: 'A', text: 'Alias for g$lshzxe' },
  ],
  success: success_func
});

var yes_or_no_option = "#protected-mode,#stop-writes-on-bgsave-error,#rdbcompression," +
  "#slave-serve-stale-data,#slave-read-only, #repl-disable-tcp-nodelay, #repl-diskless-sync," +
  "#lazyfree-lazy-eviction,#lazyfree-lazy-expire,#lazyfree-lazy-server-del,#slave-lazy-flush," +
  "#no-appendfsync-on-rewrite,#aof-load-truncated,#aof-use-rdb-preamble,#appendonly," +
  "#cluster-require-full-coverage,#activedefrag, #activerehashing,#aof-rewrite-incremental-fsync";

$(yes_or_no_option).editable({
  send: "always",
  source: [
    { value: "yes", text: 'Yes' },
    { value: "no", text: 'No' },
  ],
  success: success_func
});

$('.myeditable').editable({
  emptytext: "not set",
  send: "always",
  placement: "right",
  success: success_func
});

