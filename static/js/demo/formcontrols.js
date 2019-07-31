// Call the dataTables jQuery plugin
$(document).ready(function() {
  $('#locationRadios').click(function(){
    $('#inputEdgeip3').parents('div.form-group').addClass('d-none');
    $('#inputLocation3').parents('div.form-group').removeClass('d-none');
  });
  $('#edgeipRadios').click(function(){
    $('#inputLocation3').parents('div.form-group').addClass('d-none');
    $('#inputEdgeip3').parents('div.form-group').removeClass('d-none');
  });

  if ($('#locationRadios').prop("checked", true)) {
    $('#inputLocation3').parents('div.form-group').removeClass('d-none');
    $('#inputEdgeip3').parents('div.form-group').addClass('d-none');
  }
  if ($('#edgeipRadios').prop("checked", true)) {
    $('#inputEdgeip3').parents('div.form-group').removeClass('d-none');
    $('#inputLocation3').parents('div.form-group').addClass('d-none');
  }

});
