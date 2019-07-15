import dt from 'datatables.net';
// import 'datatables.net-bs4/css/dataTables.bootstrap4.min.css'; not work

$("#data-table").dataTable({
  "columnDefs": [{
    "targets": 'nosort',
    "orderable": false
  }],
  "dom": "<'row'<'col-sm-12 col-md-6'f><'col-sm-12 col-md-6'<'table-action'>>>" +
    "<'row'<'col-sm-12'tr>>" +
    "<'row'<'col-sm-12 col-md-5'li><'col-sm-12 col-md-7'p>>",
  "iDisplayLength": 25
});

var btn = '<a href="#" class="btn btn-primary" id="keydetail-add-btn"><i class="fas fa-plus"></i>Add</a> ' +
  '<a href="#" class="btn btn-danger" id="keydetail-del-btn"><i class="fas fa-trash"></i>Remove</a>'

$(".table-action").html(btn);


window.$("#rename-btn").fireModal({
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


window.$("#ttl-btn").fireModal({
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

window.$('.keydetail-editable').editable({
  emptytext: "not set",
  send: "always",
  placement: "right",
  success: success_func
});


