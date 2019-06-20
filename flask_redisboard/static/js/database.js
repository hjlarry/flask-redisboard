
$("[data-checkboxes]").each(function() {
  var me = $(this),
    group = me.data('checkboxes'),
    role = me.data('checkbox-role');

  me.change(function() {
    var all = $('[data-checkboxes="' + group + '"]:not([data-checkbox-role="dad"])'),
      checked = $('[data-checkboxes="' + group + '"]:not([data-checkbox-role="dad"]):checked'),
      dad = $('[data-checkboxes="' + group + '"][data-checkbox-role="dad"]'),
      total = all.length,
      checked_length = checked.length;

    if (role == 'dad') {
      if (me.is(':checked')) {
        all.prop('checked', true);
      } else {
        all.prop('checked', false);
      }
    } else {
      if (checked_length >= total) {
        dad.prop('checked', true);
      } else {
        dad.prop('checked', false);
      }
    }
  });
});

function flush_db(db) {
  $.ajax({
    method: "delete",
    url: '/redisboard/db/' + db + '/flush',
    success: function(data) {
      console.log(data)
      Cookies.set("toast", "Flush DB Success!");
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


$('.selectric').selectric().on('change', function() {
  var operation = $(this).val();
  var keyname = new Array();
  $('input[name="id"]:checked').each(function() {
    keyname.push($(this).data("keyname"));
  });
  if (Array.isArray(keyname) && keyname.length === 0) {
    iziToast.error({
      title: 'Error!',
      message: 'Please choose at least an item',
      position: 'topRight'
    });
  } else if (operation == "expire") {
    $("#batchTTL").modal('show');
  } else if (operation == "delete") {
    $("#batchDel").modal('show');
  }
});

$('#batch-ttl-btn').click(function() {
  var keyname = new Array();
  $('input[name="id"]:checked').each(function() {
    keyname.push($(this).data("keyname"));
  });
  var ttl = $('input[name="batchttl"]').val();
  var data = {
    'keys': keyname,
    'ttl': ttl,
  };
  $.ajax({
    method: "post",
    contentType: 'application/json',
    url: 'batchttl',
    data: JSON.stringify(data),
    success: function(data) {
      if (data.code == 0) {
        Cookies.set("toast", "Set TTL Success!");
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
});

$('#batch-del-btn').click(function() {
  var keyname = new Array();
  $('input[name="id"]:checked').each(function() {
    keyname.push($(this).data("keyname"));
  });
  var data = {
    'keys': keyname
  };
  $.ajax({
    method: "post",
    contentType: 'application/json',
    url: 'batchdel',
    data: JSON.stringify(data),
    success: function(data) {
      if (data.code == 0) {
        Cookies.set("toast", "Delete Keys Success!");
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
});