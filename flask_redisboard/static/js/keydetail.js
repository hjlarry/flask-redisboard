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

$("#hash-add-btn").fireModal({
  title: 'Add value to current hash',
  body: $("#hash-add-value"),
  footerClass: 'bg-whitesmoke',
  autoFocus: false,
  onFormSubmit: function(modal, e, form) {
    let form_data = $(e.target).serialize();
    console.log(form_data)
    $.ajax({
      method: "post",
      url: e.target.baseURI + '/hash_add',
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


function hash_del(index) {
  $.ajax({
    method: "post",
    url: window.location.pathname + '/hash_rem',
    data: { 'index': index },
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


$("#set-add-btn").fireModal({
  title: 'Add value to current set',
  body: $("#set-add-value"),
  footerClass: 'bg-whitesmoke',
  autoFocus: false,
  onFormSubmit: function(modal, e, form) {
    let form_data = $(e.target).serialize();
    console.log(form_data)
    $.ajax({
      method: "post",
      url: e.target.baseURI + '/set_add',
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

$("#set-del-btn").fireModal({
  title: 'Remove value from current set',
  body: $("#set-del-value"),
  footerClass: 'bg-whitesmoke',
  autoFocus: false,
  onFormSubmit: function(modal, e, form) {
    let form_data = $(e.target).serialize();
    console.log(form_data)
    $.ajax({
      method: "post",
      url: e.target.baseURI + '/set_rem',
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


$("#zset-add-btn").fireModal({
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

$("#zset-del-btn").fireModal({
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