$(document).ready(()=>{
    $('#language-icon-container').click(()=>{
        $('.language-drop').toggleClass('show');
    });

    $('.fa-envelope').parent().parent().click(function(){
        $('#form').css('display','flex');
        $('#layer').css('display','block');
    });
    $('#close').click(function(){
        $('#form').css('display','none');
        $('#layer').css('display','none');
    });

    $('#layer').click(function(){
        $('#form').css('display','none');
        $('#layer').css('display','none');
    })
    $("#form").submit(function(e) {
        e.preventDefault();
        $.ajax({
          type:'POST',
          url:'/',
          data:{
            email:$("#email").val(),
            message:$("#message").val()
          },
        });
        $('#email').val('');
        $('#message').val('');
    });
    $('#send').click(()=>{
        $('#form').css('display','none');
        $('#layer').css('display','none');

    });
});