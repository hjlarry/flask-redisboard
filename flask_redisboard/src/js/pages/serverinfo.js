import dt from 'datatables.net';

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