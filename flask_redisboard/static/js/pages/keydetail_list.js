$("#ListTable").dataTable({
  "columnDefs": [
    { "sortable": true, "targets": '_all' }
  ],
  "dom": "<'row'<'col-sm-12 col-md-6'f><'col-sm-12 col-md-6'<'table-action'>>>" +
    "<'row'<'col-sm-12'tr>>" +
    "<'row'<'col-sm-12 col-md-5'li><'col-sm-12 col-md-7'p>>",
  "iDisplayLength": 25
});

var btn = '<a href="#" class="btn btn-primary" id="keydetail-add-btn"><i class="fas fa-plus"></i>Add</a> ' +
  '<a href="#" class="btn btn-danger" id="keydetail-del-btn"><i class="fas fa-trash"></i>Remove</a>'
$(".table-action").html(btn);


$("#keydetail-add-btn").fireModal({
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

$("#keydetail-del-btn").fireModal({
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