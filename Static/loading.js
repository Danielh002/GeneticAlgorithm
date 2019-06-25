$(document).ready(function() {
    $(function(){
      var image = new Image();
      image.src='http://127.0.0.1:5000/static/loading.gif'
      $('#iniciar').click(function(){
        $('#img').show();
        $('#content').hide();
      });
      $('#opciones').click(function(){
        $('div').show();
      });
    });
  })