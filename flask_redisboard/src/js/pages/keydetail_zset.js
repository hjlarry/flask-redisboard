function zset_del(member) {
  $.ajax({
    method: "post",
    url: window.location.pathname + '/zset_rem',
    data: { 'member': member },
    success: function(data) {
      if (data.code == 0) {
        Cookies.set("toast", "Delete Value Success!");
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
};


$("#keydetail-add-btn").fireModal({
  title: 'Add value to current zset',
  body: $("#zset-add-value"),
  footerClass: 'bg-whitesmoke',
  autoFocus: false,
  onFormSubmit: function(modal, e, form) {
    let form_data = $(e.target).serialize();
    $.ajax({
      method: "post",
      url: e.target.baseURI + '/zset_add',
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
  title: 'Remove value from current zset',
  body: $("#zset-del-value"),
  footerClass: 'bg-whitesmoke',
  autoFocus: false,
  onFormSubmit: function(modal, e, form) {
    let form_data = $(e.target).serialize();
    console.log(form_data)
    $.ajax({
      method: "post",
      url: e.target.baseURI + '/zset_rem',
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
      text: 'Remove',
      submit: true,
      class: 'btn btn-danger btn-shadow',
      handler: function(modal) {
      }
    }
  ]
});