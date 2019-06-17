/**
 *
 * You can write your JS code here, DO NOT touch the default style file
 * because it will make it harder for you to update.
 * 
 */

"use strict";
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

function delete_key(keyname, db) {
  $.ajax({
    method: "delete",
    url: '/api/' + db + '/key/' + keyname + '/del',
    success: function(data) {
      console.log(data)
      Cookies.set("toast", "Delete Success!");
      window.location.assign('/db/' + db);
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
}

function flush_db(db) {
  $.ajax({
    method: "delete",
    url: '/api/' + db + '/flush',
    success: function(data) {
      console.log(data)
      Cookies.set("toast", "Flush DB Success!");
      window.location.assign('/db/' + db);
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
}

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

$("#rename_button").fireModal({
  title: 'Rename',
  body: $("#rename-panel"),
  footerClass: 'bg-whitesmoke',
  autoFocus: false,
  onFormSubmit: function(modal, e, form) {
    let form_data = $(e.target).serialize();
    $.ajax({
      method: "post",
      url: e.target.baseURI + '/rename',
      data: form_data,
      success: function(data) {
        Cookies.set("toast", "Rename Success!");
        window.location.assign(data.data);
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
  },
  shown: function(modal, form) {
    console.log(form)
  },
  buttons: [
    {
      text: 'Save',
      submit: true,
      class: 'btn btn-primary btn-shadow',
      handler: function(modal) {
      }
    }
  ]
});

$("#ttl_button").fireModal({
  title: 'Set TTL',
  body: $("#ttl-panel"),
  footerClass: 'bg-whitesmoke',
  autoFocus: false,
  onFormSubmit: function(modal, e, form) {
    let form_data = $(e.target).serialize();
    console.log(form_data)
    $.ajax({
      method: "post",
      url: e.target.baseURI + '/ttl',
      data: form_data,
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
    let fake_ajax = setTimeout(function() {
      form.stopProgress();
      clearInterval(fake_ajax);
    }, 1500);

    e.preventDefault();
  },
  shown: function(modal, form) {
    console.log(form)
  },
  buttons: [
    {
      text: 'Save',
      submit: true,
      class: 'btn btn-primary btn-shadow',
      handler: function(modal) {
      }
    }
  ]
});
$("#list-add-btn").fireModal({
  title: 'Add value to current list',
  body: $("#list-add-value"),
  footerClass: 'bg-whitesmoke',
  autoFocus: false,
  onFormSubmit: function(modal, e, form) {
    let form_data = $(e.target).serialize();
    console.log(form_data)
    $.ajax({
      method: "post",
      url: e.target.baseURI + '/list_add',
      data: form_data,
      success: function(data) {
        if (data.code == 0) {
          Cookies.set("toast", "Add Value Success!");
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
    let fake_ajax = setTimeout(function() {
      form.stopProgress();
      clearInterval(fake_ajax);
    }, 1500);

    e.preventDefault();
  },
  shown: function(modal, form) {
    console.log(form)
  },
  buttons: [
    {
      text: 'Save',
      submit: true,
      class: 'btn btn-primary btn-shadow',
      handler: function(modal) {
      }
    }
  ]
});

$("#list-del-btn").fireModal({
  title: 'Remove value from current list',
  body: $("#list-del-value"),
  footerClass: 'bg-whitesmoke',
  autoFocus: false,
  onFormSubmit: function(modal, e, form) {
    let form_data = $(e.target).serialize();
    console.log(form_data)
    $.ajax({
      method: "post",
      url: e.target.baseURI + '/list_rem',
      data: form_data,
      success: function(data) {
        if (data.code == 0) {
          Cookies.set("toast", "Remove Value Success!");
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
    let fake_ajax = setTimeout(function() {
      form.stopProgress();
      clearInterval(fake_ajax);
    }, 1500);

    e.preventDefault();
  },
  shown: function(modal, form) {
    console.log(form)
  },
  buttons: [
    {
      text: 'Submit',
      submit: true,
      class: 'btn btn-primary btn-shadow',
      handler: function(modal) {
      }
    }
  ]
});

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