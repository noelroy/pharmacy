$(function(){

    $("#approvebtn").click(function(){
    var username = $(this).attr("username");
    var csrf = $(this).attr("csrf");
    $.ajax({
      url: '/useradmin/approve/',
      data: {
        username: username,
        csrfmiddlewaretoken: csrf
      },
      type: 'post',
      cache: false,
      success: function (data) {
        $("#approve").html(data);
      }
    });

});
});