$("#switch1").click(function() {
  $("#beginstation").attr('readonly', !$("#beginstation").attr('readonly'));
});

$("#switch2").click(function() {
  $("#station").attr('readonly', !$("#station").attr('readonly'));
});